import unittest
import blindspot
import led_notification
import lsm303
import RPi.GPIO as GPIO
import time


class BlindspotTest(unittest.TestCase):
    '''
    unit test for blindspot detection
    '''
    # minimum and maximum value to test for from US sensor
    MIN = 0
    MAX = 250

    def setUp(self):
        self.leftFront = blindspot.USensor(0x71)
        self.rightFront = blindspot.USensor(0x70)
        self.leftBack = blindspot.USensor(0x72)
        self.rightBack = blindspot.USensor(0x73)

    ### Check for sensor reading, GT 0(noise readings) and LT 250(in CM)
    def test_leftFront_gt_0(self):
        self.assertGreater(self.leftFront.get_value(), self.MIN, "Sensor reading greater than 0")

    def test_rightFront_gt_0(self):
        self.assertGreater(self.rightFront.get_value(), self.MIN, "Sensor reading greater than 0")

    def test_leftBack_gt_0(self):
        self.assertGreater(self.leftFront.get_value(), self.MIN, "Sensor reading greater than 0")

    def test_rightBack_gt_0(self):
        self.assertGreater(self.rightFront.get_value(), self.MIN, "Sensor reading greater than 0")

    def test_leftFront_lt_250(self):
        self.assertLess(self.leftFront.get_value(), self.MAX)

    def test_rightFront_lt_250(self):
        self.assertLess(self.rightFront.get_value(), self.MAX)

    def test_leftBack_lt_250(self):
        self.assertLess(self.leftBack.get_value(), self.MAX)

    def test_rightBack_lt_250(self):
        self.assertLess(self.rightBack.get_value(), self.MAX)


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


class TipOverTest(unittest.TestCase):
    def setUp(self):
        self.lsm303 = lsm303.LSM303()
        self.accel = lsm303.read()
        self.acc_x, self.acc_y, self.acc_z = accel

    def test_get_x_axis(self):
        self.assertTrue(-)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
