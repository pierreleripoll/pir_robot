#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import math

from node import Node
from cell import Cell

class Robot :
    def __init__(self, name, start=None, goal= None) :
        self.name = name
        self.start = start
        if start :
            self.start.txt = name
        self.goal = goal
        if goal :
            self.goal.txt = name
        self.path = []
        self.time = [] # liste contenant le temps théorique à chaque noeud du path
        if start :
            self.x = start.x
            self.y = start.y
        self.state=None#Etat de la checkbox du robot (affichage)
    # Renvoie 1 si le robot doit tourner pour atteindre ce noeud, 0 sinon
    def isTurning(self, node) :
        index = 1
        for i in range(len(self.path)) :
            if(self.path[i].x == node.x and self.path[i].y == node.y) :
                index = i
        if(index > 1) :
            if(node.x == self.path[index-1].x) :
                if(self.path[index-1].x == self.path[index-2].x) :
                    return 0
                else :
                    return 1
            elif(node.y == self.path[index-1].y) :
                if(self.path[index-1].y == self.path[index-2].y) :
                    return 0
                else :
                    return 1
        else :
            return 0

    # Calcule le temps à chaque noeud du path
    def setTime(self) :
        self.time.append(0)
        for i in range(1, len(self.path)) :
            self.time.append(self.time[i-1] + 5 -self.isTurning(self.path[i])) # constantes arbitraires
        for i, node in enumerate(self.path) :
            node.time=self.time[i]

    # Induit un délai supplémentaire avant d'atteindre le noeud donné en paramètre
    def wait(self, node, delay) :
        print(self.name)
        index = 0
        while(self.path[index].x != node.x or self.path[index].y != node.y) :
            index += 1
        for i in range(index-1, len(self.path)) :
            self.time[i] += delay
            self.path[i].time += delay

    def __repr__(self) :
        return "Robot " + str(self.name) + " is at node (" + str(self.x) + "," + str(self.y) + ") and going to (" + str(self.goal.x) + "," + str(self.goal.y) + ")"


    def createMsg(self):
        msg = self.name
        for node in self.path:
            msg += "/"+node.msg()
        return msg

    def readMsg(self, msg):
        cmd = msg.split('/')
        if cmd[0]==self.name:
            path = []
            for s in cmd[1:]:
                s = s.split(',')
                print("Node :")
                print(s)
                cell = Cell(int(s[0]),int(s[1]))
                node = Node(cell,s[2])
                node.time = float(s[3])
                path.append(node)
        print(path)
        self.start = path[0]
        self.goal = path[-1]
        self.path = path
