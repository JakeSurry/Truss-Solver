import pygame as pg
pg.init()
import numpy as np

import mojmatrix
import mojlinear

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
[4, 2],   #1
[24, 36.341], #2
[44, 2]  #3
]

pin_and_roller = [1, 3]

connections = [
[1, 2],  #1
[1, 3],  #2
[2, 3]  #3
]

applied_forces = [
[2, 10]
]
"""
joints = [
[5, 5],
[30.712, 35.642],
[56.423, 5]
]

pin_and_roller = [1, 3]

connections = [
[1, 2],
[2, 3],
[3, 1]
]

applied_forces = [
[2, 10]
]

"""


bridge = mojmatrix.truss(joints, pin_and_roller, connections, applied_forces)

graphics = vis_output(bridge)
graphics.out()
