#!/usr/bin/env python
# encoding: utf-8

import sys, os
import wx
import wx.xrc
from wx.lib.evtmgr import eventManager
from sbPalette import Palette, Appearance
from sbShader import Shader

#==============================================================================

shader_bucket = None
def debug( msg ):
    global shader_bucket
    if shader_bucket:
        shader_bucket.debug( msg )

# Class for our custom tree control
class PaletteTree(wx.TreeCtrl):
    def __init__(self, parent, style):
        wx.TreeCtrl.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize, style)
        self.root = None
        self.clear()
        self.appearance_window = None
        self.last_appearance = None
        eventManager.Register(self.changeLabel, wx.EVT_TREE_END_LABEL_EDIT, self)
        eventManager.Register(self.selectionChange, wx.EVT_TREE_SEL_CHANGED, self)
        
    def addPalette(self, parent, palette):
        node = None
        if not parent:
            node = self.root = self.AddRoot("ShaderBucket")
        else:
            node = self.AppendItem(parent, palette.getAttribute('name'), data=wx.TreeItemData(palette) )
        for item in palette.contents:
            if isinstance(item,Palette):
                self.addPalette(node, item)
            if isinstance(item,Shader):
                self.addAppearance(node, item)
                
    def addAppearance(self, parent, appearance):
        appearance.createGui( self.appearance_window )
        self.hideAppearance( appearance )
        app = self.AppendItem(parent, appearance.getAttribute('name'), data=wx.TreeItemData(appearance) ) 
        
    def clear(self):
        self.DeleteAllItems()
        
    def showAppearance( self, appearance ):
        appearance.gui.Show() 
        sizer = self.appearance_window.GetSizer()
        sizer.Add( appearance.gui, 1, wx.ALL|wx.EXPAND )
        sizer.Layout()       
        
    def hideAppearance( self, appearance ):
        sizer = self.appearance_window.GetSizer()
        sizer.Detach( appearance.gui )
        sizer.Layout()
        appearance.gui.Hide()        

    def rebuild(self):
        self.clear()
        if self.bucket:
            self.addPalette(None, self.bucket.root)
        else:
            print "Error: tree could not find it's shaderbucket!"
            
    def changeLabel(self,evt):
        data = self.GetItemPyData(evt.GetItem())
        lbl = evt.GetLabel()
        if data and lbl!="":
            data.setAttribute( 'name', evt.GetLabel() )
    def selectionChange(self,evt):
        data = self.GetItemPyData(evt.GetItem())
        if data:
            debug( data.getAttribute( 'name' ) )
            if self.last_appearance:
                self.hideAppearance( self.last_appearance )
            if data.gui:
                self.showAppearance( data )
                self.last_appearance = data        

class PaletteTreeXmlHandler(wx.xrc.XmlResourceHandler):
    def __init__(self):
        wx.xrc.XmlResourceHandler.__init__(self)
        # Specify the styles recognized by objects of this type
        self.AddStyle("wxNO_3D", wx.NO_3D)
        self.AddStyle("wxTAB_TRAVERSAL", wx.TAB_TRAVERSAL)
        self.AddStyle("wxWS_EX_VALIDATE_RECURSIVELY", wx.WS_EX_VALIDATE_RECURSIVELY)
        self.AddStyle("wxCLIP_CHILDREN", wx.CLIP_CHILDREN)
        self.AddWindowStyles()

    def CanHandle(self, node):
        return self.IsOfClass(node, "PaletteTree")

    def DoCreateResource(self):
        assert self.GetInstance() is None
        
        tree = PaletteTree(self.GetParentAsWindow(),
                             # self.GetStyle(defaults=wx.TR_DEFAULT_STYLE|wx.BORDER_SUNKEN|wx.TR_HIDE_ROOT|wx.TR_EDIT_LABELS) )
                             self.GetStyle(defaults=wx.TR_DEFAULT_STYLE|wx.BORDER_SUNKEN|wx.TR_EDIT_LABELS) )
        self.SetupWindow(tree)
        self.CreateChildren(tree)

        # setup some stuff
        tree.SetName( self.GetName() ) # set out name
        tree.bucket = None # the shaderbucket this represents

        return tree

#==============================================================================

# Our application
class App(wx.App):
    def __init__(self, bucket=None, redirect=False):
        global shader_bucket
        self.bucket = bucket
        if bucket:
            shader_bucket = bucket
        wx.App.__init__(self, redirect=redirect )
        
    # recursively add gui components to a global contents dictionary
    def StoreChildrenByName(self, root, contents):
        for child in root.GetChildren():
            contents[child.GetName()] = child
            self.StoreChildrenByName( child, contents )

    # load the xrc and create the main_frame
    def OnInit(self, bucket=None):
        self.xrc = wx.xrc.XmlResource( "src/xrc/shaderbucket.xrc" )
        self.xrc.AddHandler(PaletteTreeXmlHandler())
        self.win = self.xrc.LoadFrame( None, "main_frame" )
        self.contents = {}
        self.StoreChildrenByName( self.win, self.contents )
        
        print ""
        for name in self.contents.iterkeys():
            print name
        print ""

        if self.bucket:
            self.contents['palette_tree'].bucket = self.bucket
            self.contents['palette_tree'].appearance_window = self.contents['appearance_panel']
            self.contents['palette_tree'].rebuild()
            self.contents['palette_tree'].ExpandAll()            
            self.bucket.gui = self.win

        # setup some gui components
        self.contents['leftright_split'].SetSashSize(6)
        self.contents['leftright_split'].SetMinimumPaneSize(200)
    
        self.SetTopWindow(self.win)        
        self.win.Show(True)
        self.win.SetSize( (640,480) )

        return True
    
    def refresh(self):
        self.win.refresh()