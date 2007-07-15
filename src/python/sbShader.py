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
        if filename!="":
            self.load(filename)  
    def dump(self):
        print "==shader=="
        for item in self.contents:
            item.dump()            
    def addParameter(self, parameter):
        self.parameters.append(copy.deepcopy(parameter))
    def load(self,filename):
        parser = xml.sax.make_parser()
        parser.setContentHandler( shaderReader(self) )
        #parser.parse( filename )
        
#==============================================================================

# Create a class to handle reader palette files
class shaderReader(xml.sax.handler.ContentHandler):
    # init palette reader
    def __init__(self, parent):  
        pass    

    # start/end document
    def startDocument(self):
        pass        
    def endDocument(self):
        pass       

    # start/end element
    def startElement(self,name,attrs):
        pass
    def endElement(self,name):
        pass

    # element contents
    def characters(self,content):
        pass
