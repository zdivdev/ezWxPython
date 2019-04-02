import os
import sys
import time
import wx
import ezWxPython as ew

number = 10

def initCtrls():
    global number
    number = 10
    
def onExit(event):
    appWin.close()
   
def onClose(event): #return True if want to exit
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    appWin.messageBox("About", "Menu Demo\nzdiv")

def onTimer(event):
    global number
    led = ew.getWxCtrl('led')
    led.SetValue("00:" + str(number))
    number += 1

menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.LedNumber(str(number),expand=True,proportion=1,key='led'), 
      { 'expand' : True, 'proportion' : 1 }
    ],
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
    appWin = ew.WxApp(u"Menu Demo", 320, 320)
    appWin.makeLayout(layout)
    initCtrls()
    appWin.closeHandle(onClose)
    appWin.timerHandle(onTimer,1000,start=True,key='timer')
    appWin.run()
