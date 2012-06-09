'''
Created on 04.06.2012

@author: cristi
'''

class SimplTypesScope(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
    @classmethod
    def get(scope, classType):
        pass
    
    def serialize(self, obj, output, serializationFormat):
        pass
    
    def deserialize(self, input, serializationFormat):
        pass
    
    @classmethod
    def enableGraphSerialization():
        pass