'''
Created on 17.06.2012

@author: cristi
'''
def createClass(className):
    newClass = type(className, (object,), {})
    globals()[className] = newClass
    return newClass

def getClassInstance(className):
    return globals()[className]()