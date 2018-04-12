import sys
import math
import time


class AStar:
    def __init__(self,lab):
        self.lab = lab
        self.lab.resetNodes()
        self.openList = []
        self.closedList = []


    def alreadyBestIn(self,node,list):
        for n in list:
            if n.x == node.x and n.y == node.y:
                if node.cout >= n.cout:
                    return 1
        return 0


    def insert(self,node,list):
        for n in list:
            if node.dist(n)==0:
                if node.cout < n.cout:
                    n=node.copy()
                else:
                    return

        list.append(node.copy())

    def returnPath(self,start,goal):
        path = []

        self.insert(goal,path)
        findPath = 1
        if goal.typeN == 'T':
            print("Closed list :",self.closedList,file=sys.stderr)


        while findPath and path[-1].dist(start)!=1:
            findPath = 0
            for i, node in enumerate(self.closedList):
                if node.dist(path[-1]) == 1:
                    findPath = 1
                    self.insert(node,path)
                    self.closedList.pop(i)
        if not findPath :
            return []
        if goal.typeN=='?':
            path.pop(0)
        print("Path :",list(reversed(path)),file=sys.stderr)
        return list(reversed(path))

    def findPath(self,start,goal):
        self.openList.clear()
        self.closedList.clear()
        self.addNodeToOpenList(start.copy(),goal)
        notFinish = 1
        print("FindPath : ",repr(start)," to ",repr(goal),file=sys.stderr)

        if not self.lab.isReachable(goal) :
            return []

        print("openList before :",self.openList,file=sys.stderr)


        while(notFinish and self.openList):
            #print("notFinish :",notFinish,file=sys.stderr)
            #if goal.typeN=='T':
                #print("closedList :",self.closedList,file=sys.stderr)
            self.openList.sort(key=h)

            notFinish = self.treat(self.openList[0],goal)

        #print("Closed list :",self.closedList," goal :",repr(goal),file=sys.stderr)
        return self.returnPath(start,goal)

    def treat(self,node,goal):

        #print("openList before :",self.openList,file=sys.stderr)



        self.insert(node,self.closedList)

        voisins = self.lab.findVoisins(node)
        #print("Voisins :",voisins,file=sys.stderr)
        for n in voisins:
            self.addNodeToOpenList(n.copy(),goal,node.cout)


        self.openList.pop(0)
        if not self.openList or len(self.openList)==0:
            #print("OpenList empty",file=sys.stderr)
            return 0
        if node.dist(goal) == 0:
            print("Goal find",file=sys.stderr)
            return 0
        if goal.typeN == '?' and node.dist(goal)==1:
            print("Goal find",file=sys.stderr)
            return 0

        return 1


    def addNodeToOpenList(self,node,goal,cout=0):
        node.cout = cout+1
        node.h = int(cout +node.dist(goal))
        if not self.alreadyBestIn(node,self.closedList):
            self.insert(node,self.openList)



def h(elem):
    return elem.h

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



class Grille:

    def __init__(self,r,c):
        self.nRows = r
        self.nColumns = c
        self.plan = []

        for i in range(c):
            self.plan.append([])
            for j in range(r):
                self.plan[i].append(Node(i,j))

    def chgNode(self,x,y,typeN):
        self.plan[x][y].changeType(typeN)


    def findVoisins(self,node, obstacle = "false",range = 1):
        voisins = []
        X = node.x
        Y = node.y

        voisin = self.getNode(X+range,Y)
        if not voisin.isObstacle() or obstacle=="true":
            voisins.append(voisin)
        voisin = self.getNode(X,Y+range)
        if not voisin.isObstacle()or obstacle=="true":
            voisins.append(voisin)
        voisin = self.getNode(X-range,Y)
        if not voisin.isObstacle()or obstacle=="true":
            voisins.append(voisin)
        voisin = self.getNode(X,Y-range)
        if not voisin.isObstacle()or obstacle=="true":
            voisins.append(voisin)

        return voisins


    def getCarre(self,pos,l = 0):
        carre= []

        for i in range(2*l+1)
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
        for j,node in enumerate(row):
            self.chgNode(j,i,node)



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
