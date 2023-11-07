#!/usr/bin/env python
from __future__ import print_function
import rospy
from std_msgs.msg import String
import json
import threading

#import roslib; roslib.load_manifest('teleop_twist_keyboard')
import tf2_ros
import geometry_msgs.msg
br = tf2_ros.TransformBroadcaster()
t = geometry_msgs.msg.TransformStamped()
from geometry_msgs.msg import PoseWithCovarianceStamped
import random
import time
TwistMsg = PoseWithCovarianceStamped

def callback(msg):
    print(msg.pose.pose.orientation)
    #data={"linear_dict": {"x": msg.linear.x, "y": msg.linear.y, "z": msg.linear.z},"angular_dict" : {"x": msg.angular.x, "y": msg.angular.y, "z": msg.angular.z}}
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "/map"
    t.child_frame_id = "/odom_combined"
    t.transform.translation.x = msg.pose.pose.position.x
    t.transform.translation.y = msg.pose.pose.position.y
    t.transform.translation.z = msg.pose.pose.position.z
    #t.transform.translation=imu.linear_acceleration
    t.transform.rotation = msg.pose.pose.orientation
    #dir(msg.pose)
    #t.transform.rotation.x=0
    #t.transform.rotation.y=0
    #t.transform.rotation.z=0
    #t.transform.rotation.w=0
    br.sendTransform(t)
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub = rospy.init_node('robot_state_publisher', anonymous=True)
    rospy.Subscriber('initialpose', TwistMsg, callback)
    msg = String()
    msg.data = pub
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
