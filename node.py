
import math

class Node:

    def __init__(self,x,y,typeN = '?', txt=None):
        self.x = x
        self.y = y
        self.typeN = typeN
        self.txt = txt # texte à afficher le cas échéant
        self.cout = 0
        self.h = math.inf # heuristique
        self.parent = None;

    def changeType(self,typeN):
        self.typeN = typeN

    def rotation(self,node):
        nodeParent = node.parent
        if nodeParent :
            if self.x == nodeParent.x or self.y == nodeParent.y :
                return 0
            else :
                return 1
        else :
            return 0

    def isObstacle(self):
        if self.typeN == "?" or self.typeN == "#":
            return 1
        else:
            return 0

    def setParent(self,node):
        self.parent = node

    def copy(self):
        returnV = Node(self.x,self.y)
        returnV.typeN = self.typeN
        returnV.h = self.h
        returnV.cout = self.cout
        returnV.parent = self.parent
        returnV.txt = self.txt
        return returnV

    def __repr__(self):
        return str(self.x)+","+str(self.y)+":"+str(self.typeN)+",h"+str(self.h)

    def __str__(self):
        return str(self.typeN)

    def dist(self,node2):
        dx = abs(node2.x-self.x)
        dy = abs(node2.y-self.y)
        dist=dx+dy

        return dist

    def reset(self):
        self.cout = 0
        self.h= 0
        self.parent = None
