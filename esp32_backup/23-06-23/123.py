import netman
import time
from umqttsimple import MQTTClient
import machine

country = 'IT'
ssid = 'vistan12345'
password = 'welcome1'
#wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.245.215'
client_id = 'PicoW'
user_t = 'pico'
password_t = 'picopassword'
topic_pub = 'hello'

last_message = 0
message_interval = 5
counter = 0

#MQTT connect
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
#    client = mqtt_connect()

while True:
    try:
       client = mqtt_connect()
    except OSError as e:
        reconnect()
    
    while True:
        try:
            client.publish(topic_pub, msg='Hi 12345!')
            print('published')
            time.sleep(3)
        except:
            reconnect()
            pass
    client.disconnect()
    