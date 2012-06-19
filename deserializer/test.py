'''
Created on 17.06.2012

@author: cristi
'''

def createClass():
        globals()["Dummy"] = type("Dummy", (object,), {})
    
    
createClass()

dum = Dummy()
dum.a = 5
print(dum.a)

if ('b' in getattr(dum)):
    print("ok")
#print (globals())