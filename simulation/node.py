import math
from cell import Cell

class Node(Cell):

    DIRECTIONS = ["U","R","D","L"]

    def __init__(self, cell, dir):
        Cell.__init__(self, cell.x, cell.y, cell.typeC, cell.txt,cell.rectangle)
        self.dir = dir
        self.cout = 0
        self.h = float('inf') # heuristique
        self.parent = None
        self.arrow=[]
        self.time = 0

    def equals(self,node):
        if self.isSame(node) and self.dir == node.dir :
            return 1
        else :
            return 0

    def setParent(self,node):
        self.parent = node

    def copy(self):
        returnV = Node(self,self.dir)
        returnV.h = self.h
        returnV.cout = self.cout
        returnV.parent = self.parent
        return returnV

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+")"+","+self.dir+",t"+str(self.time)



    def reset(self):
        self.cout = 0
        self.h= math.inf
        self.parent = None

    def msg(self):
        return str(self.x)+","+str(self.y)+","+self.dir+","+str(self.time)
