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



    def __repr__(self) :
        return "Robot " + str(self.name) + " is at node (" + str(self.start.x) + "," + str(self.start.y) + ") and going to (" + str(self.goal.x) + "," + str(self.goal.y) + ")"
