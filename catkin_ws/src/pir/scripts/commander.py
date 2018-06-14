#!/usr/bin/env python


import rospy
from std_msgs.msg import String


pub = rospy.Publisher("/command", String)
rospy.init_node('commander')


def loop():
    while not rospy.is_shutdown():
        cmd = raw_input()
        pub.publish(String(cmd))

if __name__ == '__main__':
    try:
        loop()
    except rospy.ROSInterruptException:
        pass
