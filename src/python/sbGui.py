#!/usr/bin/env python
# encoding: utf-8

import sys, os
import wx
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
        self.addPalette(None, wx.GetTopLevelParent(self).bucket.root)
            
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

#==============================================================================

# Class for our custom main window thingy
class MainFrame(wx.Frame):
    def __init__( self, parent, title ):
        wx.Frame.__init__( self, parent, -1, title, pos=(800,100), size=(640,480) )
        self.bucket = None
        
        # main bits & bobs
        #self.CreateMenuBar()
        self.status_bar = self.CreateStatusBar()
        
        # main panel
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizer(main_sizer)
        
        # top/bottom splitter
        main_splitter = wx.SplitterWindow(main_panel, -1, style=wx.SP_LIVE_UPDATE)
        main_splitter.SetSashSize(6)        
        
        # appearance left/right splitter
        appearance_splitter = wx.SplitterWindow(main_splitter, -1, style=wx.SP_LIVE_UPDATE)
        appearance_splitter.SetSashSize(6)
        appearance_splitter.SetMinimumPaneSize(20)

        self.tree = PaletteTree( appearance_splitter, wx.TR_DEFAULT_STYLE|wx.BORDER_SUNKEN|wx.TR_HIDE_ROOT|wx.TR_EDIT_LABELS )
        self.appearance = wx.Panel( appearance_splitter, -1, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_SUNKEN )
        
        app_sizer = wx.BoxSizer( wx.VERTICAL )
        self.appearance.SetSizer( app_sizer )        
        
        appearance_splitter.SplitVertically(self.tree, self.appearance, 240)
        self.tree.appearance_window = self.appearance
        
        # bucket pane
        self.bucket_pane = wx.Panel( main_splitter, -1 )
        self.bucket_pane.SetBackgroundColour( "yellow" )
        
        # main splitter
        main_splitter.SplitHorizontally( appearance_splitter, self.bucket_pane )
        
        # add stuff to main panel
        main_sizer.Add(main_splitter, 1, wx.ALL|wx.EXPAND, 5)        
        
        # setup events
        self.Bind(wx.EVT_CLOSE, self.CloseWindow)
        
        
    # OnClose
    def CloseWindow(self, evt):
        """Event handler for the close event."""
        self.Destroy()
    
    # add our menu bars
    def CreateMenuBar( self ):
        # Create the menubar
        menuBar = wx.MenuBar()
        
        # add some stuff to it        
        '''menu1 = wx.Menu()
        menu1.Append(101, "&Mercury", "This the text in the Statusbar")
        menu1.Append(102, "&Venus", "")
        menu1.Append(103, "&Earth", "You may select Earth too")
        menu1.AppendSeparator()
        menu1.Append(104, "&Close", "Close this frame")
        menuBar.Append(menu1, "&Planets")
        '''
        menu2 = wx.Menu()
        menu2.Append(201, "&Help", "Some help innit")
        menuBar.Append(menu2, "&Help")
        
        self.Bind(wx.EVT_MENU, self.CloseWindow, id=104)
        
        # add to menu bar
        self.SetMenuBar(menuBar)
    
    def setBucket(self, bucket):
        self.bucket = bucket
        self.refresh()
        
    def refresh(self):
        self.tree.rebuild()


#==============================================================================

# Our application
class App(wx.App):
    def __init__(self, bucket=None, redirect=False):
        global shader_bucket
        self.bucket = bucket
        if bucket:
            shader_bucket = bucket
        wx.App.__init__(self, redirect=redirect )

    def OnInit(self, bucket=None):
        self.win = MainFrame(None,"ShaderBucket")
        if self.bucket:
            self.win.setBucket( self.bucket )
            self.bucket.gui = self.win
        self.SetTopWindow(self.win)
        self.win.Show(True)
        return True
    
    def refresh(self):
        self.win.refresh()

