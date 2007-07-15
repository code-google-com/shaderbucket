#!/usr/bin/env python
# encoding: utf-8

import wx
from wx.lib.evtmgr import eventManager

#==============================================================================

# Class for our custom appearance pane
class AppearancePane(wx.Panel):
    def __init__(self, appearance, parent, style):
        wx.Panel.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize, style)
                
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( sizer )
        
        top_info = wx.Panel( self, -1, style=wx.NO_BORDER)
        top_sizer = wx.BoxSizer( wx.HORIZONTAL )
        
        preview_img =  wx.BitmapButton( top_info, -1, style = wx.SIMPLE_BORDER, size=(64,64) )      
        top_info_sizer = wx.BoxSizer( wx.VERTICAL )
        
        
        
        
         
        
        top_sizer.Add( preview_img, 0, wx.ALL, 5 )
        top_sizer.Add( top_info_sizer, 0, wx.ALL|wx.EXPAND, 5 )
        top_info.SetSizer( top_sizer )
        
        
        
        
        
        text1 = wx.StaticText(self, -1, appearance.getAttribute('name'))
        text2 = wx.StaticText(self, -1, appearance.getAttribute('file'))
        
        sizer.Add( top_info, 0, wx.ALL|wx.EXPAND, 0 )
        sizer.Add( text1, 0, wx.ALL, 0 )
        sizer.Add( text2, 0, wx.ALL, 0 )

