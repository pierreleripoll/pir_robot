
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


# Liste des robots

# Robot A
aStart = Node(Cell(8,12,"S"),"L")
aGoal = Node(Cell(13, 12,"G"),"L")
a = Robot("A", aStart, aGoal)
print(a)


astar = AStar(lab)

# Liste des chemins des robots
aPath = astar.findPath(aStart,aGoal)




dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp= Display(lab,dic)

#disp.showPath(aPath, "red")
#disp.showPath(bPath, "yellow")
#disp.showPath(cPath, "purple")
