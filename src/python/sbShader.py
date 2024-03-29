#!/usr/bin/env python
# encoding: utf-8

import sys, copy, os.path
import wx
import xml.sax, xml.sax.handler, xml.sax.saxutils, xml.sax.xmlreader
from sbItem import Item
from sbWidgets import AppearancePane

#==============================================================================

# Class to describe a shader interface
class ShaderParameter(Item):
    def __init__(self):
        Item.__init__(self)
        self.changed = False
    def dump(self):
        print "==shader parameter (%s, %s, %s)==" % (self.getAttribute('name'), self.getAttribute('type'), self.getAttribute('default'))
        if self.value:
            print "value: " + self.value
        Item.dump(self)
    def setValue(self,value):
        data_type = self.getAttribute('type') # validate against this type
        self.value = value
        self.changed = True
    def hasChanged(self):
        return self.changed
    def initFromDefault(self):
        self.setValue( self.getAttribute( 'default' ) )
        self.changed = False
        
class Separator(Item):
    def __init__(self):
        Item.__init__(self)
    def dump(self):
        print "-----"
        Item.dump(self)

class Shader(Item):
    def __init__( self, filename=None ):
        Item.__init__(self)
        self.description = None
        self.note = None
        self.contents = []
        self.gui = None
        if filename:
            self.load(filename)
    def dump(self):
        print "==shader=="
        for item in self.contents:
            item.dump()  
            
    # static function for finding shader descriptions for specified shader file
    def getFilename( self, filename, cwd=None ):
        (root,ext) = os.path.splitext(filename)
        xml_file = root+".xml"
        result = None
        
        print "looking for %s" % xml_file
        
        # first try absolute
        if os.path.exists( xml_file ):
            result = xml_file
        
        # have we been supplied with a current directory by the calling palette
        if cwd and not result: 
            path = os.path.abspath(os.path.join( cwd, xml_file ))
            if os.path.exists( path ):
                result = path
                
        # next loop through the SHADERBUCKET_SHADER_PATH envvar
        shaderpath = os.getenv( "SHADERBUCKET_SHADER_PATH", None)
        if shaderpath:
            tokens = shaderpath.split(":")
            for tok in tokens:
                print "path: %s"%tok
                path = os.path.abspath(os.path.join( tok, xml_file ))
                if os.path.exists( path ):
                    result = path
                    break
                
        # finally try os.path.cwd()
        if not result:
            path = os.path.abspath(os.path.join( os.getcwd(), xml_file )) 
            if os.path.exists( path ):
                result = path
                
        # if no luck try again with a shortened filename
        if not result:
            shortname = os.path.basename( xml_file )
            if shortname!=xml_file: 
                result = self.getFilename( shortname, cwd )        
                
        # return what we found                
        return result
    
    # set all parameters to their defaults            
    def initParametersFromDefault(self):
        for item in self.contents:
            item.initFromDefault()
    
    # add a parameter to the contents of this shader 
    def addParameter(self, parameter):
        name = parameter.getAttribute('name')
        if self.findParameter(name)==-1:
            self.contents.append(copy.deepcopy(parameter))
        else:
            print "Error: parameter "+name+" already exists!"
            
    # add a separator to the contents of this shader
    def addSeparator(self):
        self.contents.append(Separator())
        
    # load a shader interface file
    def load(self,filename):
        if os.path.exists(filename):
            parser = xml.sax.make_parser()
            parser.setContentHandler( shaderReader(self) )
            parser.parse( filename )
        else:
            print "Error: could not read %s!" % filename

    # set a parameter value
    def setValue( self, name, value ):
        index = self.findParameter(name)
        if index>-1:
            self.contents[index].setValue(value)
            return True
        return False
        
    def findParameter(self,name):
        index = -1
        i = 0
        for p in self.contents:
            if p.getAttribute('name')==name:
                index = i
            i+=1
        return index
        
    # create an interface pane for a shader instance
    def createGui(self, parent):
        pane = AppearancePane( self, parent, wx.BORDER_NONE )        
        sizer = parent.GetSizer()
        sizer.Add( pane, 0 )
        sizer.Layout()        
        self.gui = pane
        
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
        if name=="separator":
            self.startSeparator(attrs)
        self.mode.append( name )
    def endElement(self,name):   
        if name=="shader":
            self.endShader()
        if name=="parameter":
            self.endParameter()
        if name=="group":
            self.endGroup() 
        if name=="separator":
            self.endSeparator()
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
        self.curr_parameter = param
    def endParameter(self):
        self.parent.addParameter(self.curr_parameter)
    def startGroup(self,attrs):
        pass
    def endGroup(self):
        pass
    def startSeparator(self,attrs):
        self.parent.addSeparator()
    def endSeparator(self):
        pass
