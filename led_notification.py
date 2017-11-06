import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

class LED:
    '''
    to manage led notification
    '''

    def __init__(self, PIN):
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.OUT)
        ## init led indication
        GPIO.output(self.PIN, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.PIN, GPIO.LOW)


    def ledOn(self):
        GPIO.output(self.PIN, GPIO.HIGH)


    def ledOff(self):
        GPIO.output(self.PIN, GPIO.LOW)

## must be called before exiting
def cleanUp():
    GPIO.cleanup() 
