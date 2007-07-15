#!/usr/bin/env python
# encoding: utf-8

import sys, copy, os.path
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
        self.contents.append(copy.deepcopy(parameter))
    def load(self,filename):
        interfacefile = filename+".xml"
        if os.path.exists(interfacefile):
            parser = xml.sax.make_parser()
            parser.setContentHandler( shaderReader(self) )
            parser.parse( interfacefile )
        
#==============================================================================

# Create a class to handle reader palette files
class shaderReader(xml.sax.handler.ContentHandler):
    # init palette reader
    def __init__(self, parent): 
        self.parent = parent
        self.curr_parameter = None 
        self.mode = []
        pass    

    # start/end document
    def startDocument(self):
        pass        
    def endDocument(self):
        pass       

    # start/end element
    def startElement(self,name,attrs):
        if name=="shader":
            self.startShader(attrs)
        if name=="parameter":
            self.startParameter(attrs)
        if name=="group":
            self.startGroup(attrs)
        self.mode.append( name )
    def endElement(self,name):   
        if name=="shader":
            self.endShader()
        if name=="parameter":
            self.endParameter()
        if name=="group":
            self.endGroup() 
        self.mode = self.mode[:-1]

   # element contents
    def characters(self,content):
        # description values
        if self.mode[-1]=="description":
            self.parent.description = content
            
    def startShader(self,attrs):
        for name in attrs.getNames():
            self.parent.setAttribute(name, attrs.getValue(name))
    def endShader(self):
        pass
    def startParameter(self,attrs):
        param = ShaderParameter()
        for name in attrs.getNames():
            param.setAttribute(name, attrs.getValue(name))
        self.parent.addParameter(param)
    def endParameter(self):
        pass
    def startGroup(self,attrs):
        pass
    def endGroup(self):
        pass
