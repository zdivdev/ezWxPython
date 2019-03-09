import os
import sys
import time
import ezWxPython as ezwx

######################################################################
# Global 
######################################################################

window = None

def setStatusText(text,index=0):
    if window is not None and window.statusbar is not None:
        if index < window.statusbar.GetFieldsCount():
            window.statusbar.SetStatusText(text,index)

######################################################################
# Handler
######################################################################

def onExit(event):
    ezwx.WxAppClose()

def onClose(event): #return True if want to exit
    rv = ezwx.MessageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    ezwx.MessageBox("About", "StyledTextCtrl Demo\nzdiv")

def onDirSelect(event):
    ctrl = ezwx.getWxCtrl('dir')
    print(event.GetPath())
    print(ctrl.GetPath())
    
def onFileSelect(event):
    ctrl = ezwx.getWxCtrl('file')
    print(event.GetPath())
    print(ctrl.GetPath())

def onDateSelect(event):
    ctrl = ezwx.getWxCtrl('date')
    print(event.GetDate())
    print(ctrl.GetValue())

def onTimeSelect(event):
    ctrl = ezwx.getWxCtrl('time')
    print(event.GetDate())
    print(ctrl.GetValue())
    
def onColorSelect(event):
    ctrl = ezwx.getWxCtrl('color')
    print(event.GetColour())
    print(ctrl.GetColour()) 
    
def onFontSelect(event):
    ctrl = ezwx.getWxCtrl('font')
    font = event.GetFont()
    print(font.GetFaceName(), font.GetFamily(), font.GetPixelSize(), font.GetPointSize())
    font = ctrl.GetSelectedFont()
    print(font.GetFaceName(), font.GetFamily(), font.GetPixelSize(), font.GetPointSize())
    font = ctrl.GetFont()
    print(font.GetFaceName(), font.GetFamily(), font.GetPixelSize(), font.GetPointSize())
    

def onDirSelect2(event):
    ctrl = ezwx.getWxCtrl('dir2')
    print(event.GetPath())
    print(ctrl.GetPath())
    
def onFileSelect2(event):
    ctrl = ezwx.getWxCtrl('file2')
    print(event.GetPath())
    print(ctrl.GetPath())

def onDateSelect2(event):
    ctrl = ezwx.getWxCtrl('date2')
    print(event.GetDate())
    print(ctrl.GetValue())

def onTimeSelect2(event):
    ctrl = ezwx.getWxCtrl('time2')
    print(event.GetDate())
    print(ctrl.GetValue())
          
def onColorSelect2(event):
    ctrl = ezwx.getWxCtrl('color2')
    print(event.GetColour())
    print(ctrl.GetColour()) 
    
def onFontSelect2(event):
    ctrl = ezwx.getWxCtrl('font2')
    font = event.GetFont()
    print(font.GetFaceName(), font.GetFamily(), font.GetPixelSize(), font.GetPointSize())    
    font = ctrl.GetSelectedFont()
    print(font.GetFaceName(), font.GetFamily(), font.GetPixelSize(), font.GetPointSize())
    font = ctrl.GetFont()
    print(font.GetFaceName(), font.GetFamily(), font.GetPixelSize(), font.GetPointSize())
        
######################################################################
# Layout
######################################################################

menu_def = { 
    "File" : { 
        "Exit" : onExit,
        }, 
    "Help" : { 
        "About" : onAbout 
        },
}

status_def = [
    ["Ready", -1],
]

body_def = [
    [ ezwx.Picker("dir",  expand=True, proportion=1, handler=onDirSelect, key="dir"),], 
    [ ezwx.Picker("file", expand=True, proportion=1, handler=onFileSelect, key="file"),], 
    [ ezwx.Picker("date",expand=True, handler=onDateSelect, key="date"),], 
    [ ezwx.Picker("time",expand=True, handler=onTimeSelect, key="time"),], 
    [ ezwx.Picker("color",expand=True, handler=onColorSelect, key="color"),], 
    [ ezwx.Picker("font", expand=True, size=(240,72), handler=onFontSelect, key="font"),],     
    [ ezwx.Line(),],     
    [ ezwx.DirPicker(expand=True, proportion=1, handler=onDirSelect2, key="dir2"),], 
    [ ezwx.FilePicker(expand=True, proportion=1, handler=onFileSelect2, key="file2"),], 
    [ ezwx.DatePicker(expand=True, handler=onDateSelect2, key="date2"),], 
    [ ezwx.TimePicker(expand=True, handler=onTimeSelect2, key="time2"),], 
    [ ezwx.ColorPicker(expand=True, handler=onColorSelect2, key="color2"),], 
    [ ezwx.FontPicker(expand=True, size=(240,72), handler=onFontSelect2, key="font2"),],     
]


layout = {
    "menu"   : menu_def,
    "status" : status_def, 
    "body"   : body_def, 
}

######################################################################
# Main
######################################################################

if __name__ == "__main__":
    window = ezwx.WxApp(u"wxPython Template", 480, 480)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    window.run()
