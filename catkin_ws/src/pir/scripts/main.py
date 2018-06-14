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

import rospy
from std_msgs.msg import String

lab = Grille(20,20)
lab.setRect(5,5,10,2,".")
lab.setRect(5,5,2,10,".")
lab.setRect(10,5,2,10,".")
lab.setRect(5,12,10,2,".")

lab.setCell(Cell(10,12,"?"))
lab.setCell(Cell(12,13,"?"))

astar = AStar(lab)

dic = { "?":"grey", ".":"white","S":"green","G":"blue"}

disp = Display(lab, astar, dic)

masterPub = rospy.Publisher("master", String, queue_size=10)
rospy.init_node("master")

if __name__ == '__main__':
	try:
		print("master")
		for robot in disp.robots :
			robotMsg = robot.createMsg()
			masterPub.publish(robotMsg)
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
