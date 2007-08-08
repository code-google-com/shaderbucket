#!/usr/bin/env python
# encoding: utf-8

import wx
import string
import os.path
from wx.lib.evtmgr import eventManager
        
class CtrlValidator(wx.PyValidator):
    def __init__(self, flag, update_func=None):
        wx.PyValidator.__init__(self)
        self.type = flag
        self.update = update_func
        self.Bind(wx.EVT_CHAR, self.OnChar)
    def Clone(self):
        return CtrlValidator(self.type)        
    def OnChar(self, event):    
        key = event.GetKeyCode()
        val = self.GetWindow().GetValue()
        
        # spaces and escapes and backspaces etc
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
            
        # float
        if self.type=='float':
            if chr(key) in string.digits:
                event.Skip()
                return
            if chr(key)=='.' and not '.' in val:
                event.Skip()
                return
        
        # ring?
        if not wx.Validator_IsSilent():
            wx.Bell()
        return

class Ctrl(wx.Panel):
    def __init__(self, parent, parameter):
        wx.Panel.__init__(self, parent, -1)
        self.parameter = parameter
        self.sizer = wx.BoxSizer( wx.HORIZONTAL )
        self.SetSizer( self.sizer )
        
        # common widgets
        self.help_btn = wx.Button(self, -1, "")
        self.help_btn.SetMinSize((15, 15))
        
        self.lbl = wx.StaticText(self, -1, parameter.getAttribute('name'), size=(160,20))
        self.lbl.SetMinSize((120, 17))
        
        self.sizer.Add( (20,20), 0, wx.ADJUST_MINSIZE, 0)
        self.sizer.Add( self.help_btn, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add( (10,20), 0, wx.ADJUST_MINSIZE, 0)
        self.sizer.Add( self.lbl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add( (20,20), 0, wx.ADJUST_MINSIZE, 0)
    
class FloatCtrl(Ctrl):
    def __init__(self, parent, parameter):
        Ctrl.__init__(self, parent, parameter)
        
        # value
        self.ctrl = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.updateField) )        
        self.ctrl.SetValue( parameter.value )
        self.ctrl.Bind( wx.EVT_TEXT, self.updateField )
        
        # slider        
        self.slider = wx.Slider(self, -1, 0, 0, 100, style=wx.SL_HORIZONTAL) 
        self.slider.Bind( wx.EVT_SCROLL, self.updateSlider )       
        
        self.sizer.Add( self.ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE|wx.ALIGN_RIGHT, 0 )
        self.sizer.Add( (10,20), 0, wx.ADJUST_MINSIZE, 0 )
        self.sizer.Add( self.slider, 1, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE|wx.ALIGN_RIGHT, 0 )
        self.sizer.Add( (20,20), 0, wx.ADJUST_MINSIZE, 0 )
    def updateField(self, event):
        self.parameter.setValue(self.ctrl.GetValue())
        event.Skip()
        return
    def updateSlider(self, event):
        value = float(self.slider.GetValue()/100.0)
        self.parameter.setValue(value)
        self.ctrl.SetValue(str(value))
        event.Skip()
        return
        
class StringCtrl(Ctrl):
    def __init__(self, parent, parameter):
        Ctrl.__init__(self, parent, parameter)
        self.ctrl = wx.TextCtrl(self, -1 )    
        if not parameter.value: # occasionally we might have a None value
            parameter.value = ""
        self.ctrl.SetValue( parameter.value )
        self.ctrl.Bind( wx.EVT_TEXT, self.update )
        self.sizer.Add( self.ctrl, 1, wx.ALIGN_CENTER_VERTICAL, 0 )
        self.sizer.Add( (20,20), 0, wx.ADJUST_MINSIZE, 0 )
    def update(self, event):
        self.parameter.setValue(self.ctrl.GetValue())
        event.Skip()
        return

class BoolCtrl(Ctrl):
    def __init__(self, parent, parameter):
        Ctrl.__init__(self, parent, parameter)
        self.ctrl = wx.CheckBox(self, -1 )        
        self.ctrl.SetValue( bool(parameter.value) )
        self.ctrl.Bind( wx.EVT_CHECKBOX, self.update )
        self.sizer.Add( self.ctrl, 0, wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0 )
        self.sizer.Add( (20,20), 0, wx.ADJUST_MINSIZE, 0 )
    def update(self, event):
        self.parameter.setValue(str(self.ctrl.GetValue()))
        event.Skip()
        return

class ColourCtrl(Ctrl):
    def __init__(self, parent, parameter):
        Ctrl.__init__(self, parent, parameter)
        self.ctrl = {}
        self.ctrl[0] = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update), size=(60,25) )        
        self.ctrl[1] = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update), size=(60,25) )        
        self.ctrl[2] = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update), size=(60,25) )           
        self.ctrl[0].Bind( wx.EVT_TEXT, self.update )           
        self.ctrl[1].Bind( wx.EVT_TEXT, self.update )           
        self.ctrl[2].Bind( wx.EVT_TEXT, self.update )        
        toks = parameter.value.split(',')
        for i in range(len(toks)):
            self.ctrl[i].SetValue( toks[i] )          
        self.sizer.Add(self.ctrl[0], 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add((10, 20), 0, wx.ADJUST_MINSIZE, 0)
        self.sizer.Add(self.ctrl[1], 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add((10, 20), 0, wx.ADJUST_MINSIZE, 0)
        self.sizer.Add(self.ctrl[2], 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
    def update(self, event):
        value = "%s,%s,%s"%(self.ctrl[0].GetValue(), self.ctrl[1].GetValue(), self.ctrl[2].GetValue())
        self.parameter.setValue(value)
        event.Skip()
        return
        
class PointCtrl(Ctrl):
    def __init__(self, parent, parameter):
        Ctrl.__init__(self, parent, parameter)
        self.ctrl = {}
        self.ctrl[0] = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update), size=(60,25) )        
        self.ctrl[1] = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update), size=(60,25) )        
        self.ctrl[2] = wx.TextCtrl(self, -1, validator=CtrlValidator('float', self.update), size=(60,25) )           
        self.ctrl[0].Bind( wx.EVT_TEXT, self.update )           
        self.ctrl[1].Bind( wx.EVT_TEXT, self.update )           
        self.ctrl[2].Bind( wx.EVT_TEXT, self.update )        
        toks = parameter.value.split(',')
        for i in range(len(toks)):
            self.ctrl[i].SetValue( toks[i] )          
        self.sizer.Add(self.ctrl[0], 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add((10, 20), 0, wx.ADJUST_MINSIZE, 0)
        self.sizer.Add(self.ctrl[1], 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add((10, 20), 0, wx.ADJUST_MINSIZE, 0)
        self.sizer.Add(self.ctrl[2], 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE, 0)
        self.sizer.Add((20, 20), 0, wx.ADJUST_MINSIZE, 0)
    def update(self, event):
        value = "%s,%s,%s"%(self.ctrl[0].GetValue(), self.ctrl[1].GetValue(), self.ctrl[2].GetValue())
        self.parameter.setValue(value)
        event.Skip()
        return

#==============================================================================

# Class for our custom appearance pane
class AppearancePane(wx.ScrolledWindow):
    def __init__(self, appearance, parent, style):
        wx.ScrolledWindow.__init__(self, parent, -1, wx.DefaultPosition, wx.DefaultSize, style)
        self.SetScrollRate(10, 10)
        sizer = wx.BoxSizer( wx.VERTICAL )
        self.SetSizer( sizer )
        self.SetMinSize( (10,10) )
        self.SetSize((10,10))        

        top_info = wx.Panel( self, -1, style=wx.NO_BORDER)
        top_sizer = wx.BoxSizer( wx.HORIZONTAL )

        preview_img =  wx.BitmapButton( top_info, -1, style = wx.SIMPLE_BORDER, size=(64,64) )      
        top_info_sizer = wx.BoxSizer( wx.VERTICAL )
        
        name = wx.StaticText( top_info, -1, label="%s (%s)"%( appearance.getAttribute('name'), os.path.basename(appearance.getAttribute('xml'))) )
        top_info_sizer.Add( name, 0, wx.ALL, 5 )   
        
        top_sizer.Add( preview_img, 0, wx.ALL, 5 )
        top_sizer.Add( top_info_sizer, 0, wx.ALL|wx.EXPAND, 5 )
        top_info.SetSizer( top_sizer )
        
        sizer.Add( top_info, 0, wx.ALL, 0 )

        for param in appearance.contents:
            widget = self.addParameter( param )
            if widget:
                sizer.Add( widget, 0, wx.EXPAND|wx.TOP|wx.BOTTOM, 2 )
    
    def addParameter(self, parameter):
        result = None
        param_type = parameter.getAttribute('type')
        
        if param_type=='colour':
            result = ColourCtrl( self, parameter )
        elif param_type=='float':
            result = FloatCtrl( self, parameter )
        elif param_type=='file':
            result = StringCtrl( self, parameter )
        elif param_type=='string':
            result = StringCtrl( self, parameter )
        elif param_type=='bool':
            result = BoolCtrl( self, parameter )
        elif param_type=='point':
            result = PointCtrl( self, parameter )
        return result
        
