'''
Created on 03.07.2012

@author: cristi
'''
def createClass(class_name):
    if class_name in globals():
        return globals()[class_name]
    newClass = type(class_name, (object,), {})
    globals()[class_name] = newClass
    return newClass

def getClassInstance(class_name):
    return globals()[class_name]()

def enum(**enums):
    return type('Enum', (), enums)

DeserializationState = enum(INIT=1, 
                              ATTRIBUTES=2, 
                              ATTRIBUTES_DONE=3,
                              ELEMENTS = 4,
                              ELEMENTS_DONE = 5)

FieldType=enum(UNSET_TYPE=-999,
                BAD_FIELD=-99,
                IGNORED_ATTRIBUTE=-1,
                SCALAR=0x12,
                COMPOSITE_ELEMENT=3,
                IGNORED_ELEMENT=-3,
                COLLECTION_ELEMENT=4,
                COLLECTION_SCALAR=5,
                MAP_ELEMENT=6,
                MAP_SCALAR=7,
                WRAPPER=0x0a,
                PSEUDO_FIELD_DESCRIPTOR=0x0d,
                NAMESPACE_IGNORED_ELEMENT=-2,
                XMLNS_ATTRIBUTE=0x0e,
                XMLNS_IGNORED=0x0f,
                NAME_SPACE_MASK=0x10)