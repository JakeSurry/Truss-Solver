import random as rand

class washington():

    def __init__(self):
        self.joints = []
        self.members = []

    def build(self, par, applied):

        joints = []
        members = []

        joints.append(par[0])
        joints.append(par[1])
        joints.append(applied[0])

        num_joints = rand.randint(1, 10)

        for _ in range(num_joints):
            while 1:
                j = [rand.randint(0, 65), rand.randint(0, 40)]
                if j not in joints:
                    joints.append(j)
                    break

        for _ in range(num_joints*2+3):

            while 1:
                for i in range(len(joints)):
                    if members.count(i) <= 2:
                        j = i
                        break
                #j = rand.randint(0, len(joints)-1)
                #break

            while 1:
                m = [j, rand.randint(0, len(joints)-1)]
                if m[0] != m[1] and m not in members:
                    members.append(m)
                    break


        self.joints = joints
        self.members = members

        print(len(members))
        for m in members:print(m)
        
        return self.joints, self.members




