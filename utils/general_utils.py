'''
Created on 13.08.2012

@author: cristi
'''

def enum(**enums):
    return type('Enum', (), enums)

def getObjectSimplId(simpl_object):
    address = id(simpl_object)
    object_type = str(type(simpl_object))
    for i in range(0,len(object_type)):
        address += ord(object_type[i]) 
    return str(address)
    
