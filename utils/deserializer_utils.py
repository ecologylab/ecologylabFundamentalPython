'''
Created on 03.07.2012

@author: cristi
'''
def createClass(class_name):
    class_name = str(unicode(class_name))
    if class_name in globals():
        return globals()[class_name]
    newClass = type(class_name, (object,), {})
    globals()[class_name] = newClass
    return newClass

def getClassInstance(class_name):
    return globals()[class_name]()