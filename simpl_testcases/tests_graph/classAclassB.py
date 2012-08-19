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
from utils.format import Format
import json

class Circle(unittest.TestCase):
    '''
    classdocs
    '''

    def setUp(self):
        self.scope = SimplTypesScope(Format.JSON, "classAclassB_scope")
        self.scope.enableGraphSerialization()
        fileReader = open("classAclassB.xml", "r")
        self.pointXMLResult = fileReader.read()
        fileReader.close()
                
    def test_xml_run(self):
        simpl_object = self.scope.deserialize("classAclassB.xml", Format.XML)
        xmlelement = self.scope.serialize(simpl_object, Format.XML)
        print(prettify(xmlelement))
        
        expected_result = self.pointXMLResult
        print(expected_result)
        
        self.assertTrue(xmlelement, ElementTree.fromstring(expected_result))
        
    def test_json_run(self):
        simpl_object = self.scope.deserialize("classAclassB.json", Format.JSON)
        json_text = deserialize_from_file("classAclassB.json")
        print(json_text)
        json_element = self.scope.serialize(simpl_object, Format.JSON)
        
        print (json.dumps(json_element))
        self.assertTrue(json_text, json.dumps(json_element))
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()