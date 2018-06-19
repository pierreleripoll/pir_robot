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
from simulation.robot import Robot
from tf.transformations import euler_from_quaternion, quaternion_from_euler


BOX_SIZE = 0.6
DELTA_GOAL = 0.01
DELTA_TURN = 0.08
SPEED_FORWARD = 0.2
SPEED_TURN = 0.8

pose = Pose()
position = [0, 0]
INIT_DIRECTION = "L" # fixe pour l'instant
orientation = math.pi/2
yaw = 0

robot = Robot("Nevers")

def cmdCallBack(data):
	msg = data.data
	print data.data
	if msg[0] == "F" or msg[0] == "f":
		forward(float(msg[1:]))
	elif msg[0] == "T" or msg[0]=="t":
		turn(math.pi * float(msg[1:])/180)

	if msg[0] =="P" or msg[0] == "p":
		pass

	resetOdom()

def odomCallBack(msg):
	global pose
	pose = msg.pose.pose
	global roll, pitch, yaw
	orientation_q = msg.pose.pose.orientation
	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
	(roll, pitch, yaw) = euler_from_quaternion (orientation_list)

def masterCallBack(data) :
	print("MASTERCALLBACK")
	msg = data.data
	print msg
	robot.readMsg(msg)
	print robot.path
	followPath()


twistPub=rospy.Publisher("/cmd_vel_mux/input/teleop",Twist, queue_size=10)
rospy.init_node(robot.name)
motion = Twist()
odomSub = rospy.Subscriber("/odom", Odometry, odomCallBack)
cmdSub = rospy.Subscriber("/command", String, cmdCallBack)
reset_odom = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)
masterSub = rospy.Subscriber("/master", String, masterCallBack)


def resetOdom():
	timer = time()
	while time() - timer < 0.5:
	    reset_odom.publish(Empty())



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
	angle = yaw
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
	rospy.sleep(0.3)
	global yaw
	global pose
	print("INIT YAW :"+str(yaw))
	print(pose)
	z0 = yaw
	zF = yaw + abs(angle)
	z=yaw
	zcount = 0
	goal = False
	dz = 0
	print "z0 ",z0," zF ", zF
	deriv = abs(zcount-abs(angle))
	while not goal and not rospy.is_shutdown() :
		print yaw
		if np.sign(yaw) == np.sign(z):
			dz = abs(yaw -z)
		else:
			z=yaw
		if dz>0.005:
			zcount += dz
			z=yaw
		if abs(zcount-abs(angle))>deriv  :
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
			print("GOAL REACHED DERIV "+str(deriv))

		twistPub.publish(motion)
		rospy.sleep(0.01)
	motion.angular.z = 0
	twistPub.publish(motion)
	print("END TURN YAW : "+str(yaw)+ " COUNT :"+str(zcount))



def getNodeAngle(node) :

	node_angle = 0 #absolu
	if(node.dir == "R") :
		node_angle = -math.pi/2
	elif(node.dir == "D") :
		node_angle = math.pi
	elif(node.dir == "L") :
		node_angle = math.pi/2
	return node_angle



def goTo(node) :
	global position
	global orientation
	node.x = node.x * BOX_SIZE
	node.y = node.y * BOX_SIZE
	print("POSITION : " + str(position) + "ORIENTATION : "+ str(orientation))
	rospy.sleep(0.3)
	dz =getNodeAngle(node)-orientation
	if abs(dz)>DELTA_TURN:
		if abs(dz) > math.pi:
			dz = (-1)*(dz-(np.sign(dz)*math.pi))
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


def followPath() :
	init = rospy.get_time()
	global position
	global INIT_DIRECTION
	position[0] = robot.path[0].x * BOX_SIZE
	position[1] = robot.path[0].y * BOX_SIZE
	INIT_DIRECTION = robot.path[0].dir
	robot.path.pop(0)
	for node in robot.path :
		print("-------")
		print("NEW NODE")
		print(repr(node))
		goTo(node)
		end = rospy.get_time()
		chrono = end - init
		print("TIME : " + str(chrono))
		while(chrono < node.time and not rospy.is_shutdown()) :
			end = rospy.get_time()
			chrono = end - init
			rospy.sleep(0.01)
		print("TIME : " + str(chrono))
		print("-------")



def getOrientation(x,y):
	dx = x - position[0]
	dy = y - position[1]
	return math.atan2(dy,dx)



if __name__ == '__main__':
	try:
		print(pose)
		#a = Node(Cell(0.8, 0), "R")
		#a.time = 0
		#b = Node(Cell(0.8, 0), "U")
		#b.time = 6
		#c = Node(Cell(0.8, 0.8), "U")
		#b.time = 12
		#d = Node(Cell(0.8, 0.8), "L")
		#c.time = 18
		#e = Node(Cell(0, 0.8), "L")
		#d.time = 24
		#f = Node(Cell(0, 0.8), "D")
		#f.time = 30
		#g = Node(Cell(0, 0), "D")
		#g.time = 50
		#h = Node(Cell(0, 0), "R")
		#h.time = 56

		#robot.path = [a, b, c, d, e, f, g ,h] # après on récupérera par message

		print(robot.path)
		#followPath()

		#twister()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
