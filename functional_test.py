import unittest
import blindspot
import led_notification
import lsm303
import location_info_v2 as gps
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
    LEFT_LED = 21

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
        self.assertEqual(GPIO.input(self.RIGHT_LED), 1)
        time.sleep(1)

    def test_leftLed_on(self):
        self.leftLed.ledOn()
        self.assertEqual(GPIO.input(self.LEFT_LED), 1)
        time.sleep(1)

    def test_rightLed_off(self):
        self.rightLed.ledOff()
        self.assertEqual(GPIO.input(self.RIGHT_LED), 0)
        time.sleep(1)

    def test_leftLed_off(self):
        self.leftLed.ledOff()
        self.assertEqual(GPIO.input(self.LEFT_LED), 0)
        time.sleep(1)


class AccelTest(unittest.TestCase):
    def setUp(self):
        self.lsm303 = lsm303.LSM303()
        self.accel = self.lsm303.getRealAccel()
        self.acc_x, self.acc_y, self.acc_z = self.accel
        self.angle = self.lsm303.get_angle(self.accel)

    def test_get_x_axis(self):
        self.assertTrue(-2000 <= self.acc_x <= 2000)

    def test_get_y_axis(self):
        self.assertTrue(-2000 <= self.acc_y <= 2000)

    def test_get_z_axis(self):
        self.assertTrue(-2000 <= self.acc_y <= 2000)

    def test_get_angle(self):
        self.assertTrue(-180 <= self.acc_y <= 180)

    def test_moving_average(self):
        for i in range(40, 51): # feed 10 values which should average out to 48
            self.angle_filtered = self.lsm303.sma.nextVal(i)

        self.assertEqual(self.angle_filtered, 48)


class GPSTest(unittest.TestCase):
    def setUp(self):
        self.gps3 = gps.GPS3()
        for i in range(10):
            self.lat, self.lon = self.gps3.getlatlon()
            self.speed, self.track = self.gps3.getmovement()
            if self.lat is not None and self.lon is not None:
                break
            time.sleep(1)

    def test_lat(self):
        if self.lat is not None:
            self.assertTrue(-90 <= self.lat <= 90)
        else:
            raise unittest.SkipTest("None value for latitude")

    def test_lon(self):
        if self.lon is not None:
            self.assertTrue(-180 <= self.lon <= 180)
        else:
            raise unittest.SkipTest("None value for longitude")

    def test_speed(self):
        if self.speed is not None:
            self.assertTrue(0 <= self.speed <= 999)
        else:
            raise unittest.SkipTest("None value for speed")

    def test_track(self):
        if self.speed is not None:
            self.assertTrue(-180 <= self.speed <= 180)
        else:
            raise unittest.SkipTest("None value for track")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
