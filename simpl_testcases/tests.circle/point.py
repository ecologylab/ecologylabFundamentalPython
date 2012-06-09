'''
Created on 04.06.2012

@author: cristi
'''
import unittest
from serialization import SimplTypesScope
from simplTestCases.tests import TestingUtils

class Point(unittest.TestCase):

    def __init__(self, x = None, y = None):
        if (not x is None and not y is None):
            self.x = x;
            self.y = y;
    
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @x.deleter
    def x(self):
        del self._x
    
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._x = value

    @y.deleter
    def y(self):
        del self._y
        
    def run(self):
        p = Point(1, 2)
        scope = SimplTypesScope.get("pointTScope", Point.__class__)
        
        result1 = TestingUtils.getSerialization(p, scope, "XML");
        result2 = TestingUtils.getDeserialization(p, scope, "JSON");
        
        assertTrue(TestingUtils.xml_compare(result11, result22))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()