'''
Created on Jun 8, 2017

@author: albert
'''
import unittest
from tests.test_models import FHUSERTest

class Test(unittest.TestCase):


    def suite(self):
        s = unittest.suite()
        s.addTest(FHUSERTest())
    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()