'''
Created on Dec 6, 2012

@author: rhema
'''
import unittest
from serializer.simpl_types_scope import SimplTypesScope
from utils.format import Format
import os

scopes_and_instances_location = "test_scopes_and_instances/"
scope_end = "_scope.json"

class TestScopesAndInstances(unittest.TestCase):
    """
        This test class tests xml and json serialization from serialized typescopes 
        and json and xml instances of objects in thoses typescopes.
    """
    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def assert_serialization_works(self,scope_location,json_instance_location,format):
        self.scope = SimplTypesScope(Format.JSON, scope_location)
        simpl_object = self.scope.deserialize_file(json_instance_location, format)
        serialized_original = open(json_instance_location).read()
        serialized_now = self.scope.serialize(simpl_object, format)
        self.assertTrue(serialized_original, serialized_now)

    def test_choice(self):
        for filename in os.listdir (scopes_and_instances_location):
            if scope_end in filename:
                scope_name = filename.split(scope_end)[0]
                print scope_name
                print scopes_and_instances_location
                scope_spot = scopes_and_instances_location+scope_name+scope_end
                print scope_spot
                instance = scopes_and_instances_location+scope_name+".json"
                print instance
                instance_xml = scopes_and_instances_location+scope_name+".xml"
                print instance_xml
                self.assert_serialization_works(scope_spot,instance, Format.JSON)
                self.assert_serialization_works(scope_spot,instance_xml, Format.XML)
                
        print "one"
        thing = True
        self.assertTrue(thing) 

    def test_choice_2(self):
        print "two"
        thing = True
        self.assertTrue(thing)

#def create_test():  ##TBD structure so that we get more granular test results.
#    def do_test_expected(self):
#        self.assertTrue()
#    return do_test_expected

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()