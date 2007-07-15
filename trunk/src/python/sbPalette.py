#!/usr/bin/env python
# encoding: utf-8

import sys, copy, os.path
import xml.sax, xml.sax.handler, xml.sax.saxutils, xml.sax.xmlreader
import wx
from sbItem import Item
from sbShader import Shader
from sbWidgets import AppearancePane

#==============================================================================

# Class to handle palettes
class Palette(Item):
    # init palette with optional file
    def __init__(self, bucket, filename=""):
        Item.__init__(self)
        self.bucket = bucket
        self.note = ""
        self.contents = []
        self.gui = None
        self.filename = os.path.abspath(filename)
        if filename!="":
            self.load(filename)
            
    # dump information to stdout
    def dump(self):
        print "==palette=="
        Item.dump(self)
        for item in self.contents:
            item.dump()
            
    # add a shader appearance as a child
    def addAppearance(self,appearance):
        # appearance shader file
        filename = appearance.getAttribute( 'file' )
        
        # get shader file relative to this palette
        (root,ext) = os.path.splitext(filename)
        shader_file = os.path.abspath( os.path.join( os.path.dirname( self.filename ), root ) )
        if not self.bucket.shaders.has_key( shader_file ):
            self.bucket.shaders[shader_file] = Shader( shader_file )
        appearance.shader = self.bucket.shaders[shader_file]
        
        self.contents.append(copy.deepcopy(appearance))
        
    # add a palette as a child
    def addPalette(self,palette):
        self.contents.append(copy.deepcopy(palette))
        
    # load a palette into this instance
    def load(self,filename):
        parser = xml.sax.make_parser()
        parser.setContentHandler( paletteReader(self) )
        parser.parse( filename )
        
    # save this instance to a file
    def save(self,filename):
        paletteWriter(filename, self)

#==============================================================================

# Class to describe a shader appearance
class Appearance(Item):
    def __init__( self ):
        Item.__init__(self)
        self.note = ""
        self.parameters = []
        self.shader = None
        self.gui = None   
    def dump(self):
        print "==appearance=="
        Item.dump(self)
        for param in self.parameters:
            param.dump()            
    def addParameter(self, parameter):
        self.parameters.append(copy.deepcopy(parameter))
    def createGui(self, parent):
        # create a gui pane        
        pane = AppearancePane( self, parent, wx.BORDER_NONE )        
        sizer = parent.GetSizer()
        sizer.Add( pane, 1, wx.ALL|wx.EXPAND )
        sizer.Layout()        
        self.gui = pane  
        
#==============================================================================

# Class to describe an appearance parameter
class Parameter(Item):
    def __init__( self ):
        Item.__init__(self)
        self.value = None
    def dump(self):
        print "==parameter=="
        Item.dump(self)
        print "value: ", self.value

#==============================================================================

# Create a class to handle reader palette files
class paletteReader(xml.sax.handler.ContentHandler):
    # init palette reader
    def __init__(self, parent):        
        # shaders/parameters
        self.curr_appearance = None
        self.curr_parameter = None        
        # palettes
        self.palettes = [parent]
        self.curr_palette = parent
        self.done_top_level = False
        # mode
        self.mode = []
        self.bucket = parent.bucket
        self.parent = parent
        pass    

    # start/end document
    def startDocument(self):
        pass        
    def endDocument(self):
        pass       

    # start/end element
    def startElement(self,name,attrs):
        if name=="palette":
            self.startPalette(attrs)
        if name=="shader":
            self.startAppearance(attrs)
        if name=="parameter":
            self.startParameter(attrs)
        self.mode.append( name )
    def endElement(self,name):
        if name=="palette":
            self.endPalette()
        if name=="shader":
            self.endAppearance()
        if name=="parameter":
            self.endParameter()
        self.mode = self.mode[:-1]

    # element contents
    def characters(self,content):
        # parameter values
        if self.mode[-1]=="parameter":
            self.curr_parameter.value = content
            
        # notes can either go on shader appearances on a palette
        if self.mode[-1]=="note":
            if self.curr_appearance:
                self.curr_appearance.note = content
            else:
                self.curr_palette.note = content

    # start/end palettes
    def startPalette(self,attrs):
        if self.done_top_level:
            self.curr_palette = Palette(self.bucket) # create a new palette
            self.curr_palette.filename = self.parent.filename
            
        for name in attrs.getNames():
            self.curr_palette.setAttribute(name, attrs.getValue(name))
        if self.done_top_level:
            self.palettes.append( self.curr_palette ) # push onto the end of the stack
        else:
            self.done_top_level = True

    def endPalette(self):
        if len(self.palettes)>1:
            self.palettes = self.palettes[:-1] # pop from the end of the stack
            self.palettes[-1].addPalette( self.curr_palette ) # add to the previous palette
            self.curr_palette = self.palettes[-1] # set current to previous palette

    # start/end shaders
    def startAppearance(self,attrs):
        self.curr_appearance = Appearance()
        for name in attrs.getNames():
            self.curr_appearance.setAttribute(name, attrs.getValue(name))
    def endAppearance(self):
        self.curr_palette.addAppearance(self.curr_appearance)
        self.curr_appearance = None

    # start/end parameters
    def startParameter(self,attrs):
        self.curr_parameter = Parameter()
        for name in attrs.getNames():
            self.curr_parameter.setAttribute(name, attrs.getValue(name))
    def endParameter(self):
        self.curr_appearance.addParameter( self.curr_parameter )
        self.curr_parameter = None

#==============================================================================

# Class to write a palette out to a file
class paletteWriter:
    def __init__(self, filename, palette):
        outfile = open(filename,"w")
        self.depth = 0
        self.logger = xml.sax.saxutils.XMLGenerator(outfile, "utf-8")
        self.logger.startDocument()
        self.writePalette(palette)
        self.logger.endDocument()
        outfile.close()

    def writePalette(self, palette):    
        attrs = xml.sax.xmlreader.AttributesImpl(palette.attributes)
        self.indent()
        self.logger.startElement('palette', attrs)
        self.newline()
        self.depth+=1
        if palette.note!="":
            self.writeNote( palette.note )
        for item in palette.contents:
            # write out a shader appearance
            if isinstance(item, Appearance):
                self.writeAppearance(item)
            # write out a palette
            if isinstance(item, Palette):
                self.writePalette(item)
        self.depth-=1
        self.indent()
        self.logger.endElement('palette')
        self.newline()
    
    def writeAppearance(self, appearance): 
        attrs = xml.sax.xmlreader.AttributesImpl(appearance.attributes)
        self.indent()
        self.logger.startElement('shader', attrs)
        self.depth+=1
        self.newline()
        if appearance.note!="":
            self.writeNote( appearance.note )
        for param in appearance.parameters:
            if isinstance(param, Parameter):
                self.writeParameter(param)
        self.depth-=1
        self.indent()
        self.logger.endElement('shader')
        self.newline()
        
    def writeParameter(self, parameter):   
        attrs = xml.sax.xmlreader.AttributesImpl(parameter.attributes)
        self.indent()
        self.logger.startElement('parameter', attrs)
        if parameter.value:
            self.logger.characters(parameter.value)
        self.logger.endElement('parameter')
        self.newline()

    def writeNote(self, note):   
        attrs = xml.sax.xmlreader.AttributesImpl({})
        self.indent()
        self.logger.startElement('note', attrs)
        self.logger.characters(note)
        self.logger.endElement('note')
        self.newline()
    
    def newline(self):
        self.logger.characters('\n')
        
    def indent(self):
        tabstr=""
        for i in range(self.depth):
            tabstr+='    '
        self.logger.characters(tabstr)
