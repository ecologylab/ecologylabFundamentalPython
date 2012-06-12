'''
Created on 05.06.2012

@author: cristi
'''
from serializer import simpl_types_scope

def getSerialization(obj, scope, serializationFormat):
    return scope.serialize(obj, serializationFormat)

def getDeserialization(obj, scope, serializationFormat):
    serializedResult = getSerialization(obj, scope, serializationFormat);
    output = scope.deserialize(serializedResult, serializationFormat)
    return getSerialization(output, scope, "XML")

def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

def xml_compare(x1, x2, reporter=None):
    if x1.tag != x2.tag:
        return False
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            return False
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            return False
    if not text_compare(x1.text, x2.text):
        return False
    if not text_compare(x1.tail, x2.tail):
        return False
    cl1 = x1.getchildren()
    cl2 = x2.getchildren()
    if len(cl1) != len(cl2):
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2):
            return False
    return True