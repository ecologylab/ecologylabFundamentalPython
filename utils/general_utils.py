'''
Created on 13.08.2012

@author: cristi
'''

def enum(**enums):
    return type('Enum', (), enums)