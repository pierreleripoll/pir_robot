#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
import json
import numpy as np
from geometry_msgs.msg import PoseStamped, Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from std_msgs.msg import Empty
from time import time
import sys
sys.path.insert(0, '../')
from simulation.node import Node
from simulation.cell import Cell


DELTA_GOAL = 0.01
DELTA_TURN = 0.002
SPEED_FORWARD = 0.2
SPEED_TURN = 0.8

pose = Pose()
INIT_DIRECTION = "U" # fixe pour l'instant
orientation = 0

def callbackCmd(data):
	msg = data.data
	print data.data
	if msg[0] == "F" or msg[0] == "f":
		forward(float(msg[1:]))
	elif msg[0] == "T" or msg[0]=="t":
		turn(float(msg[1:]))
	resetOdom()

def odomCallBack(msg):
	global pose
	pose = msg.pose.pose



twistPub=rospy.Publisher("/cmd_vel_mux/input/teleop",Twist, queue_size=10)
rospy.init_node("twister")
motion = Twist()
odomSub = rospy.Subscriber("/odom", Odometry, odomCallBack)
cmdSub = rospy.Subscriber("/command", String, callbackCmd)
reset_odom = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)


def resetOdom():
	timer = time()
	while time() - timer < 0.25:
	    reset_odom.publish(Empty())

def callbackCmd(msg):
	print(msg)
	if msg[0] == "F":
		forward(double(msg[1:]))
	elif msg[0] == "T":
		turn(double(msg[1:]))




def twister():
	global pose
	print(pose)
	while not rospy.is_shutdown():
		rospy.sleep(0.3)
		forward(0.5)
	 	rospy.sleep(0.3)
	 	turn(0.5)
	#	print pose
	print "TWISTER"


# Renvoie une position erronée (loi normale) en fonction de la position en paramètre
def getPosition(node) :
	return np.random.normal((node.x, node.y), 0.1, 2)



def forward(dist):
	global pose
	print(pose)
	x0 = pose.position.x
	y0 = pose.position.y
	angle = pose.orientation.z * math.pi
	print("teta "+str(angle))
	dx = math.cos(angle) * dist
	dy = math.sin(angle) * dist
	xF = x0+dx
	yF = y0+dy
	goal = False

	x = pose.position.x

	xcount = 0
	deriv = abs(xcount-xF)
	#print "x0",x0," y0",y0,"xF ",xF," yF ",yF

	while not goal and not rospy.is_shutdown() :
		dx = abs(pose.position.x-x)

		if dx>0.005:
			x = pose.position.x
			if np.sign(dist)>0:
				xcount += dx
			else :
				xcount -= dx

		#print "("+str(x)+","+str(y)+")"
		if abs(xcount-xF)>deriv :
			print("ON DEPASSE")
			goal = True
		deriv = abs(xcount-xF)

		if (abs(xF-x0)<2*DELTA_GOAL or abs(xF-x)>DELTA_GOAL):
			print(abs(xF-x))
			if np.sign(dist)>0:
				motion.linear.x = SPEED_FORWARD
			else:
				motion.linear.x = -SPEED_FORWARD
		else:
			goal = True
			print("GOAL REACHED")

		twistPub.publish(motion)
		rospy.sleep(0.01)

	motion.linear.x = 0
	twistPub.publish(motion)
	print "END FORWARD"


#angle en radian/PI
def turn(angle):
	global pose
	print(pose)
	z0 = pose.orientation.z
	zF = pose.orientation.z + abs(angle)
	z=pose.orientation.z
	zcount = 0
	goal = False
	dz = 0
	print "z0 ",z0," zF ", zF
	deriv = abs(zcount-abs(angle))
	while not goal and not rospy.is_shutdown() :
		if np.sign(pose.orientation.z) == np.sign(z):
			dz = abs(pose.orientation.z -z)
		else:
			z=pose.orientation.z
		if dz>0.005:
			zcount += dz
			z=pose.orientation.z
	#	print "("+str(z)+")"
		if abs(zcount-abs(angle))>deriv :
			print("ON DEPASSE")
			goal = True
		deriv = abs(zcount-abs(angle))

		if deriv>DELTA_TURN:
			print (deriv)
			if np.sign(angle)>0:
				motion.angular.z = SPEED_TURN
			else:
				motion.angular.z = -SPEED_TURN
		else:
			goal = True
			print("GOAL REACHED")

		twistPub.publish(motion)
		rospy.sleep(0.01)
	print("END TURN")



def getNodeAngle(node) :
	if(node.dir == INIT_DIRECTION) :
		return 0

	else :
		init_angle = 0 #absolu
		if(INIT_DIRECTION == "R") :
			init_angle = 0.5
		elif(INIT_DIRECTION == "D") :
			init_angle = 1
		elif(INIT_DIRECTION == "L") :
			init_angle = -0.5

		node_angle = 0 #absolu
		if(node.dir == "R") :
			node_angle = 0.5
		elif(node.dir == "D") :
			node_angle = 1
		elif(node.dir == "L") :
			node_angle = -0.5

		if(node_angle - init_angle == 1.5) :
			return -0.5
		else :
			return node_angle - init_angle



def goTo(node) :
	position = getPosition(node)
	rospy.sleep(0.3)
	if(abs(node.x - position[0]) <= DELTA_GOAL) :
		turn(getNodeAngle(node) - orientation)
		rospy.sleep(0.3)
		forward(node.y - position[1])
	elif(abs(node.x - position[1]) <= DELTA_GOAL) :
		turn(getNodeAngle(node) - orientation)
		rospy.sleep(0.3)
		forward(node.x - position[0])
	else :
		print("We fucked up")


# ajouter position erronée
def followPath(path) :
	for node in path :
		goTo(node)






if __name__ == '__main__':
	try:
		print(pose)
		a = Node(Cell(0, 0), "U")
		b = Node(Cell(1, 0), "R")
		c = Node(Cell(1, 1), "U")
		path = [a, b, c]
		followPath(path)
		#twister()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
