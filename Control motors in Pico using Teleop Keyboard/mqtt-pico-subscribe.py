from machine import Pin
import time
from umqttsimple import MQTTClient
import ubinascii
import machine
import micropython
import network
import netman

#import gc
#gc.collect()

country = 'IT'
ssid = 'vistan12345'
password = 'welcome1'
mqtt_server = '192.168.242.17'  #Replace with your MQTT Broker IP

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

#def sub_cb():
#    print ('Received Message %s from topic %s' % msg)
#    print('Hello Swetha Bhandekar')


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
       new_msg = client.check_msg()
     
  except OSError as e:
    restart_and_reconnect

