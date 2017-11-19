# The MIT License (MIT)
#
# Copyright (c) 2016 Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import struct, time, math
from datetime import datetime as dt

# Minimal constants carried over from Arduino library:
LSM303_ADDRESS_ACCEL = (0x32 >> 1)  # 0011001x
LSM303_ADDRESS_MAG   = (0x3C >> 1)  # 0011110x
# Default    Type
LSM303_REGISTER_ACCEL_CTRL_REG1_A = 0x20  # 00000111   rw
LSM303_REGISTER_ACCEL_CTRL_REG4_A = 0x23  # 00000000   rw
LSM303_REGISTER_ACCEL_OUT_X_L_A = 0x28
LSM303_REGISTER_MAG_CRB_REG_M = 0x01
LSM303_REGISTER_MAG_MR_REG_M = 0x02
LSM303_REGISTER_MAG_OUT_X_H_M = 0x03

ACCEL_SCALE = 2


class LSM303(object):
    """LSM303 accelerometer & magnetometer."""

    def __init__(self, hires=True, accel_address=LSM303_ADDRESS_ACCEL, i2c=None, **kwargs):
        """Initialize the LSM303 accelerometer & magnetometer.  The hires
        boolean indicates if high resolution (12-bit) mode vs. low resolution
        (10-bit, faster and lower power) mode should be used.
        """
        # Setup I2C interface for accelerometer and magnetometer.
        if i2c is None:
            import Adafruit_GPIO.I2C as I2C
            i2c = I2C
        self._accel = i2c.get_i2c_device(accel_address, **kwargs)
        # self._mag = i2c.get_i2c_device(mag_address, **kwargs)
        # Enable the accelerometer
        self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG1_A, 0x27)
        # Select hi-res (12-bit) or low-res (10-bit) output mode.
        # Low-res mode uses less power and sustains a higher update rate,
        # output is padded to compatible 12-bit units.
        if hires:
            # self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00111000)
            self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00011000)
        else:
            self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0)
            # Enable the magnetometer
            # self._mag.write8(LSM303_REGISTER_MAG_MR_REG_M, 0x00)

    def read(self):
        """Read the accelerometer and magnetometer value.  A tuple of tuples will
        be returned with:
          ((accel X, accel Y, accel Z), (mag X, mag Y, mag Z))
        """
        # Read the accelerometer as signed 16-bit little endian values.
        accel_raw = self._accel.readList(LSM303_REGISTER_ACCEL_OUT_X_L_A | 0x80, 6)
        accel = struct.unpack('<hhh', accel_raw)
        # Convert to 12-bit values by shifting unused bits.
        accel = [accel[0] >> 4, accel[1] >> 4, accel[2] >> 4]
        # Read the magnetometer.
        # mag_raw = self._mag.readList(LSM303_REGISTER_MAG_OUT_X_H_M, 6)
        # mag = struct.unpack('>hhh', mag_raw)

        for i in range(3):
            if accel[i] > 32767:
                accel[i] = accel[i] - 65536

        return accel

    def getRealAccel(self):
        realAccel = [0.0, 0.0, 0.0]
        accel = self.read()
        for i in range(3):
            realAccel[i] = round(accel[i] * 0.002, 3)
        return realAccel


if __name__ == "__main__":
    lsm303 = LSM303()
    while True:
        accel = lsm303.getRealAccel()
        acc_x, acc_y, acc_z = accel
        now = dt.now().isoformat()
        print('{}: X= {:>6.3f}G,  Y= {:>6.3f}G,  Z= {:>6.3f}G'.format(now, acc_x, acc_y, acc_z))
        time.sleep(0.2)
