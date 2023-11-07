import netman
import time
from umqttsimple import MQTTClient
import machine
import sys
#from rotary_irq_rp2 import RotaryIRQ
from rotary_irq_esp import RotaryIRQ
import uasyncio as asyncio

country = 'IT'
ssid = 'vistan12345'
password = 'welcome1'
wifi_connection = netman.connectWiFi(ssid,password,country)

#mqtt config
mqtt_server = '192.168.172.17'
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
                        client.publish(topic_pub, msg=f"Readings:  rotary 1 = {self.r1.value()}, rotary 2 = {self.r2.value()}")
                                                                             
                        print('Readings:  rotary 1 = {}, rotary 2 = {}'. format(
                        self.r1.value(), self.r2.value()))
            # do something with the encoder results ...
                        self.myevent.clear()


                async def main():
                    rotary_encoder_1 = RotaryIRQ(pin_num_clk=14,
                                 pin_num_dt=15,
                                 min_val=0,
                                 max_val=200,
                                 reverse=False,
                                 range_mode=RotaryIRQ.RANGE_WRAP)

                    rotary_encoder_2 = RotaryIRQ(pin_num_clk=18,
                                 pin_num_dt=19,
                                 min_val=300,
                                 max_val=500,
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
    
