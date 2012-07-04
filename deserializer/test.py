'''
Created on 17.06.2012

@author: cristi
'''
from serializer.simpl_types_scope import SimplTypesScope
from deserializer.json_deserializer import *
from serializer.json_serializer import JSONSimplSerializer

if False:
    def createClass():
            globals()["Dummy"] = type("Dummy", (object,), {})
        
        
    createClass()
    
    dum = Dummy()
    dum.a = 5
    print(dum.a)
    
    if ('b' in getattr(dum)):
        print("ok")
        
    scope = SimplTypesScope("JSON", "scope_test")
    json_tree = deserialize_from_file("example.json")
    json_des = SimplJsonDeserializer(scope, json_tree)
    json_des.start_deserialize()
    new_instance = json_des.instance
    serializer = JSONSimplSerializer(new_instance, scope)
    serializer.serialize()
    print(serializer.toString())
    
x = json.loads("""{"circle":{"radius":"3","center":{"x":"2","y":"1"}}}""")

y = json.loads("""{"circle":{"center":{"x":"2","y":"1"}, "radius":"3"}}""")
print (x==y)
