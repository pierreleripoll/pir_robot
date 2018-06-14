#!/usr/bin/env python


import rospy
from std_msgs.msg import String

import json
from bottle import run, post, request, response

@post('/')
def my_process():
  req = request.body.read()
  # do something with req_obj
  # ...
  pub.publish(req)
  return 'All done'


pub = rospy.Publisher("/command", String)
rospy.init_node('commander')


def loop():
    while not rospy.is_shutdown():
        cmd = raw_input()
        print cmd
        pub.publish(String(cmd))

if __name__ == '__main__':
    try:
        #loop()
        print("RUNING")
        run(host='localhost', port=8000, debug=True)
        print("RUNING")
    except rospy.ROSInterruptException:
        pass
