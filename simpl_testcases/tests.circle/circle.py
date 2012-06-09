'''
Created on 05.06.2012

@author: cristi
'''

import unittest
import Point

from serialization import SimplTypesScope
from simplTestCases.tests import TestingUtils

class Circle(unittest.TestCase):
    '''
    classdocs
    '''

    def __init__(self, *args):
        if (len(args) == 2):
            self.radius = args[0]
            self.center = args[1]
        if (len(args) == 3):
            self.radius = args[0]
            self.center = Point(args[1], args[2])
            
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @radius.deleter
    def radius(self):
        del self._radius
               
    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = value

    @center.deleter
    def center(self):
        del self._center

    def run(self):
        c = Circle(3, 2, 1)
        scope = SimplTypesScope.get("circleTScope", Point.__class__)
        SimplTypesScope.enableGraphSerialization();
        
        result1 = TestingUtils.getSerialization(c, scope, "XML");
        result2 = TestingUtils.getDeserialization(c, scope, "JSON");
        
        assertTrue(TestingUtils.xml_compare(result11, result22))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()