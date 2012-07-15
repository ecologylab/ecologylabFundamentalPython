'''
Created on 15.07.2012

@author: cristi
'''
from deserializer.deserializer_utils import enum

DeserializationState = enum(INIT=1, 
                              ATTRIBUTES=2, 
                              ATTRIBUTES_DONE=3,
                              ELEMENTS = 4,
                              ELEMENTS_DONE = 5)