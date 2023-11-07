import netman
from umqttsimple import MQTTClient
import time
import machine
import json

def imu():
    
    i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
    imu = BNO055_BASE(i2c)
    country = 'IT'
    ssid = 'vistan12345'
    password = 'welcome1'
    wifi_connection = netman.connectWiFi(ssid,password,country)
    
# Define the callback function to handle incoming messages
def sub_cb(topic, msg):
    print((topic, msg))

# Define the MQTT broker parameters
mqtt_server = "192.168.87.215"
mqtt_port = 1883
mqtt_user = "pico"
mqtt_pass = "picopassword"
mqtt_topic = "Node"

# Create an MQTT client instance
client_id = "PicoW"
client = MQTTClient(client_id, mqtt_server, mqtt_port, mqtt_user, mqtt_pass)

# Set the callback function
client.set_callback(sub_cb)

# Connect to the MQTT broker
#client.connect()
def mqtt_connect():
        client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60)
        client.connect()
        print('Connected to %s MQTT Broker'%(mqtt_server))
        return client
#reconnect & reset
def reconnect():
        print('Failed to connected to MQTT Broker. Reconnecting...')
        time.sleep(5)
        machine.reset()
        
# Subscribe to the topic
        client.subscribe(mqtt_topic)

# Wait for incoming messages
while True:
        client.check_msg()
        time.sleep(1)