'''
Created on 15.06.2012

@author: cristi
'''
from codegenerator.generator_backend import GeneratorUtils

def generateClasses(scope):
    for classDescriptor in scope.classDescriptors:
        str= generateClass(classDescriptor)
        
def generateClass(cd):
    gb = GeneratorUtils()
    gb.begin()
    gb.write("class " + cd.simpleName + "():")
    gb.increaseIndent()
    for fd in cd.fieldDescriptors():
        appendFieldDescriptor(gb)
    