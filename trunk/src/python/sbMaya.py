import maya.cmds as cmds
from shaderBucket import ShaderBucket
from sbPalette import Palette, Appearance
from sbGui import App
import thread
import time

# have one global bucket instance
__shader_bucket__ = None

def shaderBucket():
    return sbMaya()    

class sbMaya:
    __singleton_shared_state__ = {}
    
    def __init__(self):
        self.__dict__ = self.__singleton_shared_state__
    
        # initialise!
        if not self.__dict__.has_key('bucket'):
            self.bucket = ShaderBucket()
            self.gui = None
    
            '''
            # looks
            looks = cmds.sets( name="Looks", empty=True )
            
            # attributes
            geo_attrs = cmds.sets( name="Geometry", empty=True )
            light_attrs = cmds.sets( name="Lights", empty=True )
            attrs = cmds.sets( geo_attrs, light_attrs, name="Attributes" )

            # top-level set
            sb_set = cmds.sets( looks, attrs, name="ShaderBucket" )
            '''
        
            # create a blind data node    
            #sb = cmds.createNode( 'oldBlindDataBase', n='shaderBucket' )
            
            # our shaderbucket instance
            #__shader_bucket__.root.addPalette( Palette(__shader_bucket__, "/home/danb/dev/projects/shaderbucket/tests/palettes/palette.xml" ) )
    
    def show(self):
        # init our gui
        if not self.gui:
            thread.start_new_thread(self.goGui, ())
        else:
            # should raise the window
            pass
        
    def lock(self):
        self.bucket.mutex.acquire()
        
    def unlock(self):
        self.bucket.mutex.release()
          
    def msg(self, msg):
        print( '[ShaderBucket] '+msg )
        
    def goGui(self):
        self.gui = App(bucket=self.bucket, redirect=False)
        self.gui.MainLoop()
        self.gui = None
        
    def removeFromScene(self):
        result = cmds.confirmDialog( title='Remove ShaderBucket?', message='This will remove all ShaderBucket stuff from your scene.\nAre you sure?!', button=['Yes','No'], defaultButton='No', cancelButton='No', dismissString='No' )
        if result=='Yes':
            cmds.delete( 'ShaderBucket' )
            self.msg( "Removed!" )

    def initFromScene(self):
        shaders = cmds.ls(type="delightShader", long=True)
        if shaders:
            result = cmds.confirmDialog( title='Init ShaderBucket?', message='Found '+str(len(shaders))+' shaders - import into ShaderBucket?', button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
            if result=='Yes':            
                self.lock() # lock our shader bucket
                for shd in shaders:
                    self.msg( "Importing "+shd )                
                    
                    # create an appearance               
                    app = Appearance()
                    app.setAttribute( "name", shd )
                    app.setAttribute( "file", cmds.getAttr( shd+".shaderFile" ) )
                    
                    # add it to our palette
                    self.bucket.root.addAppearance( app )
                 
                self.unlock() # unlock our shader bucket       

            
    def sync():
        print "syncing maya"
    
        # traverse bucket looking for shaders

        # if shader doesn't exist create it
        self.addAppearance( app )

        # if shader does exist update it
        self.updateAppearance( app )


        scene_shaders = self.getSceneShaders()
        for shd in scene_shaders:
            # if shd doesn't exist in bucket then delete it
            self.deleteAppearance( shd )        
         
'''
    def createFromScene():
        print "creates a shader bucket from the current scene"
        scene_shaders = self.getSceneShaders()
        for shd in scene_shaders:
            app = self.createAppearanceFromMaya( shd )            

 

    def addAppearance( app ):
        pass
        
    def updateAppearance( app ):
        pass
        
    def deleteAppearance( app ):
        pass
        
    def addPalette( palette ):
        self.initBucket()
'''
