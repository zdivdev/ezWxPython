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

def onBack(event):
    web.PageUp()

def onForward(event):
    web.PageDown()

def onGo(event):
    web.LoadFile(addr.GetValue())
    
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
    [wx.ART_GO_BACK, onBack, "Back" ],
    [wx.ART_GO_FORWARD, onForward, "Forward" ],
]

status_def = [
    ["Ready", -1],  
]

url = r'D:/a.pdf'

body_def = [
    [ ew.Label ("Address: "), 
      ew.Text  (url,key="addr",expand=True,proportion=1),
      ew.Button("Go",handler=onGo),
    ],
    [ ew.VerticalSpliter([
        600,
        [ 
            [ ew.PdfView(url,key='web',expand=True,proportion=1),
              { 'expand':True, 'proportion':1 } ],
        ],
        300,
        [
            [ ew.StyledText(key='text',expand=True,proportion=1),
              { 'expand':True, 'proportion':1 }],
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

