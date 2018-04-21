
from node import Node
from grille import Grille
from astar import AStar
from robot import Robot
from coordination import Coordination

from InterfaceV3 import *

lab = Grille(30,30)
lab.setRect(15,15,10,2,".")
lab.setRect(15,15,2,10,".");
lab.setRect(20,15,2,10,".")
lab.setRect(15,22,10,2,".")

# Liste des robots
robots = []

# Robot A
aStart = Node(18,22,"S")
aGoal = Node(23, 22,"G")
a = Robot("A", aStart, aGoal)
print(a)
robots.append(a)

# Robot B
bStart = Node(21, 19, "S")
bGoal = Node(21, 24, "G")
b = Robot("B", bStart, bGoal)
print(b)
robots.append(b)

# Robot C
cStart = Node(20, 24, "S")
cGoal = Node(17, 16, "G")
c = Robot("C", cStart, cGoal)
print(c)
robots.append(c)

lab.setRobots(robots)

astar = AStar(lab)

# Liste des chemins des robots
paths = astar.findAllPaths(robots)
aPath = paths[0]
bPath = paths[1]
cPath = paths[2]

a.setTime()
b.setTime()
c.setTime()

coord = Coordination(robots)
#print(coord.getFirstCollisionNode(a, b))
'''print(a.time)
print(b.time)
print(c.time)'''
coord.coordinateRobots()
'''print(a.time)
print(b.time)
print(c.time)'''


dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp= Display(lab,dic)

disp.dispPath(aPath, "red")
disp.dispPath(bPath, "yellow")
disp.dispPath(cPath, "purple")
