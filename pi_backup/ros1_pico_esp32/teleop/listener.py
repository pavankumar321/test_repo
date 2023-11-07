#!/usr/bin/env python
from __future__ import print_function
import rospy
from std_msgs.msg import String

import threading

#import roslib; roslib.load_manifest('teleop_twist_keyboard')

from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped

import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


TwistMsg = Twist

def callback(msg):
    print(msg.linear)
    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', msg)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub = rospy.init_node('teleop_twist_keyboard', anonymous=True)
    print('out : ',TwistMsg.linear)
    rospy.Subscriber('cmd_vel', TwistMsg, callback)
    msg = String()
    msg.data = pub
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
