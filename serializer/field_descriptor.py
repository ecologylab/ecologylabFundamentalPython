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
        if self.type == FieldType.MAP_ELEMENT or \
            self.type == FieldType.MAP_SCALAR or \
            self.type == FieldType.COLLECTION_ELEMENT or \
            self.type == FieldType.COLLECTION_SCALAR:
            return True
        return False
    
    def isNested(self):
        return self.type == FieldType.COMPOSITE_ELEMENT
    
    def getScalarType(self):
        return self.scalar_type