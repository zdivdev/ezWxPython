import os
import sys
import time
import wx
import ezWxPython as ew

def initCtrls():
    global label
    label = ew.getWxCtrl('label')
    label.SetBackgroundColour(wx.Colour(200,200,240))
    
def setStatusText(text,index=0):
    appWin.setStatusText(text,index)

def onExit(event):
    appWin.close()
   
def onClose(event): #return True if want to exit
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    appWin.messageBox("About", "Menu Demo\nzdiv")

def getMenuHandler(text):
    def onMenu(event):
        appWin.messageBox("Alert", text + ' Pressed')
    return onMenu
    
menu_def = { 
    "File" : { 
        "Options" : { "Option1" : getMenuHandler("Option1"),  
                      "Option2" : { 
                            "Option2-1" : getMenuHandler("Option2-1"), 
                            "Option2-2" : getMenuHandler("Option2-2"), 
                        }
                    },
        "Settings" : None,
        "-" : None,
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Label("Hello ezWxPython",expand=True,proportion=1,key='label'),
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
    appWin.closeHandle(onClose)
    initCtrls()
    appWin.run()
