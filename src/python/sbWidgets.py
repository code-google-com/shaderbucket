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

        sizer.Add( top_info, 0, wx.ALL|wx.EXPAND, 0 )

        if appearance.shader:
            parameters = appearance.shader.contents
            for param in parameters:
                string = param.getAttribute('name') + ": " + param.getAttribute('default')
                text = wx.StaticText(self, -1, string)
                sizer.Add( text, 0, wx.ALL, 5 )
