import os
import sys
import wx
import wx.xrc

from threading import Thread

######################################################################
# Library
######################################################################

ID_START = 1000
CtrlTable = {}

def getId():
    global ID_START
    ID_START += 1
    return ID_START

def registerCtrl(name,ctrl):
    global CtrlTable
    CtrlTable[name] = ctrl

def getCtrl(name):
    global CtrlTable
    if name in CtrlTable:
        return CtrlTable[name]
    else:
        return None

def encodeIcon(filename):
    from zlib import compress
    from base64 import b64encode
    with open(filename, "rb") as f:
        data = b64encode(compress(f.read()))
    return data
    
def decodeIcon(data):
    from base64 import b64decode
    from zlib import decompress
    image_data = decompress(b64decode(data))
    return image_data

def getBitmap(data):
    from io import BytesIO
    image_data = decodeIcon(data)
    stream = BytesIO(bytearray(image_data)) # just bytes() for py3
    image = wx.Image(stream, wx.BITMAP_TYPE_ANY) # wx.ImageFromStream for legacy wx
    bitmap = wx.Bitmap(image) # wx.BitmapFromImage for legacy wx
    return bitmap
    
######################################################################
# Layouts
######################################################################

class VBox():
    def __init__(self,orient=wx.VERTICAL,proportion=0):
        self.ctrl = wx.BoxSizer( orient )
    
    def add(self,child,proportion=0,expand=True,border=0,align=0):
        flags = align
        flags |= wx.EXPAND if expand == True else 0
        flags |= wx.ALL if border > 0 else 0            
        self.ctrl.Add( child, proportion, flags, border ) 
        
    def addSpacer(self,proportion=1):
        self.ctrl.Add( ( 0, 0), proportion, wx.EXPAND, 5 )
    
class HBox(VBox):
    def __init__(self,orient=wx.HORIZONTAL,proportion=0):
        super().__init__(orient,proportion)
        pass

######################################################################
# Controls
######################################################################

class Control():
    def __init__(self,name,expand=False,proportion=0,border=2):
        self.ctrl = None
        self.name = name
        self.expand = expand
        self.proportion = proportion    
        self.border=2

class Bitmap(Control):
    def __init__(self,name,filename=None,bitmap=None,expand=False,proportion=0):
        super().__init__(name,expand,proportion)
        self.bitmap = bitmap
        self.filename = filename
    def create(self,parent):
        flags = wx.ALIGN_CENTER
        if self.filename is not None:
            self.bitmap = wx.Bitmap( self.filename, wx.BITMAP_TYPE_ANY )
        self.ctrl = wx.StaticBitmap( parent, wx.ID_ANY, self.bitmap, wx.DefaultPosition, wx.DefaultSize, 0|flags )
        self.ctrl.Bind( wx.EVT_SIZE, self.onEvtBitmapSize )
        registerCtrl( self.name, self.ctrl )
    def onEvtBitmapSize(self,event):
        #print("onEvtBitmapSize()",event.GetSize()) #(width, height)
        event.Skip()

class Button(Control):
    def __init__(self,name,label="",handler=None,expand=False,proportion=0):
        super().__init__(name,expand,proportion)
        self.label = label
        self.handler = handler
    def create(self,parent):        
        id = getId()
        self.ctrl = wx.Button( parent, id, self.label, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.ctrl.Bind( wx.EVT_BUTTON, self.handler, id=id )
        registerCtrl( self.name, self.ctrl )
    
class Choice(Control):
    def __init__(self,name,select=0,choices=[],handler=None,expand=False,proportion=0):
        super().__init__(name,expand,proportion)
        self.select = select
        self.choices = choices
        self.handler = handler
    def create(self,parent):        
        id = getId()
        self.ctrl = wx.Choice( parent, id, wx.DefaultPosition,  wx.DefaultSize, self.choices, 0 )
        self.ctrl.SetSelection(self.select)
        self.ctrl.Bind( wx.EVT_CHOICE, self.handler, id=id )
        registerCtrl( self.name, self.ctrl )

class Combo(Control):
    def __init__(self,name,value="",choices=[],handler=None,expand=False,proportion=0):
        super().__init__(name,expand,proportion)
        self.value = value
        self.choices = choices
        self.handler = handler
    def create(self,parent):        
        id = getId()
        self.ctrl = wx.ComboBox( parent, id, self.value, wx.DefaultPosition, wx.DefaultSize, self.choices, 0 )
        self.ctrl.Bind( wx.EVT_COMBOBOX, self.handler, id=id )
        registerCtrl( self.name, self.ctrl )
         
class Label(Control):
    def __init__(self,name,text="",expand=False,proportion=0,multiline=False):
        super().__init__(name,proportion)
        self.text = text
        self.multiline = multiline
    def create(self,parent):
        flags = 0
        if self.multiline == True:
            flags |= wx.TE_MULTILINE
        self.ctrl = wx.StaticText( parent, wx.ID_ANY, self.text, wx.DefaultPosition, wx.DefaultSize, 0|flags )
        registerCtrl( self.name, self.ctrl )
    

class List(Control):
    def __init__(self,name,select=0,choices=[],handler=None,expand=False,proportion=0):
        super().__init__(name,expand,proportion)
        self.select = select
        self.choices = choices
        self.handler = handler
    def create(self,parent):        
        id = getId()
        self.ctrl = wx.ListBox( parent, id, wx.DefaultPosition,  wx.DefaultSize, self.choices, 0 )
        self.ctrl.SetSelection(self.select)
        self.ctrl.Bind( wx.EVT_CHOICE, self.handler, id=id )
        registerCtrl( self.name, self.ctrl )
    
class Text(Control):
    def __init__(self,name,text="",expand=False,proportion=0,multiline=False):
        super().__init__(name,expand,proportion)
        self.text = text
        self.multiline = multiline
        self.expand = True if multiline == True else False
    def create(self,parent):
        flags = 0
        if self.multiline == True:
            flags |= wx.TE_MULTILINE
        self.ctrl = wx.TextCtrl( parent, wx.ID_ANY, self.text, wx.DefaultPosition, wx.DefaultSize, 0|flags )
        registerCtrl( self.name, self.ctrl )

######################################################################
# Dialogs
######################################################################
            
def OpenFileDialog(defaultDir="",multiple=False,save=False):
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if save is False else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    style |= wx.FD_MULTIPLE if multiple is True else 0
    dlg = wx.FileDialog(None,defaultDir=defaultDir,style=style)
    dlg.ShowModal()
    if multiple == True:
        files = []
        for file in dlg.GetFilenames():
            files.append( os.path.join(dlg.GetDirectory(), file) )
        return files
    else:
        return os.path.join(dlg.GetDirectory(), dlg.GetFilename())
        
def SaveFileDialog(defaultDir=""):
    return OpenFileDialog(defaultDir=defaultDir, multiple=False, save=True)

def DirectoryDialog(defaultPath=""):
    dlg = wx.DirDialog(None,defaultPath=defaultPath)
    dlg.ShowModal()
    return dlg.GetPath()

def MessageBox(title,message):
    dlg = wx.MessageDialog(None, message, caption=title, style=wx.OK|wx.CENTER, pos=wx.DefaultPosition)    
    dlg.ShowModal()
    
def MessageYesNo(title,message):
    dlg = wx.MessageDialog(None, message, caption=title, style=wx.YES|wx.NO|wx.CENTER, pos=wx.DefaultPosition)     
    rv = dlg.ShowModal()
    if rv == wx.ID_OK or rv == wx.ID_YES:
        return True
    else: #wx.ID_CANCEL, wx.ID_NO 
        return False
    
def MessageYesNoCancel(title,message):
    dlg = wx.MessageDialog(None, message, caption=title, style=wx.YES|wx.NO|wx.CANCEL|wx.CENTER, pos=wx.DefaultPosition)     
    rv = dlg.ShowModal()
    if rv == wx.ID_OK or rv == wx.ID_YES:
        return True
    elif rv == wx.ID_NO:
        return False
    else: #wx.ID_CANCEL, 
        return None
    
######################################################################
# WxApp
######################################################################
    
class WxApp():
    def __init__( self, title, width=800, height=600 ):
        self.app = wx.PySimpleApp()
        self.frame = wx.Frame( parent=None, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( width,height ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.frame.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )  
        
    def run(self):
        self.frame.Show()
        self.app.MainLoop()
    
    def Show(self):
        self.frame.Show()
        
    def makeMenu(self, value):
        menu = wx.Menu()
        for k, v in value.items():
            if k[0] == '-':
                menu.AppendSeparator()
            else:
                if type(v) is dict:
                    submenu = self.makeMenu(v)
                    menu.AppendSubMenu(submenu, k)
                else:
                    if type(v) is list:
                        handler = v[0]
                        icon = v[1]
                    else: 
                        handler = v
                        icon = None
                    item = wx.MenuItem( menu, getId(), k, wx.EmptyString, wx.ITEM_NORMAL )
                    if icon is not None:
                        item.SetBitmap(getBitmap(icon))
                    if handler is None:
                        item.Enable( False )
                    else:
                        self.frame.Bind(wx.EVT_MENU, handler, item)
                    menu.Append(item)
        return menu
    
    def makeMenuBar(self, menu_def):
        self.menubar = wx.MenuBar(0)
        for key, value in menu_def.items():
            if type(value) is dict:
                menu = self.makeMenu(value)
                self.menubar.Append( menu, key )
        self.frame.SetMenuBar(self.menubar)
            
    def makeStatusBar(self, status_def):
        self.statusbar = self.frame.CreateStatusBar( len(status_def), wx.STB_SIZEGRIP, wx.ID_ANY )
        widths = []
        for i in range(len(status_def)):
            self.statusbar.SetStatusText( status_def[i][0], i)
            widths.append(status_def[i][1])
        self.statusbar.SetStatusWidths(widths)
            
    def makeToolBar(self, tool_def):  #icon, text, handler
        '''
        AddLabelTool(self, id, label, bitmap, bmpDisabled=wx.NullBitmap, kind=wx.ITEM_NORMAL, shortHelp="", longHelp="", clientData=None)
        '''
        flags = wx.TB_FLAT|wx.TB_HORIZONTAL
        if len(tool_def[0]) == 3:
            flags |= wx.TB_TEXT
        self.toolbar = self.frame.CreateToolBar( flags, wx.ID_ANY )
        for value in tool_def:
            if value[0] is None:
                self.toolbar.AddSeparator()
            else:
                text = handler = None
                if len(value) >= 2:
                    handler = value[1]
                if len(value) == 3:
                    text = value[2]
                icon = getBitmap(value[0])
                id = getId()
                if flags & wx.TB_TEXT:
                    tool = self.toolbar.AddLabelTool( id, text, icon, wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
                else:
                    tool = self.toolbar.AddSimpleTool( id, icon, wx.EmptyString, wx.EmptyString, None )
                if handler is None:
                    tool.Enable( False )               
                else:    
                    self.toolbar.Bind( wx.EVT_TOOL, handler, id = id )
        self.toolbar.Realize()

    def makeBodyLayout(self,body_def,parent):
        vbox = VBox()
        for row in body_def:
            hbox = HBox()
            prop = 0
            for col in row:
                if type(col) is bool:
                    prop = 1 if col is True else 0
                elif type(col) is int:
                    prop = col
                elif col is None:
                    hbox.addSpacer(proportion=1)
                else:
                    col.create(parent)
                    hbox.add(col.ctrl,proportion=col.proportion,expand=col.expand,border=col.border,align=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
            vbox.add(hbox.ctrl,proportion=prop,expand=True,border=2,align=wx.ALIGN_CENTER_HORIZONTAL)
        return vbox

    def makeBody(self,body_def):
        self.sizer = wx.BoxSizer()
        self.panel = wx.Panel( self.frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        body = self.makeBodyLayout(body_def,self.panel)
        self.panel.SetSizer( body.ctrl )
        self.panel.Layout()      
        self.sizer.Add( self.panel, 1, wx.EXPAND, 0 )
        self.sizer.Fit( self.panel )
        self.frame.SetSizer( self.sizer )
        self.frame.Layout()          
            
    def makeBodyByChild(self,child):
        self.sizer = wx.BoxSizer()
        self.panel = wx.Panel( self.frame, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        self.panel.SetSizer( child )
        self.panel.Layout()      
        self.sizer.Add( self.panel, 1, wx.EXPAND, 0 )
        self.sizer.Fit( self.panel )
        self.frame.SetSizer( self.sizer )
        self.frame.Layout()          

    def makeLayout(self,layout):
        if 'menu' in layout:
            self.makeMenuBar(layout['menu'])
        if 'tool' in layout:
            self.makeToolBar(layout['tool'])
        if 'status' in layout:
            self.makeStatusBar(layout['status'])
        if 'body' in layout:
            self.makeBody(layout['body'])
        
    
