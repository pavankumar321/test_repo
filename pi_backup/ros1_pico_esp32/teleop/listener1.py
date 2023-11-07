#!/usr/bin/env python
from __future__ import print_function
import rospy
from std_msgs.msg import String
import json
import threading

#import roslib; roslib.load_manifest('teleop_twist_keyboard')

from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
import random
import time

from paho.mqtt import client as mqtt_client


broker = '192.168.4.147'
port = 1883
topic = "python/cmd_vel"
# generate client ID with pub prefix randomly
client_id = 'PicoW'
username = 'pico'
password = 'picopassword'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
client = connect_mqtt()
client.loop_start()
import sys
from select import select

if sys.platform == 'win32':
    import msvcrt
else:
    import termios
    import tty


TwistMsg = Twist

def callback(msg):
    data={"linear_dict": {"x": msg.linear.x, "y": msg.linear.y, "z": msg.linear.z},"angular_dict" : {"x": msg.angular.x, "y": msg.angular.y, "z": msg.angular.z}}
    data = str(json.dumps(data))
    client.publish(topic, data)
    print(data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pub = rospy.init_node('teleop_twist_keyboard', anonymous=True)
    print('out : ',TwistMsg.linear)
    rospy.Subscriber('/cmd_vel', TwistMsg, callback)
    msg = String()
    msg.data = pub
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
