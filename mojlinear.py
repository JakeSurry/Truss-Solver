import numpy as np 
import time

class truss():

    def __init__(self, joints, pin_and_roller, connections, applied_forces):

        self.joints = [joint(j[0], j[1]) for j in joints]
        self.members = []

        self.pin = pin_and_roller[0]-1
        self.roller = pin_and_roller[1]-1

        for i, connection in enumerate(connections):
            self.members.append(member(i, [self.joints[connection[0]-1], self.joints[connection[1]-1]]))

        self.applied_forces = applied_forces

        self.solve()
        
    def solve(self):
        
        time_start = time.time()

        #Setting up the reactionary forces
        for force in self.applied_forces:
            rel_joint = force[0]-1
            self.joints[rel_joint].fy = force[1]

            froller = round(((self.joints[force[0]-1].x-self.joints[self.pin].x)*force[1])/(self.joints[self.roller].x-self.joints[self.pin].x),3)

            self.joints[self.roller].fy = froller
            self.joints[self.pin].fy = force[1] - froller
        
        i = 0
        complete = 0

        while complete != len(self.joints)-1:
            
            joint = self.joints[i]

            rel_mem = [mem for mem in self.members if joint in mem.joints]
            y_unk = 0
            x_unk = 0
            y_total = 0
            x_total = 0
            x_unk_mem = None
            
            for mem in rel_mem:
                if mem.force == None and mem.theta != 0:
                    y_unk += 1
                    y_unk_mem = mem
                elif mem.theta != 0:
                    y_total += mem.force*np.sin(mem.theta)
                    x_total += mem.force*np.cos(mem.theta)
                elif mem.force != None:
                    x_total += mem.force*np.cos(mem.theta)
                if mem.force == None and mem.theta == 0:
                    x_unk_mem = mem
            
            if y_unk == 1: 
                
                y_unk_mem.force = (-y_total-joint.fy)/(np.sin(y_unk_mem.theta))
                print(f"Mem {y_unk_mem.num}: {round(y_unk_mem.force,3)}")
                
                if x_unk_mem != None:
                    x_unk_mem.force = -y_unk_mem.force*np.cos(y_unk_mem.theta)+x_total
                    print(f"Mem {x_unk_mem.num}: {round(x_unk_mem.force,3)}")

                complete += 1

            i += 1
            if i >= len(self.joints):
                i = 0

        print(time.time()-time_start)

        print(f"Pin X: {self.joints[self.pin].fx}")
        print(f"Pin Y: {self.joints[self.pin].fy}")
        print(f"Rlr Y: {self.joints[self.roller].fy}")


            
class joint():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fx = 0
        self.fy = 0
        
class member():
    def __init__(self, i, joints):
        self.num = i+1
        self.joints = joints
        try:
            theta = abs(np.arctan((joints[1].y-joints[0].y)/(joints[1].x-joints[0].x)))
        except ZeroDivisionError:
            theta = 0
        self.theta = theta
        self.force = None
