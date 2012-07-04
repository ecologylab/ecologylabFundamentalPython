'''
Created on 23.06.2012

@author: cristi
'''
from xml.etree.ElementTree import Element, tostring
from serializer import class_descriptor
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")

class XmlSimplSerializer:
    def __init__(self, simpl_object, simpl_types_scope):
        self.simpl_object = simpl_object
        self.scope = simpl_types_scope
        self.top = None
    
    def serialize(self):
        self.top = self.serializeInDepth(self.simpl_object, self.simpl_object.simpl_tag_name)
        return self.top

    def serializeInDepth(self, simpl_object, simpl_name):
        tag_name = simpl_object.simpl_tag_name
        xml_element = Element(simpl_name)
        class_descriptor = self.scope.classDescriptors[tag_name]
        
        for fd_key in class_descriptor.fieldDescriptors:
            fd = class_descriptor.fieldDescriptors[fd_key]
            if hasattr(simpl_object, fd.name):
                if (fd.simpl_type == "scalar"):
                    if (hasattr(fd, "xml_hint")):
                        if (fd.xml_hint == "XML_LEAF"):
                            child = Element(fd.tagName)
                            child.text = getattr(simpl_object, fd.name)
                            xml_element.append(child)
                        if (fd.xml_hint == "XML_ATTRIBUTE"):
                            xml_element.set(fd.tagName, getattr(simpl_object, fd.name))
                    else:
                        xml_element.set(fd.tagName, getattr(simpl_object, fd.name))
                else:
                    xml_element.append(self.serializeInDepth(getattr(simpl_object, fd.name), fd.name))
        return xml_element
    
    def toString(self):
        return tostring(self.top)