import machine
import time
from bno055_base import BNO055_BASE

i2c = machine.I2C(0, scl=machine.Pin(22), sda=machine.Pin(21))
imu = BNO055_BASE(i2c)
calibrated = False
while True:
    time.sleep(1)
    if not calibrated:
        calibrated = imu.calibrated()
        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    #print('Temperature {}°C'.format(imu.temperature()))
    #print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
    #print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
    #print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
    print('Orientation   x {:5.1f}    y {:5.1f}     z {:5.1f}    w {:5.1f}'.format(*imu.quaternion()))