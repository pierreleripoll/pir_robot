#!/usr/bin/env python
# -*- coding: utf-8 -*
import sys
import math

from node import Node

class Coordination :
    def __init__(self, robots) :
        self.robots = robots

    # Renvoie l'intersection entre les chemins de 2 robots, càd les noeuds communs aux 2 chemins
    def intersection(self, robot1, robot2) :
        intersection = []
        print("Robot",robot1.name," path :",robot1.path)
        print("Robot",robot2.name," path :",robot2.path)
        for node1 in robot1.path :
            for node2 in robot2.path :
                if node1.isSame(node2) :
                    intersection.append(node1)
        print(intersection)
        return intersection

    # Vérifie s'il y a un problème entre les chemins de 2 robots
    def checkPath(self, robot1, robot2) :
        # Pas bon si [robot2.start OU EXCLUSIF robot2.goal appartient à robot1.path] ET [direction de robot2 opposée à direction de robot1]
        #               OU [robot2.start ET robot2.goal appartiennent à robot1.path]

        s1 = False
        g1 = False
        s2 = False
        g2 = False
        intersect = self.intersection(robot1, robot2)
        print("INTERSECT : ",intersect,"\n")
        for node in intersect :
            if node.isSame(robot1.start) :
                s1 = True
            if node.isSame(robot1.goal) :
                g1 = True
            if node.isSame(robot2.start) :
                s2 = True
            if node.isSame(robot2.goal) :
                g2 = True


        if s1 and g1 :
            #intersection possède a la fois s and goal d'un robot
            return 1, intersect[int(len(intersect)/2)]
        if s2 and g2:
            return 1, intersect[int(len(intersect)/2)]
        elif s1 and s2 :
            #les deux starts
            return 2, robot2.start
        elif g1 and g2 :
            #les deux goals
            return 3, robot2.goal
        else :
            return 0, None

    # Valide le chemin d'un robot s'il n'y a aucun pb avec les chemins des robots précédemment créés
    def validatePath(self, robot) :
        for r in self.robots :
            if robot is not r :
                check, node = self.checkPath(robot,r)
                #print(robot,r,check,node)
                if check != 0 :
                    return check, node
        return 0,0

    # Renvoie le robot le plus prioritaire des 2 donnés en paramètre,
    # lorsqu'ils vont collisionner au noeud node
    def getBestRobot(self, robot1, robot2, node) :
        timeGoal1 = robot1.time[len(robot1.time)-1]
        timeGoal2 = robot2.time[len(robot2.time)-1]
        if(timeGoal1 <= timeGoal2) :
            return robot1
        else :
            return robot2

    # Renvoie le noeud où a lieu la 1ère collision entre 2 robots le cas échéant
    def getFirstCollisionNode(self, robot1, robot2) :
        for i in range(len(robot1.path)) :
            for j in range(len(robot2.path)) :
                if(robot1.path[i].isSame(robot2.path[j]) and robot1.time[i] == robot2.time[j]) :
                    return robot1.path[i]
        return None

    # Impose des délais à certains robots jusqu'à ce qu'il n'y ait plus de collisions
    def coordinateRobots(self) :
        collisionsCounter = 0
        # Pour l'instant, de façon arbitraire, on parcourt les robots dans l'ordre de la liste
        for i in range(len(self.robots)) :
            for j in range(len(self.robots)) :
                if(i != j) :
                    collNode = self.getFirstCollisionNode(self.robots[i], self.robots[j])
                    if(collNode != None) :
                        collisionsCounter += 1
                        bestRobot = self.getBestRobot(self.robots[i], self.robots[j], collNode)
                        bestRobot.wait(collNode, 10)
        if(collisionsCounter != 0) :
            self.coordinateRobots()
