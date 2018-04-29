
import math

class Node:

    DIRECTIONS = ["U","R","D","L"]

    def __init__(self,cell,dir):
        self.dir = dir
        self.cell = cell
        self.cout = 0
        self.x = cell.x
        self.y = cell.y
        self.h = math.inf # heuristique
        self.parent = None;


    def equals(self,node):
        if self.cell.isSame(node.cell) and self.dir == node.dir :
            return 1
        else :
            return 0

    def isObstacle(self):
    #    print("Appel isObstacle")
        return self.cell.isObstacle()

    def setParent(self,node):
        self.parent = node

    def dist(self,node):
        return self.cell.dist(node.cell)

    def copy(self):
        returnV = Node(self.cell,self.dir)
        returnV.x = self.x
        returnV.y = self.y
        returnV.h = self.h
        returnV.cout = self.cout
        returnV.parent = self.parent
        return returnV

    def __repr__(self):
        return repr(self.cell)+","+self.dir+",h"+str(self.h)

    def __str__(self):
        return str(self.typeN)



    def reset(self):
        self.cout = 0
        self.h= math.inf
        self.parent = None
