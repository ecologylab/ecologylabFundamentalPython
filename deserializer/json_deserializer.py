'''
Created on 09.06.2012

@author: cristi
'''
import json
#from serializer.simpl_types_scope import SimplTypesScope
from deserializer.deserializer_utils import *
from deserializer.pull_deserializer import PullDeserializer
from ijson import items, parse

from deserializer.field_type import FieldType

def deserialize_from_string(data_string):
    deserialized_obj = json.loads(data_string)
    return deserialized_obj

def deserialize_from_file(filename):
    json_file = open(filename, "r")
    data_string = json_file.read()
    scope = deserialize_from_string(data_string)
    json_file.close()
    return scope

def deserialize_events_from_file(filename):
    json_file = open(filename, "r")
    return iter(parse(json_file))

class SimplJsonDeserializer(PullDeserializer):
    def __init__(self, scope, input_file, deserializationHookStrategy = None):
        super(SimplJsonDeserializer, self).__init__(scope, input_file)
        self.scope = scope
        self.root = None
        self.current_collection = None
        self.current_collection_fd = None
        self.prefix = None
        self.event = None
        self.value = None
        self.current_field_descriptor = None
        self.deserializedSimplIds = {}
        self.deserializationHookStrategy = deserializationHookStrategy
        try:
            self.pull_events = deserialize_events_from_file(input_file)
        except IOError as e:
            print ("Cannot read from file: " + e.strerror)

    def nextEvent(self):
        self.prefix, self.event, self.value = self.pull_events.next()
    
    def nextElement(self):
        tag = self.getTagName()
        while (self.isNewElement()) and (tag == self.getTagName()):
            self.nextEvent()
            
        
    
    def parse(self):
        self.nextEvent()
        if self.isStartDocument():
            self.nextEvent()
        self.rootTag = self.value 
        self.root = self.getObjectModel(self.rootTag, self.rootTag)
    
    def getObjectModel(self, name, rootName):
        class_descriptor = self.scope.classDescriptors[name]
        class_name = class_descriptor.simpl_name
        self.simpl_class = createClass(class_name)
        root = getClassInstance(class_name)
        setattr(root, "simpl_tag_name", class_descriptor.tagName)
        self.nextEvent()
        self.xmlText = ""

        self.currentFileDescriptor = None

        while (not self.isEndDocument()) and \
                (not self.isEndMap() or (not rootName == self.getTagName())):
            if (not self.isNewElement()):
                if self.isEndMap():
                    name = self.current_collection
                self.nextEvent()
                continue
            
            if self.isStartMap():
                self.nextEvent()
            tag = self.value
            self.nextEvent()
            if self.isGraphTag(tag):
                if tag == "simpl.id":
                    self.deserializedSimplIds[self.value] = root
                    self.nextEvent()
                else:
                    return self.deserializedSimplIds[self.value]
            else:
                self.current_field_descriptor = self.scope.getFileDescriptorFromTag(tag, name)
                if self.current_field_descriptor.getType() == FieldType.SCALAR:
                    self.deserializeScalar(root, self.current_field_descriptor)
                elif self.current_field_descriptor.getType() == FieldType.COMPOSITE_ELEMENT:
                    self.deserializeComposite(root, self.current_field_descriptor)
                elif self.current_field_descriptor.getType() == FieldType.COLLECTION_ELEMENT:
                    self.deserializeCompositeCollection(root, self.current_field_descriptor)
                elif self.current_field_descriptor.getType() == FieldType.COLLECTION_SCALAR:
                    self.deserializeScalarCollection(root, self.current_field_descriptor)
                elif self.current_field_descriptor.getType() == FieldType.MAP_ELEMENT:
                    self.deserializeCompositeMap(root, self.current_field_descriptor)
                elif self.current_field_descriptor.getType() == FieldType.MAP_SCALAR:
                    self.deserializeScalarMap(root, self.current_field_descriptor)
                    
                else:
                    self.nextEvent()
        return root

    def isGraphTag(self, tag):
        return tag == "simpl.id" or tag == "simpl.ref"
    
    def deserializeScalar(self, parent, fd):
        setattr(parent, fd.name, fd.getValue(self.value))
        self.nextEvent()

    def deserializeComposite(self, parent, field_descriptor):
        tag = self.getTagName()
        class_name = self.scope.findClassByFullName(field_descriptor.element_class)
        subRoot = self.getObjectModel(class_name, tag)
        setattr(parent, tag, subRoot)
        self.nextEvent()
    
    def deserializeCompositeMap(self, parent, fd):
        if hasattr(parent, fd.name):
            current_dict = getattr(parent, fd.name)
        else:
            current_dict = {}
        self.current_collection = fd.name
        self.current_collection_fd = fd
        
        if fd.wrapped:
            self.skipWrappedStartTag() 
        if self.isStartArray():
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if not self.isNewElement():
                    break
                else:
                    self.skipPolymorphicWrapper()
                    tagName = self.getTagName()
                    if fd.isPolymorphicField(tagName, self.current_collection_fd):
                        child_tag_name = tagName
                    else:
                        child_tag_name = self.scope.findClassByFullName(fd.element_class)
                    subRoot = self.getObjectModel(child_tag_name, tagName)
                    key_fd = self.scope.classDescriptors[subRoot.simpl_tag_name].key_field
                    current_dict[getattr(subRoot, key_fd.map_key)] = subRoot
                    setattr(parent, fd.name, current_dict)
                    if self.current_collection_fd.isPolymorphicCollection():
                        self.nextEvent()
                    self.nextEvent()
                    tagName = self.getTagName()
        if fd.wrapped:
            self.skipWrappedEndTag()
    
    def deserializeScalarMap(self, parent, fd):
        if hasattr(parent, fd.name):
            current_dict = getattr(parent, fd.name)
        else:
            current_dict = {}
        self.current_collection = fd.name
        self.current_collection_fd = fd
        
        if fd.wrapped:
            self.skipWrappedStartTag()
        if self.isStartArray():
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if not self.isNewElement():
                    break
                else:
                    value = fd.getValue(self.value)
                    # this is an implementation based on the key being equal to the value
                    current_dict[value] = value
                    setattr(parent, fd.name, current_dict)    
                    self.nextEvent()
                    tagName = self.getTagName() 
                    
        if fd.wrapped:
            self.skipWrappedEndTag()
            
    def deserializeScalarCollection(self, parent, fd):
        if hasattr(parent, fd.name):
            current_list = getattr(parent, fd.name)
        else:
            current_list = []
        self.current_collection = fd.name
        self.current_collection_fd = fd
        
        if fd.wrapped:
            self.skipWrappedStartTag()
        if self.isStartArray():
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if self.isEndArray():
                    self.nextEvent()
                    break
                else:
                    current_list.append(fd.getValue(self.value))
                    setattr(parent, fd.name, current_list)    
                    self.nextEvent()
                    tagName = self.getTagName()
        if fd.wrapped:
            self.skipWrappedEndTag()
            
    def deserializeCompositeCollection(self, parent, fd):
        if hasattr(parent, fd.name):
            current_list = getattr(parent, fd.name)
        else:
            current_list = []
        self.current_collection = fd.name
        self.current_collection_fd = fd

        if fd.wrapped:
            self.skipWrappedStartTag()
        if self.isStartArray():
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if not self.isNewElement():
                    break
                else:
                    self.skipPolymorphicWrapper()
                    tagName = self.getTagName()
                    if fd.isPolymorphicField(tagName, self.current_collection_fd):
                        child_tag_name = tagName
                    else:
                        child_tag_name = self.scope.findClassByFullName(fd.element_class)
                    subRoot = self.getObjectModel(child_tag_name, tagName)
                    current_list.append(subRoot)
                    setattr(parent, fd.name, current_list)
                    if self.current_collection_fd.isPolymorphicCollection():
                        self.nextEvent()
                    self.nextEvent()
                    tagName = self.getTagName()
        if self.isEndArray():
            self.nextEvent()
        if fd.wrapped:
            self.skipWrappedEndTag()
        
    def isStartDocument(self):
        return (self.prefix == "" and self.event == "start_map" and self.value == None)
    
    def isEndDocument(self):
        return (self.prefix == "" and self.event == "end_map" and self.value == None)
        
    def isStartMap(self):
        return self.event == "start_map"
    
    def isStartElement(self):
        return self.event == "map_key" 
    
    def isNewElement(self):
        return self.isStartMap() or self.isStartElement()
    
    def isEndMap(self):
        return self.event == "end_map"

    def isStartArray(self):
        return self.event == "start_array"
    
    def isEndArray(self):
        return self.event == "end_array"
    
    def getTagName(self):
        if (self.prefix == None):
            return None
        else:
            split_string = self.prefix.split(".")
            tag = split_string[len(split_string) - 1]
            if tag != "item":
                return tag
            else:
                return split_string[len(split_string) - 2]
    
    def ignoreTag(self, tag):
        while (not self.isEndMap()) or (not self.getTagName() == tag):
            self.nextEvent()
        self.nextEvent()
        
    def skipPolymorphicWrapper(self):
        if self.current_collection_fd.isPolymorphicCollection():
            self.nextEvent()
            while self.event != "start_map":
                self.nextEvent()
        
    def skipWrappedStartTag(self):
        while self.event != "start_array":
            self.nextEvent()
            
    def skipWrappedEndTag(self):
        while self.event != "map_key":
            self.nextEvent()
            if self.isEndDocument():
                break