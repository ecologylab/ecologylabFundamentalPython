'''
Created on 16.06.2012

@author: cristi
'''
from xml.sax import ContentHandler, make_parser
from serializer.simpl_types_scope import SimplTypesScope

currentInstance = None

def deserialize_from_scope(scope):
    pass

def createClass(className):
    newClass = type(className, (object,), {})
    globals()[className] = newClass
    return newClass

def getClassInstance(className):
    return globals()[className]()

class SimplHandler(ContentHandler):
    '''
    SAX handler for deserializing SIMPL object
    '''
    def startElement(self, name, attrs):
        '''
        check every XML new node
        '''
        global currentInstance
        if currentInstance == None:
            classDescriptor = scope.classDescriptors[name]
            className = classDescriptor.simpleName
            currentInstance = createClass(className)
            obj = getClassInstance(className)           
            if len(attrs) > 0:
                for key, value in attrs.items():
                    fd = classDescriptor.fieldDescriptors[key];
                    if (fd.simplType == "scalar"):
                        setattr(obj, fd.name, value)

        print ('Start of element:', name, attrs.keys())

    def endElement(self, name):
        print('End of element:', name)
        
        
        
        
if False:
    scope = SimplTypesScope("JSON", "example_scope")
    
    parser = make_parser();
    parser.setContentHandler(SimplHandler())
    parser.parse("example.xml")