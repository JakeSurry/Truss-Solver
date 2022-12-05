import numpy as np 
import time

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
        self.print()

    def solve(self):

        time_start = time.time()

        force_matrix = []
        for joint in self.joints:

            x_force = []
            y_force = []

            [x_force.append(0) for _ in range(len(self.members)+3)]
            [y_force.append(0) for _ in range(len(self.members)+3)]

            rel_mem = [mem for mem in self.members if joint in mem]

            for mem in rel_mem:

                try:
                    theta = abs(np.arctan((mem[2][1]-mem[1][1])/(mem[2][0]-mem[1][0])))
                except ZeroDivisionError:
                    theta = 0

                x, y = self.get_dir(joint, mem)

                x_force[mem[0]] = np.cos(theta)*x
                y_force[mem[0]] = np.sin(theta)*y

            force_matrix.append(x_force)
            force_matrix.append(y_force)

        force_matrix[self.pin][-3] = 1
        force_matrix[self.pin+1][-2] = 1
        force_matrix[self.roller+1][-1] = 1

        applied = [0 for _ in range(len(self.joints)*2)]
        for force in self.applied_forces:
            applied[force[0]*2-1] = force[1]

        print(applied)
        forces = np.dot(np.linalg.pinv(force_matrix), applied)
        
        print(time.time()-time_start)
        return forces, force_matrix

    def get_dir(self, joint, mem):
    
        m = mem.copy()
        m.remove(joint)
        m.pop(0)
        m = m[0]

        x = 0
        y = 0

        if not m[0]-joint[0] == 0:
            x = (m[0]-joint[0])/abs(m[0]-joint[0])
        if not m[1]-joint[1] == 0:
            y = (m[1]-joint[1])/abs(m[1]-joint[1])

        return x, y

    def print(self):

        print('')
        #print(np.matrix(np.round(self.matrix, 4)))

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

