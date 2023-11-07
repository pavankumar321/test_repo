#!/usr/bin/env python3
import rospy
import time
import json
from std_msgs.msg import String
import paho.mqtt.client as mqtt
import json
from geometry_msgs.msg  import Vector3Stamped
Vector3Stamped_data=Vector3Stamped
Vector3Stamped_msg=Vector3Stamped()
pub = rospy.Publisher('/speed',Vector3Stamped_data, queue_size=50)
rospy.init_node('base_footprint_odom', anonymous=True)
rate = rospy.Rate(10) 
header=[0]
print('success')
radius=0.0625
previous_ticks=[0,0,0]
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
    speed_data=Vector3Stamped_msg
    rospy.loginfo(data)
    speed_data.header.stamp=rospy.Time.now()
    left_motor_ticks=data1['rotary1']
    right_motor_ticks=data1['rotary2']
    if previous_ticks[0]==0 and previous_ticks[1]==0:
        previous_ticks[0]=data1['rotary1']
        previous_ticks[1]=data1['rotary2']
        previous_ticks[2]=time.time()
    else:
        t_diff=time.time()-previous_ticks[2]
        right_motor_ticks_diff=data1['rotary2']-previous_ticks[1]
        left_motor_ticks_diff=previous_ticks[0]-data1['rotary1']
        speed_data.vector.x=((right_motor_ticks_diff / 2786) * 2 * (22 / 7) * radius) * t_diff
        speed_data.vector.y=((left_motor_ticks_diff / 2786) * 2 * (22 / 7) * radius) * t_diff
        speed_data.vector.z=t_diff
        previous_ticks[0]=data1['rotary1']
        previous_ticks[1]=data1['rotary2']
        previous_ticks[2]=time.time()
        pub.publish(speed_data)
        rate.sleep()

client = mqtt.Client("mqtt-test") # client ID "mqtt-test"
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set("pico", "picopassword")
client.connect('192.168.4.147', 1883)
client.loop_forever()  # Start networking daemon
