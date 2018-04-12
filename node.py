class Node:

    def __init__(self,x,y,typeN = '?'):
        self.x = x
        self.y = y
        self.typeN = typeN
        self.cout = math.inf
        self.h = 0 #heuristique

    def changeType(self,typeN):
        self.typeN = typeN

    def isObstacle(self):
        if self.typeN == "?" or self.typeN == "#":
            return 1
        else:
            return 0

    def copy(self):
        returnV = Node(self.x,self.y)
        returnV.typeN = self.typeN
        returnV.h = self.h
        return returnV

    def __repr__(self):
        return str(self.x)+","+str(self.y)+":"+str(self.typeN)+",h"+str(self.h)



    def __str__(self):
        return str(self.typeN)

    def dist(self,node2):
        dx = node2.x-self.x
        dy = node2.y-self.y
        dist=dx+dy

        return dist

    def reset(self):
        self.cout = 0
        self.h= 0
