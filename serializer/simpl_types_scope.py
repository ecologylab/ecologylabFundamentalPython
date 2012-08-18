'''
Created on 04.06.2012

@author: cristi
'''

from deserializer.json_deserializer import *
from serializer.class_descriptor import ClassDescriptor
from serializer.field_descriptor import FieldDescriptor
from utils.format import *
from serializer.xml_serializer import *
from serializer.json_serializer import *
from deserializer.xml_deserializer import *
from serializer import class_descriptor
from utils.user_exceptions import *
from utils.deserializer_utils import *

class SimplTypesScope(object):
    '''
    classdocs
    '''
    def __init__(self, format, serializedScope, inputType = None):
        if inputType == None or inputType == InputType.FILE:
            input_file = open(serializedScope, "r")
            data_string = input_file.read()
        else:
            data_string = serializedScope
        if format == Format.JSON:
            self.initializeFromJSON(data_string)
        if format == Format.XML:
            self.initializeFromXML(data_string)
        self.graphSerialization = False;
        
    def initializeFromJSON(self, serializedScope):
        jsonScope = deserialize_from_string(serializedScope)
        root = jsonScope['simpl_types_scope']
        self.name = root['name']

        self.classDescriptors = {}
        self.simplIdToObject = {}

        for cd in root['class_descriptor']:
            self.parseRoot(cd)
        self.resolveGraphReferences()
        
    def parseRoot(self, cd):
        if 'simpl.id' in cd:
            classDescriptor = ClassDescriptor()
            classDescriptor.name = cd['name']
            classDescriptor.tagName = cd['tag_name']
            classDescriptor.simpl_name = cd['described_class_simple_name']
            classDescriptor.simplePackageName = cd['described_class_package_name']
            if 'super_class' in cd:
                superClass = cd['super_class']
                if 'simpl_id' in cd['super_class']:
                    self.parseRoot()
                    classDescriptor.super_class = self.classDescriptors[superClass['tag_name']]
                else:
                    classDescriptor.super_class = superClass # to be replaced with the tag_name after parsing the whole SerializedScope
            else:
                classDescriptor.super_class = None            
            for fd in cd['field_descriptor']:
                if 'simpl.ref' in fd:
                    classDescriptor.inheritedFieldDescriptors.append(fd['simpl.ref']) 
                    continue
                else:
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
                        self.parseRoot(declaringClass)
                        fieldDescriptor.declaring_class = self.classDescriptors[declaringClass['tag_name']]
                    else:
                        fieldDescriptor.declaring_class = declaringClass # to be replaced with the tag_name after parsing the whole SerializedScope
                    if "map_key_field_name" in fd:
                        fieldDescriptor.map_key = fd["map_key_field_name"]
                        classDescriptor.key_field = fieldDescriptor
                    if 'xml_hint' in fd:
                        fieldDescriptor.xml_hint = fd['xml_hint']
                    
                    self.setFieldDescriptorType(fieldDescriptor, fd)
                    
                    if 'simpl.id' in fd:
                        fieldDescriptor.simpl_id = fd['simpl.id']
                        self.simplIdToObject[fd['simpl.id']] = fieldDescriptor
                    classDescriptor.fieldDescriptors[fieldDescriptor.tagName] = fieldDescriptor
                    
                    #collectionFieldDescriptors describe only nowrap collection members
                    if fieldDescriptor.simpl_type == 'collection':
                        classDescriptor.collectionFieldDescriptors[fieldDescriptor.collection_tag_name] = fieldDescriptor
            self.classDescriptors[classDescriptor.tagName] = classDescriptor;
            self.simplIdToObject[cd['simpl.id']] = classDescriptor


    def resolveGraphReferences(self):
        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key];
            for fd_key in cd.fieldDescriptors:
                fd = cd.fieldDescriptors[fd_key]
                if 'simpl.ref' in fd.declaring_class:
                    fd.declaring_class = self.simplIdToObject[fd.declaring_class['simpl.ref']]
                if hasattr(fd, "super_class"):
                    if 'simpl_ref' in fd.super_class:
                        try:
                            fd.super_class = self.simplIdToObject[fd.super_class['simpl.ref']]
                        except KeyError:
                            raise SimplIDNotFound("class not defined in the SimplTypesScope")
                if hasattr(fd, "polymorph_classes"):
                    index = 0;
                    for polymorph_class in fd.polymorph_classes:
                        if (not type(polymorph_class) is ClassDescriptor) and 'simpl.ref' in polymorph_class:
                            try:
                                fd.polymorph_classes[index] = self.simplIdToObject[polymorph_class['simpl.ref']]
                            except KeyError:
                                raise SimplIDNotFound("class not defined in the SimplTypesScope")
                        index += 1
        
        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key]
            for fd_ref in cd.inheritedFieldDescriptors:
                try:
                    fd = self.simplIdToObject[fd_ref]
                except KeyError:
                    raise SimplIDNotFound("Field Descriptor not defined in the SimplTypesScope")
                cd.fieldDescriptors[fd.tagName] = fd
                if fd.isCollection():
                    cd.collectionFieldDescriptors[fd.collection_tag_name] = fd        
                    
    def setFieldDescriptorType(self, fieldDescriptor, fd):
        if fieldDescriptor.getType() == FieldType.SCALAR:
                fieldDescriptor.scalar_type = fd['scalar_type']
                fieldDescriptor.simpl_type = "scalar"
        if fieldDescriptor.getType() == FieldType.COMPOSITE_ELEMENT:
            fieldDescriptor.simpl_type = "composite"
            fieldDescriptor.composite_tagame = fd['composite_tag_name']
            elementClassDescriptor = fd['element_class_descriptor']
            if 'simpl.id' in elementClassDescriptor:
                self.parseRoot(elementClassDescriptor)
        if fieldDescriptor.isCollection():
            fieldDescriptor.simpl_type = "collection"
            if 'wrapped' in fd:
                fieldDescriptor.wrapped = True
            else:
                fieldDescriptor.wrapped = False
            fieldDescriptor.is_generic = fd['is_generic']
            if fd['collection_or_map_tag_name'] != "":
                fieldDescriptor.collection_tag_name = fd['collection_or_map_tag_name']
            else:
                fieldDescriptor.collection_tag_name = fieldDescriptor.tagName
            if 'scalar_type' in fd:
                fieldDescriptor.scalar_type = fd['scalar_type']
            if 'element_class_descriptor' in fd:
                elementClassDescriptor = fd['element_class_descriptor']
                if 'simpl.id' in elementClassDescriptor:
                        self.parseRoot(elementClassDescriptor)
            if 'polymorph_class_descriptors' in fd:
                fieldDescriptor.polymorph_classes = []
                for cd in fd['polymorph_class_descriptors']['polymorph_class_descriptor']:
                    if 'simpl.id' in cd:
                        self.parseRoot(cd)
                        fieldDescriptor.polymorph_classes.append(self.classDescriptors[cd['tag_name']])
                    else:
                        fieldDescriptor.polymorph_classes.append(cd)
        return fieldDescriptor
        
    def findClassByFullName(self, name):
        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key];
            if (cd.name == name):
                return cd.tagName
        raise ClassNotDefined("Class " + name + " not defined in the SimplTypesScope")
    
    def findClassByName(self, name):
        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key];
            split_string = cd.name.split(".")
            class_name = split_string[len(split_string) - 1]
            if (class_name == name):
                return cd.tagName
        raise ClassNotDefined("Class " + name + " not defined in the SimplTypesScope")
    
    def getFileDescriptorFromTag(self, tag, rootTag):
        class_descriptor = self.classDescriptors[rootTag]
        if tag in class_descriptor.collectionFieldDescriptors:
            return class_descriptor.collectionFieldDescriptors[tag]
        return class_descriptor.fieldDescriptors[tag]

    def initializeFromXML(self, serializedScope):
        pass

    def serialize(self, obj, serialization_format):
        if serialization_format == Format.XML:
            xmlserializer = XmlSimplSerializer(obj, self)
            return xmlserializer.serialize()
        elif serialization_format == Format.JSON:
            serializer = JSONSimplSerializer(obj, self)
            return serializer.serialize()
        else:
            raise UnknownFormat("Unknown format provided, only XML and JSON supported")

    def deserialize(self, input_file, serialization_format):
        if serialization_format == Format.XML:
            xml_deserializer = SimplXmlDeserializer(self, input_file)
            xml_deserializer.parse()
            return xml_deserializer.root
        elif serialization_format == Format.JSON:
            json_des = SimplJsonDeserializer(self,input_file)
            json_des.parse()
            return json_des.root
        else:
            raise UnknownFormat("Unknown format provided, only XML and JSON supported")

    def enableGraphSerialization(self):
        self.graphSerialization = True

    def createDynamicClasses(self):
        for class_descriptor in self.classDescriptors:
            createClass(self.classDescriptors[class_descriptor].simpl_name)
                
    
    def SimplType(self, class_name):
        self.createDynamicClasses()
        new_instance = getClassInstance(class_name)
        new_instance.simpl_tag_name = self.findClassByName(class_name)
        class_descriptor = self.classDescriptors[new_instance.simpl_tag_name]
        for fd_key in class_descriptor.collectionFieldDescriptors:
            fd = class_descriptor.collectionFieldDescriptors[fd_key]
            if fd.getType() == FieldType.MAP_ELEMENT or fd.getType() == FieldType.MAP_SCALAR:
                setattr(new_instance, fd.name, {})
            elif fd.getType() == FieldType.COLLECTION_ELEMENT or fd.getType() == FieldType.COLLECTION_SCALAR:
                setattr(new_instance, fd.name, [])
                
        return new_instance
        
    def printSerialized(self, obj, format):
        element = self.serialize(obj, format)
        if format == Format.XML:
            print(prettify(element))
        elif format == Format.JSON:
            print (json.dumps(element))
        else:
            raise UnknownFormat("Unknown format provided, only XML and JSON supported")
