#! /usr/bin/env python
"""pyfuk module, where is call for brainfuck interpreting

defines own exception InterpretationError, main class is
class BrainInterpreter. If you want to use this as a program,
please run mindfuck.py"""

import sys

class InterpretationError(Exception):
    """If there is something bad with interpretation"""
    pass

class BrainInterpreter():
    """BrainInterpreter, main class of pyfuk
    
    interprets code, when called its interpret(code) method
    uses method __interpretOneChar for char-to-char interpreting,
    loops is handled in interpret method. Stack of brainfuck
    is in self.brainstack and reserver words of brainfuck are
    in list reservedWords. Standard output is given through
    constructor, default is sys.stdout.write. Standard input
    is given through constructor argument too, default is raw_input
    If you want to step-by-step debug, set debug=1 in constructor"""
    
    reservedWords = ['+','-','.',',','>','<','[',']']
    
    def __init__(self,writeFunction=sys.stdout.write,readFunction=raw_input,debug=0,eof=0,hud=0):
        """Initialization. Takes several arguments.
        writeFunction is standard output - default is sys.stdout.write
        readFunction is standard input - default is raw_input
        set debug to 0 or 1 whether you want to display debugging symbols"""
         
        self.brainstack = [0, 0, 0]
        self.__position = 1
        self.__loopposition = []
        self.__output = writeFunction
        self.__input = readFunction
        self.__inputstack = []
        self.__debug = debug
        self.__eof = eof
        self.__hud = hud
        if debug != 0:
            self.debugstep = 0
    
    def interpret(self, code):
        """interpret method
        
        for parsing brainfuck words and calling
        __interpretOneChar for interpreting itself.
        Here are loops handled."""
        
        if code.count('[')!=code.count(']'):
            raise InterpretationError, "bad loop count"
        
        x = 0
        
        while x < len(code):
            if self.__debug != 0:
                if x<len(code):
                    print "Position in code: ",x+1, ", char is: ",
                    print code[x], ", step is: ", self.debugstep
                self.debugstep = self.debugstep + 1
                print self
                raw_input()
            if code[x] == '[':
                if self.brainstack[self.__position] != 0:
                    self.__loopposition.append(x)
                    x = x + 1
                else:
                    x = x + 1
                    countBack = 1
                    while countBack > 0:
                        if code[x] == ']':
                            countBack -= 1
                        elif code[x] == '[':
                            countBack += 1
                        x = x + 1
            elif code[x] == ']':
                if self.__loopposition != []:
                    x = self.__loopposition[-1]
                    del(self.__loopposition[-1])
                else:
                    raise InterpretationError, "must be '[' before ']' in loop"
            elif code[x] in self.reservedWords:
                self.__interpretOneChar(code[x])
                x = x + 1
            else:
                x = x + 1
        #print x
    
    def __interpretOneChar(self, char):
        """__interpretOneChar(char)
        
        for brainfuck interpreting itself"""
        
        if char == '+':
            if self.brainstack[self.__position] < 255:
                self.brainstack[self.__position] += 1
        elif char == '-':
            if self.brainstack[self.__position] > 0:
                self.brainstack[self.__position] -= 1
        elif char == '.':
            try:
                self.__output(chr(self.brainstack[self.__position]))
            except ValueError:
                if self.__debug: print "# Cannot print cell with -1" 
        elif char == ',':
            if self.__inputstack == []:
                try:
                    if self.__hud:
                        self.__inputstack = list(self.__input("Input: "))
                    else:
                        self.__inputstack = list(self.__input())
                    if self.__inputstack != []:
                        self.brainstack[self.__position] = ord(self.__inputstack.pop(0))
                    else:
                        self.brainstack[self.__position] = 10
                except EOFError:
                    self.brainstack[self.__position] = 0 if self.__eof == 0 else -1 if self.__eof\
                        == 2 else self.brainstack[self.__position]
            else:
                self.brainstack[self.__position] = ord(self.__inputstack.pop(0))
        elif char == '>':
            self.__position += 1
            if len(self.brainstack)<(self.__position+1):
                self.brainstack.append(0)
        elif char == '<':
            if self.__position == 0:
                self.brainstack.insert(0,0)
            else:
                self.__position -= 1
    
    def __str__(self):
        """printf of BrainIterpreter
        
        if you want to print whole stack (e.g. when debugging)"""

        chain = ""        

        for x in range(len(self.brainstack)):
            chain += `self.brainstack[x]`+' '
            if self.__position == x:
                chain += "<-"
        chain += "\n"
        return chain

if __name__ == "__main__":
    print "You must run mindfuck.py module for brainfuck interpreting"
