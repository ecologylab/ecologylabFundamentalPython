'''
Created on 12.06.2012

@author: cristi
'''
from deserializer.field_type import FieldType

class FieldDescriptor(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    def isScalarTag(self):
        if hasattr(self, "scalar_type"):
            return True
        return False

    def isCollection(self):
        if self.getType() == FieldType.MAP_ELEMENT or \
            self.getType() == FieldType.MAP_SCALAR or \
            self.getType() == FieldType.COLLECTION_ELEMENT or \
            self.getType() == FieldType.COLLECTION_SCALAR:
            return True
        return False

    def isNested(self):
        return self.type == FieldType.COMPOSITE_ELEMENT

    def getScalarType(self):
        return self.scalar_type

    def getType(self):
        return int(self.type)

    def isCollectionTag(self, tagName, current_collection_fd):
        if self.isPolymorphicField(tagName, current_collection_fd):
            return True
        elif hasattr(self, "collection_tag_name"):
            return tagName == self.collection_tag_name
    
    def isPolymorphicField(self, tagName, current_collection_fd):
        if hasattr(current_collection_fd, "polymorph_classes"):
            for cd in current_collection_fd.polymorph_classes:
                if cd.tagName == tagName:
                    return True
            return False
        
    def isPolymorphicCollection(self):
        return hasattr(self, "polymorph_classes")
    
    def isWrappedCollection(self):
        if hasattr(self, "wrapped"):
            return self.wrapped == True
        else:
            return False
    
    def getValue(self, textValue):
        if hasattr(self, "scalar_type"):
            if self.scalar_type == "Integer" or self.scalar_type == "int":
                return int(textValue)
            if self.scalar_type == "Float" or self.scalar_type == "float":
                return float(textValue)
            if self.scalar_type == "String":
                return textValue
            