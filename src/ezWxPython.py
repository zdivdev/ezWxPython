import os
import sys
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

#wx.ART_ADD_BOOKMARK
#wx.ART_CDROM
#wx.ART_CLOSE
#wx.ART_COPY
#wx.ART_CROSS_MARK
#wx.ART_CUT
#wx.ART_DELETE
#wx.ART_DEL_BOOKMARK
#wx.ART_ERROR
#wx.ART_EXECUTABLE_FILE
#wx.ART_FILE_OPEN
#wx.ART_FILE_SAVE
#wx.ART_FILE_SAVE_AS
#wx.ART_FIND
#wx.ART_FIND_AND_REPLACE
#wx.ART_FLOPPY
#wx.ART_FOLDER
#wx.ART_FOLDER_OPEN
#wx.ART_GOTO_FIRST (since 2.9.2)
#wx.ART_GOTO_LAST (since 2.9.2)
#wx.ART_GO_BACK
#wx.ART_GO_DIR_UP
#wx.ART_GO_DOWN
#wx.ART_GO_FORWARD
#wx.ART_GO_HOME
#wx.ART_GO_TO_PARENT
#wx.ART_GO_UP
#wx.ART_HARDDISK
#wx.ART_HELP
#wx.ART_HELP_BOOK
#wx.ART_HELP_FOLDER
#wx.ART_HELP_PAGE
#wx.ART_HELP_SETTINGS
#wx.ART_HELP_SIDE_PANEL
#wx.ART_INFORMATION
#wx.ART_LIST_VIEW
#wx.ART_MINUS (since 2.9.2)
#wx.ART_MISSING_IMAGE
#wx.ART_NEW
#wx.ART_NEW_DIR
#wx.ART_NORMAL_FILE
#wx.ART_PASTE
#wx.ART_PLUS (since 2.9.2)
#wx.ART_PRINT
#wx.ART_QUESTION
#wx.ART_QUIT
#wx.ART_REDO
#wx.ART_REPORT_VIEW
#wx.ART_TICK_MARK
#wx.ART_TIP
#wx.ART_UNDO
#wx.ART_WARNING
        
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
        pass

class Control():
    def __init__(self,key=None,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,border=2):
        self.ctrl = None
        self.key = key
        self.expand = expand
        self.proportion = proportion
        self.size = size
        self.pos = pos
        self.border=2

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
        if type(row) is list:
            for col in row:
                if type(col) is dict:
                    prop = dictValue( col.get('proportion'), prop )
                    expand = dictValue( col.get('expand'), expand )
                elif col is None:
                    hbox.addSpacer(proportion=1)
                else:
                    col.create(parent)
                    hbox.add(col.ctrl,proportion=col.proportion,expand=col.expand,border=col.border,align=wx.ALIGN_CENTER_VERTICAL|wx.ALL)
        vbox.add(hbox.ctrl,proportion=prop,expand=expand,border=2,align=wx.ALIGN_LEFT|wx.ALL)
    return vbox

class Book(Control):
    '''
    wx.SHOW_EFFECT_NONE No effect, equivalent to normal wx.Window.Show or Hide() call.
    wx.SHOW_EFFECT_ROLL_TO_LEFT Roll window to the left.
    wx.SHOW_EFFECT_ROLL_TO_RIGHT Roll window to the right.
    wx.SHOW_EFFECT_ROLL_TO_TOP Roll window to the top.
    wx.SHOW_EFFECT_ROLL_TO_BOTTOM Roll window to the bottom.
    wx.SHOW_EFFECT_SLIDE_TO_LEFT Slide window to the left.
    wx.SHOW_EFFECT_SLIDE_TO_RIGHT Slide window to the right.
    wx.SHOW_EFFECT_SLIDE_TO_TOP Slide window to the top.
    wx.SHOW_EFFECT_SLIDE_TO_BOTTOM Slide window to the bottom.
    wx.SHOW_EFFECT_BLEND Fade in or out effect.
    wx.SHOW_EFFECT_EXPAND Expanding or collapsing effect.
    wx.SHOW_EFFECT_MAX
    '''
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,style='note',key=None):
        super().__init__(key,expand,proportion)
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
        '''
        for layout in self.layouts:
            title = layout[0]
            layout.remove(title)
            panel = Panel(layout, self.ctrl, create=True)
            if self.style == 'simple':
                self.simplePages.append(panel.ctrl);
            else:
                self.ctrl.AddPage( panel.ctrl, title, False )
        '''
        if self.style == 'simple':
            self.setPage(0)
    def setEffect(self,):
        if self.style == 'simple':
            self.ctrl.SetEffect(wx.SHOW_EFFECT_SLIDE_TO_LEFT)
    def setPage(self,index):
        if self.style == 'simple':
            if index >= len(self.simplePages):
                index = 0
            self.ctrl.ShowNewPage(self.simplePages[index])

class Notebook(Book):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,key=None):
        super().__init__(layouts,parent,create,horizontal,expand,proportion,style='note',key=key)

class Choicebook(Book):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,key=None):
        super().__init__(layouts,parent,create,horizontal,expand,proportion,style='choice',key=key)

class Simplebook(Book):
    def __init__(self,layouts,parent=None,create=False,horizontal=True,expand=False,proportion=0,key=None):
        super().__init__(layouts,parent,create,horizontal,expand,proportion,style='simple',key=key)

class Panel(Control):
    import wx.lib.scrolledpanel
    def __init__(self,layout,parent=None,create=False,expand=False,proportion=0,label="",style=None,key=None):
        super().__init__(key,expand,proportion)
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
    def __init__(self,layout,parent=None,create=False,expand=False,proportion=0,label="",key=None):
        super().__init__(layout,parent=parent,create=create,expand=expand,proportion=proportion,label=label,style='scroll',key=key)

class CollapsiblePanel(Panel):
    def __init__(self,layout,parent=None,create=False,expand=False,proportion=0,label="",key=None):
        super().__init__(layout,parent=parent,create=create,expand=expand,proportion=proportion,label=label,style='collapsible',key=key)

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

#use MultiSplitterWindow instead of SplitterWindow
#class Spliter1(Control):
#    def __init__(self,layouts,parent=None,create=False,style='vertical',expand=False,proportion=0,key=None):
#        super().__init__(key,expand,proportion)
#        self.layouts = layouts #left(top),right(bottom)
#        self.style = style
#        if create is True and parent is not None:
#            self.create(parent)
#    def create(self,parent):
#        self.ctrl = wx.SplitterWindow( parent, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_3D )
#        self.sashpos = 0
#        self.panels = []
#        for layout in self.layouts:
#            if type(layout) is int:
#                self.sashpos = layout
#            else:
#                self.panels.append(Panel(layout, self.ctrl, create=True))
#        if self.style == 'vertical':
#            self.ctrl.SplitVertically( self.panels[0].ctrl, self.panels[1].ctrl, self.sashpos )
#        else:
#            self.ctrl.SplitHorizontally( self.panels[0].ctrl, self.panels[1].ctrl, self.sashpos )

class Spliter(Control):
    import wx.lib.splitter
    def __init__(self,layouts,parent=None,create=False,style='vertical',expand=False,proportion=0,key=None):
        super().__init__(key,expand,proportion)
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

class VerticalSpliter(Spliter):
    def __init__(self,layouts,parent=None,create=False,expand=False,proportion=0,key=None):
        super().__init__(layouts,parent=parent,create=create,style='vertical',expand=expand,proportion=proportion,key=key)

class HorizontalSpliter(Spliter):
    def __init__(self,layouts,parent=None,create=False,expand=False,proportion=0,key=None):
        super().__init__(layouts,parent=parent,create=create,style='horizontal',expand=expand,proportion=proportion,key=key)

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
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,filename=None,bitmap=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Button(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,label="",handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.label = label
        self.handler = handler
    def create(self,parent):
        id = getId()
        if type(self.label) is str: 
            self.ctrl = wx.Button( parent, id, self.label, self.pos, self.size, 0 )
        else:
            self.ctrl = wx.BitmapButton( parent, id, getButtonBitmap(self.label), self.pos, self.size, 0 )
        self.ctrl.Bind( wx.EVT_BUTTON, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )

class Calendar(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,date=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.date = date
    def create(self,parent):
        self.ctrl = wx.adv.CalendarCtrl( parent, wx.ID_ANY, wx.DefaultDateTime, self.pos, self.size, wx.adv.TP_DEFAULT )
        if self.key is not None:
            registerCtrl( self.key, self )

class Check(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,label="",handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.label = label
        self.handler = handler
    def create(self,parent):
        id = getId()
        self.ctrl = wx.CheckBox( parent, id, self.label, self.pos, self.size, 0 )
        self.ctrl.Bind( wx.EVT_CHECKBOX, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )

class Choice(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,choices=[],select=0,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Combo(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,choices=[],value="",handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.choices = choices
        self.value = value
        self.handler = handler
    def create(self,parent):
        id = getId()
        self.ctrl = wx.ComboBox( parent, id, self.value, self.pos, self.size, self.choices, 0 )
        self.ctrl.Bind( wx.EVT_COMBOBOX, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )

class Date(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,date=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.date = date
    def create(self,parent):
        self.ctrl = wx.adv.DatePickerCtrl( parent, wx.ID_ANY, wx.DefaultDateTime, self.pos, self.size, wx.adv.TP_DEFAULT )
        if self.key is not None:
            registerCtrl( self.key, self )

class Label(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,text="",expand=False,proportion=0,multiline=False,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.text = text
        self.multiline = multiline
    def create(self,parent):
        flags = 0
        if self.multiline == True:
            flags |= wx.TE_MULTILINE
        self.ctrl = wx.StaticText( parent, wx.ID_ANY, self.text, self.pos, self.size, 0|flags )
        if self.key is not None:
            registerCtrl( self.key, self )

class Line(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,text="",expand=False,proportion=0,style="horizontal",
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.style = style
    def create(self,parent):
        flags = wx.LI_HORIZONTAL if self.style == "horizontal" else wx.LI_VERTICAL
        self.ctrl = wx.StaticLine( parent, wx.ID_ANY, self.pos, self.size, 0|flags )
        if self.key is not None:
            registerCtrl( self.key, self )

class Link(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,text="",url="",expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.text = text
        self.url = url
    def create(self,parent):
        self.ctrl = wx.adv.HyperlinkCtrl( parent, wx.ID_ANY, self.text, self.url, self.pos, self.size)
        if self.key is not None:
            registerCtrl( self.key, self )

class List(Control):
    '''
    Methods Summary: ListBox
        Deselect(self, n)
        EnsureVisible(self, n)
        FindString(self, string, caseSensitive=False)
        GetCount(self)
        GetSelection(self)
        GetSelections(self)
        GetString(self, n)
        HitTest(self, *args, **kw)
        HitTest (self, point)
        HitTest (self, x, y)
        InsertItems(self, items, pos)
        IsSelected(self, n)
        IsSorted(self)
        SetFirstItem(self, *args, **kw)
        SetFirstItem (self, n)
        SetFirstItem (self, string)
        SetItemBackgroundColour(self, item, c)
        SetItemFont(self, item, f)
        SetItemForegroundColour(self, item, c)
        SetSelection(self, n)
        SetString(self, n, string)
        SetStringSelection(self, *args, **kw)
        SetStringSelection (self, s, select)
        SetStringSelection (self, s)
    Methods Summary: ListCtrl
        Append(self, entry)
        AppendColumn(self, heading, format=LIST_FORMAT_LEFT, width=-1)
        Arrange(self, flag=LIST_ALIGN_DEFAULT)
        AssignImageList(self, imageList, which)
        ClearAll(self)
        ClearColumnImage(self, col)
        Create(self, parent, id=ID_ANY, pos=DefaultPosition, size=DefaultSize, style=LC_ICON, validator=DefaultValidator, name=ListCtrlNameStr)
        DeleteAllColumns(self)
        DeleteAllItems(self)
        DeleteColumn(self, col)
        DeleteItem(self, item)
        EditLabel(self, item)
        EnableAlternateRowColours(self, enable=True)
        EnableBellOnNoMatch(self, on=True)
        EnsureVisible(self, item)
        FindItem(self, *args, **kw)
        FindItem (self, start, str, partial=False)
        FindItem (self, start, data)
        FindItem (self, start, pt, direction)
        Focus(self, idx)
        GetColumn(self, col)
        GetColumnCount(self)
        GetColumnIndexFromOrder(self, pos)
        GetColumnOrder(self, col)
        GetColumnWidth(self, col)
        GetColumnsOrder(self)
        GetCountPerPage(self)
        GetEditControl(self)
        GetFirstSelected(self, *args)
        GetFocusedItem(self)
        GetImageList(self, which)
        GetItem(self, itemIdx, col=0)
        GetItemBackgroundColour(self, item)
        GetItemCount(self)
        GetItemData(self, item)
        GetItemFont(self, item)
        GetItemPosition(self, item)
        GetItemRect(self, item, code=LIST_RECT_BOUNDS)
        GetItemSpacing(self)
        GetItemState(self, item, stateMask)
        GetItemText(self, item, col=0)
        GetItemTextColour(self, item)
        GetMainWindow(self)
        GetNextItem(self, item, geometry=LIST_NEXT_ALL, state=LIST_STATE_DONTCARE)
        Searches for an item with the given geometry or state, starting from item but excluding the item itself.
        GetNextSelected(self, item)
        GetSelectedItemCount(self)
        GetSubItemRect(self, item, subItem, rect, code=LIST_RECT_BOUNDS)
        GetTextColour(self)
        GetTopItem(self)
        GetViewRect(self)
        HasColumnOrderSupport(self)
        HitTest(self, point)
        HitTestSubItem(self, itTestSubItem(point)
        InReportView(self)
        InsertColumn(self, *args, **kw)
        InsertColumn (self, col, info)
        InsertColumn (self, col, heading, format=LIST_FORMAT_LEFT, width=LIST_AUTOSIZE)
        InsertItem(self, *args, **kw)
        InsertItem (self, info)
        InsertItem (self, index, label)
        InsertItem (self, index, imageIndex)
        InsertItem (self, index, label, imageIndex)
        IsSelected(self, idx)
        IsVirtual(self)
        OnGetItemAttr(self, item)
        OnGetItemColumnImage(self, item, column)
        OnGetItemImage(self, item)
        OnGetItemText(self, item, column)
        RefreshItem(self, item)
        RefreshItems(self, itemFrom, itemTo)
        ScrollList(self, dx, dy)
        Select(self, idx, on=1)
        SetAlternateRowColour(self, colour)
        SetBackgroundColour(self, col)
        SetColumn(self, col, item)
        SetColumnImage(self, col, image)
        SetColumnWidth(self, col, width)
        SetColumnsOrder(self, orders)
        SetImageList(self, imageList, which)
        SetItem(self, *args, **kw)
        SetItem (self, info)
        SetItem (self, index, column, label, imageId=-1)
        SetItemBackgroundColour(self, item, col)
        SetItemColumnImage(self, item, column, image)
        SetItemCount(self, count)
        SetItemData(self, item, data)
        SetItemFont(self, item, font)
        SetItemImage(self, item, image, selImage=-1)
        SetItemPosition(self, item, pos)
        SetItemState(self, item, state, stateMask)
        SetItemText(self, item, text)
        SetItemTextColour(self, item, col)
        SetSingleStyle(self, style, add=True)
        SetTextColour(self, col)
        SetWindowStyleFlag(self, style)
        SortItems(self, fnSortCallBack)
        def ListCompareFunction(self, item1, item2):
    '''
    def __init__(self,choices=[],select=0,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,check=False,label="",style=None,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Picker(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class DirPicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('dir',value,handler,expand,proportion,size,pos,key)

class FilePicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('file',value,handler,expand,proportion,size,pos,key)

class ColorPicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('color',value,handler,expand,proportion,size,pos,key)

class FontPicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('font',value,handler,expand,proportion,size,pos,key)

class DatePicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('date',value,handler,expand,proportion,size,pos,key)

class TimePicker(Picker):
    def __init__(self,style="",value=None,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__('time',value,handler,expand,proportion,size,pos,key)

class Progress(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    import wx.lib.progressindicator as pi
    def __init__(self,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Radio(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,label="",choices=[],value="",handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,style='row',key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Slider(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,text="",value=0,minValue=0,maxValue=100,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,style="horizontal",key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Spin(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,text="",value="",minValue=0,maxValue=100,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.value = str(value)
        self.minValue = minValue
        self.maxValue = maxValue
        self.handler = handler
    def create(self,parent):
        id = getId()
        flags = wx.SP_ARROW_KEYS
        self.ctrl = wx.SpinCtrl( parent, wx.ID_ANY, self.value, self.pos, self.size, 0|flags, self.minValue, self.maxValue )
        self.ctrl.Bind( wx.EVT_SPIN, self.handler, id=id )
        if self.key is not None:
            registerCtrl( self.key, self )

class StyledText(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    import wx.stc
    def __init__(self,text="",expand=True,proportion=1,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.text = text
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

class Text(Control):
    '''
    Methods Summary: TextEntry
        AppendText(self, text)
        AutoComplete(self, *args, **kw)
        AutoComplete (self, choices)
        AutoComplete (self, completer)
        AutoCompleteDirectories(self)
        AutoCompleteFileNames(self)
        CanCopy(self)
        CanCut(self)
        CanPaste(self)
        CanRedo(self)
        CanUndo(self)
        ChangeValue(self, value)
        Clear(self)
        Copy(self)
        Cut(self)
        GetHint(self)
        GetInsertionPoint(self)
        GetLastPosition(self)
        GetMargins(self)
        GetRange(self, from_, to_)
        GetSelection(self)
        GetStringSelection(self)
        GetValue(self)
        IsEditable(self)
        IsEmpty(self)
        Paste(self)
        Redo(self)
        Remove(self, from_, to_)
        Replace(self, from_, to_, value)
        SelectAll(self)
        SelectNone(self)
        SetEditable(self, editable)
        SetHint(self, hint)
        SetInsertionPoint(self, pos)
        SetInsertionPointEnd(self)
        SetMargins(self, *args, **kw)
        SetMargins (self, pt)
        SetMargins (self, left, top=-1)
        SetMaxLength(self, len)
        SetSelection(self, from_, to_)
        SetValue(self, value)
        Undo(self)
        WriteText(self, text)
    Methods Summary: TextCtrl
        DiscardEdits(self)
        EmulateKeyPress(self, event)
        GetDefaultStyle(self)
        GetLineLength(self, lineNo)
        GetLineText(self, lineNo)
        GetNumberOfLines(self)
        GetStyle(self, position, style)
        HideNativeCaret(self)
        HitTestPos(self, pt)
        HitTest(self, pt)
        IsModified(self)
        IsMultiLine(self)
        IsSingleLine(self)
        LoadFile(self, filename, fileType=TEXT_TYPE_ANY)
        MacCheckSpelling(self, check)
        MarkDirty(self)
        PositionToCoords(self, pos)
        PositionToXY(self, pos)
        SaveFile(self, filename="", fileType=TEXT_TYPE_ANY)
        SetDefaultStyle(self, style)
        SetModified(self, modified)
        SetStyle(self, start, end, style)
        ShowNativeCaret(self, show=True)
        ShowPosition(self, pos)
        XYToPosition(self, x, y)
        flush(self)
        write(self, text)
    '''
    def __init__(self,text="",expand=True,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,
                 multiline=False,password=False,readonly=False,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.text = text
        self.multiline = multiline
        self.password = password
        self.readonly = readonly
        #self.expand = True if multiline == True else False
    def create(self,parent):
        flags = 0
        flags |= wx.TE_MULTILINE if self.multiline is True else 0
        flags |= wx.TE_PASSWORD if self.password is True else 0
        flags |= wx.TE_READONLY if self.readonly is True else 0
        self.ctrl = wx.TextCtrl( parent, wx.ID_ANY, self.text, self.pos, self.size, 0|flags )
        drop_target = FileDrop(self)
        self.ctrl.SetDropTarget(drop_target)
        if self.key is not None:
            registerCtrl( self.key, self )
    def drop_handle(self,filenames):
        for filename in filenames:
            self.ctrl.AppendText( filename + '\n' )
            if self.multiline is False:
                break

class Ticker(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    import wx.lib.ticker
    def __init__(self,text="",fgcolor=wx.BLACK,bgcolor=wx.WHITE,expand=True,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Time(Control):
    '''
    Methods Summary
    Properties Summary
    '''
    def __init__(self,date=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.date = date
    def create(self,parent):
        self.ctrl = wx.adv.TimePickerCtrl( parent, wx.ID_ANY, wx.DefaultDateTime, self.pos, self.size, wx.adv.TP_DEFAULT )
        if self.key is not None:
            registerCtrl( self.key, self )


class Tree(Control):
    '''
    Methods Summary
        AppendText(self, text)
        Clear()
        Copy()
    Properties Summary
    '''
    def __init__(self,data=None,collapse=False,handler=None,expand=False,proportion=0,
                 size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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

class Web(Control):
    import wx.lib.iewin
    '''
    Methods Summary
        CanGoBack(self)
        CanGoForward(self)
        CommandStateChange(self, this, command, enable)
        GetStringSelection(self, asHTML=True) Returns the contents of the selected portion of the document as either html or plain text.
        GetText(self, asHTML=True) Returns the contents of the the html document as either html or plain text.
        GoBack(self)
        GoForward(self)
        GoHome(self)
        GoSearch(self)
        LoadStream(self, stream)
        Load the html document from a Python file-like object.
        LoadString(self, html)
        Load the html document from a string
        LoadUrl(self, URL, Flags=0)
        Load the document from url.
        Navigate(self, URL, Flags=0, TargetFrameName=None, PostData=None, Headers=None)
        Print(self, showDialog=False)
        PrintPreview(self)
        Quit(self)
        RefreshPage(self, Level=REFRESH_NORMAL)
        Stop(self)
    Properties Summary
        busy
        document
        locationname
        locationurl
        offline
        readystate
        registerasbrowser
        registerasdroptarget
        silent
        type
    '''
    def __init__(self,url=None,engine='ie',expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.url = url
        self.engine = engine
    def create(self,parent):
        if self.engine == 'ie':
            self.ctrl = wx.lib.iewin.IEHtmlWindow( parent, wx.ID_ANY, self.pos, self.size, 0 )
            if self.url is not None:
                self.ctrl.LoadUrl(self.url)
            if self.key is not None:
                registerCtrl( self.key, self )
                
class PdfWin(Control):
    import wx.lib.pdfwin
    def __init__(self,url=None,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
        self.url = url
    def create(self,parent):
        self.ctrl = wx.lib.pdfwin.PDFWindow( parent, wx.ID_ANY, self.pos, self.size, 0 )
        if self.url is not None:
            self.ctrl.LoadFile(self.url)
        if self.key is not None:
            registerCtrl( self.key, self )

class PdfView(Control):
    import wx.lib.pdfviewer
    def __init__(self,url=None,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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
                
class Media(Control):
    import wx.media
    def __init__(self,url=None,expand=False,proportion=0,size=wx.DefaultSize,pos=wx.DefaultPosition,key=None):
        super().__init__(key,expand,proportion,size,pos)
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


######################################################################
# Dialogs
######################################################################

def OpenFileDialog(defaultDir="",multiple=False,save=False):
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

def onProgressDialog(dlg,percent):
    dlg.Update(percent)

def progressDialogUpdate(dlg,percent):
    wx.CallAfter(onProgressDialog, dlg, percent)

def CalendarDialog(parent=None,year=None,month=None,day=None):
    dlg = wx.lib.CalenDlg(parent,month,day,year)
    #TODO

######################################################################
# WxApp
######################################################################

WxMainWindow = None

def WxAppClose():
    global WxMainWindow
    if WxMainWindow is not None:
        WxMainWindow.frame.Close()

class WxApp():
    def __init__( self, title, width=800, height=600, popup=False ):
        global WxMainWindow
        if popup is False:
            WxMainWindow = self
            self.app = wx.PySimpleApp()
            self.app.locale = wx.Locale(wx.Locale.GetSystemLanguage())
            self.frame = wx.Frame( parent=None, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( width,height ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
            self.frame.Bind(wx.EVT_CLOSE, self.closeEvent)
            registerCtrl( 'WxApp', self )
        else:
            self.frame = wx.Frame( parent=None, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size( width,height ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
        self.frame.Bind(wx.EVT_SHOW, self.openEvent)
        self.frame.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.openHandler = None
        self.closeHandler = None

    def run(self):
        self.frame.Show()
        self.app.MainLoop()

    def close(self):
        self.frame.Close()

    def Show(self):
        self.frame.Show()

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

    def timerStart(key,interval):
        timer = getWxTimer(key)
        if timer is not None and interval > 0:
            timer.Start(interval)

    def timerStop(key):
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
                icon = getToolbarBitmap(value[0])
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

class WxPopup(WxApp):
    def __init__( self, title, width=800, height=600 ):
        super().__init__( title, width=width, height=height, popup=True )
