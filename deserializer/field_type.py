'''
Created on 15.07.2012

@author: cristi
'''

from deserializer.deserializer_utils import enum

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

FieldType.NAMESPACE_TRIAL_ELEMENT = FieldType.NAME_SPACE_MASK
FieldType.NAME_SPACE_SCALAR = FieldType.NAME_SPACE_MASK + FieldType.SCALAR
FieldType.NAME_SPACE_NESTED_ELEMENT = FieldType.NAME_SPACE_MASK + FieldType.COMPOSITE_ELEMENT