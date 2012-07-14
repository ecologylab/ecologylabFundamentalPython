'''
Created on 14.07.2012

@author: cristi
'''


class PullDeserializer(object):
    def __init__(self, scope, input_file):
        self.scope = scope
        self.input_file = input_file
        
    
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
    
    def nextDeserializationProcedureStare(self, field_type):
        pass