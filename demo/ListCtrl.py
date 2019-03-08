import os
import sys
import time
import ezWxPython as ezwx

######################################################################
# Global 
######################################################################

window = None

def findControls():
    pass
    
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
    [ ezwx.List([[('Name',100,-1),('Sex',32,0),('Age',64,1)], #label, width, align
                 ["Willy","M","32"],
                 ["Jane","F","28"],
        ], expand=True, proportion=1, multicol=True),
      { 'expand' : True, 'proportion' : 1 } ], 
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
    window = ezwx.WxApp(u"wxPython Template", 300, 200)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    findControls()
    window.run()
