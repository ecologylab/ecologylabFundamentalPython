'''
Created on 04.07.2012

@author: cristi
'''
import json
from deserializer.field_type import FieldType
from utils.general_utils import *

class JSONSimplSerializer:
    def __init__(self, simpl_object, simpl_types_scope):
        self.simpl_object = simpl_object
        self.scope = simpl_types_scope
        self.top = None
        self.serializedObjects = {}
        
    def serialize(self):
        self.top = dict()
        self.top[self.simpl_object.simpl_tag_name] = self.serializeInDepth(self.simpl_object)
        return self.top

    def serializeInDepth(self, simpl_object):
        tag_name = simpl_object.simpl_tag_name
        class_descriptor = self.scope.classDescriptors[tag_name]
        new_dict = dict()
        if self.handleGraphSerialization(simpl_object, new_dict):
            return new_dict
        for fd_key in class_descriptor.fieldDescriptors:
            fd = class_descriptor.fieldDescriptors[fd_key]
            if hasattr(simpl_object, fd.name):
                if fd.simpl_type == "scalar":
                    new_dict[str(fd.tagName)] = str(getattr(simpl_object, fd.name))
                if fd.simpl_type == "composite":
                    new_dict[str(fd.tagName)] = self.serializeInDepth(getattr(simpl_object, fd.name))
                if fd.simpl_type == "collection":
                    new_dict = self.serializeCollection(simpl_object, fd, new_dict)
        return new_dict
    
    def serializeCollection(self,simpl_object, fd, new_dict):
        collection_dict = dict()
        collection_dict[fd.collection_tag_name] = []
        children = getattr(simpl_object, fd.name)
        for child in children:
            if fd.getType() == FieldType.COLLECTION_ELEMENT:
                if fd.isPolymorphicCollection():
                    child_dict = {}
                    child_dict[child.simpl_tag_name] = self.serializeInDepth(child)
                    collection_dict[fd.collection_tag_name].append(child_dict)
                else:
                    collection_dict[fd.collection_tag_name].append(self.serializeInDepth(child))
            if fd.getType() == FieldType.COLLECTION_SCALAR:
                collection_dict[fd.collection_tag_name].append(str(child))
            if fd.getType() == FieldType.MAP_ELEMENT:
                aux = self.serializeInDepth(children[child])
                collection_dict[fd.collection_tag_name].append(aux)
                       
        if fd.isWrappedCollection() and not fd.isPolymorphicCollection():
            new_dict[fd.tagName] = collection_dict
        else:
            new_dict[fd.collection_tag_name] = collection_dict[fd.collection_tag_name]
        return new_dict
    
    def handleGraphSerialization(self, simpl_object, json_element):
        if (self.isGraphSerialization()):
            simpl_id = getObjectSimplId(simpl_object)
            if (simpl_id in self.serializedObjects):
                json_element["simpl:ref"] = simpl_id
                self.serializedObjects[simpl_id]["simpl:id"] = simpl_id
                return True
            else:
                self.serializedObjects[simpl_id] = json_element
                return False
        else:
            return False
        
    def toString(self):
        return json.dumps(self.top)
    
    def isGraphSerialization(self):
        return self.scope.graphSerialization == True
    
