'''
Created on 09.06.2012

@author: cristi
'''
import json

def deserialize_from_string(data_string):
    deserialized_obj = json.loads(data_string)
    return deserialized_obj
    
def deserialize_from_file(filename):
    json_file = open(filename, "r")
    data_string = json_file.read()
    
    scope = deserialize_from_string(data_string)
    return scope

if __name__ == '__main__':
    
    scope = deserialize_from_file("sample_typesscope2")
    
    print(scope)
