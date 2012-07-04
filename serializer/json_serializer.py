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
        self.top[self.simpl_object.simpl_tag_name] = [self.serializeInDepth(self.simpl_object, self.simpl_object.simpl_tag_name)]
        return self.top

    def serializeInDepth(self, simpl_object, simpl_name):
        tag_name = simpl_object.simpl_tag_name
        class_descriptor = self.scope.classDescriptors[tag_name]
        new_dict = dict()
        for fd_key in class_descriptor.fieldDescriptors:
            fd = class_descriptor.fieldDescriptors[fd_key]
            if hasattr(simpl_object, fd.name):
                if (fd.simpl_type == "scalar"):
                    new_dict[fd.tagName] = getattr(simpl_object, fd.name)
                else:
                    new_dict[fd.tagName] = self.serializeInDepth(getattr(simpl_object, fd.name), fd.name)
        return new_dict
    
    def toString(self):
        return json.dumps(self.top)
    
    
