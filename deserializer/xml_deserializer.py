'''
Created on 16.06.2012

@author: cristi
'''
from xml.sax import ContentHandler, make_parser
from serializer.xml_serializer import prettify, XmlSimplSerializer
from deserializer.deserializer_utils import *
from deserializer.pull_deserializer import PullDeserializer

from xml.etree import ElementTree
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
        self.root = self.getObjectModel(self.rootTag)

    def getObjectModel(self, name):
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
                (self.current_event != pulldom.END_ELEMENT or (not self.rootTag == self.getTagName())):
            if self.current_event != pulldom.START_ELEMENT:
                if self.current_event == pulldom.CHARACTERS:
                    self.xmlText += self.current_node.wholeText
                elif self.current_event == pulldom.END_ELEMENT:
                    pass #to implement !!!!!!!!!!
                self.nextEvent()
                continue

            tag = self.getTagName()

            self.current_field_descriptor = self.scope.getFileDescriptorFromTag(tag, name)
            if self.current_field_descriptor.getType() == FieldType.SCALAR:
                self.deserializeScalar(root, self.current_field_descriptor)
            elif self.current_field_descriptor.getType() == FieldType.COMPOSITE_ELEMENT:
                self.deserializeComposite(root, self.current_field_descriptor)
            else:
                self.nextEvent()
        return root


    def deserializeAttributes(self, root, attrs, class_descriptor):
        if len(attrs) > 0:
            for key, value in attrs.items():
                fd = class_descriptor.fieldDescriptors[key];
                if fd.isScalarTag():
                    print("just set attr " + fd.name + ", with the value " + value)
                    setattr(root, fd.name, value)


    def deserializeScalar(self, parent, fd):
        value = ""
        while self.current_event != pulldom.END_ELEMENT:
            if self.current_event == pulldom.CHARACTERS:
                value += self.current_node.wholeText
            self.nextEvent()

        setattr(parent, fd.name, value)
        self.nextEvent()

    def deserializeComposite(self, parent, field_descriptor):
        tag = self.getTagName()
        class_name = self.scope.findClassByFullName(field_descriptor.element_class)
        subRoot = self.getObjectModel(class_name)
        setattr(parent, tag, subRoot)
        
    def deserializeCompositeCollection(self, parent, field_descriptor):
        pass

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