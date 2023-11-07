import netman
import time
from umqttsimple import MQTTClient
import machine
import sys
#from rotary_irq_rp2 import RotaryIRQ
from rotary_irq_esp import RotaryIRQ
import uasyncio as asyncio
from bno055_base import BNO055_BASE
import json


i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
imu = BNO055_BASE(i2c)

country = 'IT'
ssid = 'vistan12345'
password = 'welcome1'
#wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.4.17'
client_id = 'PicoW'
user_t = 'pico'
password_t = 'picopassword'
topic_pub = 'hello'

last_message = 0
message_interval = 5
counter = 0

#MQTT connect
def mqtt_connect():
    client = MQTTClient(client_id, mqtt_server, user=user_t, password=password_t, keepalive=60000)
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
    while True:
        try:
            class Application2():
                def __init__(self, r1, r2):
                    self.r1 = r1
                    self.r2 = r2
                    self.establish_connection()
                    self.myevent = asyncio.Event()
                    asyncio.create_task(self.action())
                    r1.add_listener(self.callback)
                    r2.add_listener(self.callback)
                    
                def establish_connection(self):
                    try:
                        self.client = mqtt_connect()
                    except OSError as e:
                        reconnect() 
                def callback(self):
                    self.myevent.set()

                async def action(self):
                    while True:
                        
                        calibrated = imu.calibrated()
                        await self.myevent.wait()
                        data = {'rotary1' :self.r1.value(),'rotary2' : self.r2.value(),'imu':{'Mag': imu.mag(),'Accel': imu.accel(),'Lin acc': imu.lin_acc(),
                                                                                              'Orientation': imu.quaternion(), 'ang_vel': imu.gyro()}}
                                                                   
                        try:
                            print(data)
                            print('start')
                            self.client.publish(topic_pub, msg = json.dumps(data))
                            print('end')  
                            # client.publish(topic_pub, msg=f"Readings:  rotary 1 = {self.r1.value()}, rotary 2 = {self.r2.value()}, {*imu.mag()}")
                                                                            
                            print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
                            print('Orientation       x {:5.0f}    y {:5.0f}     z {:5.0f}    w {:5.0f}'.format(*imu.quaternion()))
                            print('Readings:  rotary 1 = {}, rotary 2 = {}'. format(
                            self.r1.value(), self.r2.value()))
  
                            # do something with the encoder results ...
                            self.myevent.clear()

                        except Exception as e:
                            self.establish_connection()
                            print(e)
                        
                async def main():
                    rotary_encoder_1 = RotaryIRQ(pin_num_clk=4,
                                 pin_num_dt=35,
                                 min_val=0,
                                 max_val=20000,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_WRAP)

                    rotary_encoder_2 = RotaryIRQ(pin_num_clk=18,
                                 pin_num_dt=19,
                                 min_val=0,
                                 max_val=20000,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_WRAP)

    # create tasks that use the rotary encoders
    #app1 = Application1(rotary_encoder_1)
                    Readings = Application2(rotary_encoder_1, rotary_encoder_2)

    # keep the event loop active
                    while True:
                        await asyncio.sleep_ms(10)

                try:
                    asyncio.run(main())
                except (KeyboardInterrupt, Exception) as e:
                    print('Exception {} {}\n'.format(type(e).__name__, e))
                finally:
                    ret = asyncio.new_event_loop()  # Clear retained uasyncio state

#             client.publish(topic_pub, msg='Hello from Pico!')
#             print('Readings:  rotary 1 = {}, rotary 2 = {}'. format(self.r1.value(), self.r2.value()))
            
            time.sleep(3)
        except:
            reconnect()
            pass
    client.disconnect()
    



