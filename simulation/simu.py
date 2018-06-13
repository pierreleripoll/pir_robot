
from node import Node
from grille import Grille
from astar import AStar
from cell import Cell
from robot import Robot
from coordination import Coordination

from InterfaceV3 import *

lab = Grille(8,8)
lab.setRect(0,0,4,8,".")

lab.setRect(2,5,1,2,"?");
lab.setRect(2,1,1,1,"?");



# Liste des robots
robots = []
#Liste des chemins
paths=[]
astar = AStar(lab)

dic = { "?":"grey", ".":"white","S":"green","G":"blue"}
coord = Coordination(robots)

disp= Display(lab,astar,dic,paths,robots)

#disp.showPath(aPath, "red")
#disp.showPath(bPath, "yellow")
#disp.showPath(cPath, "purple")
