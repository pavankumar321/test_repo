#!/usr/bin/env python3
import rospy
import time
import json
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json
import tf2_ros
import geometry_msgs.msg
br = tf2_ros.TransformBroadcaster()
t = geometry_msgs.msg.TransformStamped()
from sensor_msgs.msg  import Imu
Imu_data=Imu
imu_msg=Imu()
pub = rospy.Publisher('/imu_data', Imu_data, queue_size=50)
rospy.init_node('static_transform_publisher', anonymous=True)
rate = rospy.Rate(10) 
header=[0]
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
    #t.header.stamp = rospy.Time.now()
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
    #pub = rospy.init_node('robot_state_publisher', anonymous=True)
    rospy.Subscriber('initialpose', TwistMsg, callback)
    msg = String()
    msg.data = pub
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spinonce()
    return msg

if __name__ == '__main__':
    listener()

def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("hello")
i=[0]
def on_message(client, userdata, msg):
    print('hello')
    data=msg.payload.decode('utf-8')
    print(data)
    data1=json.loads(data)
    imu=imu_msg
    rospy.loginfo(data)
    imu.header.stamp=rospy.Time.now()
    imu.header.frame_id="imu"
    imu.orientation.x=data1["imu"]["Orientation"][0]
    imu.orientation.y=data1["imu"]["Orientation"][1]
    imu.orientation.z=data1["imu"]["Orientation"][2]
    imu.orientation.w=data1["imu"]["Orientation"][3]
    imu.angular_velocity.x=data1["imu"]["ang_vel"][0]
    imu.angular_velocity.y=data1["imu"]["ang_vel"][1]
    imu.angular_velocity.z=data1["imu"]["ang_vel"][2]
    imu.linear_acceleration.x=data1["imu"]["Lin acc"][0]
    imu.linear_acceleration.y=data1["imu"]["Lin acc"][1]
    imu.linear_acceleration.z=data1["imu"]["Lin acc"][2]
    t.header.stamp = imu.header.stamp
    t.header.frame_id = "/map"
    t.child_frame_id = "/odom_combined"
    listener()
    if i[0]==0:
        t.transform.translation.x = 0.242
        t.transform.translation.y = -2.562
        t.transform.translation.z = 0
        #t.transform.translation=imu.linear_acceleration
        #t.transform.rotation = imu.orientation
        t.transform.rotation.x=0
        t.transform.rotation.y=0
        t.transform.rotation.z= -0.9250348903825633
        t.transform.rotation.w= 0.37988215485189514
    i[0]=i[0]+1
    br.sendTransform(t)
    t.header.frame_id = "/odom_combined"
    t.child_frame_id = "/base_footprint"
    br.sendTransform(t)
    t.child_frame_id = "/base_link"
    t.header.frame_id = "/base_footprint"
    br.sendTransform(t)
    t.child_frame_id = "/imu"
    t.header.frame_id = "/base_link"
    br.sendTransform(t)

    header[0]=+1
    pub.publish(imu)
    rate.sleep()

client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("pico", "picopassword")
client.connect('192.168.4.17', 1883)
client.loop_forever()  # Start networking daemon
