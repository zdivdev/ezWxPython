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

def onOpen(event): 
    tree = ezwx.getWxCtrl('tree')
    if tree is not None:
        root = tree.AddRoot('Root')
        for i in range(10):
            name1 = 'Item_' + str(i)
            node = tree.AppendItem(root,name1)
            for k in range(10):
                name2 = name1 + '_' + str(k)
                tree.AppendItem(node,name2)
        tree.ExpandAllChildren(root)
    
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
    [ ezwx.Tree(expand=True,proportion=1,key="tree"),
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
    window.openHandle(onOpen)
    window.run()
