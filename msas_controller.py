import sys
import time
import blindspot
import led_notification

## Threshold for blindspot detection
DETECT = 100
RIGHT_LED = 20
LEFT_LED = 26

left_front = blindspot.USensor(0)
right_front = blindspot.USensor(1)
left_back = blindspot.USensor(2)
right_back = blindspot.USensor(3)

print("Initializing notification LEDs..")
leftLed = led_notification.LED(LEFT_LED)
rightLed = led_notification.LED(RIGHT_LED)

print("Starting detection cycle")
try:
    while True:
        val1 = left_front.get_value()
        val2 = right_front.get_value()
        val3 = left_back.get_value()
        val4 = right_back.get_value()
        print("| {:>6} | {:>6} | {:>6} | {:>6} |".format(val1, val2, val3, val4))

        if left_front.get_value() > DETECT and left_back.get_value() < DETECT:
            leftLed.ledOn()
        else:
            leftLed.ledOff()

        if right_front.get_value() > DETECT and right_back.get_value() < DETECT:
            rightLed.ledOn()
        else:
            rightLed.ledOff()
        time.sleep(0.2)

except KeyboardInterrupt:
    led_notification.cleanUp()
