'''
Created on 09.06.2012

@author: cristi
'''
import json
#from serializer.simpl_types_scope import SimplTypesScope
from deserializer.deserializer_utils import *

def deserialize_from_string(data_string):
    deserialized_obj = json.loads(data_string)
    return deserialized_obj
    
def deserialize_from_file(filename):
    json_file = open(filename, "r")
    data_string = json_file.read()
    scope = deserialize_from_string(data_string)
    return scope

class SimplJsonDeserializer:
    def __init__(self, scope, json_tree):
        self.scope = scope
        self.json_tree = json_tree
        self.instance = None
        
    def start_deserialize(self):
        name = list(self.json_tree.keys())[0]
        attrs = self.json_tree[name]
        self.instance = self.deserialize(name, attrs)
        
    def deserialize(self, name, attrs):
        class_descriptor = self.scope.classDescriptors[name]
        class_name = class_descriptor.simpl_name
        self.simpl_class = createClass(class_name)
        new_instance = getClassInstance(class_name)
        setattr(new_instance, "simpl_tag_name", class_descriptor.tagName)      
        if len(attrs) > 0:
            for key, value in attrs.items():
                fd = class_descriptor.fieldDescriptors[key];
                if (fd.simpl_type == "scalar"):
                    print("just set attr " + fd.name + ", with the value " + value)
                    setattr(new_instance, fd.name, value)
                else:
                    child_tag_name = self.scope.findClassBySimplName(fd.field_type)
                    setattr(new_instance, key, self.deserialize(child_tag_name, value))          
        return new_instance

