import sys
import time
import blindspot
import led_notification

DETECT = 100
##GPIO.setmode(GPIO.BCM)
RIGHT_LED = 20
LEFT_LED = 26
##GPIO.setup([RIGHT_LED,LEFT_LED], GPIO.OUT)

left_front = blindspot.USensor(0)
right_front = blindspot.USensor(1)
leftLed = led_notification.LED(LEFT_LED)
rightLed = led_notification.LED(RIGHT_LED)



try:
    while True:
        val1 = left_front.get_value()
        val2 = right_front.get_value()
        print("| {:>6} | {:>6}".format(val1, val2))

        if left_front.get_value() < DETECT:
            leftLed.ledOn()
        else:
            leftLed.ledOff()

        if right_front.get_value() < DETECT:
            rightLed.ledOn()
        else:
            rightLed.ledOff()
        time.sleep(0.2)

except KeyboardInterrupt:
    led_notification.cleanUp()
