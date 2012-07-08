'''
Created on 17.06.2012

@author: cristi
'''
from serializer.simpl_types_scope import SimplTypesScope
from serializer.xml_serializer import prettify, XmlSimplSerializer
from deserializer.json_deserializer import *
from serializer.json_serializer import JSONSimplSerializer
from xml.sax import make_parser
from xml.etree import ElementTree
from deserializer.xml_deserializer import SimplXmlDeserializer, deserialize_xml_from_file 

if False:
    def createClass():
            globals()["Dummy"] = type("Dummy", (object,), {})
        
        
    createClass()
    
    dum = Dummy()
    dum.a = 5
    print(dum.a)
    
    if ('b' in getattr(dum)):
        print("ok")
        

    
    x = json.loads("""{"circle":{"radius":"3","center":{"x":"2","y":"1"}}}""")
    
    y = json.loads("""{"circle":{"center":{"x":"2","y":"1"}, "radius":"3"}}""")
    print (x==y)


    class Dummy():
        def __init__(self):
            self.a = []
            
    instance = Dummy()
    setattr(instance, "a", [1,2,3])
    print(instance.a)
    
    scope = SimplTypesScope("JSON", "scope_test")
    json_tree = deserialize_from_file("example.json")
    json_des = SimplJsonDeserializer(scope, json_tree)
    json_des.start_deserialize()
    new_instance = json_des.instance
    
    serializer = JSONSimplSerializer(new_instance, scope)
    serializer.serialize()
    print(serializer.toString())

    scope = SimplTypesScope("JSON", "scope_test")  
    xmlsax_handler = SimplHandler(scope);
    parser = make_parser();
    parser.setContentHandler(xmlsax_handler)
    parser.parse("example.xml")
    
scope = SimplTypesScope("JSON", "scope_test")
xml_tree = deserialize_xml_from_file("example.xml")
xml_deserializer = SimplXmlDeserializer(scope, xml_tree)
xml_deserializer.start_deserialize()
obj = xml_deserializer.instance
xmlserializer = XmlSimplSerializer(obj, scope)
print(prettify(xmlserializer.serialize()))