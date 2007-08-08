#!/usr/bin/env python
# encoding: utf-8

import sys, copy, os, os.path
import xml.sax, xml.sax.handler, xml.sax.saxutils, xml.sax.xmlreader
import wx
from sbItem import Item
from sbShader import Shader, ShaderParameter

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
        self.filename = None
        self.valid = True
        self.cwd = os.getcwd()
        if filename!="":
            self.filename = os.path.abspath(filename)
            self.load(filename)
            
    # dump information to stdout
    def dump(self):
        print "==palette=="
        Item.dump(self)
        for item in self.contents:
            item.dump()
            
    # add a shader appearance as a child
    def addAppearance(self, appearance):
        # appearance shader file
        filename = appearance.getAttribute( 'file' )
        
        # get a shader description for our shader
        print "==="
        print "palette: " + self.getAttribute('name')
        print "dir: " + self.cwd
        print "==="
        
        xml_file = Shader().getFilename( filename, cwd=self.cwd ) # this function returns the shader description file for the sdl in question
        if not xml_file:
            print "Error: Could not find shader description for shader %s!" % filename
        
        # load the shader if we haven't already
        if not self.bucket.shaders.has_key( xml_file ):
            self.bucket.shaders[xml_file] = Shader( xml_file )
        shader = self.bucket.shaders[xml_file]
        shader.setAttribute( 'xml', xml_file )
        
        # add an instance of our shader to our palette
        if shader:
                
            # firstly copy the default shader description
            self.contents.append(copy.deepcopy(shader))
            instance = self.contents[-1]
            instance.initParametersFromDefault()
                        
            # then override each of the attributes & parameters for our appearance
            instance.note = appearance.note
            for (name, value) in appearance.attributes.iteritems():
                instance.setAttribute(name, value)
            for p in appearance.parameters:
                instance.setValue(p.getAttribute('name'), p.value)
        
    # add a palette as a child
    def addPalette(self, palette):
        palette.cwd = self.cwd # child inherits our cwd
        self.contents.append(copy.copy(palette))
        
    # load a palette into this instance
    def load(self, filename):
        self.cwd = os.path.dirname( filename )
        parser = xml.sax.make_parser()
        parser.setContentHandler( paletteReader(self) )
        parser.parse( filename )
        
    # save this instance to a file
    def save(self, filename):
        paletteWriter(filename, self)

class AppearanceParameter(Item):
    def __init__(self):
        Item.__init__(self)
        self.value = None

class Appearance(Item):
    def __init__(self):
        Item.__init__(self)
        self.note = ""
        self.parameters = []
    def addParameter(self, parameter):
        self.parameters.append( copy.deepcopy( parameter ) )

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
        self.parent.valid = False
    def endDocument(self):
        self.parent.valid = True

    # start/end element
    def startElement(self, name, attrs):
        if name=="palette":
            self.startPalette(attrs)
        if name=="shader":
            self.startAppearance(attrs)
        if name=="parameter":
            self.startParameter(attrs)
        self.mode.append( name )
    def endElement(self, name):
        if name=="palette":
            self.endPalette()
        if name=="shader":
            self.endAppearance()
        if name=="parameter":
            self.endParameter()
        self.mode = self.mode[:-1]

    # element contents
    def characters(self, content):
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
    def startPalette(self, attrs):
        if self.done_top_level:
            self.curr_palette = Palette(self.bucket) # create a new palette
            self.curr_palette.filename = self.parent.filename # inherit filename & cwd
            self.curr_palette.cwd = self.parent.cwd
            
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
    def startAppearance(self, attrs):
        self.curr_appearance = Appearance()
        for name in attrs.getNames():
            self.curr_appearance.setAttribute(name, attrs.getValue(name))
    def endAppearance(self):
        self.curr_palette.addAppearance(self.curr_appearance)
        self.curr_appearance = None

    # start/end parameters
    def startParameter(self, attrs):
        self.curr_parameter = AppearanceParameter()
        for name in attrs.getNames():
            self.curr_parameter.setAttribute(name, attrs.getValue(name))
    def endParameter(self):
        self.curr_appearance.addParameter( self.curr_parameter )
        
        # sometimes we have a string/file parameter with a null value - set as an empty string
        if self.curr_parameter.getAttribute('type')=='string' or self.curr_parameter.getAttribute('type')=='file':
            if self.curr_parameter.value==None:
                self.curr_parameter.value=""
        
        self.curr_parameter = None

#==============================================================================

# Class to write a palette out to a file
class paletteWriter:
    def __init__(self, filename, palette):
        outfile = open(filename,"w")
        self.depth = 0
        self.logger = xml.sax.saxutils.XMLGenerator(outfile, "utf-8")
        self.outfile = outfile
        self.logger.startDocument()
        self.writePalette(palette)
        self.logger.endDocument()
        outfile.close()
        
    def comment(self, msg):    
        self.indent()
        self.outfile.write( "<!-- "+msg+" -->" )
        self.newline()

    def writePalette(self, palette):    
        attrs = xml.sax.xmlreader.AttributesImpl(palette.attributes)
        self.newline()
        self.comment(palette.getAttribute('name'))
        self.indent()
        self.logger.startElement('palette', attrs)
        self.newline()
        self.depth+=1
        if palette.note!="":
            self.writeNote( palette.note )
        for item in palette.contents:
            # write out a shader appearance
            if isinstance(item, Shader):
                self.writeAppearance(item)
            # write out a palette
            if isinstance(item, Palette):
                self.writePalette(item)
        self.depth-=1
        self.indent()
        self.newline()
        self.indent()
        self.logger.endElement('palette')
        self.newline()
    
    def writeAppearance(self, appearance): 
        appearance_attrs = {'name':appearance.getAttribute('name'), 'file': appearance.getAttribute('file')} #required 
        if appearance.hasAttribute('preview'): # optional
            appearance_attrs['preview'] = appearance.getAttribute('preview')
        attrs = xml.sax.xmlreader.AttributesImpl(appearance_attrs)
        self.newline()
        self.comment(appearance.getAttribute('name'))
        self.indent()
        self.logger.startElement('shader', attrs)
        self.depth+=1
        self.newline()
        if appearance.note:
            self.writeNote( appearance.note )
        for param in appearance.contents:
            if isinstance(param, ShaderParameter):
                if param.hasChanged():
                    self.writeParameter(param)
        self.depth-=1
        self.indent()
        self.logger.endElement('shader')
        self.newline()
        
    def writeParameter(self, parameter):       
        element_attrs = {'name': parameter.getAttribute('name')}
        attrs = xml.sax.xmlreader.AttributesImpl(element_attrs)
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
