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

def onOpen(event):
    filename = ezwx.OpenFileDialog()
    if filename is not None:
        stc = ezwx.getWxCtrl('stc')

def onClear(event):
    setStatusText("Clear",0)
    stc = ezwx.getWxCtrl('stc')
    if stc is not None:
        stc.ClearAll()

def onCopy(event):
    setStatusText("Copy",0)
    stc = ezwx.getWxCtrl('stc')
    if stc is not None:
        stc.Copy()

def onPaste(event):
    setStatusText("Paste",0)
    stc = ezwx.getWxCtrl('stc')
    if stc is not None:
        stc.Paste()

def onAbout(event):
    ezwx.MessageBox("About", "StyledTextCtrl Demo\nzdiv")

######################################################################
# Layout
######################################################################

menu_def = { 
    "File" : { 
        "Open" : onOpen,
        "-" : None,
        "Exit" : onExit,
    }, 
    "Edit" : { 
        "Clear" : onClear,
        "Copy"  : onCopy,
        "Paste" : onPaste,
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

status_def = [
    ["Ready", -1],
]

body_def = [
    [ ezwx.StyledText(expand=True,proportion=1,key="stc"), True], 
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
    window = ezwx.WxApp(u"StyledTextCtrl Demo", 600, 480)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    window.run()
    
