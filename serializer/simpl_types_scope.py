'''
Created on 04.06.2012

@author: cristi
'''

from deserializer.json_deserializer import *
from serializer.class_descriptor import ClassDescriptor
from serializer.field_descriptor import FieldDescriptor
from constants import format
from xml.sax import make_parser, ContentHandler
from serializer.xml_serializer import XmlSimplSerializer
from deserializer.xml_deserializer import SimplHandler
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
                if 'simpl.ref' in fd.declaringClass:
                    fd.declaringClass = self.simplIdToTag[fd.declaringClass['simpl.ref']]
                    
    def parseRoot(self, cd):
        print(cd)
        if 'simpl.id' in cd:
            classDescriptor = ClassDescriptor()
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
                declaringClass = fd['declaring_class_descriptor']
                if 'simpl_id' in declaringClass:
                    fieldDescriptor.declaringClass = declaringClass['tag_name'] #dictionary or simple element?
                    self.parseRoot(declaringClass)
                else:
                    fieldDescriptor.declaringClass = declaringClass # to be replaced with the tag_name after parsing the whole SerializedScope 
                
                if 'scalar_type' in fd:
                    fieldDescriptor.scalar_type = fd['scalar_type']
                    fieldDescriptor.simpl_type = "scalar"
                else: # to see other types, like collections
                    if 'composite_tag_name' in fd:
                        fieldDescriptor.simpl_type = "composite"
                        fieldDescriptor.composite_tagame = fd['composite_tag_name']
                        fieldDescriptor.element_class = fd['element_class']
                        elementClassDescriptor = fd['element_class_descriptor']
                        if 'simpl.id' in elementClassDescriptor:
                            self.parseRoot(elementClassDescriptor)
                fieldDescriptor.libraryNamespaces = fd['library_namespaces']
                if 'xml_hint' in fd:
                    fieldDescriptor.xml_hint = fd['xml_hint']
                
                classDescriptor.fieldDescriptors[fieldDescriptor.tagName] = fieldDescriptor
                
            self.classDescriptors[classDescriptor.tagName] = classDescriptor;
            self.simplIdToTag[cd['simpl.id']] = classDescriptor.tagName
               
    def findClassBySimplName(self, simpl_name):
        for cd_key in self.classDescriptors:
            cd = self.classDescriptors[cd_key];
            if (cd.simpl_name == simpl_name):
                return cd.tagName
         
        
    def initializeFromXML(self, serializedScope):
        pass
    
    
    def serialize(self, obj, serialization_format):
        if (serialization_format == "XML"):
            xmlserializer = XmlSimplSerializer(obj, self)
            return xmlserializer.serialize()
        
    def deserialize(self, input_file, serialization_format):
        if (serialization_format == "XML"):
            xmlsax_handler = SimplHandler(self);
            parser = make_parser();
            parser.setContentHandler(xmlsax_handler)
            parser.parse(input_file)
            return xmlsax_handler.instance
        
    @classmethod
    def enableGraphSerialization():
        pass
    
if __name__ == '__main__':
    
    scope = SimplTypesScope("JSON", "sample_typesscope3")
    print(scope.classDescriptors)
    
    print(scope.simplIdToTag)
