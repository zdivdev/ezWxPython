import os
import sys
import time
import wx
import ezWxPython as ew

def initCtrls():
    ew.getWxCtrl('top1').SetBackgroundColour(wx.Colour(200,200,240))
    
def onExit(event):
    appWin.close()
   
def onAbout(event):
    appWin.messageBox("About", "Control Demo\nzdiv")

def onGo(event):
    kind = ew.getValue('kind')
    action = ew.getValue('action')
    if action == 'get':
        ew.setValue('value',ew.getValue(kind))
    if action == 'set':
        ew.setValue(kind,ew.getValue('value'))
    if action == 'fg':
        ew.setValue('value',ew.getValue(kind))
    if action == 'bg':
        ew.setValue(kind,ew.getValue('value'))
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Choice(['label','button','text','choice','combo','list'], key='kind'),
      ew.Choice(['set','get','fg','bg'], key='action'),
      ew.Text("",key='value'),
      ew.Button("Go",handler=onGo),
    ], 
    [ ew.Label("Label: ",expand=True),
      ew.Label("Value",expand=True,proportion=1,key='label',size=(64,-1)), ],
    [ ew.Label("Button: ",expand=True),
      ew.Button("Value",expand=True,proportion=1,key='button',size=(64,-1)), ],
    [ ew.Label("Text: ",expand=True),
      ew.Text("Value",expand=True,proportion=1,key='text',size=(64,-1)), ],
    [ ew.Label("Choice: ",expand=True),
      ew.Choice(['apple','lemon'],expand=True,size=(64,-1),proportion=1,key='choice'), ],
    [ ew.Label("Combo: ",expand=True),
      ew.Combo(['apple','lemon'],expand=True,size=(64,-1),proportion=1,key='combo'),], 
    [ ew.Label("List: ",expand=True),
      ew.List(['apple','lemon'],expand=True,size=(64,-1),proportion=1,key='list'),],       
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
    appWin = ew.WxApp(u"Control Demo", 320, 480)
    appWin.makeLayout(layout)
    appWin.run()
