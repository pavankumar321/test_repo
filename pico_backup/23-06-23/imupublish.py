import netman
import time
from umqttsimple import MQTTClient
import machine
from bno055_base import BNO055_BASE
import json
def imu():
    
    i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
    imu = BNO055_BASE(i2c)
    country = 'IT'
    ssid = 'vistan12345'
    password = 'welcome1'
    wifi_connection = netman.connectWiFi(ssid,password,country)
    topic_pub = 'Node'

    last_message = 0
    message_interval = 5
    counter = 0
#mqtt config
mqtt_server = '192.168.87.215'
client_id = 'PicoW'
user_t = 'pico'
password_t = 'picopassword'



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
                      
   
    calibrated = False
    while True:
        time.sleep(1)
        if not calibrated:
            calibrated = imu.calibrated()
            try:
                dictionary = ('Mag  x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()),
                                                'Gyro x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()),
                                                'Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()),
                                                'Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()),
                                                'Temperature {}°C'.format(imu.temperature()),
                                                'Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity())),
                
                client.subscribe(topic_pub, msg = json.dumps(dictionary)
                                                        )

                                        #  msg1 = f"{'Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro())}")
                #"{Mag  'x': f{:5.*imu.mag()}, 'y': '2', 'z': '3'}"
                #client.publish(topic_pub, msg=f"Readings:  rotary 1 = {self.r1.value()}, rotary 2 = {self.r2.value()}")
                                               #"print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))"
                                               #print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
                                               #print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
                                               #print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
                                               #print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
                                               #print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))"}
                                               
                print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
                print('Temperature {}°C'.format(imu.temperature()))
                print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
                print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
                print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
                print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
                print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
                print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
        
                time.sleep(3)
            except:
                reconnect()
                pass
    client.disconnect()


