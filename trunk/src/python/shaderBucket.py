#!/usr/bin/env python
# encoding: utf-8

import sys, os, thread
from sbGui import App
from sbPalette import Palette
from sbShader import Shader
        
#==============================================================================

# Class for the top-level shader bucket
class ShaderBucket:
    # init our bucket
    def __init__(self):
        self.clear()
        self.shaders = {}
        self.root = Palette(self)
        self.root.setAttribute('name', "ShaderBucket")
        self.mutex = thread.allocate_lock()
        self.gui = None
        self.print_debug = False
    # print a load of debug information
    def dump(self):
        print str(len(self.root.contents))+" items in bucket"
        print "--"
        print self.root.dump()
    # clear up this bucket
    def clear(self):
        self.contents = [] # our contents
        self.shaders = [] # loaded shader details
    def debug(self, msg):
        if self.gui and self.print_debug:
            self.gui.SetStatusText( msg )
        if self.print_debug:
            print msg
            
#==============================================================================
       
# Main Block
if __name__ == '__main__': 
    # create a shader bucket 
    sb = ShaderBucket()
    #sb.print_debug = True;
    
    argv = sys.argv
    argc = len(argv)
    
    for arg in argv[1:]:
        sb.root.addPalette( Palette(sb, arg ) )
    
    # do some gui stuff
    gui = App(bucket=sb, redirect=False)
    gui.MainLoop()    
    
    # test write of our new palette
    #sb.root.contents[0].save("outfile.xml")
