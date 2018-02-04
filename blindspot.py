"""
..module:: project_documentation
         : Raspbian Linux
         : Module to communicate with ultrasonic sensor
"""

import time
import smbus2 as smbus


class USensor:
    """
    Class to create blindsport sensor object, communication will use SMBUS2 module
    Provides methods to trigger ultrasonic sensor and obtain the reading of that trigger after the required
    time to wait.
    """
    I2C = smbus.SMBus(1)

    def __init__(self, i2caddr):
        """Constructor. Will take in I2C device address as an argument"""
        self.i2caddr = i2caddr

    def rrange(self):
        """Ultrasonic trigger method, which will send pulses to get the distance of object"""
        self.I2C.write_byte_data(self.i2caddr, 0, 81)

    ## For testing
    def rrange_norange(self):
        """Testing method, to trigger and read without ranging feature"""
        self.I2C.write_byte_data(self.i2caddr, 0, 92)

    def rread(self):
        """Method to read the values after calling the trigger method. Need to re-call trigger method again before
        reading this value, else there will be no update"""
        return self.I2C.read_word_data(self.i2caddr, 2) / 255

    def get_value(self):
        """Testing method which combines the trigger and read method with the required time wait. Simplifies testing of
        individual sensors"""
        self.rrange()
        time.sleep(0.7)
        return self.rread()


if __name__ == "__main__":
    test_sensor = USensor(0x71)
    print("Address is {}".format(test_sensor.i2caddr))
    while True:
        print("Sensor value is {}".format(test_sensor.get_value()))
