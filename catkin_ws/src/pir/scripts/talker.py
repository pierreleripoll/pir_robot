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
position = [0, 0]
INIT_DIRECTION = "R" # fixe pour l'instant
orientation = -0.5

def callbackCmd(data):
	msg = data.data
	print data.data
	if msg[0] == "F" or msg[0] == "f":
		forward(float(msg[1:]))
	elif msg[0] == "T" or msg[0]=="t":
		turn(float(msg[1:]))

	if msg[0] =="P" or msg[0] == "p":
		pass

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
	return np.random.normal((node.x, node.y), 0.01, 2)



def forward(dist):
	resetOdom()
	global pose
	#print(pose)
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
	print "x0",x0," y0",y0,"xF ",xF," yF ",yF

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
			#print(abs(xF-x))
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
	print("ANGLE : "+str(angle))
	resetOdom()
	global pose
	#print(pose)
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
			#print (deriv)
			if np.sign(angle)>0:
				motion.angular.z = SPEED_TURN
			else:
				motion.angular.z = -SPEED_TURN
		else:
			goal = True
			print("GOAL REACHED")

		twistPub.publish(motion)
		rospy.sleep(0.01)
	motion.angular.z = 0
	twistPub.publish(motion)
	print("END TURN")



def getNodeAngle(node) :

	node_angle = 0 #absolu
	if(node.dir == "R") :
		node_angle = -0.5
	elif(node.dir == "D") :
		node_angle = 1
	elif(node.dir == "L") :
		node_angle = 0.5
	return node_angle



def goTo(node) :
	global position
	global orientation
	print("POSITION : " + str(position) + "ORIENTATION : "+ str(orientation))
	print("abs(node.x - position[0]) " + str(abs(node.x - position[0])))
	print("abs(node.y - position[1]) " + str(abs(node.y - position[1])))
	rospy.sleep(0.3)
	dz =getNodeAngle(node)-orientation
	if abs(dz)>DELTA_TURN:
		if abs(dz) > 1:
			dz = (-1)*(dz-np.sign(dz))
		print("\n\nTURN "+str(dz)+'\n\n')
		turn(dz)

		rospy.sleep(0.3)
	else:
		f= max(abs(node.y - position[1]),abs(node.x - position[0]))

		print("\n\nFORWARD " + str(f)+'\n\n')
		forward(abs(f))
		# if(abs(node.x - position[0]) <= DELTA_GOAL) :
		# 	forward(node.y - position[1])
		# elif(abs(node.y - position[1]) <= DELTA_GOAL) :
		# 	forward(node.x - position[0])

	position = getPosition(node)
	orientation = getNodeAngle(node)


# ajouter position erronée
def followPath(path) :
	for node in path :
		print("NEW NODE")
		print(repr(node))
		goTo(node)



def getOrientation(x,y):
	dx = x - position[0]
	dy = y - position[1]
	return math.atan2(dy,dx)



if __name__ == '__main__':
	try:
		print(pose)
		a = Node(Cell(0.2, 0), "R")
		b = Node(Cell(0.2, 0), "U")
		c = Node(Cell(0.2, 0.2), "U")
		d = Node(Cell(0.2, 0.2), "L")
		e = Node(Cell(0, 0.2), "L")
		f = Node(Cell(0, 0.2), "D")
		g = Node(Cell(0, 0), "D")
		h = Node(Cell(0, 0), "R")

		path = [a, b, c, d, e, f, g ,h]
		#followPath(path)
		#twister()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
