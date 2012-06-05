'''
Created on 05.06.2012

@author: cristi
'''
import unittest
import tests.circle
from tests.circle import *

def run_test(ClassType):
    suite = unittest.TestLoader().loadTestsFromTestCase(ClassType)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test(Point)
    run_test(Circle)
    