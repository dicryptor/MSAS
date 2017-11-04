import time
import Adafruit_ADS1x15
import RPi.GPIO

class USensor:
    '''
    class to create blindsport sensor object
    '''
    GAIN = 2
    ADC = Adafruit_ADS1x15.ADS1015()

    def __init__(self, channel):
        self.channel = channel

    def get_value(self):
        value = self.ADC.read_adc(self.channel, gain=self.GAIN)
        return value



if __name__ == "__main__":
    left_front = USensor(0)
    right_front = USensor(1)

    for i in range(5):
        print(left_front.get_value())
        print(right_front.get_value())
        time.sleep(0.5)
