#!/usr/bin/env python3
import rospy
import time
import json
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json
import tf2_ros
import geometry_msgs.msg
#br = tf2_ros.TransformBroadcaster()
#t = geometry_msgs.msg.TransformStamped()
from sensor_msgs.msg  import Imu
Imu_data=Imu
imu_msg=Imu()
pub = rospy.Publisher('/imu_data', Imu_data, queue_size=50)
rospy.init_node('static_transform_publisher', anonymous=True)
rate = rospy.Rate(10) 
header=[0]
def on_connect(client, userdata, flags, rc):
    # This will be called once the client connects
    print(f"Connected with result code {rc}")
    # Subscribe here!
    client.subscribe("hello")
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
    #t.header.stamp = imu.header.stamp
    #t.header.frame_id = "/map"
    #t.child_frame_id = "/odom_combined"
    #t.transform.translation.x = 3.520897388458252
    #t.transform.translation.y = -0.11706339567899704
    #t.transform.translation.z = 0.0
    #t.transform.translation=imu.linear_acceleration
    #t.transform.rotation = imu.orientation
    #t.transform.rotation.x=0
    #t.transform.rotation.y=0
    #t.transform.rotation.z=0
    #t.transform.rotation.w=1
    #br.sendTransform(t)
    #t.header.frame_id = "/odom_combined"
    #t.child_frame_id = "/base_footprint"
    #br.sendTransform(t)
    #t.child_frame_id = "/base_link"
    #t.header.frame_id = "/base_footprint"
    #br.sendTransform(t)
    #t.child_frame_id = "/imu"
    #t.header.frame_id = "/base_link"
    #br.sendTransform(t)

    header[0]=+1
    pub.publish(imu)
    rate.sleep()

client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("pico", "picopassword")
client.connect('192.168.4.147', 1883)
client.loop_forever()  # Start networking daemon
