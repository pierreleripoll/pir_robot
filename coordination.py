import sys
import math

from node import Node

class Coordination :
    def __init__(self, robots) :
        self.robots = robots

    # Renvoie le robot le plus prioritaire des 2 donnés en paramètre,
    # lorsqu'ils vont collisionner au noeud node
    def getWorstRobot(self, robot1, robot2, node) :
        # Pour l'instant, arbitrairement, le critère de choix est la distance
        # euclidienne au noeud goal
        dist1 = node.dist(robot1.goal)
        dist2 = node.dist(robot2.goal)
        if(dist1 <= dist2) :
            return robot2
        else :
            return robot1

    # Renvoie le noeud où a lieu la 1ère collision entre 2 robots le cas échéant
    def getFirstCollisionNode(self, robot1, robot2) :
        for i in range(len(robot1.path)) :
            for j in range(len(robot2.path)) :
                if(robot1.path[i].x == robot2.path[j].x and robot1.path[i].y == robot2.path[j].y and robot1.time[i] == robot2.time[j]) :
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
                        worstRobot = self.getWorstRobot(self.robots[i], self.robots[j], collNode)
                        worstRobot.wait(collNode, 10)
        if(collisionsCounter != 0) :
            self.coordinateRobots()
