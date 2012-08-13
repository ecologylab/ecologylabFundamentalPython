'''
Created on 04.06.2012

@author: cristi
'''
import unittest
from serializer.simpl_types_scope import SimplTypesScope
from serializer.xml_serializer import prettify, XmlSimplSerializer
from simpl_testcases.tests import testing_utils
from deserializer.json_deserializer import deserialize_from_file
from simpl_testcases.tests import testing_utils
from xml.etree import ElementTree
from xml.etree.ElementTree import tostring
from utils.format import Format
import json

class Point(unittest.TestCase):

    def setUp(self):
        self.scope = SimplTypesScope(Format.JSON, "personDirectory_scope")
        self.pointXMLResult = open("personDirectory.xml", "r").read()
        
    def test_xml_run(self):
        simpl_object = self.scope.deserialize("personDirectory.xml", Format.XML)
        if False:
            xmlelement = self.scope.serialize(simpl_object, Format.XML)
            print(prettify(xmlelement))
            
            expected_result = self.pointXMLResult
            print(expected_result)
            
            self.assertTrue(testing_utils.xml_compare(xmlelement, ElementTree.fromstring(expected_result)))

    def test_json_run(self):
        simpl_object = self.scope.deserialize("personDirectory.json", Format.JSON)
        if False:    
            json_text = deserialize_from_file("personDirectory.json")
            print(json_text)
            json_element = self.scope.serialize(simpl_object, Format.JSON)
            
            print (json.dumps(json_element))
            self.assertTrue(json_text, json.dumps(json_element))
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()