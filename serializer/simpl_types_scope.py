'''
Created on 04.06.2012

@author: cristi
'''

from deserializer.json_deserializer import *
from serializer.class_descriptor import ClassDescriptor
from serializer.field_descriptor import FieldDescriptor
from constants import format
from serializer.xml_serializer import XmlSimplSerializer
from serializer.json_serializer import *
from deserializer.xml_deserializer import *

class SimplTypesScope(object):
    '''
    classdocs
    '''
    def __init__(self, format, serializedScopeFile):
        if format == "JSON":
            self.initializeFromJSON(serializedScopeFile)
        if format == "XML":
            self.initializeFromXML(serializedScopeFile)

    def initializeFromJSON(self, serializedScopeFile):
        jsonScope = deserialize_from_file(serializedScopeFile)
        root = jsonScope['simpl_types_scope']
        self.name = root['name']

        self.classDescriptors = {}
        self.simplIdToTag = {}

        for cd in root['class_descriptor']:
            self.parseRoot(cd)

        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key];
            for fd_key in cd.fieldDescriptors:
                fd = cd.fieldDescriptors[fd_key]
                if 'simpl.ref' in fd.declaring_class:
                    fd.declaring_class = self.simplIdToTag[fd.declaring_class['simpl.ref']]

    def parseRoot(self, cd):
        print(cd)
        if 'simpl.id' in cd:
            classDescriptor = ClassDescriptor()
            classDescriptor.name = cd['name']
            classDescriptor.tagName = cd['tag_name']
            classDescriptor.simpl_name = cd['described_class_simple_name']
            classDescriptor.simplePackageName = cd['described_class_package_name']

            for fd in cd['field_descriptor']:
                fieldDescriptor = FieldDescriptor()
                fieldDescriptor.name = fd['name']
                fieldDescriptor.tagName = fd['tag_name']
                fieldDescriptor.type = fd['type']
                fieldDescriptor.field = fd['field']
                fieldDescriptor.field_type = fd['field_type']
                fieldDescriptor.libraryNamespaces = fd['library_namespaces']
                if 'element_class' in fd:
                    fieldDescriptor.element_class = fd['element_class']
                declaringClass = fd['declaring_class_descriptor']
                if 'simpl_id' in declaringClass:
                    fieldDescriptor.declaring_class = declaringClass['tag_name'] #dictionary or simple element?
                    self.parseRoot(declaringClass)
                else:
                    fieldDescriptor.declaring_class = declaringClass # to be replaced with the tag_name after parsing the whole SerializedScope
                if 'scalar_type' in fd:
                    fieldDescriptor.scalar_type = fd['scalar_type']
                    fieldDescriptor.simpl_type = "scalar"
                if 'composite_tag_name' in fd:
                    fieldDescriptor.simpl_type = "composite"
                    fieldDescriptor.composite_tagame = fd['composite_tag_name']
                    elementClassDescriptor = fd['element_class_descriptor']
                    if 'simpl.id' in elementClassDescriptor:
                        self.parseRoot(elementClassDescriptor)
                if 'collection_type' in fd:
                    fieldDescriptor.simpl_type = "collection"
                    if 'wrapped' in fd:
                        fieldDescriptor.wrapped = True
                    else:
                        fieldDescriptor.wrapped = False
                    fieldDescriptor.is_generic = fd['is_generic']
                    fieldDescriptor.collection_tag_name = fd['collection_or_map_tag_name']
                    if fieldDescriptor.getType() == FieldType.COLLECTION_ELEMENT:
                        elementClassDescriptor = fd['element_class_descriptor']
                        if 'simpl.id' in elementClassDescriptor:
                            self.parseRoot(elementClassDescriptor)

                if 'xml_hint' in fd:
                    fieldDescriptor.xml_hint = fd['xml_hint']

                classDescriptor.fieldDescriptors[fieldDescriptor.tagName] = fieldDescriptor

                #collectionFieldDescriptors describe only nowrap collection members
                if fieldDescriptor.simpl_type == 'collection':
                    classDescriptor.collectionFieldDescriptors[fieldDescriptor.collection_tag_name] = fieldDescriptor
            self.classDescriptors[classDescriptor.tagName] = classDescriptor;
            self.simplIdToTag[cd['simpl.id']] = classDescriptor.tagName


    def findClassByFullName(self, name):
        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key];
            if (cd.name == name):
                return cd.tagName

    def getFileDescriptorFromTag(self, tag, rootTag):
        class_descriptor = self.classDescriptors[rootTag]
        if tag in class_descriptor.collectionFieldDescriptors:
            return class_descriptor.collectionFieldDescriptors[tag]
        return class_descriptor.fieldDescriptors[tag]


    def initializeFromXML(self, serializedScope):
        pass


    def serialize(self, obj, serialization_format):
        if serialization_format == "XML":
            xmlserializer = XmlSimplSerializer(obj, self)
            return xmlserializer.serialize()
        if serialization_format == "JSON":
            serializer = JSONSimplSerializer(obj, self)
            return serializer.serialize()


    def deserialize(self, input_file, serialization_format):
        if serialization_format == "XML":
            xml_tree = deserialize_xml_from_file(input_file)
            xml_deserializer = SimplXmlDeserializer(self, xml_tree)
            xml_deserializer.start_deserialize()
            return xml_deserializer.instance

        if serialization_format == "JSON":
            json_tree = deserialize_from_file(input_file)
            json_des = SimplJsonDeserializer(self, json_tree)
            json_des.start_deserialize()
            return json_des.instance

    @classmethod
    def enableGraphSerialization():
        pass

if __name__ == '__main__':

    scope = SimplTypesScope("JSON", "sample_typesscope")
    print(scope.classDescriptors)

    print(scope.simplIdToTag)
