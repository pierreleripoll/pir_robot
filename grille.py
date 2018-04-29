
import sys
import math



from cell import Cell

class Grille:

    def __init__(self,r,c):
        self.nRows = r
        self.nColumns = c
        self.plan = []
        self.robots = [] # liste des robots évoluant dans la grille

        for i in range(c):
            self.plan.append([])
            for j in range(r):
                self.plan[i].append(Cell(i,j))

    def chgCell(self,x,y,typeC):
        self.plan[x][y].changeType(typeC)


    def findNeighbors(self,cell, obstacle = "false",range = 1):
        neighbors = []
        X = cell.x
        Y = cell.y

        neighbor = self.getCell(X+range,Y)
        if not neighbor.isObstacle() or obstacle=="true":
            neighbors.append(neighbor)
        neighbor = self.getCell(X,Y+range)
        if not neighbor.isObstacle()or obstacle=="true":
            neighbors.append(neighbor)
        neighbor = self.getCell(X-range,Y)
        if not neighbor.isObstacle()or obstacle=="true":
            neighbors.append(neighbor)
        neighbor = self.getCell(X,Y-range)
        if not neighbor.isObstacle()or obstacle=="true":
            neighbors.append(neighbor)

        return neighbors


    def getSquare(self,pos,l = 0):
        square= []

        for i in range(2*l+1):
            square.append(self.getCell(pos.x-l+i,pos.y-l).copy())
            square.append(self.getCell(pos.x-l+i,pos.y+l).copy())

        for i in range(2*(l-1)+2):
            square.append(self.getCell(pos.x-l,pos.y-l+i).copy())
            square.append(self.getCell(pos.x+l,pos.y-l+i).copy())

        #sorted(square, key= lambda Cell: Cell.dist(pos))
        return square


    def getCell(self,x,y):
        #print("Get Cell :",repr(self.plan[y][x]),file=sys.stderr)
        if x < 0 or x >=self.nColumns or y<0 or y>=self.nRows:
            #print("Out of boundary",file=sys.stderr)
            return
        return self.plan[x][y]

    def resetCells(self):
        for r in self.plan:
            for c in r:
                c.reset()




    def chgRow(self,i,row):
        #print("New row : ",row,file=sys.stderr)
        for j,typeC in enumerate(row):
            self.chgCell(j,i,typeC)

    def setCell(self,cell):
        self.plan[cell.x][cell.y] = cell

    def setPath(self,path, typeC = "*"):
        for cell in path:
            cell.changeType(typeC)
            self.setCell(cell)

    def setRect(self,x,y,width,height,typeC):
        for i,column in enumerate(self.plan[x:x+width]):
            for j in range(y,y+height):
                self.chgCell(i+x,j,typeC)

    # Initialise la liste des robots et set les noeuds start et goal de chacun
    def setRobots(self, robots) :
        for i in range(len(robots)) :
            self.robots.append(robots[i])
            self.setCell(self.robots[i].start)
            self.setCell(self.robots[i].goal)

    def __repr__(self):
        toPrint = []
        for j in range(self.nRows):
            toPrint.append("")
        for column in self.plan:
            for i,cell in enumerate(column):
                    toPrint[i] += str(cell)+" "

        returnPrint  ="  "

        for i in range(self.nColumns):
            if(len(str(i))<2):
                returnPrint+=" "
            returnPrint += str(i)

        returnPrint += '\n'

        for i,string in enumerate(toPrint):
            if(len(str(i))<2):
                returnPrint += " "
            returnPrint += str(i)+" "+string+"\n"

        return returnPrint
