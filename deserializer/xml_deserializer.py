'''
Created on 16.06.2012

@author: cristi
'''
from utils.deserializer_utils import *
from deserializer.pull_deserializer import PullDeserializer

from xml.dom import pulldom
from deserializer.field_type import FieldType


def get_parser_from_file(filename):
    xml_file = open(filename, "r")
    return pulldom.parse(xml_file)

class SimplXmlDeserializer(PullDeserializer):
    '''
    XML Deserializer class for SIMPL objects
    
    uses the xml.dom.pulldom pull deserializer
    To deserialize a S.IM.PL object:
    1. instantiate the class with the simplTypesScope instance and the input XML file as parameters
    2. call parse
    3. the resulted object is returned in the class's root element
    
    Another way to use the deserializer is by calling the deserialize method of the
    simplTypesScope instance, giving the input file as parameter:
    
    exp: scope.deserialize("input.xml", "XML")
    '''
    
    def __init__(self, scope, input_file, deserializationHookStrategy = None):
        super(SimplXmlDeserializer, self).__init__(scope, input_file)
        self.scope = scope
        self.root = None
        self.is_collection_member = None
        self.is_composite = None
        self.current_collection = None
        self.current_collection_fd = None
        self.is_xml_leaf = None
        self.current_event = None
        self.current_node = None
        self.current_field_descriptor = None
        self.deserializedSimplIds = {}
        self.deserializationHookStrategy = deserializationHookStrategy
        try:
            self.pull_events = get_parser_from_file(input_file)
        except IOError as e:
            print ("Cannot read from file: " + e.strerror)

    def nextEvent(self):
        while True:
            self.current_event, self.current_node = self.pull_events.getEvent()
            if self.current_event == pulldom.CHARACTERS:
                nodeText = self.current_node.wholeText
                nodeText = nodeText.replace(' ','')
                nodeText = nodeText.replace('\n', '')
                nodeText = nodeText.replace('\t', '')
                if nodeText == "":
                    continue
            if self.current_event == pulldom.START_DOCUMENT or \
                self.current_event == pulldom.START_ELEMENT or \
                self.current_event == pulldom.END_ELEMENT or \
                self.current_event == pulldom.END_DOCUMENT or \
                self.current_event == pulldom.CHARACTERS:
                break

    def parse(self):
        self.nextEvent()
        if self.current_event == pulldom.START_DOCUMENT:
            self.nextEvent()
        self.rootTag = self.getTagName()
        self.root = self.getObjectModel(self.rootTag, self.rootTag)

    def getObjectModel(self, name, rootName):
        class_descriptor = self.scope.classDescriptors[name]
        class_name = class_descriptor.simpl_name
        self.simpl_class = createClass(class_name)
        root = getClassInstance(class_name)
        setattr(root, "simpl_tag_name", class_descriptor.tagName)
        attrs = self.current_node.attributes
        root = self.deserializeAttributes(root, attrs, class_descriptor)
        self.nextEvent()
        self.xmlText = ""

        self.currentFileDescriptor = None

        while self.current_event != pulldom.END_DOCUMENT and \
                (self.current_event != pulldom.END_ELEMENT or (not rootName == self.getTagName())):
            if self.current_event != pulldom.START_ELEMENT:
                if self.current_event == pulldom.CHARACTERS:
                    self.xmlText += self.current_node.wholeText
                elif self.current_event == pulldom.END_ELEMENT:
                    name = self.current_collection
                self.nextEvent()
                continue

            tag = self.getTagName()

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


    def deserializeAttributes(self, root, attrs, class_descriptor):
        if len(attrs) > 0:
            for key, value in attrs.items():
                if key == "xmlns:simpl":
                    continue
                if key == "simpl:ref":
                    return self.deserializedSimplIds[value]
                elif key == "simpl:id":
                    self.deserializedSimplIds[value] = root
                else:
                    fd = class_descriptor.fieldDescriptors[key];
                    if fd.isScalarTag():
                        setattr(root, fd.name, fd.getValue(value))   
        return root
    
    def deserializeScalar(self, parent, fd):
        value = ""
        while self.current_event != pulldom.END_ELEMENT:
            if self.current_event == pulldom.CHARACTERS:
                value += self.current_node.wholeText
            self.nextEvent()

        setattr(parent, fd.name, fd.getValue(value))
        self.nextEvent()

    def deserializeComposite(self, parent, field_descriptor):
        tag = self.getTagName()
        class_name = self.scope.findClassByFullName(field_descriptor.element_class)
        subRoot = self.getObjectModel(class_name, tag)
        setattr(parent, field_descriptor.name, subRoot)
        self.nextEvent()

    def deserializeCompositeMap(self, parent, fd):
        if hasattr(parent, fd.name):
            current_dict = getattr(parent, fd.name)
        else:
            current_dict = {}
        self.current_collection = fd.name
        self.current_collection_fd = fd
        if fd.wrapped:
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if self.current_event != pulldom.START_ELEMENT:
                    break
                else:
                    if fd.isPolymorphicField(tagName, self.current_collection_fd):
                        child_tag_name = tagName
                    else:
                        child_tag_name = self.scope.findClassByFullName(fd.element_class)
                    subRoot = self.getObjectModel(child_tag_name, tagName)
                    key_fd = self.scope.classDescriptors[subRoot.simpl_tag_name].key_field
                    current_dict[getattr(subRoot, key_fd.map_key)] = subRoot
                    setattr(parent, fd.name, current_dict)
                    self.nextEvent()
                    tagName = self.getTagName()
        if fd.wrapped:
            self.nextEvent()
    
    def deserializeScalarMap(self, parent, fd):
        if hasattr(parent, fd.name):
            current_dict = getattr(parent, fd.name)
        else:
            current_dict = {}
        self.current_collection = fd.name
        self.current_collection_fd = fd
        
        if fd.wrapped:
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if self.current_event != pulldom.START_ELEMENT:
                    break
                else:
                    value = ""
                    while self.current_event != pulldom.END_ELEMENT:
                        if self.current_event == pulldom.CHARACTERS:
                            value += self.current_node.wholeText
                        self.nextEvent()
                    
                    # this is an implementation based on the key being equal to the value
                    current_dict[value] = value
                    setattr(parent, fd.name, current_dict)    
                    self.nextEvent()
                    tagName = self.getTagName() 
        if fd.wrapped:
            self.nextEvent()
                      
    def deserializeScalarCollection(self, parent, fd):
        if hasattr(parent, fd.name):
            current_list = getattr(parent, fd.name)
        else:
            current_list = []
        self.current_collection = fd.name
        self.current_collection_fd = fd
        
        if fd.wrapped:
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if self.current_event != pulldom.START_ELEMENT:
                    break
                else:
                    value = ""
                    while self.current_event != pulldom.END_ELEMENT:
                        if self.current_event == pulldom.CHARACTERS:
                            value += self.current_node.wholeText
                        self.nextEvent()
                    
                    current_list.append(fd.getValue(value))
                    setattr(parent, fd.name, current_list)    
                    self.nextEvent()
                    tagName = self.getTagName()    
            if fd.wrapped:
                self.nextEvent()
            
    def deserializeCompositeCollection(self, parent, fd):
        if hasattr(parent, fd.name):
            current_list = getattr(parent, fd.name)
        else:
            current_list = []
        self.current_collection = fd.name
        self.current_collection_fd = fd
        
        if fd.wrapped:
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName, self.current_collection_fd):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName, self.current_collection_fd):
                if self.current_event != pulldom.START_ELEMENT:
                    break
                else:
                    if fd.isPolymorphicField(tagName, self.current_collection_fd):
                        child_tag_name = tagName
                    else:
                        child_tag_name = self.scope.findClassByFullName(fd.element_class)
                    subRoot = self.getObjectModel(child_tag_name, tagName)
                    current_list.append(subRoot)
                    setattr(parent, fd.name, current_list)
    
                    self.nextEvent()
                    tagName = self.getTagName()
        if fd.wrapped:
            self.nextEvent()

    def getSimplReference(self):
        pass

    def getTagName(self):
        node = self.current_node
        if node.prefix != None and node.prefix != "":
            return node.prefix + ":" + node.localName
        else:
            return node.localName
        
    def ignoreTag(self, tag):
        while self.current_event != pulldom.END_ELEMENT or (not self.getTagName() == tag):
            self.nextEvent()
        self.nextEvent()
