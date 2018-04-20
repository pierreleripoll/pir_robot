import sys
import math

from node import Node
from grille import Grille

class Robot :
    def __init__(self, name, start, goal) :
        self.name = name
        self.start = start
        self.start.txt = name
        self.goal = goal
        self.goal.txt = name
        self.path = []
        self.x = start.x
        self.y = start.y

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


    def __repr__(self) :
        return "Robot " + str(self.name) + " is at node (" + str(self.start.x) + "," + str(self.start.y) + ") and going to (" + str(self.goal.x) + "," + str(self.goal.y) + ")"
