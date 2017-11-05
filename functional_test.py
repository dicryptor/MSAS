import unittest
import blindspot

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


if __name__ == "__main__":
    unittest.main(warnings='ignore')

