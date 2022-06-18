import pygame as pg
pg.init()
import numpy as np

import bots

class truss():

    def __init__(self, joints, pin_and_roller, connections, applied_forces):

        self.joints = joints
        self.members = []

        self.pin = ((pin_and_roller[0]-1)*2)
        self.roller = ((pin_and_roller[1]-1)*2)

        for i, connection in enumerate(connections):
            self.members.append([i, joints[connection[0]-1], joints[connection[1]-1]])

        self.applied_forces = applied_forces

        self.mem_forces, self.matrix = self.solve()

    def solve(self):

        force_matrix = []
        for joint in self.joints:

            #Creates an array full of zeros for the x and y forces
            x_force = []
            y_force = []

            [x_force.append(0) for _ in range(len(self.members)+3)]
            [y_force.append(0) for _ in range(len(self.members)+3)]

            #Generates a list of all members connected to current joint
            rel_mem = [mem for mem in self.members if joint in mem]

            for mem in rel_mem:

                #Finds angle between point of reference (horizontal line) and the member
                try:
                    theta = abs(np.arctan((mem[2][1]-mem[1][1])/(mem[2][0]-mem[1][0])))
                except ZeroDivisionError:
                    theta = 0

                #Gets direction (tension or compression) of member
                x, y = self.get_dir(joint, mem)

                #Changes the 0 in the specific members slot to the value, 
                #that when multiplied by the force of the member provides the reaction force
                x_force[mem[0]] = np.cos(theta)*x
                y_force[mem[0]] = np.sin(theta)*y

            force_matrix.append(x_force)
            force_matrix.append(y_force)

        #Adds anchors
        force_matrix[self.pin][-3] = 1
        force_matrix[self.pin+1][-2] = 1
        force_matrix[self.roller+1][-1] = 1

        #Creates applied force B vector
        applied = [0 for _ in range(len(self.joints)*2)]
        for force in applied_forces:
            applied[force[0]*2-1] = force[1]

        #Calculates force values, however if the matrix is singular, it informs the user and generalizes the inverse
        forces = np.dot(np.linalg.pinv(force_matrix), applied)

        return forces, force_matrix

    def get_dir(self, joint, mem):
    
        m = mem.copy()
        m.remove(joint)
        m.pop(0)
        m = m[0]

        x = 0
        y = 0

        #Gets the direction of a member by taking the difference between the protruding joint and the main joint,
        #then sets the value of x and y as positive or negative, positive being tension and negative being compression
        if not m[0]-joint[0] == 0:
            x = (m[0]-joint[0])/abs(m[0]-joint[0])
        if not m[1]-joint[1] == 0:
            y = (m[1]-joint[1])/abs(m[1]-joint[1])

        return x, y

    def print(self):

        print('')
        print(np.matrix(np.round(self.matrix, 4)))

        print('')
        for i, force in enumerate(self.mem_forces):
            if i == len(self.mem_forces)-3:
                print(f'Pin X: {round(force, 3)}')
            elif i == len(self.mem_forces)-2:
                print(f'Pin Y: {round(force, 3)}')
            elif i == len(self.mem_forces)-1:
                print(f'Rlr Y: {round(force, 3)}')
            else:
                print(f'Mem {i+1}: {round(force, 3)}')

        if np.linalg.det(self.matrix) == 0:
            print('\nSingular Matrix Encountered, Generalized Solution Provided')

class vis_output():

    def __init__(self, truss):

        self.truss = truss

        self.display = pg.display.set_mode((1300, 800))
        pg.display.set_caption('Truss Simulator')

        self.grid_surface = self.init_grid()
        self.truss_surface = self.visualize_truss(truss.joints, truss.members, truss.pin, truss.roller, truss.applied_forces, truss.mem_forces)

    def init_grid(self):

        grid_surface = pg.Surface((1300, 800))
        grid_surface.fill((255, 255, 255))

        for x in range(66):
            if x%5 == 0:
                pg.draw.rect(grid_surface, (150, 150, 150), (x*20, 0, 1, 800))
            else:
                pg.draw.rect(grid_surface, (220, 220, 220), (x*20, 0, 1, 800))

        for y in range(40):
            if y%5 == 0:
                pg.draw.rect(grid_surface, (150, 150, 150), (0, y*20, 1300, 1))
            else:
                pg.draw.rect(grid_surface, (220, 220, 220), (0, y*20, 1300, 1))

        return grid_surface
    
    def visualize_truss(self, joints, members, pin, roller, af, mf):

        #Creates truss surface and fills the background white
        truss_surface = pg.Surface((1300, 800))
        truss_surface.fill((255, 255, 255))

        #Draws the member, and passes the absolute value of the force through a rational function to get a color intsesity scaler,
        #then applies that scaler to either blue or red, blue for tension and red for compression
        for i, member in enumerate(members):
            intensity = 1500/(-abs(mf[i])-10)+150
            f = round(mf[i], 2)
            if f < 0:
                color = (100+intensity, 0, 0)
            elif f > 0:
                color = (0, 0, 100+intensity)
            else:
                color = (150, 0, 150)
            pg.draw.line(truss_surface, color, (member[1][0]*20, member[1][1]*20), (member[2][0]*20, member[2][1]*20), 5)


        #Draws all the joints
        for joint in joints:
            pg.draw.circle(truss_surface, (100, 100, 100), (joint[0]*20, joint[1]*20), 8)
        
        #Takes the pin value from the truss class and divides by 2 (as the previous value was set with x and y forces, whereas now
        #it is whatever joint number the pin and roller are)
        pin = int(pin/2)
        roller = int(roller/2)

        #Draws the pin and roller
        pg.draw.polygon(truss_surface, (255, 0, 0), points=[(joints[pin][0]*20, joints[pin][1]*20-8), (joints[pin][0]*20-10, joints[pin][1]*20-28), (joints[pin][0]*20+10, joints[pin][1]*20-28)])
        pg.draw.circle(truss_surface, (255, 0, 0), (joints[roller][0]*20, joints[roller][1]*20-18), 10)

        #Draws arrows pointing to all the applied forces
        for force in af:
            pg.draw.polygon(truss_surface, (0, 200, 0), points=[(joints[force[0]-1][0]*20, joints[force[0]-1][1]*20+10), (joints[force[0]-1][0]*20-10, joints[force[0]-1][1]*20+30), (joints[force[0]-1][0]*20+10, joints[force[0]-1][1]*20+30)])

        #Removes all the white pixels, and flips the canvas upside down, as initially the y values count top to bottom
        truss_surface.set_colorkey((255, 255, 255))
        truss_surface = pg.transform.flip(truss_surface, False, True)

        return truss_surface

    def out(self):

        self.display.blit(self.grid_surface, (0, 0))
        self.display.blit(self.truss_surface, (0, 0))

        pg.display.update()

        run = True
        while run:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False


joints = [
[4, 4],   #1
[16, 13], #2
[28, 4],  #3
[40, 13], #4
[52, 4]   #5
]

pin_and_roller = [1, 5]

connections = [
[1, 2],  #1
[1, 3],  #2
[2, 3],  #3
[2, 4],  #4
[3, 4],  #5
[3, 5],  #6
[4, 5]   #7
]

applied_forces = [
[2, 10]
]


'''
pin_and_roller = [(1, 5), (60, 5)]
applied_forces = [(30, 30)]

ai = bots.washington()
joints, connections = ai.build(pin_and_roller, applied_forces)

pin_and_roller = [1, 2]
applied_forces = [
[3, 10]
]
'''
bridge = truss(joints, pin_and_roller, connections, applied_forces)
graphics = vis_output(bridge)

bridge.print()
graphics.out()