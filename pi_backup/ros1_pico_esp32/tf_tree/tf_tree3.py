#!/usr/bin/env python
from __future__ import print_function
from std_msgs.msg import String
import rospy
import tf
import geometry_msgs.msg
from nav_msgs.msg import Odometry
br = tf.TransformBroadcaster()
t = geometry_msgs.msg.TransformStamped()
from geometry_msgs.msg import PoseWithCovarianceStamped
TwistMsg = PoseWithCovarianceStamped
odomMsg=Odometry
class tf_tree:
    def __init__(self):
        self.translation_x=4.243
        self.translation_y=-1.378
        self.translation_z=0.0
        self.rotation_x=0
        self.rotation_y=0
        self.rotation_z=-0.989
        self.rotation_w=0.146
        self.final_translation_x=4.243
        self.final_translation_y=-1.378
        self.final_translation_z=0.0
        self.final_rotation_x=0
        self.final_rotation_y=0
        self.final_rotation_z=-0.989
        self.final_rotation_w=0.146
        #self.updatePose(self.translation_x,self.translation_y,self.rotation_z,self.rotation_w)
    def callback(self,msg):
        print('Inside callback')
        #print(msg.pose.pose)
        #t.header.frame_id = "/map"
        #t.child_frame_id = "/odom"
        self.final_translation_x = msg.pose.pose.position.x
        self.final_translation_y = msg.pose.pose.position.y
        self.final_translation_z = msg.pose.pose.position.z
        self.final_rotation_x = msg.pose.pose.orientation.x
        self.final_rotation_y = msg.pose.pose.orientation.y
        self.final_rotation_z = msg.pose.pose.orientation.z
        self.final_rotation_w = msg.pose.pose.orientation.w
        self.translation_x=self.final_translation_x
        self.translation_y=self.final_translation_y
        self.translation_z=self.final_translation_z
        self.rotation_x=self.final_rotation_x
        self.rotation_y=self.final_rotation_y
        self.rotation_z=self.final_rotation_z
        self.rotation_w=self.final_rotation_w
        #self.updatePose(self.translation_x,self.translation_y,self.rotation_z,self.rotation_w)
        #print(msg.pose.pose.position.z)
        #print(msg.pose.pose.position.z)
    def listener(self):
        #print('entered listner')
        pub = rospy.init_node('robot_state_publisher', anonymous=True)
        rospy.Subscriber('/initialpose', TwistMsg, self.callback)
        msg = String()
        msg.data = pub
    def callback1(self,msg):
        #print('Inside callback1')
        #print(msg.pose.pose)
        #t.header.frame_id = "/map"
        #t.child_frame_id = "/odom"
        self.final_translation_x = msg.pose.pose.position.x + self.translation_x
        self.final_translation_y = msg.pose.pose.position.y + self.translation_y
        self.final_translation_z = msg.pose.pose.position.z + self.translation_z
        self.final_rotation_x = msg.pose.pose.orientation.x + self.rotation_x
        self.final_rotation_y = msg.pose.pose.orientation.y + self.rotation_y
        self.final_rotation_z = msg.pose.pose.orientation.z + self.rotation_z
        self.final_rotation_w = msg.pose.pose.orientation.w + self.rotation_w
        #self.updatePose(self.translation_x + msg.pose.pose.position.x,self.translation_y + msg.pose.pose.position.y,0,1)
        #print(msg.pose.pose.position.z)
    def listener1(self):
        #print('entered listener1')
        pub = rospy.init_node('robot_state_publisher', anonymous=True)
        rospy.Subscriber('/odom', odomMsg, self.callback1)
        msg = String()
        msg.data = pub
    def tf_tree_create(self):
        #print('start')
        t.header.stamp = rospy.Time.now()
        t.header.frame_id = "/map"
        t.child_frame_id = "/odom"   
        self.listener()
        self.listener1()
        br.sendTransform((self.final_translation_x,self.final_translation_y,self.final_translation_z),(self.final_rotation_x,self.final_rotation_y,self.final_rotation_z,self.final_rotation_w),rospy.Time.now(),"/odom_combined","/map")
        br.sendTransform((0,0,0),(0,0,0,1),rospy.Time.now(),"/base_footprint","/odom_combined")
        br.sendTransform((0,0,0),(0,0,0,1),rospy.Time.now(),"/base_link","/base_footprint")
        #br.sendTransform((0,0,0),(0,0,0,1),rospy.Time.now(),"/map","/base_footprint")
        br.sendTransform((0,0,0),(0,0,0,1),rospy.Time.now(),"/imu","/base_link")
        #print('end')

br = tf.TransformBroadcaster()
t = geometry_msgs.msg.TransformStamped()
rospy.init_node('robot_state_publisher', anonymous=True)
rate = rospy.Rate(10) 
tf_tree_create=tf_tree()
while True:
    tf_tree_create.tf_tree_create()
