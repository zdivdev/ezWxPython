import os
import sys
import time
import wx
import wx.adv

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

def getWxCtrl(name):
    global CtrlTable
    if name in CtrlTable:
        return CtrlTable[name].ctrl
    else:
        return None

def getWxTimer(name):
    return getCtrl(name)

def getWxAppCtrl():
    global CtrlTable
    name = 'WxApp'
    if name in CtrlTable:
        return CtrlTable[name].ctrl
    else:
        return None

def clearValue(key):
    ctrl = getCtrl(key)
    if ctrl is not None:
        return ctrl.clearValue() 
    else:
        return None

def getLabel(key):
    ctrl = getCtrl(key)
    if ctrl is not None:
        return ctrl.getLabel() 
    else:
        return None

def setLabel(key,value):
    ctrl = getCtrl(key)
    if ctrl is not None:
        ctrl.setLabel(value) 

def getValue(key):
    ctrl = getCtrl(key)
    if ctrl is not None:
        return ctrl.getValue() 
    else:
        return None

def setValue(key,value):
    ctrl = getCtrl(key)
    if ctrl is not None:
        ctrl.setValue(value) 

def appendValue(key,value):
    ctrl = getCtrl(key)
    if ctrl is not None:
        return ctrl.appendValue(value) 
    else:
        return None

def removeValue(key,value):
    ctrl = getCtrl(key)
    if ctrl is not None:
        return ctrl.removeValue(value) 
    else:
        return None
 
def setFgColor(key,color):
    ctrl = getCtrl(key)
    if ctrl is not None:
        ctrl.setFgColor(color)

def setBgColor(key,color):
    ctrl = getCtrl(key)
    if ctrl is not None:
        ctrl.setBgColor(color)

def castValue(key,value):
    ctrl = getCtrl(key)
    if ctrl is not None:
        return ctrl.castValue(value)
    else:
        return value
        
def encodeIcon(filename):
    from zlib import compress
    from base64 import b64encode
    with open(filename, "rb") as f:
        data = b64encode(compress(f.read()))
    return data

def encodeIconToStr(filename):
    icon = encodeIcon(filename)
    return icon.decode('utf-8')
    
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

def getMenuBitmap(data, size=(16,16)):
    if data[0] == b'w'[0] and data[1] == b'x'[0]:
        return wx.ArtProvider.GetBitmap(data, wx.ART_MENU, size)
    else:
        return getBitmap(data)

def getToolbarBitmap(data, size=(32,32)):
    if data[0] == b'w'[0] and data[1] == b'x'[0]:
        return wx.ArtProvider.GetBitmap(data, wx.ART_TOOLBAR, size)
    else:
        return getBitmap(data)

def getButtonBitmap(data, size=(16,16)):
    if data[0] == b'w'[0] and data[1] == b'x'[0]:
        return wx.ArtProvider.GetBitmap(data, wx.ART_BUTTON, size)
    else:
        return getBitmap(data)

def threadHandle(handler,start=False,key=None,daemon=True,args=()):
    #from threading import *
    import threading
    thread = threading.Thread(target=handler,args=args)
    thread.daemon = daemon
    if key is not None:
        registerCtrl(key,thread)
    if start is True:
        thread.start()

def threadStart(key):
    thread = getCtrl(key)
    if thread is not None:
        thread.start()

def threadJoin(key):
    thread = getCtrl(key)
    if thread is not None:
        thread.join()

def callAfter(handler,*args):
    wx.CallAfter(handler,*args)

def doBusyJob(job,args=(),message="Please wait ...",parent=None,bgColor=None,fgColor=None):
    import wx.lib.busy
    with wx.lib.busy.BusyInfo(message,parent,bgColor,fgColor):
        job(args)

######################################################################
# Layouts
######################################################################

class VBox():
    def __init__(self,parent=None,label=None,orient=wx.VERTICAL,proportion=0):
        if label is None:
            self.ctrl = wx.BoxSizer( orient )
        else:
            self.ctrl = wx.StaticBoxSizer( wx.StaticBox( parent, wx.ID_ANY, label ), orient )

    def add(self,child,proportion=0,expand=True,border=5,align=0):
        flags = align
        flags |= wx.EXPAND if expand == True else 0
        flags |= wx.ALL if border > 0 else 0
        self.ctrl.Add( child, proportion, flags, border )

    def addSpacer(self,proportion=1):
        self.ctrl.Add( ( 0, 0), proportion, wx.EXPAND|wx.ALL, 5 )

class HBox(VBox):
    def __init__(self,parent=None,label=None,orient=wx.HORIZONTAL,proportion=0):
        super().__init__(parent,label,orient,proportion)

class Control():
    def __init__(self,key=None,expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,tooltip=None):
        self.ctrl = None
        self.key = key
        self.tooltip = tooltip
        self.expand = expand
        self.proportion = proportion
        self.border = border
        self.size = size
        self.pos = pos
    def getLabel(self): #button
        return self.ctrl.GetLabel()
    def setLabel(self,value): #button
        self.ctrl.SetLabel(value)
    def getValue(self):
        return self.ctrl.GetValue()
    def setValue(self,value):
        self.ctrl.SetValue(value)
    def clearValue(self):
        self.ctrl.SetValue('')
    def appendValue(self,value):
        self.ctrl.Append(value)
    def deleteValue(self,value):
        if type(value) is str:
            n = self.ctrl.FindString(value)
            if n != wx.NOT_FOUND:
                self.ctrl.Delete(n)
        elif type(value) is int:
                self.ctrl.Delete(value)
    def removeValue(self,value):
        self.deleteValue(value)
    def setFgColor(self,value):
        self.ctrl.SetForegroundColour(value)
        self.ctrl.Refresh()
    def setBgColor(self,value):
        self.ctrl.SetBackgroundColour(value)
        self.ctrl.Refresh()
    def castValue(self,value):
        return value
        
######################################################################
# Containers
######################################################################

def wrapSizer(widget):
    sizer = wx.BoxSizer()
    sizer.Add( widget, 1, wx.EXPAND, 0 )
    sizer.Fit( widget )
    return sizer

def dictValue(new_value,old_value):
    try:
        if new_value is not None:
            return new_value
    except:
        pass
    return old_value

def makeLayout(layout,parent):
    if type(layout) is not list:
        return VBox();
    vbox_label = None;
    if type(layout[0]) is str:
        vbox_label = layout[0]
        layout.remove(layout[0])
    vbox = VBox(parent,vbox_label)
    for row in layout:
        hbox_label = None;
        if type(row[0]) is str:
            hbox_label = row[0]
            row.remove(row[0])
        hbox = HBox(parent,hbox_label)        
        prop = 0
        expand = True
        border = 2
        if type(row) is list:
            for col in row:
                if type(col) is dict:
                    prop = dictValue( col.get('proportion'), prop )
                    expand = dictValue( col.get('expand'), expand )
                    border = dictValue( col.get('border'), border )
                elif col is None:
                    hbox.addSpacer(proportion=1)
                else:
                    col.create(parent)
                    hbox.add(col.ctrl,proportion=col.proportion,expand=col.expand,border=col.border,align=wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        else: #compound control
            row.create(parent)
        vbox.add(hbox.ctrl,proportion=prop,expand=expand,border=border,align=wx.ALIGN_LEFT|wx.ALL)
    return vbox

class Book(Control):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,border=2,
                size=wx.DefaultSize,pos=wx.DefaultPosition,style='note',key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.layouts = layouts
        self.style = style
        self.simplePages = []
        if create is True and parent is not None:
            self.create(parent)
    def create(self,parent):
        if self.style == 'note':
            self.ctrl = wx.Notebook( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        elif self.style == 'choice':
            self.ctrl = wx.Choicebook( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        else: #simple
            self.ctrl = wx.Simplebook( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.titles = []
        self.panels = []
        for layout in self.layouts:
            if type(layout) == str:
                self.titles.append(layout)
            elif type(layout) == list:
                self.panels.append(Panel(layout, self.ctrl, create=True))
        for i in range(len(self.panels)):
            if self.style == 'simple':
                self.simplePages.append(self.panels[i].ctrl);
            else:
                self.ctrl.AddPage( self.panels[i].ctrl, self.titles[i], False )              
        if self.style == 'simple':
            self.setPage(0)
        if self.key is not None:
            registerCtrl( self.key, self )            
    def setEffect(self,effect=None):
        if self.style == 'simple':
            if effect == 'roll_to_left':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_ROLL_TO_LEFT)
            elif effect == 'roll_to_right':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_ROLL_TO_RIGHT)
            elif effect == 'roll_to_top':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_ROLL_TO_TOP)
            elif effect == 'roll_to_bottom':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_ROLL_TO_BOTTOM)
            elif effect == 'slide_to_left':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_SLIDE_TO_LEFT)
            elif effect == 'slide_to_right':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_SLIDE_TO_RIGHT)
            elif effect == 'slide_to_top':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_SLIDE_TO_TOP)
            elif effect == 'slide_to_bottom':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_SLIDE_TO_BOTTOM)
            elif effect == 'blend':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_BLEND)
            elif effect == 'expand':
                self.ctrl.SetEffect(wx.SHOW_EFFECT_EXPAND)
            else:
                self.ctrl.SetEffect(wx.SHOW_EFFECT_NONE)                
    def setPage(self,index):
        if self.style == 'simple':
            if index >= len(self.simplePages):
                index = 0
            self.ctrl.ShowNewPage(self.simplePages[index])

class Notebook(Book):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent,create,horizontal,expand,proportion,style='note',size=size,pos=pos,key=key)

class Choicebook(Book):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent,create,horizontal,expand,proportion,style='choice',size=size,pos=pos,key=key)

class Simplebook(Book):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent,create,horizontal,expand,proportion,style='simple',size=size,pos=pos,key=key)

class Panel(Control):
    import wx.lib.scrolledpanel
    def __init__(self,layout,parent=None,create=False,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,label="",style=None,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.layout = layout
        self.label = label
        self.style = style
        if create is True and parent is not None:
            self.create(parent)
    def create(self,parent):
        if self.style is None:
            self.ctrl = wx.Panel( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
            self.sizer = makeLayout(self.layout,self.ctrl)
            self.ctrl.SetSizer( self.sizer.ctrl )
            self.ctrl.Layout()
        elif self.style == 'scroll':
            self.ctrl = wx.lib.scrolledpanel.ScrolledPanel( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.HSCROLL|wx.VSCROLL|wx.TAB_TRAVERSAL )
            self.sizer = makeLayout(self.layout,self.ctrl)
            self.ctrl.SetSizer( self.sizer.ctrl )
            #begin for scrolledwindow
            self.ctrl.SetAutoLayout(1)
            #self.ctrl.SetupScrolling(scroll_y = True)
            width = self.ctrl.GetBestSize().width
            height = self.ctrl.GetBestSize().height
            self.ctrl.SetSize((width, height))
            self.ctrl.SetScrollbars( 1, 1, 1, 1 )
            self.sizer.ctrl.SetSizeHints(self.ctrl)
            #end
            self.ctrl.Layout()
        elif self.style == 'collapsible':
            self.ctrl = wx.CollapsiblePane( parent, wx.ID_ANY, self.label, wx.DefaultPosition, wx.DefaultSize, wx.CP_DEFAULT_STYLE|wx.CP_NO_TLW_RESIZE )
            pane = self.ctrl.GetPane()
            self.sizer = makeLayout(self.layout,pane)
            pane.SetSizer( self.sizer.ctrl )
            self.ctrl.Expand()
            self.sizer.ctrl.SetSizeHints(pane)
            pane.Layout()

class ScrolledPanel(Panel):
    def __init__(self,layout,parent=None,create=False,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,label="",key=None):
        super().__init__(layout,parent=parent,create=create,expand=expand,proportion=proportion,size=size,pos=pos,label=label,style='scroll',key=key)

class CollapsiblePanel(Panel):
    def __init__(self,layout,parent=None,create=False,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,label="",key=None):
        super().__init__(layout,parent=parent,create=create,expand=expand,proportion=proportion,size=size,pos=pos,label=label,style='collapsible',key=key)

##class Scroll(Control): #TODO: Change ScrolledWindow -> ScrolledPane
##    def __init__(self,layout,parent=None,create=False,horizontal=True,expand=False,proportion=0,key=None):
##        super().__init__(key,expand,proportion)
##        self.layout = layout
##        if create is True and parent is not None:
##            self.create(parent)
##    def create(self,parent):
##        self.ctrl = wx.ScrolledWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,  wx.HSCROLL|wx.VSCROLL  )
##        #self.ctrl.EnableScrolling(True,True)
##        #self.ctrl.SetAutoLayout(1)
##        #self.ctrl.ShowScrollbars( True, True )
##        self.sizer = makeLayout(self.layout,self.ctrl)
##        self.ctrl.SetSizer( self.sizer.ctrl )
##        width = self.ctrl.GetBestSize().width
##        height = self.ctrl.GetBestSize().height
##        self.ctrl.SetSize((width, height))
##        self.ctrl.SetScrollbars( 1, 1, 1, 1 )
##        #self.ctrl.SetScrollRate( 5, 5 )
##        #panel = Panel(self.layout, self.ctrl, create=True)
##        #self.ctrl.SetSizer( wrapSizer(panel.ctrl) )
##        self.ctrl.Layout()

class Spliter(Control):
    def __init__(self,layouts,parent=None,create=False,style='vertical',expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.layouts = layouts #left(top),right(bottom)
        self.style = style
        if create is True and parent is not None:
            self.create(parent)
    def create(self,parent):
        self.ctrl = wx.SplitterWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
        self.sashpos = 0
        self.panels = []
        for layout in self.layouts:
            if type(layout) is int:
                self.sashpos = layout
            else:
                self.panels.append(Panel(layout, self.ctrl, create=True))
        if self.style == 'vertical':
            self.ctrl.SplitVertically( self.panels[0].ctrl, self.panels[1].ctrl, self.sashpos )
        else:
            self.ctrl.SplitHorizontally( self.panels[0].ctrl, self.panels[1].ctrl, self.sashpos )

class VerticalSpliter(Spliter):
    def __init__(self,layouts,parent=None,create=False,expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent=parent,create=create,style='vertical',expand=expand,proportion=proportion,border=border,size=size,pos=pos,key=key)

class HorizontalSpliter(Spliter):
    def __init__(self,layouts,parent=None,create=False,expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent=parent,create=create,style='horizontal',expand=expand,proportion=proportion,border=border,size=size,pos=pos,key=key)

class MultiSpliter(Control):
    import wx.lib.splitter
    def __init__(self,layouts,parent=None,create=False,style='vertical',expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.layouts = layouts #left(top),right(bottom)
        self.style = style
        if create is True and parent is not None:
            self.create(parent)
    def create(self,parent):
        self.ctrl = wx.lib.splitter.MultiSplitterWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.sashpos = []
        self.panels = []
        for layout in self.layouts:
            if type(layout) is int:
                self.sashpos.append(layout)
            else:
                self.panels.append(Panel(layout, self.ctrl, create=True))
        if self.style == 'vertical': # reverted concept compared with Splitter
            self.ctrl.SetOrientation(wx.HORIZONTAL)
        else:
            self.ctrl.SetOrientation(wx.VERTICAL)
        for i in range(len(self.panels)):
            self.ctrl.AppendWindow(self.panels[i].ctrl, self.sashpos[i])

class VerticalMultiSpliter(MultiSpliter):
    def __init__(self,layouts,parent=None,create=False,expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent=parent,create=create,style='vertical',expand=expand,proportion=proportion,border=border,size=size,pos=pos,key=key)

class HorizontalMultiSpliter(MultiSpliter):
    def __init__(self,layouts,parent=None,create=False,expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(layouts,parent=parent,create=create,style='horizontal',expand=expand,proportion=proportion,border=border,size=size,pos=pos,key=key)


######################################################################
# Controls
######################################################################

class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
    def OnDropFiles(self, x, y, filenames):
        self.window.drop_handle(filenames)
        return True

class Bitmap(Control):
    def __init__(self,filename=None,bitmap=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos,tooltip=tooltip)
        self.bitmap = bitmap
        self.filename = filename
    def create(self,parent):
        flags = wx.ALIGN_CENTER
        if self.filename is not None:
            self.bitmap = wx.Bitmap( self.filename, wx.BITMAP_TYPE_ANY )
        self.ctrl = wx.StaticBitmap( parent, wx.ID_ANY, self.bitmap, self.pos, self.size, 0|flags )
        self.ctrl.Bind( wx.EVT_SIZE, self.onEvtBitmapSize )
        if self.key is not None:
            registerCtrl( self.key, self )
    def onEvtBitmapSize(self,event):
        #print("onEvtBitmapSize()",event.GetSize()) #(width, height)
        event.Skip()
    #TODO: getValue,setValue check

class Button(Control):
    def __init__(self,label="",handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos,tooltip=tooltip)
        self.label = label
        self.handler = handler
    def create(self,parent):
        id = getId()
        if type(self.label) is str:
            self.ctrl = wx.Button( parent, id, self.label, self.pos, self.size, 0 )
        else:
            self.ctrl = wx.BitmapButton( parent, id, getButtonBitmap(self.label), self.pos, self.size, 0 )
        if self.handler:
            self.ctrl.Bind( wx.EVT_BUTTON, self.handler, id=id )
        if self.tooltip:
            self.ctrl.SetToolTip(wx.ToolTip(self.tooltip))
        if self.key:
            registerCtrl( self.key, self )
    def getValue(self):
        pass
    def setValue(self,value):
        pass
    def clearValue(self):
        pass
    def appendValue(self,value):
        pass
    def removeValue(self,value):
        pass  

class Calendar(Control):
    def __init__(self,handler=None,date=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.date = date
        self.handler = handler
    def create(self,parent):
        self.ctrl = wx.adv.CalendarCtrl( parent, wx.ID_ANY, wx.DefaultDateTime, self.pos, self.size, wx.adv.TP_DEFAULT )
        self.ctrl.Bind( wx.adv.EVT_CALENDAR, self.handler ) #double click
        self.ctrl.Bind( wx.adv.EVT_CALENDAR_SEL_CHANGED, self.handler )
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class CheckButton(Control):
    def __init__(self,label="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos,tooltip=tooltip)
        self.label = label
        self.handler = handler
        self.value = value
    def create(self,parent):
        id = getId()
        self.ctrl = wx.CheckBox( parent, id, self.label, self.pos, self.size, 0 )
        self.ctrl.Bind( wx.EVT_CHECKBOX, self.handler, id=id )
        if self.value is not None:
            self.setValue(self.value)
        if self.tooltip is not None:
            self.ctrl.SetToolTip(wx.ToolTip(self.tooltip))
        if self.key is not None:
            registerCtrl( self.key, self )
    def clearValue(self):
        pass
    def appendValue(self,value):
        pass
    def removeValue(self,value):
        pass  
    def castValue(self,value):
        return bool(value)
        
class Check(CheckButton):
    def __init__(self,label="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None):
        super().__init__(label,value,handler,expand,proportion,border,size,pos,key,tooltip)

class Choice(Control):
    def __init__(self,choices=[],select=0,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.choices = choices
        self.select = select
        self.handler = handler
    def create(self,parent):
        id = getId()
        self.ctrl = wx.Choice( parent, id, self.pos, self.size, self.choices, 0 )
        self.ctrl.SetSelection(self.select)
        self.ctrl.Bind( wx.EVT_CHOICE, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )
    def getValue(self,):
        return self.ctrl.GetString(self.ctrl.GetCurrentSelection())
    def setValue(self,value):
        n = self.ctrl.FindString(value)
        if n != wx.NOT_FOUND:
            self.ctrl.SetSelection(n)

class Clock(Control):
    import wx.lib.analogclock
    def __init__(self,handler=None,date=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.date = date
        self.handler = handler
    def create(self,parent):
        self.ctrl = wx.lib.analogclock.analogclock.AnalogClock( parent, wx.ID_ANY, self.pos, self.size, wx.NO_BORDER)
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Combo(Control):
    def __init__(self,choices=[],value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.choices = choices
        self.value = value
        self.handler = handler
    def create(self,parent):
        id = getId()
        if self.value is None:
            self.value = self.choices[0]
        self.ctrl = wx.ComboBox( parent, id, self.value, self.pos, self.size, self.choices, 0 )
        #self.ctrl.SetValue(self.value)
        self.ctrl.Bind( wx.EVT_COMBOBOX, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )

class Date(Control):
    def __init__(self,date=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.date = date
    def create(self,parent):
        self.ctrl = wx.adv.DatePickerCtrl( parent, wx.ID_ANY, wx.DefaultDateTime, self.pos, self.size, wx.adv.TP_DEFAULT )
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Gauge(Control): #842
    def __init__(self,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
    def create(self,parent):
        self.ctrl = wx.Gauge(parent=parent,pos=self.pos,size=self.size)
        if self.key is not None:
            registerCtrl( self.key, self )
    def setMaxValue(self,maxValue):
        self.ctrl.SetRange(maxValue)
    def update(self,percent):
        wx.CallAfter(self.updateAfter, percent)
    def updateAfter(self,percent):
        self.ctrl.SetValue(percent)
    def pulse(self):
        wx.CallAfter(self.pulseAfter)
    def pulseAfter(self):
        self.ctrl.Pulse()
    #TODO: getValue,setValue check

class Label(Control):
    def __init__(self,text="",expand=False,proportion=0,border=2,multiline=False,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None,align='center'):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos,tooltip=tooltip)
        self.text = text
        self.multiline = multiline
        self.align = align
    def create(self,parent):
        flags = wx.ALIGN_CENTER 
        if self.align == 'left': flags = wx.ALIGN_LEFT
        if self.align == 'right': flags = wx.ALIGN_RIGHT
        flags |= wx.ALIGN_CENTER_VERTICAL
        if self.multiline == True: flags |= wx.TE_MULTILINE
        self.ctrl = wx.StaticText( parent, wx.ID_ANY, self.text, self.pos, self.size, 0|flags )
        if self.tooltip is not None:
            self.ctrl.SetToolTip(wx.ToolTip(self.tooltip))
        if self.key is not None:
            registerCtrl( self.key, self )
    def getValue(self):
        return self.ctrl.GetLabel()
    def setValue(self,item):
        self.ctrl.SetLabel(item)
    def clearValue(self):
        pass
    def appendValue(self,value):
        pass
    def removeValue(self,value):
        pass

class LedNumber(Control):
    import wx.lib.gizmos.ledctrl
    def __init__(self,text="",expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.text = text
    def create(self,parent):
        flags = wx.lib.gizmos.ledctrl.LED_ALIGN_LEFT|wx.lib.gizmos.ledctrl.LED_DRAW_FADED
        self.ctrl = wx.lib.gizmos.ledctrl.LEDNumberCtrl( parent, wx.ID_ANY, self.pos, self.size, flags )
        self.ctrl.SetValue(self.text)
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Line(Control):
    def __init__(self,text="",expand=False,proportion=0,border=2,style="horizontal",
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.style = style
    def create(self,parent):
        flags = wx.LI_HORIZONTAL if self.style == "horizontal" else wx.LI_VERTICAL
        self.ctrl = wx.StaticLine( parent, wx.ID_ANY, self.pos, self.size, 0|flags )
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Link(Control):
    def __init__(self,text="",url="",expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos,tooltip=tooltip)
        self.text = text
        self.url = url
    def create(self,parent):
        self.ctrl = wx.adv.HyperlinkCtrl( parent, wx.ID_ANY, self.text, self.url, self.pos, self.size)
        if self.tooltip is not None:
            self.ctrl.SetToolTip(wx.ToolTip(self.tooltip))
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class List(Control):
    def __init__(self,choices=[],select=0,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,check=False,label="",style=None,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.choices = choices
        self.select = select
        self.handler = handler
        self.check = check
        self.label = label
        self.style = style
    def create(self,parent):
        import sys
        id = getId()
        if self.style is None:
            if self.check is True:
                self.ctrl = wx.CheckListBox( parent, id, self.pos, self.size, self.choices, 0 )
            else:
                self.ctrl = wx.ListBox( parent, id, self.pos, self.size, self.choices, 0 )
            if self.select < len(self.choices):
                self.ctrl.SetSelection(self.select)
            self.ctrl.SetDropTarget(FileDrop(self))
            self.ctrl.Bind( wx.EVT_LISTBOX, self.handler, id=id )
        elif self.style == 'multicol':
            self.ctrl = wx.ListCtrl(parent, id, style = wx.LC_REPORT)
            widths = []
            if len(self.choices) > 1:
                aligns = (wx.LIST_FORMAT_LEFT, wx.LIST_FORMAT_CENTER, wx.LIST_FORMAT_RIGHT)
                cols = len(self.choices[0])
                for col in range(cols):
                    label = self.choices[0][col][0]
                    width = self.choices[0][col][1]
                    align = aligns[self.choices[0][col][2]+1]
                    self.ctrl.AppendColumn(label, align, width)
                    #self.ctrl.InsertColumn(col, label, align, width)
                for row in range(1,len(self.choices)):
                    self.ctrl.Append(self.choices[row])
        elif self.style == 'edit':
            self.ctrl = wx.adv.EditableListBox( parent, id, self.label, self.pos, self.size, 0 )
            #TODO:
        if self.key is not None:
            registerCtrl( self.key, self )
    def drop_handle(self,filenames):
        for filename in filenames:
            self.ctrl.Append(filename)
    def getValue(self,):
        return self.ctrl.GetString(self.ctrl.GetSelection())
    def setValue(self,item):
        n = self.ctrl.FindString(item)
        if n != wx.NOT_FOUND:
            self.ctrl.SetSelection(n)

class Picker(Control):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.style = style
        self.value = value
        self.handler = handler
    def create(self,parent):
        id = getId()
        if self.style == 'dir': #value: path str
            self.value = "" if self.value is None else self.value
            self.ctrl = wx.DirPickerCtrl( parent, id, self.value, pos=self.pos, size=self.size, style=wx.DIRP_DEFAULT_STYLE )
            self.ctrl.Bind( wx.EVT_DIRPICKER_CHANGED, self.handler, id=id )
        elif self.style == 'file':
            self.value = "" if self.value is None else self.value
            self.ctrl = wx.FilePickerCtrl( parent, id, self.value, pos=self.pos, size=self.size, style=wx.FLP_DEFAULT_STYLE )
            self.ctrl.Bind( wx.EVT_FILEPICKER_CHANGED, self.handler, id=id )
        elif self.style == 'color':
            self.value = wx.BLACK if self.value is None else self.value
            self.ctrl = wx.ColourPickerCtrl( parent, id, self.value, pos=self.pos, size=self.size, style=wx.CLRP_DEFAULT_STYLE )
            self.ctrl.Bind( wx.EVT_COLOURPICKER_CHANGED, self.handler, id=id )
        elif self.style == 'font':
            self.value = wx.NullFont if self.value is None else self.value
            self.ctrl = wx.FontPickerCtrl( parent, id, self.value, pos=self.pos, size=self.size, style=wx.FNTP_DEFAULT_STYLE )
            self.ctrl.Bind( wx.EVT_FONTPICKER_CHANGED, self.handler, id=id )
        elif self.style == 'date':
            self.value = wx.DefaultDateTime if self.value is None else self.value
            self.ctrl = wx.adv.DatePickerCtrl( parent, id, self.value, pos=self.pos, size=self.size, style=wx.adv.TP_DEFAULT )
            self.ctrl.Bind( wx.adv.EVT_DATE_CHANGED, self.handler, id=id )
        elif self.style == 'time':
            self.value = wx.DefaultDateTime if self.value is None else self.value
            self.ctrl = wx.adv.TimePickerCtrl( parent, id, self.value, pos=self.pos, size=self.size, style=wx.adv.TP_DEFAULT )
            self.ctrl.Bind( wx.adv.EVT_TIME_CHANGED, self.handler, id=id )
        else: #TODO: throw exception
            pass
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class DirPicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('dir',value,handler,expand,proportion,border,size,pos,key)

class FilePicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('file',value,handler,expand,proportion,border,size,pos,key)

class ColorPicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('color',value,handler,expand,proportion,border,size,pos,key)

class FontPicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('font',value,handler,expand,proportion,border,size,pos,key)

class DatePicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('date',value,handler,expand,proportion,border,size,pos,key)

class TimePicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('time',value,handler,expand,proportion,border,size,pos,key)

class Progress(Control):
    import wx.lib.progressindicator as pi
    def __init__(self,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
    def create(self,parent):
        self.ctrl = wx.lib.progressindicator.ProgressIndicator(parent=parent,pos=self.pos,size=self.size)
        if self.key is not None:
            registerCtrl( self.key, self )
    def setMaxValue(self,maxValue):
        self.ctrl.SetRange(maxValue)
    def update(self,percent):
        wx.CallAfter(self.callAfter, percent)
    def callAfter(self,percent):
        self.ctrl.SetValue(percent)
    #TODO: getValue,setValue check

class Radio(Control):
    def __init__(self,label="",choices=[],value="",handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,style='row',key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.label = label
        self.choices = choices
        self.value = value
        self.handler = handler
        self.style = wx.RA_SPECIFY_ROWS if style == 'row' else wx.RA_SPECIFY_COLS
    def create(self,parent):
        id = getId()
        self.ctrl = wx.RadioBox( parent, id, self.label, self.pos, self.size, self.choices, 0, self.style )
        self.ctrl.Bind( wx.EVT_RADIOBOX, self.handler, id=id )
        for i in range(len(self.choices)):
            if self.value == self.choices[i]:
                self.ctrl.SetSelection(i)
                break
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Slider(Control):
    def __init__(self,text="",value=0,minValue=0,maxValue=100,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,style="horizontal",key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.value = value
        self.minValue = minValue
        self.maxValue = maxValue
        self.handler = handler
        self.style = style
    def create(self,parent):
        id = getId()
        flags = wx.SL_HORIZONTAL if self.style == "horizontal" else wx.SL_VERTICAL
        self.ctrl = wx.Slider( parent, id, self.value, self.minValue, self.maxValue, self.pos, self.size, 0|flags )
        self.ctrl.Bind( wx.EVT_SLIDER, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Spin(Control):
    def __init__(self,text="",value="",minValue=0,maxValue=100,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.value = str(value)
        self.minValue = minValue
        self.maxValue = maxValue
        self.handler = handler
    def create(self,parent):
        id = getId()
        flags = wx.SP_ARROW_KEYS
        self.ctrl = wx.SpinCtrl( parent, id, self.value, self.pos, self.size, 0|flags, self.minValue, self.maxValue )
        self.ctrl.Bind( wx.EVT_SPIN, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class StyledText(Control):
    import wx.stc
    def __init__(self,text="",handler=None,expand=True,proportion=1,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.text = text
        self.handler = handler        
    def create(self,parent):
        flags = 0
        self.ctrl = wx.stc.StyledTextCtrl( parent, wx.ID_ANY, self.pos, self.size, 0|flags )
        self.enableLineNumber()
        self.ctrl.SetText(self.text)
        drop_target = FileDrop(self)
        self.ctrl.SetDropTarget(drop_target)
        if self.key is not None:
            registerCtrl( self.key, self )
    def drop_handle(self,filenames):
        for filename in filenames:
            self.ctrl.AppendText( filename + '\n' )
    def enableLineNumber(self):
        #self.stc.SetProperty("fold", "1")
        #self.stc.SetProperty("fold.html", "1")
        self.ctrl.SetMargins(0, 0)
        self.ctrl.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        self.ctrl.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.ctrl.SetMarginSensitive(2, True)
        self.ctrl.SetMarginWidth(1, 32) # 2,25
        self.ctrl.SetMarginWidth(2, 16) # 2,25
    #TODO: getValue,setValue check

class Text(Control):
    def __init__(self,text="",handler=None,expand=True,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,
                 multiline=False,password=False,readonly=False,wrap=True,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.text = text
        self.multiline = multiline
        self.password = password
        self.readonly = readonly
        self.wrap = wrap
        self.handler = handler
        #self.expand = True if multiline == True else False
    def create(self,parent):
        id = getId()
        flags = 0
        flags |= wx.TE_MULTILINE if self.multiline is True else 0
        flags |= wx.TE_PASSWORD if self.password is True else 0
        flags |= wx.TE_READONLY if self.readonly is True else 0
        flags |= wx.TE_DONTWRAP if self.wrap is False else 0
        self.ctrl = wx.TextCtrl( parent, id, self.text, self.pos, self.size, 0|flags )
        self.ctrl.Bind( wx.EVT_TEXT, self.handler, id=id )
        #self.ctrl.Bind( wx.EVT_CHAR, self.handler )
        drop_target = FileDrop(self)
        self.ctrl.SetDropTarget(drop_target)
        if self.key is not None:
            registerCtrl( self.key, self )
    def drop_handle(self,filenames):
        for filename in filenames:
            self.ctrl.AppendText( filename )
            if self.multiline is False:
                break
            self.ctrl.AppendText( '\n' )
    def appendValue(self,value):
        self.ctrl.AppendText(value)
        
class Ticker(Control):
    import wx.lib.ticker
    def __init__(self,text="",fgcolor=wx.BLACK,bgcolor=wx.WHITE,expand=True,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.text = text
        self.fgcolor = fgcolor
        self.bgcolor = bgcolor
    def create(self,parent):
        self.ctrl = wx.lib.ticker.Ticker( parent, wx.ID_ANY, self.text, self.fgcolor, self.bgcolor, True, pos=self.pos, size=self.size, style=wx.NO_BORDER )
        self.ctrl.Bind(wx.EVT_CLOSE, self.onClose)
        if self.key is not None:
            registerCtrl( self.key, self )
    def onClose(self,event):
        self.ctrl.Stop()
        event.Skip()
    #TODO: getValue,setValue check

class Time(Control):
    def __init__(self,date=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.date = date
    def create(self,parent):
        self.ctrl = wx.adv.TimePickerCtrl( parent, wx.ID_ANY, wx.DefaultDateTime, self.pos, self.size, wx.adv.TP_DEFAULT )
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class ToggleButton(Control):
    def __init__(self,label="",value=None,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None,tooltip=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos,tooltip=tooltip)
        self.label = label
        self.value = value
        self.handler = handler
    def create(self,parent):
        id = getId()
        if type(self.label) is str:
            self.ctrl = wx.ToggleButton( parent, id, self.label, self.pos, self.size, 0 )
            self.ctrl.Bind( wx.EVT_TOGGLEBUTTON, self.handler, id=id )
        else: #byte[]
            self.ctrl = wx.BitmapToggleButton( parent, id, getButtonBitmap(self.label), self.pos, self.size, 0 ) 
            self.ctrl.Bind( wx.EVT_TOGGLEBUTTON, self.handler, id=id )
        if self.value is not None:
            self.setValue(self.value)
        if self.tooltip is not None:
            self.ctrl.SetToolTip(wx.ToolTip(self.tooltip))
        if self.key is not None:
            registerCtrl( self.key, self )
    def clearValue(self):
        pass
    def appendValue(self,value):
        pass
    def removeValue(self,value):
        pass  
    def castValue(self,value):
        return bool(value)

class Tree(Control):
    def __init__(self,data=None,collapse=False,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.data = data
        self.collapse = collapse
        self.handler = handler
    def create(self,parent):
        id = getId()
        self.ctrl = wx.TreeCtrl( parent, id, self.pos, self.size, wx.TR_DEFAULT_STYLE )
        self.ctrl.Bind( wx.EVT_TREE_SEL_CHANGED, self.handler, id=id )
        if self.data is not None:
            root = self.ctrl.AddRoot(self.data[0])
            if type(self.data[1]) is list:
                self.addItems(root,self.data[1])
            if self.collapse is not True:
                self.ctrl.ExpandAllChildren(root)
        if self.key is not None:
            registerCtrl( self.key, self )
    def addItems(self,parent,data):
        node = None
        for item in data:
            if type(item) is list and node is not None:
                self.addItems(node,item)
            else: #list
                node = self.ctrl.AppendItem(parent,item)
    #TODO: getValue,setValue check

class Web(Control):
    import wx.lib.iewin
    def __init__(self,url=None,engine='ie',expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.url = url
        self.engine = engine
    def create(self,parent):
        if self.engine == 'ie':
            self.ctrl = wx.lib.iewin.IEHtmlWindow( parent, wx.ID_ANY, self.pos, self.size, 0 )
            if self.url is not None:
                self.ctrl.LoadUrl(self.url)
            if self.key is not None:
                registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class PdfWin(Control):
    import wx.lib.pdfwin
    def __init__(self,url=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.url = url
    def create(self,parent):
        self.ctrl = wx.lib.pdfwin.PDFWindow( parent, wx.ID_ANY, self.pos, self.size, 0 )
        if self.url is not None:
            self.ctrl.LoadFile(self.url)
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class PdfView(Control):
    import wx.lib.pdfviewer
    def __init__(self,url=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.url = url
    def create(self,parent):
        self.ctrl = wx.lib.pdfviewer.pdfViewer( parent, wx.ID_ANY, self.pos, self.size, wx.HSCROLL|wx.VSCROLL|wx.SUNKEN_BORDER )
        #self.ctrl.SetSizerProps(expand=True, proportion=1)
        #self.buttonpanel = wx.lib.pdfviewer.pdfButtonPanel(parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)
        #self.buttonpanel.SetSizerProps(expand=True)
        #self.buttonpanel.viewer = self.ctrl
        #self.ctrl.buttonpanel = self.buttonpanel            
        if self.url is not None:
            self.ctrl.LoadFile(self.url)
        if self.key is not None:
            registerCtrl( self.key, self )
    #TODO: getValue,setValue check

class Media(Control):
    import wx.media
    def __init__(self,url=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.url = url
    def create(self,parent):
        self.ctrl = wx.media.MediaCtrl( parent, wx.ID_ANY, szBackend=wx.media.MEDIABACKEND_WMP10, pos=self.pos, size=self.size )
        self.ctrl.Bind(wx.media.EVT_MEDIA_LOADED, self.onLoaded)
        if self.url is not None:
            self.ctrl.Load(self.url)
        if self.key is not None:
            registerCtrl( self.key, self )
    def onLoaded(self,event):
        self.ctrl.Play()
    #TODO: getValue,setValue check

######################################################################
# Clipboard
######################################################################
def GetClipboardText():
    if not wx.TheClipboard.IsOpened():
        do = wx.TextDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(do)
        wx.TheClipboard.Close()
        if success:
            return do.GetText()
    return ''
    
def GetClipboardHtmlText():
    if not wx.TheClipboard.IsOpened():
        do = wx.HTMLDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(do)
        wx.TheClipboard.Close()
        if success:
            return do.GetHTML()
    return 'No Html Data'
    
def GetClipboardFilenames():
    if not wx.TheClipboard.IsOpened():
        do = wx.FileDataObject()
        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(do)
        wx.TheClipboard.Close()
        if success:
            return do.Filenames
    return []
    
    
######################################################################
# Compound Control
######################################################################
class Toolbar(Control):
    def __init__(self,tool_def, largeButton=False,expand=False,proportion=0,border=2,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.ctrl = None
        self.tool_def = tool_def
        self.largeButton = largeButton
    def create(self, parent):  #icon, text, handler
        flags = wx.TB_FLAT|wx.TB_HORIZONTAL
        if len(self.tool_def[0]) >= 3:
            flags |= wx.TB_TEXT
        self.ctrl = wx.ToolBar( parent, wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=flags)
        for value in self.tool_def:
            if value[0] is None:
                self.ctrl.AddSeparator()
            else:
                text = handler = tooltip = None
                if len(value) >= 2:
                    handler = value[1]
                if len(value) >= 3:
                    text = value[2]
                if len(value) >= 4:
                    tooltip = value[3]
                if self.largeButton: 
                    icon = getToolbarBitmap(value[0],size=(32,32))
                else:
                    icon = getToolbarBitmap(value[0],size=(24,24))
                id = getId()
                if text is not None:
                    tool = self.ctrl.AddTool( id, text, icon, wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
                else:
                    tool = self.ctrl.AddTool( id, '', icon, wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
                    #tool = self.ctrl.AddSimpleTool( id, icon, wx.EmptyString, wx.EmptyString, None )
                if tooltip is not None:
                    self.ctrl.SetToolShortHelp(id, tooltip);
                if handler is None:
                    tool.Enable( False )
                else:
                    self.ctrl.Bind( wx.EVT_TOOL, handler, id = id )
        self.ctrl.Realize()
    def getValue(self):
        pass
    def setValue(self,item):
        pass
    def clearValue(self):
        pass
    def appendValue(self,value):
        pass
    def removeValue(self,value):
        pass
        
class FileBrowser(Control): 
    def __init__(self,label=None,text=None,buttonText="Browse",handler=None,save=False,directory=False,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.ctrl = None
        self.layout = [[]]
        self.label = label
        self.text = text
        self.buttonText = buttonText
        self.handler = handler
        self.save = save
        self.directory = directory
    def create(self,parent):
        self.textCtrl = Text(self.text, expand=True, proportion=1, border=2)
        self.buttonCtrl = Button(self.buttonText, handler=self.onBrowse, border=2 )
        if self.label: 
            self.layout[0].append( Label(self.label, border=2) )
        self.layout[0].append( self.textCtrl )
        self.layout[0].append( self.buttonCtrl )
        self.layout[0].append( { 'expand' : True, 'border' : 0 } )
        vbox = makeLayout(self.layout,parent)
        self.ctrl = vbox.ctrl
        if self.key is not None:
            registerCtrl( self.key, self.textCtrl )
    def onBrowse(self,event):
        if self.directory:
            f = DirectoryDialog(defaultPath=self.text)
        else:
            f = OpenFileDialog(defaultDir=self.text, save=self.save)
        if f is not None:
            self.textCtrl.ctrl.Clear()
            self.textCtrl.ctrl.AppendText(f)
            if self.handler: self.handler(f)
    def getValue(self):
        pass
    def setValue(self,item):
        pass
    def clearValue(self):
        pass
    def appendValue(self,value):
        pass
    def removeValue(self,value):
        pass
        
class DirectoryBrowser(FileBrowser):
    def __init__(self,label=None,text=None,buttonText="Browse",handler=None,save=False,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(label=label,text=text,buttonText=buttonText,handler=handler,save=save,directory=True,expand=expand,proportion=proportion,border=border,
                    size=size,pos=pos,key=key)
        
class ToolbarText(Control): 
    def __init__(self,tool_def=None,text='',largeButton=False,multiline=True,handler=None,expand=False,proportion=0,border=2,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key=key,expand=expand,proportion=proportion,border=border,size=size,pos=pos)
        self.ctrl = None
        self.layout = [[], []] #toolbar, text
        self.tool_def = tool_def
        self.text = text
        self.largeButton = largeButton
        self.multiline = multiline
        self.handler = handler
    def create(self,parent):
        if self.tool_def is None:
            self.largeButton = False
            self.tool_def = [
                [wx.ART_NEW  , self.onClear     , None, "Clear all text"],
                [wx.ART_COPY , self.onCopy      , None, "Copy text to clipboard"],
                [wx.ART_PASTE, self.onPaste     , None, "Paste text from clipboard"],
                [wx.ART_PASTE, self.onPasteHtml , None, "Paste html text from clipboard"],
            ]
        self.toolbar = Toolbar(self.tool_def,self.largeButton)
        self.textCtrl = Text(self.text, multiline=self.multiline, expand=True, proportion=1, border=0)
        self.layout[0].append( self.toolbar )
        self.layout[0].append( { 'expand' : True, 'border' : 0 } )
        self.layout[1].append( self.textCtrl )
        self.layout[1].append( { 'expand' : True, 'proportion' : 1, 'border' : 0 } )
        vbox = makeLayout(self.layout,parent)
        self.ctrl = vbox.ctrl
        if self.key is not None:
            registerCtrl( self.key, self.textCtrl )
    def onClear(self,event):
        self.textCtrl.ctrl.Clear()
    def onCopy(self,event):
        self.textCtrl.ctrl.Copy()
    def onPaste(self,event):
        self.textCtrl.ctrl.Paste()
    def onPasteHtml(self,event):
        self.textCtrl.ctrl.AppendText(GetClipboardHtmlText())

                
######################################################################
# Dialogs : deprecated use wxApp.*
######################################################################

def OpenFileDialog(defaultDir="",multiple=False,save=False):
    if not defaultDir: defaultDir = ''
    style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if save is False else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
    style |= wx.FD_MULTIPLE if multiple is True else 0
    dlg = wx.FileDialog(None,defaultDir=defaultDir,style=style)
    rv = dlg.ShowModal()
    if rv == wx.ID_OK:
        if multiple == True:
            files = []
            for file in dlg.GetFilenames():
                files.append( os.path.join(dlg.GetDirectory(), file) )
            return files
        else:
            return os.path.join(dlg.GetDirectory(), dlg.GetFilename())
    else:
        return None

def SaveFileDialog(defaultDir=""):
    return OpenFileDialog(defaultDir=defaultDir, multiple=False, save=True)

def DirectoryDialog(defaultPath=""):
    dlg = wx.DirDialog(None,defaultPath=defaultPath)
    rv = dlg.ShowModal()
    if rv == wx.ID_OK:
        return dlg.GetPath()
    else:
        return None

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

def ProgressDialog(title,message,maxValue=100):
    dlg = wx.ProgressDialog(title, message, maximum=100, parent=None, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)
    return dlg

def _onProgressDialog(dlg,percent):
    dlg.Update(percent)

def ProgressDialogUpdate(dlg,percent):
    wx.CallAfter(_onProgressDialog, dlg, percent)
    
def progressDialogUpdate(dlg,percent): #deprecated
    wx.CallAfter(_onProgressDialog, dlg, percent)

def CalendarDialog(parent=None,year=None,month=None,day=None):
    dlg = wx.lib.CalenDlg(parent,month,day,year)
    #TODO

class _process(wx.Process):
    def __init__(self,event_id,handler=None):
        super().__init__()
        self.event_id = event_id
        self.handler = handler
        self.Redirect()
    def OnTerminate(self,pid,status):
        print( pid, status )
        if self.handler is not None:
            self.handler(self.event_id,status)
    
def Execute(command,sync=False,show=False): #TODO
    #process = _process(event_id,handler)
    flags = 0
    if sync is True: 
        flags |= wx.EXEC_SYNC 
    else: 
        flags |= wx.EXEC_ASYNC
    if show is True: 
        flags |= wx.EXEC_SHOW_CONSOLE 
    else: 
        flags |= wx.EXEC_HIDE_CONSOLE
    #wx.Execute(command, flags=flags, callback=process)
    wx.Execute(command, flags=flags)
    
######################################################################
# WxApp
######################################################################

class WxApp():
    def __init__( self, title, width=800, height=600, popup=False ):
        if popup is False:
            self.app = wx.App()
            self.app.locale = wx.Locale(wx.Locale.GetSystemLanguage())
            self.frame = wx.Frame( parent=None, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( width,height ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
            self.frame.Bind(wx.EVT_CLOSE, self.closeEvent)
            registerCtrl( 'WxApp', self )
        else:
            self.frame = wx.Frame( parent=None, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( width,height ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
            self.frame.Bind(wx.EVT_CLOSE, self.popupCloseEvent)
        self.frame.Center();
        self.frame.Bind(wx.EVT_SHOW, self.openEvent)
        self.frame.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.openHandler = None
        self.closeHandler = None
        self.lastMousePos = wx.Point(0,0)
        self.menubar = None 
        self.statusbar = None 

    def run(self):
        self.frame.Center()
        self.frame.Show()
        self.app.MainLoop()

    def close(self):
        self.frame.Close()

    def show(self):
        self.frame.Show()

    def Show(self): #TODO: remove
        self.frame.Show()

    def getCtrl(self,key):
        return getCtrl(key)

    def getWxCtrl(self,key):
        return getWxCtrl(key)

    def getWxTimer(self,key):
        return getWxTimer(key)
        
    def openEvent(self,event):
        if self.openHandler is not None:
            self.openHandler(event)
            self.openHandler = None
        self.frame.Unbind(wx.EVT_SHOW)
        event.Skip()

    def openHandle(self,handler):
        self.openHandler = handler

    def closeEvent(self,event):
        if self.closeHandler is not None:
            if self.closeHandler(event) == True:
                event.Skip()
        else:
            event.Skip()

    def popupCloseEvent(self,event): 
        self.makeModal(False) 
        if self.closeHandler is not None: #841
            if self.closeHandler(event) == True:
                event.Skip()
        else:
            event.Skip()

    def closeHandle(self,handler):
        self.closeHandler = handler

    def idleHandle(self,handler):
        self.frame.Bind(wx.EVT_IDLE, handler)

    def timerHandle(self,handler,interval=1000,start=False,key=None):
        timer = wx.Timer(self.frame)
        self.frame.Bind(wx.EVT_TIMER, handler, timer)
        if key is not None:
            registerCtrl(key,timer)
        if start is True and interval > 0:
            timer.Start(interval)

    def timerStart(self,key,interval):
        timer = getWxTimer(key)
        if timer is not None and interval > 0:
            timer.Start(interval)

    def timerStop(self,key):
        timer = getWxTimer(key)
        if timer is not None:
            timer.Stop()

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
                        item.SetBitmap(getMenuBitmap(icon))
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
        flags = wx.TB_FLAT|wx.TB_HORIZONTAL
        if len(tool_def[0]) >= 3:
            flags |= wx.TB_TEXT
        self.toolbar = self.frame.CreateToolBar( flags, wx.ID_ANY )
        for value in tool_def:
            if value[0] is None:
                self.toolbar.AddSeparator()
            else:
                text = handler = tooltip = None
                if len(value) >= 2:
                    handler = value[1]
                if len(value) >= 3:
                    text = value[2]
                if len(value) >= 4:
                    tooltip = value[3]
                icon = getToolbarBitmap(value[0])
                id = getId()
                if text is not None:
                    tool = self.toolbar.AddTool( id, text, icon, wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None )
                else:
                    tool = self.toolbar.AddSimpleTool( id, icon, wx.EmptyString, wx.EmptyString, None )
                if tooltip is not None:
                    self.toolbar.SetToolShortHelp(id, tooltip);
                if handler is None:
                    tool.Enable( False )
                else:
                    self.toolbar.Bind( wx.EVT_TOOL, handler, id = id )
        self.toolbar.Realize()

    def makeBody(self,body_def):
        self.panel = Panel(body_def,self.frame,create=True)
        self.frame.SetSizer( wrapSizer(self.panel.ctrl) )
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
        
    def makeModal(self, modal=True): 
        if modal and not hasattr(self.frame, '_disabler'):
            self.frame._disabler = wx.WindowDisabler(self.frame)
        if not modal and hasattr(self.frame, '_disabler'):
            del self.frame._disabler

    def noMinimize(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.MINIMIZE_BOX))
        self.frame.Refresh()

    def noMaximize(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.MAXIMIZE_BOX))
        self.frame.Refresh()

    def NoClose(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.CLOSE_BOX))
        self.frame.Refresh()
        
    def noResize(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.RESIZE_BORDER))
        self.frame.Refresh()

    def noSystemMenu(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.SYSTEM_MENU))
        self.frame.Refresh()

    def noCaption(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.CAPTION))
        self.frame.Refresh()
          
    def noBorder(self): 
        style = self.frame.GetWindowStyle()
        self.frame.SetWindowStyle(style & (~wx.BORDER))
        self.frame.Refresh()

    def _dragMotionHandle(self, event): 
        if event.LeftIsDown():
            currMousePos = wx.GetMousePosition()
            dx = currMousePos[0] - self.lastMousePos[0]
            dy = currMousePos[1] - self.lastMousePos[1]
            self.frame.Move(wx.Point(self.lastWinPos[0] + dx, self.lastWinPos[1] + dy))
        event.Skip()

    def _dragLeftDownHandle(self, event): 
        self.lastWinPos = self.frame.GetScreenPosition()
        self.lastMousePos = wx.GetMousePosition()
        event.Skip()

    def dragEnable(self,key): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.Bind(wx.EVT_MOTION, self._dragMotionHandle)
            ctrl.Bind(wx.EVT_LEFT_DOWN, self._dragLeftDownHandle)

    def _getContextMenuHandler(self,menu): 
        def _contextMenuRightDown(event): #closure
            self.frame.PopupMenu( menu, event.GetPosition() )
        return _contextMenuRightDown

    def contextMenu(self,menu_def,key): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.Bind(wx.EVT_RIGHT_DOWN, self._getContextMenuHandler(self.makeMenu(menu_def)))

    def toolTip(self,text,key): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.SetToolTip(wx.ToolTip(text))

    def setStatusText(self,text,index=0): 
        if self.statusbar is not None:
            if index < self.statusbar.GetFieldsCount():
                self.statusbar.SetStatusText(text,index)

    # Dialog
    def openFileDialog(self,defaultDir="",defaultFile="",multiple=False,save=False):  
        style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST if save is False else wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        style |= wx.FD_MULTIPLE if multiple is True else 0
        dlg = wx.FileDialog(self.frame,defaultDir=defaultDir,defaultFile=defaultFile,style=style)
        rv = dlg.ShowModal()
        if rv == wx.ID_OK:
            if multiple == True:
                files = []
                for file in dlg.GetFilenames():
                    files.append( os.path.join(dlg.GetDirectory(), file) )
                return files
            else:
                return os.path.join(dlg.GetDirectory(), dlg.GetFilename())
        else:
            return None

    def saveFileDialog(self,defaultDir="",defaultFile=""):  
        return OpenFileDialog(defaultDir=defaultDir,defaultFile=defaultFile, multiple=False, save=True)

    def directoryDialog(self,defaultPath=""):  
        dlg = wx.DirDialog(self.frame,defaultPath=defaultPath)
        rv = dlg.ShowModal()
        if rv == wx.ID_OK:
            return dlg.GetPath()
        else:
            return None
        
    def messageBox(self,title,message):  
        dlg = wx.MessageDialog(self.frame, message, caption=title, style=wx.OK|wx.CENTER, pos=wx.DefaultPosition)
        dlg.ShowModal()

    def messageYesNo(self,title,message):  
        dlg = wx.MessageDialog(self.frame, message, caption=title, style=wx.YES|wx.NO|wx.CENTER, pos=wx.DefaultPosition)
        rv = dlg.ShowModal()
        if rv == wx.ID_OK or rv == wx.ID_YES:
            return True
        else:
            return False

    def messageYesNoCancel(self,title,message):  
        dlg = wx.MessageDialog(self.frame, message, caption=title, style=wx.YES|wx.NO|wx.CANCEL|wx.CENTER, pos=wx.DefaultPosition)
        rv = dlg.ShowModal()
        if rv == wx.ID_OK or rv == wx.ID_YES:
            return True
        elif rv == wx.ID_NO:
            return False
        else: #wx.ID_CANCEL,
            return None

    def progressDialog(self,title,message,maxValue=100):  
        dlg = wx.ProgressDialog(title, message, maximum=100, parent=self.frame, style=wx.PD_APP_MODAL|wx.PD_AUTO_HIDE)
        return dlg

    def onProgressDialog(self,dlg,percent):  
        dlg.Update(percent)

    def progressDialogUpdate(self,dlg,percent):  
        wx.CallAfter(self.onProgressDialog, dlg, percent)

    def textEntryDialog(self,title,message,value=''):
        dlg = wx.TextEntryDialog(self.frame, message, title, value=value) 
        if dlg.ShowModal() == wx.ID_OK: 
            value = dlg.GetValue()
        dlg.Destroy() 
        return value

    def dialog(self,title,layout,size=(400,300)): #TODO
        dlg = wx.Dialog( parent=self.frame, title=title, size=size )
        panel = Panel(layout,dlg,create=True)
        dlg.ShowModal()
        dlg.Destroy()

    # Control
    def clearValue(self,key):
        ctrl = self.getCtrl(key)
        if ctrl is not None:
            return ctrl.clearValue() 
        else:
            return None
    
    def getValue(self,key):
        ctrl = self.getCtrl(key)
        if ctrl is not None:
            return ctrl.getValue() 
        else:
            return None

    def setValue(self,key,value):
        ctrl = self.getCtrl(key)
        if ctrl is not None:
            ctrl.setValue(value) 

    def appendValue(self,key,value):
        ctrl = self.getCtrl(key)
        if ctrl is not None:
            return ctrl.appendValue(value) 
        else:
            return None

    def removeValue(self,key,value):
        ctrl = self.getCtrl(key)
        if ctrl is not None:
            return ctrl.removeValue(value) 
        else:
            return None
     
    # Check Button Control
    def getCheckState(self,key):  #deprecated
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            return ctrl.GetValue() 
        else:
            return None

    # Choice, Bombo, List Control
    def getSelectedText(self,key):  #deprecated
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            return ctrl.GetString(ctrl.GetSelection())
        else:
            return None

    # Text Control 
    def getText(self,key):  #deprecated
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            return ctrl.GetValue() 
        else:
            return None

    def setText(self,key,text):  #deprecated
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.Clear() 
            ctrl.AppendText(text) 
                            
    def appendText(self,key,text):  #deprecated
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.AppendText(text) 

    #def setWrap(self,key,wrap=True):
    #    ctrl = getWxCtrl(key)
    #    if ctrl is not None:
    #        ws = ctrl.GetWindowStyle()
    #        if wrap is True:
    #            ctrl.SetWindowStyle(ws & ~wx.TE_DONTWRAP ) #| wx.TE_BESTWRAP
    #        else:
    #            ctrl.SetWindowStyle(ws | wx.TE_DONTWRAP) #& ~wx.TE_BESTWRAP 
        
    # Ticker Control
    def setTickerText(self,key,text): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.SetText(text) 

    def setTickerFont(self,key,font): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.SetFont(font) 

    def setTickerPPF(self,key,text): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.SetPPF(int(text)) 
            
    def setTickerFPS(self,key,text): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.SetFPS(int(text)) 
                        
    def setTickerStart(self,key): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.Start() 

    def setTickerStop(self,key): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            ctrl.Stop() 

    def setTickerDirection(self,key,direction='right'): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            if direction == 'right':
                ctrl.SetDirection('ltr')
            elif direction == 'left':
                ctrl.SetDirection('rtl')

    # Book Control
    def setBookPage(self,key,index): 
        ctrl = getCtrl(key)
        if ctrl is not None:
            ctrl.setPage(index)
    def setBookEffect(self,key,effect="slide_to_left"): 
        ctrl = getCtrl(key)
        if ctrl is not None:
            ctrl.setEffect(effect)
    
    #Calendar Control
    def getCalendarDate(self,key): 
        ctrl = getWxCtrl(key)
        if ctrl is not None:
            date = ctrl.GetDate()
            return date.Format('%Y-%m-%d')
    
class WxPopup(WxApp):
    def __init__( self, title, width=800, height=600 ):
        super().__init__( title, width=width, height=height, popup=True )
        
        
