import sys
import time
import blindspot
import RPi.GPIO as GPIO

DETECT = 60
GPIO.setmode(GPIO.BCM)
RIGHT_LED = 20
LEFT_LED = 26
GPIO.setup(RIGHT_LED, GPIO.OUT)
GPIO.setup(LEFT_LED, GPIO.OUT)

left_front = blindspot.USensor(0)
right_front = blindspot.USensor(1)




try:
    while True:
        val1 = left_front.get_value()
        val2 = right_front.get_value()
        print("| {:>6} | {:>6}".format(val1, val2))

        if left_front.get_value() < DETECT:
            GPIO.output(LEFT_LED, GPIO.HIGH)
        else:
            GPIO.output(LEFT_LED, GPIO.LOW)

        if right_front.get_value() < DETECT:
            GPIO.output(RIGHT_LED, GPIO.HIGH)
        else:
            GPIO.output(RIGHT_LED, GPIO.LOW)
        time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
