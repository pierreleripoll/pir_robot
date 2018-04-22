import sys
import math
import time

from node import Node
from grille import Grille

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




    def returnPath(self,node):
        path = [node]
        #print("returnPath2 in use")
        while node.parent :
            path.append(node.parent)
            node = node.parent
        #print(repr(list(reversed(path))))
        return list(reversed(path))

    def findPath(self,start,goal):
        self.lab.resetNodes()
        self.openList.clear()
        self.closedList.clear()
        self.addNodeToOpenList(start.copy(),goal)
        notFinish = 1
        #print("FindPath : ",repr(start)," to ",repr(goal),file=sys.stderr)

        #print("openList before :",self.openList,file=sys.stderr)


        while(notFinish and self.openList):
            #print("notFinish :",notFinish,file=sys.stderr)
            #if goal.typeN=='T':
                #print("closedList :",self.closedList,file=sys.stderr)
            self.openList.sort(key=h)

            notFinish = self.treat(self.openList[0],goal)

        #print("Closed list :",self.closedList," goal :",repr(goal),file=sys.stderr)

        return self.returnPath(goal)

    def treat(self,node,goal):

        #print("openList before :",self.openList,file=sys.stderr)


        self.insert(node,self.closedList)

        neighbors = self.lab.findNeighbors(node)
        #print("neighbors :",neighbors,file=sys.stderr)
        for n in neighbors:
            n.setParent(node)
            self.addNodeToOpenList(n.copy(),goal,node)


        self.openList.pop(0)
        if not self.openList or len(self.openList)==0:
            #print("OpenList empty",file=sys.stderr)
            return 0
        if node.dist(goal) == 0:
            #print("Goal found, node.dist(goal)=0",file=sys.stderr)
            return 0
        if goal.typeN == '?' and node.dist(goal)==1:
            #print("Goal found",file=sys.stderr)
            return 0

        return 1


    def addNodeToOpenList(self,node,goal,nodeParent):
        node.cout = nodeParent.cout+1
        node.h = cout + node.dist(goal) + node.rotation(nodeParent)
        if not self.alreadyBestIn(node,self.closedList):
            self.insert(node,self.openList)

    # Renvoie la liste des chemins de tous les robots donnés en paramètres (dans une liste)
    def findAllPaths(self, robots) :
        paths = []
        for i in range(len(robots)) :
            paths.append(self.findPath(self.lab.robots[i].start, self.lab.robots[i].goal))
            robots[i].path = paths[i]
        return paths

def h(elem):
    return elem.h
