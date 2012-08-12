
'''
Created on 08.07.2012

@author: cristi
'''
'''
Created on 07.07.2012

@author: cristi
'''
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

class collectionWrapScalar(unittest.TestCase):
    '''
    classdocs
    '''

    def setUp(self):
        self.scope = SimplTypesScope("JSON", "collectionWrapScalar_scope")
        fileReader = open("collectionOfCircles.xml", "r")
        self.pointXMLResult = fileReader.read()
        fileReader.close()
                
    def test_xml_run(self):
        simpl_object = self.scope.deserialize("collectionWrapScalar.xml", "XML")
        xmlelement = self.scope.serialize(simpl_object, "XML")
        print(prettify(xmlelement))
        
        expected_result = self.pointXMLResult
        print(expected_result)
        
        self.assertTrue(testing_utils.xml_compare(xmlelement, ElementTree.fromstring(expected_result)))
if False:
    def test_json_run(self):
        simpl_object = self.scope.deserialize("collectionWrapScalar.json", "JSON")
        json_text = deserialize_from_file("collectionWrapScalar.json")
        print(json_text)
        json_element = self.scope.serialize(simpl_object, "JSON")
        print (json.dumps(json_element))
        self.assertTrue(json_text, json.dumps(json_element))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()