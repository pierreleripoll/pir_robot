#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')


from simulation.node import Node
from simulation.grille import Grille
from simulation.astar import AStar
from simulation.cell import Cell
from simulation.robot import Robot
from simulation.coordination import Coordination

from simulation.InterfaceV3 import *
lab = Grille(8,4)
lab.setRect(0,0,4,8,".")

lab = Grille(10,6)
lab.setRect(1,1,4,8,".")
lab.setRect(3,6,1,2,"?");
lab.setRect(3,2,1,1,"?");


robots = []
paths=[]

astar = AStar(lab)


dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp= Display(lab,astar,dic,paths,robots)
