import unittest
import blindspot

class BlindspotTest(unittest.TestCase):
    '''
    unit test for blindspot detection
    '''

    #sensors = []


    def setUp(self):
        self.left_front = blindspot.USensor(0)
        self.right_front = blindspot.USensor(1)
        #self.sensors.append(self.left_front)
        #self.sensors.append(self.right_front)

    def test_leftFront_gt_0(self):
        #self.vals = list(map(lambda x:x.get_value(), self.sensors))
        #print(self.vals)
        self.assertGreater(self.left_front.get_value(), 0, "Sensor reading greater than 0") 

    def test_rightFront_gt_0(self):
        #self.vals = list(map(lambda x:x.get_value(), self.sensors))
        #print(self.vals)
        self.assertGreater(self.right_front.get_value(), 0, "Sensor reading greater than 0") 

    def test_leftFront_lt_1600(self):
        #self.vals = list(map(lambda x:x.get_value(), self.sensors))
        #print(self.vals)
        self.assertLess(self.left_front.get_value(), 1600) 

    def test_rightFront_lt_1600(self):
        #self.vals = list(map(lambda x:x.get_value(), self.sensors))
        #print(self.vals)
        self.assertLess(self.right_front.get_value(), 1600) 


if __name__ == "__main__":
    unittest.main()



