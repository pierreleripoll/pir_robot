
import math

class Cell:

    def __init__(self, x, y, typeC = '?', txt=None):
        self.x = x
        self.y = y
        self.typeC = typeC
        self.txt = txt # texte à afficher le cas échéant


    def changeType(self,typeC):
        self.typeC = typeC



    def isObstacle(self):
        if self.typeC == "?" or self.typeC == "#":
            #print("Cell ",self.x,",",self.y," is obstacle")
            return 1
        else:
            return 0

    def isSame(self,cell):
        if self.x == cell.x and self.y == cell.y:
            return 1
        else :
            return 0

    def copy(self):
        returnV = Cell(self.x,self.y)
        returnV.typeC = self.typeC
        returnV.txt = self.txt
        return returnV

    def __repr__(self):
        return "("+str(self.x)+","+str(self.y)+","+str(self.typeC)+")"

    def __str__(self):
        return str(self.typeC)

    def dist(self,cell2):
        dx = abs(cell2.x-self.x)
        dy = abs(cell2.y-self.y)
        dist=dx+dy
        return dist
