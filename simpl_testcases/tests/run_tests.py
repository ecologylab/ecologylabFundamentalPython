'''
Created on 05.06.2012

@author: cristi
'''
import unittest
from simpl_testcases.tests_circle import circle, point

def run_test(ClassType):
    suite = unittest.TestLoader().loadTestsFromTestCase(ClassType)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_test(point.Point)
    run_test(circle.Circle)
    