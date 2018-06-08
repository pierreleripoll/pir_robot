#!/usr/bin/env python


import rospy
from std_msgs.msg import String

pub = rospy.Publisher("/command", String)
rospy.init_node('commander')


def run():
    while not rospy.is_shutdown():
        cmd = raw_input()
        print cmd
        pub.publish(String(cmd))

if __name__ == '__main__':
    try:
        run()
    except rospy.ROSInterruptException:
        pass
