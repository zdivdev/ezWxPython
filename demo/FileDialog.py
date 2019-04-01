import os
import sys
import time
import wx
import ezWxPython as ew

def onExit(event):
    appWin.close()
   
def onAbout(event):
    appWin.messageBox("About", "Menu Demo\nzdiv")

def onButton(event):
    multiple = appWin.getCheckState('multiple')
    files = appWin.openFileDialog( multiple = multiple );
    for f in files:
        appWin.appendText('text',f + '\n')
    
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Check("Enable multiple selection",expand=True,proportion=1,key='multiple'),
      ew.Button("Open", handler=onButton), ], 
    [ ew.Text('',multiline=True,expand=True,proportion=1,key='text'),
      { 'expand' : True, 'proportion' : 1 } ], 
]

status_def = [
    ["Ready", -1],
]

layout = {
    "menu"   : menu_def,
    "body"   : body_def, 
    "status"   : status_def, 
}

######################################################################
# Main
######################################################################

if __name__ == "__main__":
    appWin = ew.WxApp(u"File Dialog Demo", 320, 240)
    appWin.makeLayout(layout)
    appWin.run()
