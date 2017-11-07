import sys
import time
import blindspot
import led_notification

## Threshold for blindspot detection
DETECT = 20
RIGHT_LED = 20
LEFT_LED = 26

left_front = blindspot.USensor(0x71)
right_front = blindspot.USensor(0x70)
left_back = blindspot.USensor(0x72)
right_back = blindspot.USensor(0x73)

print("Initializing notification LEDs..")
leftLed = led_notification.LED(LEFT_LED)
rightLed = led_notification.LED(RIGHT_LED)

def trigger():
    left_front.rrange()
    right_front.rrange()
    left_back.rrange()
    right_back.rrange()


print("Starting detection cycle")
try:
    while True:
        trigger()
        time.sleep(0.2)
        val1 = left_front.rread()
        val2 = right_front.rread()
        val3 = left_back.rread()
        val4 = right_back.rread()

        print("| {:>6.2f} | {:>6.2f} | {:>6.2f} | {:>6.2f} |".format(val1, val2, val3, val4))

        if left_front.get_value() > DETECT and left_back.get_value() < DETECT:
            leftLed.ledOn()
        else:
            leftLed.ledOff()

        if right_front.get_value() > DETECT and right_back.get_value() < DETECT:
            rightLed.ledOn()
        else:
            rightLed.ledOff()

except KeyboardInterrupt:
    led_notification.cleanUp()
