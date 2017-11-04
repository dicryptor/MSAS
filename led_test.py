import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)

GPIO.output(26, GPIO.HIGH)
GPIO.output(20, GPIO.HIGH)
time.sleep(2)
GPIO.output(26, GPIO.LOW)
GPIO.output(20, GPIO.LOW)

GPIO.cleanup()

