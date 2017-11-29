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

    ALPHA = 0.1 # used for low-pass filter
    deg_sym = u'\u00b0'

    def __init__(self, hires=True, accel_address=LSM303_ADDRESS_ACCEL, i2c=None, scale=2, **kwargs):
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
            self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00001000) # default scale of 2g
            self.scale_factor = 0.001
            if scale == 4:
                self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00011000) # current scaling is 4g
                self.scale_factor = 0.002
            elif scale == 8:
                self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00101000)  # current scaling is 4g
                self.scale_factor = 0.004
            elif scale == 16:
                self._accel.write8(LSM303_REGISTER_ACCEL_CTRL_REG4_A, 0b00111000)  # current scaling is 4g
                self.scale_factor = 0.012
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

    def get_angle(self, accel):
        """ Calculate the tilt angle """
        acc_x, acc_y, acc_z = accel
        angle = math.atan2(acc_x, acc_z) * 180 / math.pi  # to calculate the the roll angle, y
        return angle


    def low_pass_filter(self, input, output=None):
        if not output: return input

        output_filtered = output + self.ALPHA * (input - output)
        return output_filtered


    def getRealAccel(self):
        realAccel = [0.0, 0.0, 0.0]
        accel = self.read()
        for i in range(3):
            realAccel[i] = round(accel[i] * self.scale_factor, 3)
        return realAccel


class MovingAverage():
    def __init__(self, period):
        """
        construct, set the period
        """
        assert period == int(period) and period > 0, "Period must be an integer >0"
        self.period = period
        self.stream = deque()    # store the data here
        self.stream.clear()

    # ---------------------------------------------
    def nextVal(self, n):
        """
        add a value to moving average and return a smoothed value
        filling the stream still leaves some issues -- but looks
        like the right way to me
        may be issues on where float() is used
        """
        stream = self.stream

        stream.append(n)    # appends on the right

        streamlength = len(stream)
        if streamlength > self.period:
            stream.popleft()
            streamlength -= 1
        if streamlength == 0:
            self.value    =  0
        else:
            self.value    = sum( stream ) / float( streamlength )

        return self.value


if __name__ == "__main__":
    lsm303 = LSM303(scale=16)
    while True:
        accel = lsm303.getRealAccel()
        acc_x, acc_y, acc_z = accel
        angle = lsm303.get_angle(accel)
        angle_filtered = None
        if angle_filtered == None:
            angle_filtered = lsm303.low_pass_filter(angle)
        else:
            angle_filtered = lsm303.low_pass_filter(angle, angle_filtered)
        now = dt.now().isoformat()
        print('{}: X= {:>6.3f}G,  Y= {:>6.3f}G,  Z= {:>6.3f}G'.format(now, acc_x, acc_y, acc_z))
        print("Tilt angle: {:>6.6f}{}".format(angle, lsm303.deg_sym))
        time.sleep(0.2)
