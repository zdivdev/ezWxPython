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
    if action == 'getLabel':
        ew.setValue('value',ew.getLabel(kind))
    elif action == 'setLabel':
        ew.setLabel(kind,ew.getValue('value'))
    elif action == 'getValue':
        ew.setValue('value',str(ew.getValue(kind)))
    elif action == 'setValue':
        ew.setValue(kind,ew.castValue(kind,ew.getValue('value')))
    elif action == 'appendValue':
        ew.appendValue(kind,ew.getValue('value'))
    elif action == 'removeValue':
        ew.removeValue(kind,ew.getValue('value'))
    elif action == 'setFgColor':
        ew.setFgColor(kind,wx.Colour(0,0,255))
    elif action == 'setBgColor':
        ew.setBgColor(kind,wx.Colour(255,0,0))
        
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Choice(['label','button','toggle','check','text','choice','combo','list','date','time'], key='kind'),
      ew.Choice(['getLabel','setLabel','getValue','setValue','appendValue','removeValue','setFgColor','setBgColor'], key='action'),
      ew.Text("",key='value'),
      ew.Button("Go",handler=onGo),
    ], 
    [ ew.Label("Label: ",expand=True),
      ew.Label("Value",expand=True,proportion=1,key='label',size=(64,-1)), ],
    [ ew.Label("Button: ",expand=True),
      ew.Button("Button",expand=True,proportion=1,key='button',size=(64,-1)), ],
    [ ew.Label("ToggleButton: ",expand=True),
      ew.ToggleButton("ToggleButton",value=True,expand=True,proportion=1,key='toggle',size=(64,-1)), ],
    [ ew.Label("CheckButton: ",expand=True),
      ew.CheckButton("CheckButton",value=True,expand=True,proportion=1,key='check',size=(64,-1)), ],
    [ ew.Label("Text: ",expand=True),
      ew.Text("Text",expand=True,proportion=1,key='text',size=(64,-1)), ],
    [ ew.Label("Choice: ",expand=True),
      ew.Choice(['apple','lemon'],expand=True,size=(64,-1),proportion=1,key='choice'), ],
    [ ew.Label("Combo: ",expand=True),
      ew.Combo(['apple','lemon'],expand=True,size=(64,-1),proportion=1,key='combo'),], 
    [ ew.Label("List: ",expand=True),
      ew.List(['apple','lemon'],expand=True,size=(64,-1),proportion=1,key='list'),],       
    [ ew.Label("Date: ",expand=True),
      ew.Date(expand=True,size=(64,-1),proportion=1,key='date'),],       
    [ ew.Label("Time: ",expand=True),
      ew.Time(expand=True,size=(64,-1),proportion=1,key='time'),],       
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
    appWin = ew.WxApp(u"Control Demo", 400, 480)
    appWin.makeLayout(layout)
    appWin.run()
