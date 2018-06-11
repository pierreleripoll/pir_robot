
from node import Node
from grille import Grille
from astar import AStar
from cell import Cell
from robot import Robot
from coordination import Coordination

from InterfaceV3 import *

lab = Grille(20,20)
lab.setRect(5,5,10,2,".")
lab.setRect(5,5,2,10,".");
lab.setRect(10,5,2,10,".")
lab.setRect(5,12,10,2,".")

lab.setCell(Cell(10,12,"?"))
lab.setCell(Cell(12,13,"?"))

# Liste des robots
robots = []
#Liste des chemins
paths=[]
# Robot A
aStart = Node(Cell(8, 12,"S"),"L")
aGoal = Node(Cell(13, 12,"G"),"L")
a = Robot("A", aStart, aGoal)
print(a)
robots.append(a)

# Robot B
bStart = Node(Cell(11, 12,"S"),"L")
bGoal = Node(Cell(9, 13,"G"),"L")
b = Robot("B", bStart, bGoal)
print(b)
robots.append(b)


astar = AStar(lab)

# Liste des chemins des robots
aPath = astar.findPath(aStart,aGoal)
paths.append(aPath)
a.path = aPath

a.setTime()
bPath = astar.findPath(bStart,bGoal)
b.path = bPath
paths.append(bPath)
b.setTime()

print("------ a.time ------")
print(a.time)
print("--------------------")

print("------ b.time ------")
print(b.time)
print("--------------------")

coord = Coordination(robots)

print("validatePath(b) : " + str(coord.validatePath(b)))


dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp= Display(lab,astar,dic,paths,robots)

#disp.showPath(aPath, "red")
#disp.showPath(bPath, "yellow")
#disp.showPath(cPath, "purple")
