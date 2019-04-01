import os
import sys
import time
import wx
import ezWxPython as ew

def onExit(event):
    appWin.close()
   
def onAbout(event):
    appWin.messageBox("About", "TextEntry Demo\nzdiv")

def onButton(event):
    value = appWin.getText('deftext')
    value = appWin.textEntryDialog("Text Entry Demo", "Enter your name", value=value)
    appWin.appendText('text',value + '\n')
  
    
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Text('Default Value', expand=True,proportion=1,key='deftext'), 
      ew.Button("Dialog",handler=onButton,key='button'), ],
    [ ew.Line() ],
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
    appWin = ew.WxApp(u"Menu Demo", 320, 240)
    appWin.makeLayout(layout)
    appWin.run()
