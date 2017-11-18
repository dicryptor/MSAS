import time
import smbus2 as smbus


class USensor:
    '''
    class to create blindsport sensor object
    '''
    I2C = smbus.SMBus(1)

    def __init__(self, i2caddr):
        self.i2caddr = i2caddr

    def rrange(self):
        self.I2C.write_byte_data(self.i2caddr, 0, 81)

    ## For testing
    def rrange_norange(self):
        self.I2C.write_byte_data(self.i2caddr, 0, 92)

    def rread(self):
        return self.I2C.read_word_data(self.i2caddr, 2) / 255

    def get_value(self):
        self.rrange()
        time.sleep(0.7)
        return self.rread()


if __name__ == "__main__":
    test_sensor = USensor(0x71)
    print("Address is {}".format(test_sensor.i2caddr))
    while True:
        print("Sensor value is {}".format(test_sensor.get_value()))
