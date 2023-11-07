from machine import Pin, PWM
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import json

# Set up the motor driver pins
IN1 = Pin(2, Pin.OUT)
IN2 = Pin(3, Pin.OUT)
PWM_PIN1 = Pin(4)
PWM_PIN2 = Pin(5)
motor_pwm1 = PWM(PWM_PIN1)
motor_pwm2 = PWM(PWM_PIN2)

def set_motor_speed(speed):
    motor_pwm1.duty_u16(int(speed * 65535))
    motor_pwm2.duty_u16(int(speed * 65535))

# Set the direction of the motor
def set_motor_direction(direction):
    set_motor_speed(0)
    if direction == "forward":
        IN1.value(1)
        IN2.value(1)
    elif direction == "backward":
        IN1.value(0)
        IN2.value(0)
    elif direction == "right":
        IN1.value(1)
        IN2.value(0)
    elif direction == "left":
        IN1.value(0)
        IN2.value(1)
    else:
        IN1.value(0)
        IN2.value(0)

country = 'IT'
ssid = 'vistan12345'
password = 'welcome1'
mqtt_server = '192.168.4.147' #Replace with your MQTT Broker IP
client_id = "picoW"
topic = 'python/cmd_vel'
user_t = 'pico'
password_t = 'picopassword'

# Connect to Wi-Fi
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)
while station.isconnected() == False:
    pass
print('Connection successful')
print(station.ifconfig())

def sub_cb(topic, msg):
    msg = msg.decode('utf-8')
    msg1 = json.loads(msg)
    print(msg1['linear_dict']['x'])
    if msg1['linear_dict']['z'] > 0:
        print('forward')
        set_motor_direction("forward")
        set_motor_speed(0.5)
    elif msg1['linear_dict']['z'] < 0:
        print('backward')
        set_motor_direction("backward")
        set_motor_speed(0.5)
    elif msg1['angular_dict']['z'] < 0:
        print('right')
        set_motor_direction("right")
        set_motor_speed(0.5)
    elif msg1['angular_dict']['z'] > 0:
        print('left')
        set_motor_direction("left")
        set_motor_speed(0.5)
    else:
        set_motor_direction("none")
        set_motor_speed(0)
    print("stop")

def connect_and_subscribe():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60000)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

while True:
    try:
        client.check_msg()
    except OSError as e:
        restart_and_reconnect()