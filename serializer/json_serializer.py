'''
Created on 04.07.2012

@author: cristi
'''
import json
#from serializer.simpl_types_scope import SimplTypesScope

class JSONSimplSerializer:
    def __init__(self, simpl_object, simpl_types_scope):
        self.simpl_object = simpl_object
        self.scope = simpl_types_scope
        self.top = None
    
    def serialize(self):
        self.top = dict()
        self.top[self.simpl_object.simpl_tag_name] = self.serializeInDepth(self.simpl_object)
        return self.top

    def serializeInDepth(self, simpl_object):
        tag_name = simpl_object.simpl_tag_name
        class_descriptor = self.scope.classDescriptors[tag_name]
        new_dict = dict()
        for fd_key in class_descriptor.fieldDescriptors:
            fd = class_descriptor.fieldDescriptors[fd_key]
            if hasattr(simpl_object, fd.name):
                if fd.simpl_type == "scalar":
                    new_dict[str(fd.tagName)] = str(getattr(simpl_object, fd.name))
                if fd.simpl_type == "composite":
                    new_dict[str(fd.tagName)] = self.serializeInDepth(getattr(simpl_object, fd.name))
                if fd.simpl_type == "collection":
                    collection_dict = dict()
                    collection_dict[fd.collection_tag_name] = []
                    children = getattr(simpl_object, fd.name)
                    for child in children:
                        collection_dict[fd.collection_tag_name].append(self.serializeInDepth(child))
                    new_dict[fd.tagName] = collection_dict
        return new_dict
    
    def toString(self):
        return json.dumps(self.top)
    
    
