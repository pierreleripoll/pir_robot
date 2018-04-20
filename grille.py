
import sys
import math



from node import Node

class Grille:

    def __init__(self,r,c):
        self.nRows = r
        self.nColumns = c
        self.plan = []
        self.robots = [] # liste des robots évoluant dans la grille

        for i in range(c):
            self.plan.append([])
            for j in range(r):
                self.plan[i].append(Node(i,j))

    def chgNode(self,x,y,typeN):
        self.plan[x][y].changeType(typeN)


    def findNeighbors(self,node, obstacle = "false",range = 1):
        neighbors = []
        X = node.x
        Y = node.y

        neighbor = self.getNode(X+range,Y)
        if not neighbor.isObstacle() or obstacle=="true":
            neighbors.append(neighbor)
        neighbor = self.getNode(X,Y+range)
        if not neighbor.isObstacle()or obstacle=="true":
            neighbors.append(neighbor)
        neighbor = self.getNode(X-range,Y)
        if not neighbor.isObstacle()or obstacle=="true":
            neighbors.append(neighbor)
        neighbor = self.getNode(X,Y-range)
        if not neighbor.isObstacle()or obstacle=="true":
            neighbors.append(neighbor)

        return neighbors


    def getCarre(self,pos,l = 0):
        carre= []

        for i in range(2*l+1):
            carre.append(self.getNode(pos.x-l+i,pos.y-l).copy())
            carre.append(self.getNode(pos.x-l+i,pos.y+l).copy())

        for i in range(2*(l-1)+2):
            carre.append(self.getNode(pos.x-l,pos.y-l+i).copy())
            carre.append(self.getNode(pos.x+l,pos.y-l+i).copy())

        #sorted(carre, key= lambda Node: Node.dist(pos))
        return carre


    def getNode(self,x,y):
        #print("Get Node :",repr(self.plan[y][x]),file=sys.stderr)
        if x < 0 or x >=self.nColumns or y<0 or y>=self.nRows:
            print("Out of boundary",file=sys.stderr)
            return
        return self.plan[x][y]

    def resetNodes(self):
        for r in self.plan:
            for c in r:
                c.reset()




    def chgRow(self,i,row):
        #print("New row : ",row,file=sys.stderr)
        for j,typeN in enumerate(row):
            self.chgNode(j,i,typeN)

    def setNode(self,node):
        self.plan[node.x][node.y] = node

    def setPath(self,path, typeN = "*"):
        for node in path:
            node.changeType(typeN)
            self.setNode(node)

    def setRect(self,x,y,largeur,hauteur,typeN):
        for i,column in enumerate(self.plan[x:x+largeur]):
            for j in range(y,y+hauteur):
                self.chgNode(i+x,j,typeN)

    # Initialise la liste des robots et set les noeuds start et goal de chacun
    def setRobots(self, robots) :
        for i in range(len(robots)) :
            self.robots.append(robots[i])
            self.setNode(self.robots[i].start)
            #self.robots[i].start.txt = self.robots[i].name
            self.setNode(self.robots[i].goal)
            #self.robots[i].goal.txt = self.robots[i].name

    def __repr__(self):
        toPrint = []
        for j in range(self.nRows):
            toPrint.append("")
        for column in self.plan:
            for i,node in enumerate(column):
                    toPrint[i] += str(node)+" "

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
