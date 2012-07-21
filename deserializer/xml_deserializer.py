'''
Created on 16.06.2012

@author: cristi
'''
from xml.sax import ContentHandler, make_parser
from serializer.xml_serializer import prettify, XmlSimplSerializer
from deserializer.deserializer_utils import *
from deserializer.pull_deserializer import PullDeserializer

from xml.dom import pulldom
from deserializer.field_type import FieldType


def get_parser_from_file(filename):
    xml_file = open(filename, "r")
    return pulldom.parse(xml_file)

class SimplXmlDeserializer(PullDeserializer):
    def __init__(self, scope, input_file, deserializationHookStrategy = None):
        super().__init__(scope, input_file)
        self.scope = scope
        self.root = None
        self.stack = []
        self.is_collection_member = None
        self.is_composite = None
        self.current_collection = None
        self.is_xml_leaf = None
        self.current_event = None
        self.current_node = None
        self.current_field_descriptor = None
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
        self.deserializeAttributes(root, attrs, class_descriptor)
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
                self.deserializeCompositeCollection(self, self.current_field_descriptor)
            elif self.current_field_descriptor.getType() == FieldType.COLLECTION_SCALAR:
                self.deserializeScalarCollection(self, self.current_field_descriptor)
            else:
                self.nextEvent()
        return root


    def deserializeAttributes(self, root, attrs, class_descriptor):
        if len(attrs) > 0:
            for key, value in attrs.items():
                if key == "xmlns:simpl":
                    continue
                fd = class_descriptor.fieldDescriptors[key];
                if fd.isScalarTag():
                    print("just set attr " + fd.name + ", with the value " + value)
                    setattr(root, fd.name, fd.getValue(value))


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
        setattr(parent, tag, subRoot)
        self.nextEvent()

    def deserializeScalarCollection(self, parent, fd):
        if hasattr(parent, fd.name):
            current_list = getattr(parent, fd.name)
        else:
            current_list = []
        self.current_collection = fd.name
        #self.nextEvent()
        if fd.wrapped:
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName):
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

        return self.current_event
    
    
    def deserializeCompositeCollection(self, parent, fd):
        #fd = class_descriptor.collectionFieldDescriptors[node_name]
        if hasattr(parent, fd.name):
            current_list = getattr(parent, fd.name)
        else:
            current_list = []
        self.current_collection = fd.name
        #self.nextEvent()
        if fd.wrapped:
            self.nextEvent()
        tagName = self.getTagName()
        if not fd.isCollectionTag(tagName):
            self.ignoreTag(tagName)
        else:
            while fd.isCollectionTag(tagName):
                if self.current_event != pulldom.START_ELEMENT:
                    break
                else:
                    child_tag_name = self.scope.findClassByFullName(fd.element_class)
                    subRoot = self.getObjectModel(child_tag_name, tagName)
                    current_list.append(subRoot)
                    setattr(parent, fd.name, current_list)
    
                    self.nextEvent()
                    tagName = self.getTagName()

        self.nextEvent()

    def deserializeCompositeMap(self, parent, field_descriptor):
        pass

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
