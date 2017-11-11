import sys
import time
import blindspot
import led_notification

## Threshold for blindspot detection
DETECT = 50
RIGHT_LED = 20
LEFT_LED = 26

left_front = blindspot.USensor(0x71)
right_front = blindspot.USensor(0x70)
left_back = blindspot.USensor(0x72)
right_back = blindspot.USensor(0x73)

print("Initializing notification LEDs..")
leftLed = led_notification.LED(LEFT_LED)
rightLed = led_notification.LED(RIGHT_LED)

def trigger_front():
    left_front.rrange()
    right_front.rrange()

def trigger_back():
    left_back.rrange()
    right_back.rrange()

vals = [0,0,0,0]
print("Starting detection cycle")
try:
    while True:
        trigger_front()
        time.sleep(0.07)
        vals[0] = left_front.rread()
        vals[1] = right_front.rread()
        trigger_back()
        time.sleep(0.07)
        vals[2] = left_back.rread()
        vals[3] = right_back.rread()

        print("| {:>6.2f} | {:>6.2f} | {:>6.2f} | {:>6.2f} |".format(*vals))

        if vals[0] > DETECT and vals[2] < DETECT:
            leftLed.ledOn()
        else:
            leftLed.ledOff()

        if vals[1] > DETECT and vals[3] < DETECT:
            rightLed.ledOn()
        else:
            rightLed.ledOff()

except KeyboardInterrupt:
    led_notification.cleanUp()
