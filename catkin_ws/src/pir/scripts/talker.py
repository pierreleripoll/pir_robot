#!/usr/bin/env python

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


DELTA_GOAL = 0.01
DELTA_TURN = 0.002
SPEED_FORWARD = 0.2
SPEED_TURN = 0.8

pose = Pose()

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



twistPub=rospy.Publisher("/cmd_vel_mux/input/teleop",Twist)
rospy.init_node("twister")
motion = Twist()
odomSub = rospy.Subscriber("/odom", Odometry, odomCallBack)
cmdSub = rospy.Subscriber("/command", String, callbackCmd)
reset_odom = rospy.Publisher('/mobile_base/commands/reset_odometry', Empty, queue_size=10)


def resetOdom():
	timer = time()
	while time() - timer < 0.25:
	    reset_odom.publish(Empty())




def twister():
	global pose
	print pose
	while not rospy.is_shutdown():
		rospy.sleep(0.3)
		forward(0.5)
	 	rospy.sleep(0.3)
	 	turn(0.5)
	#	print pose
	print "TWISTER"




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
			print "GOAL REACHED"

		twistPub.publish(motion)
		rospy.sleep(0.01)

	motion.linear.x = 0
	twistPub.publish(motion)
	print "END FORWARD"


#angle en radian/PI
def turn(angle):
	global pose
	print pose
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
			print "GOAL REACHED"

		twistPub.publish(motion)
		rospy.sleep(0.01)
	motion.angular.z = 0
	twistPub.publish(motion)

	print "END TURN"



if __name__ == '__main__':
	try:
		#twister()
		rospy.spin()
	except rospy.ROSInterruptException:
		pass
