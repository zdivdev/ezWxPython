import os
import sys
import time
import wx
import ezWxPython as ew

addr = None
web = None
text = None

def onExit(event):
    ew.WxAppClose()
    
def onClose(event): 
    return ew.MessageYesNo("Alert", "Do you want to quit ?" )

def onAbout(event):
    ew.MessageBox("About", "eezWxPython Demo\nzdiv")

def onHome(event):
    web.Stop()

def onForward(event):
    web.Play()

def onGo(event):
    web.Load(addr.GetValue())

def findCtrls():
    global addr, web, text
    addr = ew.getWxCtrl('addr')
    web = ew.getWxCtrl('web')
    text = ew.getWxCtrl('text')
    
menu_def = { 
    "File" : { 
        "Exit" : [onExit, wx.ART_QUIT],  
    }, 
    "Help" : { 
        "About" : [onAbout, wx.ART_HELP],
    },
}

tool_def = [ #icon, text, handler
    [wx.ART_GO_HOME, onHome, "Home" ],
    [wx.ART_GO_FORWARD, onForward, "Forward" ],
]

status_def = [
    ["Ready", -1],  
]

url = r'D:/video.mp4'

body_def = [
    [ ew.Label ("Address: "), 
      ew.Text  (url,key="addr",expand=True,proportion=1),
      ew.Button("Go",handler=onGo),
    ],
    [ ew.VerticalSpliter([
        600,
        [ 
            [ ew.Media(url,key='web',expand=True,proportion=1),
              { 'expand':True, 'proportion':1 } ],
        ],
      ], expand=True,proportion=1),
      { 'expand':True, 'proportion':1 }
    ],
]

layout = {
    "menu"   : menu_def, 
    "tool"   : tool_def, 
    "status" : status_def, 
    "body"   : body_def, 
}


if __name__ == "__main__":
    window = ew.WxApp(u"ezwxApp", 900, 620)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    findCtrls()
    window.run()

