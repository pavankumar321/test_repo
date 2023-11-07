import machine
import time
from bno055_base import BNO055_BASE
import sys
#from rotary_irq_rp2 import RotaryIRQ
from rotary_esp import RotaryIRQ
import uasyncio as asyncio


i2c = machine.I2C(0, scl=machine.Pin(1), sda=machine.Pin(0))
imu = BNO055_BASE(i2c)
calibrated = False

# example of a class that uses two rotary encoders
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
            #if not calibrated:
            time.sleep(1)
            calibrated = imu.calibrated()
            
            print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
            print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
            print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
            print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
            print('Temperature {}°C'.format(imu.temperature()))
            
            await self.myevent.wait()
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


