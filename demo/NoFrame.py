import os
import sys
import time
import wx
import ezWxPython as ew

def initCtrls():
    global label, idlecount, timercount
    label = ew.getWxCtrl('label')
    label.SetBackgroundColour(wx.Colour(200,200,240))
    idlecount = 0
    timercount = 0
    
def onExit(event):
    appWin.close()
   
def onClose(event): #return True if want to exit
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    appWin.messageBox("About", "Menu Demo\nzdiv")

menu_def = { 
    "File" : { 
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

layout = {
    "body"   : body_def, 
}

######################################################################
# Main
######################################################################

if __name__ == "__main__":
    appWin = ew.WxApp(u"Menu Demo", 320, 240)
    appWin.makeLayout(layout)
    initCtrls()
    appWin.closeHandle(onClose)
    appWin.noCaption()
    appWin.dragEnable('label')
    appWin.contextMenu(menu_def,'label')
    appWin.run()
