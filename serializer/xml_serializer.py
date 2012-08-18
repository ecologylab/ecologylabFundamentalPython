'''
Created on 23.06.2012

@author: cristi
'''
from xml.etree.ElementTree import Element, tostring
from serializer import class_descriptor
from xml.dom import minidom
from deserializer.field_type import FieldType

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
                if fd.simpl_type == "scalar":
                    if (hasattr(fd, "xml_hint")):
                        if (fd.xml_hint == "XML_LEAF"):
                            child = Element(fd.tagName)
                            child.text = str(getattr(simpl_object, fd.name))
                            xml_element.append(child)
                        if (fd.xml_hint == "XML_ATTRIBUTE"):
                            xml_element.set(fd.tagName, str(getattr(simpl_object, fd.name)))
                    else:
                        xml_element.set(fd.tagName, str(getattr(simpl_object, fd.name)))
                elif fd.simpl_type == "composite":
                    xml_element.append(self.serializeInDepth(getattr(simpl_object, fd.name), fd.name))
                elif fd.simpl_type == "collection":
                    xml_element = self.serializeCollection(simpl_object, fd, xml_element)
        return xml_element
    
    def serializeCollection(self, simpl_object, fd, xml_element):
        if fd.isWrappedCollection() or fd.isPolymorphicCollection():
            new_elem = Element(fd.tagName)
        else:
            new_elem = xml_element
        if hasattr(simpl_object, fd.name):
            collection_list = getattr(simpl_object, fd.name)
            for item in collection_list:
                if fd.getType() == FieldType.COLLECTION_ELEMENT:
                    if fd.isPolymorphicCollection():
                        new_elem.append(self.serializeInDepth(item, item.simpl_tag_name))
                    else:
                        new_elem.append(self.serializeInDepth(item, fd.collection_tag_name))
                if fd.getType() == FieldType.COLLECTION_SCALAR:
                    new_elem.append(self.newStringElement(fd.collection_tag_name, str(item)))
                if fd.getType() == FieldType.MAP_ELEMENT:
                    new_elem.append(self.serializeInDepth(collection_list[item], fd.collection_tag_name))
        if fd.isWrappedCollection() or fd.isPolymorphicCollection():
            xml_element.append(new_elem)
        return xml_element
        
    def newStringElement(self, tag, content):
        new_elem = Element(tag)
        new_elem.text = content
        return new_elem
    
    def toString(self):
        return tostring(self.top)