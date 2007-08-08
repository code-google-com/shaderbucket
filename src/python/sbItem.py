#!/usr/bin/env python
# encoding: utf-8
        
#==============================================================================

# Base class for items
class Item:
    def __init__(self):
        self.attributes = {}
        
    def getAttribute(self,attr):
        if self.attributes.has_key(attr):
            return self.attributes[attr]
        else:
            return "Unknown"
            
    def hasAttribute(self,attr):
        if self.attributes.has_key(attr):
            return True
        return False
        
    def setAttribute(self,attr,value):
        self.attributes[attr] = value
        
    def dump(self):    
        for attr in self.attributes.iteritems():
            print attr[0]+": ",attr[1]
