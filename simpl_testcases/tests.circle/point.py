'''
Created on 04.06.2012

@author: cristi
'''
import unittest
from serializer.simpl_types_scope import SimplTypesScope
from simpl_testcases.tests import testing_utils
from deserializer.json_deserializer import deserialize_from_file
from deserializer.xml_deserializer import SimplHandler
from xml.sax import make_parser, ContentHandler

class Point(unittest.TestCase):

    def setUp(self):
        self.scope = SimplTypesScope("JSON", "circle_scope")
        self.pointXMLResult = open("point.xml", "r").read()
        
    def test_run(self):
        parser = make_parser();
        parser.setContentHandler(SimplHandler())
        parser.parse("point.xml")
        #result1 = TestingUtils.getSerialization(p, scope, "XML");
        #result2 = TestingUtils.getDeserialization(p, scope, "JSON");
        
        #assertTrue(TestingUtils.xml_compare(result11, result22))
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()