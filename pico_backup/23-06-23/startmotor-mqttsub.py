from machine import Pin, PWM
import time
import sys
#from rotary_irq_rp2 import RotaryIRQ
from rotary_esp import RotaryIRQ
import uasyncio as asyncio
from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import netman
#import sampleDCMotor123

country = 'IT'
ssid = 'vistan12345'
password = 'welcome1'
mqtt_server = '192.168.172.17'  #Replace with your MQTT Broker IP

client_id = "PicoW"
topic = 'python/mqtt'
user_t = 'pico'
password_t = 'picopassword'
wifi_connection = netman.connectWiFi(ssid,password,country)

last_message = 0
message_interval = 5
counter = 0

station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

def sub_cb(topic, msg):
#    print("New message on topic {}".format(topic.decode('utf-8')))
    msg = msg.decode('utf-8')
    print(msg)
           
def connect_and_subscribe():
  #global client_id, mqtt_server, topic
  client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
  client.set_callback(sub_cb)
  client.connect()
  client.subscribe(topic)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic))
#  print ('Received Message %s from topic %s' % msg)
#  print('Hello Swetha Bhandekar')
  return client

def restart_and_reconnect():
  print('Failed to connect to MQTT broker. Reconnecting...')
  time.sleep(10)
  machine.reset()

try:
  client = connect_and_subscribe()
except OSError as e:
  restart_and_reconnect()
  
# Set up the motor driver pins
IN1 = Pin(12, Pin.OUT)
IN2 = Pin(13, Pin.OUT)
IN3 = Pin(18, Pin.OUT)
IN4 = Pin(19, Pin.OUT)
PWM_PIN1 = Pin(3)
PWM_PIN2 = Pin(2)

motor_pwm1 = PWM(PWM_PIN1)
motor_pwm2= PWM(PWM_PIN2)

# Set the speed of the motor
def set_motor_speed(speed):
    motor_pwm1.duty_u16(int(speed * 65535))
    motor_pwm2.duty_u16(int(speed * 65535))

IN1.value(1)
IN2.value(1)
IN3.value(1)
IN4.value(1)
set_motor_speed(0)
time.sleep(2)
# Set the direction of the motor
def set_motor_direction(direction):
    if direction == "forward":
        IN1.value(1)
        IN2.value(0)
        IN3.value(1)
        IN4.value(0)
    elif direction == "backward":
        IN1.value(0)
        IN2.value(1)
        IN3.value(0)
        IN4.value(1)
    else:
        IN1.value(0)
        IN2.value(0)
        IN3.value(0)
        IN4.value(0)
        
class Application2():
    def __init__(self, r1, r2):
        self.r1 = r1
        self.r2 = r2
        self.myevent = asyncio.Event()
        asyncio.create_task(self.action())
        r1.add_listener(self.callback)
        r2.add_listener(self.callback)

    def callback(self):
        self.myevent.set()

    async def action(self):
        while True:
            await self.myevent.wait()
            print('Readings:  rotary 1 = {}, rotary 2 = {}'. format(
                self.r1.value(), self.r2.value()))
            # do something with the encoder results ...
            self.myevent.clear()


async def main():
    rotary_encoder_1 = RotaryIRQ(pin_num_clk=12,
                                 pin_num_dt=13,
                                 min_val=0,
                                 max_val=20000,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_WRAP)

    rotary_encoder_2 = RotaryIRQ(pin_num_clk=18,
                                 pin_num_dt=19,
                                 min_val=30000,
                                 max_val=50000,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_WRAP)

    # create tasks that use the rotary encoders
    #app1 = Application1(rotary_encoder_1)
    Readings = Application2(rotary_encoder_1, rotary_encoder_2)
# Test the motor by running it forward and backward
    while True:
        set_motor_direction("forward")
        set_motor_speed(0.5)
        time.sleep(1)
        set_motor_direction("backward")
        set_motor_speed(0.5)
        time.sleep(1)
        set_motor_direction(" ")
        set_motor_speed(0)
        time.sleep(1)
        await asyncio.sleep_ms(1)
   
    
    
try:
    asyncio.run(main())
    new_msg = client.check_msg()
except (KeyboardInterrupt, Exception) as e:
    print('Exception {} {}\n'.format(type(e).__name__, e))
    restart_and_reconnect
finally:
    ret = asyncio.new_event_loop()  # Clear retained uasyncio state



