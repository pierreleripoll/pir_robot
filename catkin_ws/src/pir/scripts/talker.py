#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import PoseStamped, Pose
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

DELTA_GOAL = 0.2
SPEED_FORWARD = 0.5
SPEED_TURN = 0.5

pose = Pose()

def odomCallBack(msg):
	global pose
	pose = msg.pose.pose


twistPub=rospy.Publisher("/cmd_vel_mux/input/teleop",Twist)
rospy.init_node("twister")
motion = Twist()
odomSub = rospy.Subscriber("/odom", Odometry, odomCallBack)




def twister():
	global pose
	print pose
	rospy.sleep(1)
	forward(1)
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
	print "x0",x0," y0",y0,"xF ",xF," yF ",yF
	while not goal and not rospy.is_shutdown() :
		x = pose.position.x
		y = pose.position.y
		print "("+str(x)+","+str(y)+")"
		if abs(xF-x)>DELTA_GOAL and abs(yF-y)>DELTA_GOAL:
			motion.linear.x = SPEED_FORWARD
		else:
			motion.linear.x = 0
			goal = True

		twistPub.publish(motion)
		rospy.sleep(0.01)


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
		twister()
	except rospy.ROSInterruptException:
		pass
