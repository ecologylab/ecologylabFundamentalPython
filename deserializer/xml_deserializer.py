'''
Created on 16.06.2012

@author: cristi
'''
from xml.sax import ContentHandler, make_parser
from serializer.xml_serializer import prettify, XmlSimplSerializer
from deserializer.deserializer_utils import *

from xml.etree import ElementTree
from xml.dom import pulldom



def get_parser_from_file(filename):
    xml_file = open(filename, "r")
    return pulldom.parse(xml_file)
    
class SimplXmlDeserializer:
    def __init__(self, scope, pull_events):
        self.scope = scope
        self.pull_events = pull_events
        self.instance = None
        self.stack = []
        self.is_collection_member = None
        self.is_composite = None
        self.current_collection = None
        self.is_xml_leaf = None
        
    def deserialize(self):
        for (event, node) in self.pull_events:
            self.pullEvent(event, node)
        
    def pullEvent(self, event, node):
        if event == pulldom.START_ELEMENT:
            name = node.tagName
            attribs = node.attributes
            self.stack.append(self.newInstance(name, attribs))
            if self.instance == None:
                self.instance = self.stack[0] 
        
        if event == pulldom.END_ELEMENT:
            self.stack.pop()
            
        if event == pulldom.CHARACTERS:
            pass
            
    def newInstance(self, name, attrs):
        class_descriptor = self.scope.classDescriptors[name]
        class_name = class_descriptor.simpl_name
        self.simpl_class = createClass(class_name)
        new_instance = getClassInstance(class_name)
        setattr(new_instance, "simpl_tag_name", class_descriptor.tagName) 
        if len(attrs) > 0:
            for key, value in attrs.items():
                fd = class_descriptor.fieldDescriptors[key];
                if fd.simpl_type == "scalar":
                    print("just set attr " + fd.name + ", with the value " + value)
                    setattr(new_instance, fd.name, value)
if False:  
    def deserialize_xml_from_string(string):
        return ElementTree.fromstring(string)
    
    def deserialize_xml_from_file(filename):
        xml_file = open(filename, "r")
        data_string = xml_file.read()
        scope = deserialize_xml_from_string(data_string)
        xml_file.close()
        return scope

    class SimplXmlDeserializer:
        def __init__(self, scope, xml_tree):
            self.scope = scope
            self.xml_tree = xml_tree
            self.instance = None
            
        def start_deserialize(self):
            name = self.xml_tree.tag
            attrs = self.xml_tree.attrib
            child_nodes = list(self.xml_tree)
            self.instance = self.deserialize(name, attrs, child_nodes)
            
        def deserialize(self, name, attrs, child_nodes):
            class_descriptor = self.scope.classDescriptors[name]
            class_name = class_descriptor.simpl_name
            self.simpl_class = createClass(class_name)
            new_instance = getClassInstance(class_name)
            setattr(new_instance, "simpl_tag_name", class_descriptor.tagName)      
            if len(attrs) > 0:
                for key, value in attrs.items():
                    fd = class_descriptor.fieldDescriptors[key];
                    if fd.simpl_type == "scalar":
                        print("just set attr " + fd.name + ", with the value " + value)
                        setattr(new_instance, fd.name, value)
            if len(child_nodes) > 0:
                for node in child_nodes:
                    node_name = node.tag
                    if node_name in class_descriptor.fieldDescriptors:
                        fd = class_descriptor.fieldDescriptors[node_name];
                        if fd.simpl_type == "scalar":
                            value = node.text
                            print("just set attr " + fd.name + ", with the value " + value)
                            setattr(new_instance, fd.name, value)
                        if fd.simpl_type == "composite":
                            child_tag_name = self.scope.findClassByFullName(fd.element_class)
                            setattr(new_instance, fd.name, self.deserialize(child_tag_name, node.attrib, list(node)))
                    
                    #nowrap collections
                    elif node_name in class_descriptor.collectionFieldDescriptors:
                        fd = class_descriptor.collectionFieldDescriptors[node_name]
                        if hasattr(new_instance, fd.name):
                            current_list = getattr(new_instance, fd.name)
                        else:
                            current_list = []
                        child_tag_name = self.scope.findClassByFullName(fd.element_class)    
                        current_list.append(self.deserialize(child_tag_name, node.attrib, list(node)))
                        setattr(new_instance, fd.name, current_list)
                        if False:
                            child_tag_name = self.scope.findClassByFullName(fd.element_class)
                            members = value[fd.collection_tag_name]
                            for member in members:
                                current_list.append(self.deserialize(child_tag_name, member))
                            setattr(new_instance, fd.name, current_list)
            #if len(child_nodes) > 0:
                
            return new_instance