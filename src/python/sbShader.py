#!/usr/bin/env python
# encoding: utf-8

import sys, copy
import xml.sax, xml.sax.handler, xml.sax.saxutils, xml.sax.xmlreader
from sbItem import Item

#==============================================================================

# Class to describe a shader interface
class ShaderParameter(Item):
    def __init__(self):
        Item.__init__(self)
    def dump(self):
        print "==shader parameter (%s, %s, %s)==" % (self.name, self.type, self.default)
        Item.dump(self)   
        
class Separator(Item):
    def __init__(self):
        Item.__init__(self)
    def dump(self):
        print "-----"
        Item.dump(self)

class Shader(Item):
    def __init__( self, filename="" ):
        Item.__init__(self)
        self.description = None
        self.contents = []     
    def dump(self):
        print "==shader=="
        for item in self.contents:
            item.dump()            
    def addParameter(self, parameter):
        self.parameters.append(copy.deepcopy(parameter))
