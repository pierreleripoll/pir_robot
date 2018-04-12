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
