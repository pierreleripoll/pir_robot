
from node import Node
from grille import Grille
from astar import AStar
from robot import Robot

from InterfaceV3 import *

lab = Grille(30,30)
lab.setRect(15,15,10,2,".")
lab.setRect(15,15,2,10,".");
lab.setRect(20,15,2,10,".")
lab.setRect(15,22,10,2,".")

# Liste des robots
robots = []

# Robot A
aStart = Node(15,20,"S")
aGoal = Node(20,15,"G")
a = Robot("A", aStart, aGoal)
print(a)
robots.append(a)

# Robot B
bStart = Node(15, 22, "S")
bGoal = Node(20, 20, "G")
b = Robot("B", bStart, bGoal)
print(b)
robots.append(b)

lab.setRobots(robots)

astar = AStar(lab)

# Liste des chemins des robots
paths = astar.findAllPaths(robots)
aPath = paths[0]
bPath = paths[1]

dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp= Display(lab,dic)

disp.path(aPath, "red")
disp.path(bPath, "yellow")
