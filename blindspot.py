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


    def rread(self):
        return self.I2C.read_word_data(self.i2caddr, 2) / 255


    def get_value(self):
        self.rrange()
        time.sleep(0.1)
        return self.rread()


if __name__ == "__main__":
    test_sensor = USensor(0x70)
    print("Address is {}".format(test_sensor.i2caddr))
    print("Sensor value is {}".format(test_sensor.get_value()))
