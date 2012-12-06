'''
Created on 14.07.2012

@author: cristi
'''
from deserializer import field_type, deserialization_procedure_state

from deserializer.field_type import FieldType
from deserializer.deserialization_procedure_state import DeserializationState

class PullDeserializer(object):
    def __init__(self, scope):#, instream):  #this should be doing something, but I don't know what yet
        self.scope = scope
#        self.input_file = input_file
 
    @staticmethod
    def get_parser(readable):
        pass       
    
    def parse(self):
        pass
    
    def deserializationPreHook(self, obj):
        if (hasattr(obj, "deserializationPreHook")):
            obj.deserializationPreHook(self.scope)
            
    def deserializationInHook(self, obj):
        if (hasattr(obj, "deserializationPreHook")):
            obj.deserializationPreHook(self.scope)
            
    def deserializationPostHook(self, obj):
        if (hasattr(obj, "deserializationPreHook")):
            obj.deserializationPreHook(self.scope)

    def getDeserializer(self):
        pass
    
    def nextDeserializationProcedureStare(self, state, field_type):
        if field_type == FieldType.SCALAR:
            if state == DeserializationState.INIT:
                return DeserializationState.ATTRIBUTES
        if state == DeserializationState.INIT or state == DeserializationState.ATTRIBUTES:
            return DeserializationState.ATTRIBUTES_DONE
        