
from node import Node
from grille import Grille
from astar import AStar
from robot import Robot
from coordination import Coordination

from InterfaceV3 import *

lab = Grille(20,20)
lab.setRect(5,5,10,2,".")
lab.setRect(5,5,2,10,".");
lab.setRect(10,5,2,10,".")
lab.setRect(5,12,10,2,".")

lab.chgNode(11,12,"?")


# Liste des robots
robots = []

# Robot A
aStart = Node(8,12,"S")
aGoal = Node(13, 12,"G")
a = Robot("A", aStart, aGoal)
print(a)
robots.append(a)



lab.setRobots(robots)

astar = AStar(lab)

# Liste des chemins des robots
paths = astar.findAllPaths(robots)
aPath = paths[0]


a.setTime()


coord = Coordination(robots)
#print(coord.getFirstCollisionNode(a, b))
print(a.time)

coord.coordinateRobots()
print(a.time)



dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp= Display(lab,dic)

disp.showPath(aPath, "red")
#disp.showPath(bPath, "yellow")
#disp.showPath(cPath, "purple")
