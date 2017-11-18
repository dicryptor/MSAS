import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)


class LED:
    '''
    to manage led notification
    '''

    def __init__(self, PIN):
        self.PIN = PIN
        GPIO.setup(self.PIN, GPIO.OUT)
        ## init led indication
        self.ledBlink()
        # GPIO.output(self.PIN, GPIO.HIGH)
        # time.sleep(2)
        # GPIO.output(self.PIN, GPIO.LOW)

    def ledOn(self):
        GPIO.output(self.PIN, GPIO.HIGH)

    def ledOff(self):
        GPIO.output(self.PIN, GPIO.LOW)

    def ledBlink(self):
        for i in range(3):
            GPIO.output(self.PIN, GPIO.HIGH)
            time.sleep(0.2)
            GPIO.output(self.PIN, GPIO.LOW)
            time.sleep(0.2)


## must be called before exiting
def cleanUp():
    GPIO.cleanup()


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Define GPIO PIN number to test LED")
        print("Eg. {} 20".format('name'))
    print(sys.argv)
    pinNo = int(sys.argv[1])
    ledTest = LED(pinNo)
    cleanUp()
