'''
Created on 05.06.2012

@author: cristi
'''

import unittest
from serializer.simpl_types_scope import SimplTypesScope
from serializer.xml_serializer import prettify
from deserializer.json_deserializer import deserialize_from_file
from simpl_testcases.tests import testing_utils
from xml.etree import ElementTree
import json

class Circle(unittest.TestCase):
    '''
    classdocs
    '''

    def setUp(self):
        self.scope = SimplTypesScope("JSON", "circle_scope")
        fileReader = open("circle.xml", "r")
        self.pointXMLResult = fileReader.read()
        fileReader.close()
                
    def test_xml_run(self):
        simpl_object = self.scope.deserialize("circle.xml", "XML")
        if False:
            xmlelement = self.scope.serialize(simpl_object, "XML")
            print(prettify(xmlelement))
            
            expected_result = self.pointXMLResult
            print(expected_result)
            
            self.assertTrue(testing_utils.xml_compare(xmlelement, ElementTree.fromstring(expected_result)))
        
if False:        
    def test_json_run(self):
        json_text = deserialize_from_file("circle.json")
        print(json_text)

        simpl_object = self.scope.deserialize("circle.JSON", "JSON")
        json_element = self.scope.serialize(simpl_object, "JSON")
        
        print (json.dumps(json_element))
        self.assertTrue(json_text, json.dumps(json_element))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()