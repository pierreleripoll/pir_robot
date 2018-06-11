#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import math
import numpy as np
from geometry_msgs.msg import PoseStamped, Pose
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Image
import sys, tty, termios
from cv_bridge import CvBridge, CvBridgeError
import cv2
from node import Node

DELTA_GOAL = 0.1
DELTA_TURN = 0.02
SPEED_FORWARD = 0.2
SPEED_TURN = 0.8

pose = Pose()
INIT_DIRECTION = "U" # fixe pour l'instant

def odomCallBack(msg):
	global pose
	pose = msg.pose.pose

def callbackImage(msg):
    bridge = CvBridge()
    # Use cv_bridge() to convert the ROS image to OpenCV format
    try:
        # The depth image is a single-channel float32 image
        depth_image = bridge.imgmsg_to_cv(msg, "32FC1")
    except CvBridgeError, e:
        print e
    # depth_image.height = height of the matrix
    # depth_image.width = width of the matrix
    # depth_image[x,y] = the float value in m of a point place a a height x and width y

twistPub=rospy.Publisher("/cmd_vel_mux/input/teleop",Twist)
rospy.init_node("twister")
motion = Twist()
odomSub = rospy.Subscriber("/odom", Odometry, odomCallBack)


def callbackCmd(msg):
	print msg
	if msg[0] == "F":
		forward(double(msg[1:]))
	elif msg[0] == "T":
		turn(double(msg[1:]))




def twister():
	global pose
	print pose
	while not rospy.is_shutdown():
		rospy.sleep(0.3)
		# forward(0.5)
		# rospy.sleep(0.3)
		# turn(0.5)
	print "TWISTER"



# Renvoie une position erronée (loi normale) en fonction de la position en paramètre
def getPosition(position) :
	return np.random.normal((position.x, position.y), 1.0, 2)



def forward(dist):
	global pose
	print pose
	x0 = pose.position.x
	y0 = pose.position.y
	angle = pose.orientation.z * math.pi
	print "teta "+str(angle)
	dx = math.cos(angle) * dist
	dy = math.sin(angle) * dist
	xF = x0+dx
	yF = y0+dy
	goal = False
	print "x0",x0," y0",y0,"xF ",xF," yF ",yF
	while not goal and not rospy.is_shutdown() :
		x = pose.position.x
		y = pose.position.y
		print "("+str(x)+","+str(y)+")"
		if (abs(xF-x0)<2*DELTA_GOAL or abs(xF-x)>DELTA_GOAL) and (abs(yF-y0)<2*DELTA_GOAL or abs(yF-y)>DELTA_GOAL):
			motion.linear.x = SPEED_FORWARD
		else:
			motion.linear.x = 0
			goal = True
			print "GOAL REACHED"

		twistPub.publish(motion)
		rospy.sleep(0.01)
	print "END FORWARD"


#angle en radian/PI
def turn(angle):
	global pose
	print pose
	z0 = pose.orientation.z
	zF = pose.orientation.z +angle
	z=pose.orientation.z
	zcount = 0
	goal = False
	dz = 0
	print "z0 ",z0," zF ", zF
	while not goal and not rospy.is_shutdown() :
		if np.sign(pose.orientation.z) == np.sign(z):
			dz = abs(pose.orientation.z - z)
		zcount += dz
		z=pose.orientation.z
		print "("+str(z)+")"
		if abs(zcount-angle)>DELTA_TURN:
			motion.angular.z = SPEED_TURN
		else:
			motion.angular.z = 0
			goal = True
			print "GOAL REACHED"

		twistPub.publish(motion)
		rospy.sleep(0.01)
	print "END TURN"



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
	if(abs(node.x - pose.position.x) <= DELTA_GOAL) :
		turn(getNodeAngle(node) - pose.orientation.z)
		forward(node.y - pose.position.y)
	elif(abs(node.x - pose.position.y) <= DELTA_GOAL) :
		turn(getNodeAngle(node) - pose.orientation.z)
		forward(node.x - pose.position.x)
	else :
		print("We fucked up")


# ajouter position erronée
def followPath(path) :
	for node in path :
		goTo(node)


def forwardOld(speed,time):
	timePassed = 0
	while timePassed < time:
		motion.linear.x = speed
		motion.angular.z = 0
		twistPub.publish(motion)
		rospy.sleep(0.1)
		timePassed += 0.1
	motion.linear.x = 0
	motion.angular.z = 0
	twistPub.publish(motion)


def turnOld(speed,time):
	timePassed = 0
	global pose
	while timePassed < time:
		motion.linear.x = 0
		motion.angular.z = speed
		twistPub.publish(motion)
		rospy.sleep(0.1)
		timePassed += 0.1
		print pose
	motion.linear.x = 0
	motion.angular.z = 0
	twistPub.publish(motion)

if __name__ == '__main__':
	try:
		#twister()
		a = Node(0, 0, "U")
		b = Node(1, 0, "R")
		c = Node(1, 1, "U")
		path = [a, b, c]
		followPath(path)
	except rospy.ROSInterruptException:
		pass
