import unittest
import blindspot
import led_notification
import RPi.GPIO as GPIO
import time


class BlindspotTest(unittest.TestCase):
    '''
    unit test for blindspot detection
    '''

    def setUp(self):
        self.leftFront = blindspot.USensor(0)
        self.rightFront = blindspot.USensor(1)
        self.leftBack = blindspot.USensor(2)
        self.rightBack = blindspot.USensor(3)

    ### Check for sensor reading, GT 10(noise readings) and LT 1600(max value at current gain)
    def test_leftFront_gt_10(self):
        self.assertGreater(self.leftFront.get_value(), 10, "Sensor reading greater than 0") 

    def test_rightFront_gt_10(self):
        self.assertGreater(self.rightFront.get_value(), 10, "Sensor reading greater than 0") 

    def test_leftBack_gt_10(self):
        val = self.leftBack.get_value()
        self.assertGreater(val, 10, "Left back sensor: {}".format(val)) 

    def test_rightBack_gt_10(self):
        val = self.rightBack.get_value()
        self.assertGreater(val, 10, "Right back sensor: {}".format(val)) 

    def test_leftFront_lt_1600(self):
        self.assertLess(self.leftFront.get_value(), 1600) 

    def test_rightFront_lt_1600(self):
        self.assertLess(self.rightFront.get_value(), 1600) 

    def test_leftBack_lt_1600(self):
        self.assertLess(self.leftBack.get_value(), 1600) 

    def test_rightBack_lt_1600(self):
        self.assertLess(self.rightBack.get_value(), 1600) 

class LedTest(unittest.TestCase):
    '''
    test suite for LED notification
    '''
    # two pins used for notification, left=26 and right=20
    RIGHT_LED = 20
    LEFT_LED = 26

    def setUp(self):
        GPIO.setmode(GPIO.BCM)
        ##print("GPIO mode set to BCM")
        self.leftLed = led_notification.LED(self.LEFT_LED)
        ##print("Created left led object")
        self.rightLed = led_notification.LED(self.RIGHT_LED)
        ##print("Created right led object")

    def tearDown(self):
        led_notification.cleanUp()

    def test_rightLed_on(self):
        self.rightLed.ledOn()
        self.assertEqual(GPIO.input(20), 1)
        time.sleep(1)

    def test_leftLed_on(self):
        self.leftLed.ledOn()
        self.assertEqual(GPIO.input(26), 1)
        time.sleep(1)

    def test_rightLed_off(self):
        self.rightLed.ledOff()
        self.assertEqual(GPIO.input(20), 0)
        time.sleep(1)

    def test_leftLed_off(self):
        self.leftLed.ledOff()
        self.assertEqual(GPIO.input(26), 0)
        time.sleep(1)


if __name__ == "__main__":
    unittest.main(warnings='ignore')

