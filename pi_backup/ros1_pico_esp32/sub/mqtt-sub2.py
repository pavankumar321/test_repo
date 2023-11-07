#!/usr/bin/env python3
import rospy
import time
import json
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json
from geometry_msgs.msg  import Pose2D
Pose2D_data=Pose2D
Pose2D_msg=Pose2D()
pub = rospy.Publisher('/encoders', Pose2D_data, queue_size=1)
rospy.init_node('static_transform_publisher', anonymous=True)
rate = rospy.Rate(10) 
header=[0]
print('success')
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
    pose=Pose2D_msg
    print(dir(pose))
    rospy.loginfo(data)
    pose.theta=0.1
    pose.x=data1["rotary1"]
    pose.y=data1["rotary2"]
    header[0]=+1
    pub.publish(pose)
    rate.sleep()

client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("pico", "picopassword")
client.connect('192.168.4.147', 1883)
client.loop_forever()  # Start networking daemon
