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
    defaultDir = appWin.getText('dir')
    directory = appWin.directoryDialog(defaultPath=defaultDir);
    appWin.appendText('text',directory + '\n')
    
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Label("Default Dir:"),
      ew.Text("D:\\",expand=True,proportion=1,key='dir'),
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
    appWin = ew.WxApp(u"Directory Dialog Demo", 320, 240)
    appWin.makeLayout(layout)
    appWin.run()
