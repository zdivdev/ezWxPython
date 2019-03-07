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

######################################################################
# Layout
######################################################################

tree_data = [ 'Root', 
    ['Item-1', [ 'Item-1.1', 'Item-1.2' ],
     'Item-2', 
     'Item-3', [ 'Item-3.1', 'Item-3.2', 'Item-3.3' ],
    ] 
 ]
    
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
    [ ezwx.Tree(data=tree_data,expand=True,proportion=1,key="tree"),
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
    window = ezwx.WxApp(u"wxPython Template", 600, 480)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    window.run()
