'''
Created on 16.06.2012

@author: cristi
'''
from xml.sax import ContentHandler, make_parser
#from serializer.simpl_types_scope import SimplTypesScope
from serializer.xml_serializer import prettify, XmlSimplSerializer
from deserializer.deserializer_utils import *

def createClass(class_name):
    if class_name in globals():
        return globals()[class_name]
    newClass = type(class_name, (object,), {})
    globals()[class_name] = newClass
    return newClass

def getClassInstance(class_name):
    return globals()[class_name]()

class SimplHandler(ContentHandler):
    '''
    SAX handler for deserializing SIMPL object
    '''
    def __init__(self, scope): 
        self.simpl_class = None
        self.instance = None
        self.parent_instance = None
        self.current_instance= None
        self.scope = scope
        self.current_xml_leaf = None
        
    def startElement(self, name, attrs):
        '''
        check every XML new node
        '''
        self.current_xml_leaf = None
        
        if self.instance == None:
            self.setInstance(name, attrs)
            self.instance = self.current_instance
            self.parent_instance = self.current_instance
        else:
            field = self.scope.classDescriptors[self.parent_instance.simpl_tag_name].fieldDescriptors[name]
            field_name = name
            if hasattr(field, "xml_hint"):
                self.current_xml_leaf = field_name
            else:
                simplclass_tagname = self.scope.findClassBySimplName(field.field_type)
                self.setInstance(simplclass_tagname, attrs)
                setattr(self.parent_instance, field_name, self.current_instance)
                self.parent_instance = self.current_instance

        print ('Start of element:', name, attrs.keys())

    def endElement(self, name):
        print('End of element:', name)
    
    def characters(self, content):
        if (self.current_xml_leaf != None):
            setattr(self.parent_instance, self.current_xml_leaf, content)
    
    def setInstance(self,  name, attrs):
        scope = self.scope
        class_descriptor = scope.classDescriptors[name]
        class_name = class_descriptor.simpl_name
        self.simpl_class = createClass(class_name)
        self.current_instance = getClassInstance(class_name)           
        setattr(self.current_instance, "simpl_tag_name", class_descriptor.tagName)
        if len(attrs) > 0:
            for key, value in attrs.items():
                fd = class_descriptor.fieldDescriptors[key];
                if (fd.simpl_type == "scalar"):
                    print("just set attr " + fd.name + ", with the value " + value)
                    setattr(self.current_instance, fd.name, value)
                    
if False:
    scope = SimplTypesScope("JSON", "example_scope")
    
    parser = make_parser();
    simplHandler = SimplHandler()
    parser.setContentHandler(simplHandler)
    parser.parse("example.xml")
    
    xmlserializer = XmlSimplSerializer(simplHandler.instance, scope)
    print(prettify(xmlserializer.serialize()))
