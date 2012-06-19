'''
Created on 15.06.2012

@author: cristi
'''

class GeneratorUtils:

    def begin(self, tab="\t"):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return "\n".join(self.code)

    def write(self, string):
        self.code.append(self.tab * self.level + string)

    def increaseIndent(self):
        self.level = self.level + 1

    def decreaseIndent(self):
        if self.level == 0:
            raise SyntaxError("code generator error - 0 level reached")
        self.level = self.level - 1
        
if False:     
    c = GeneratorUtils()
    c.begin()
    c.write("for i in range(1,10)")
    c.increaseIndent()
    c.write("print(i)")
    print(c.end())
