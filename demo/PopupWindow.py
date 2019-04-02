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

# Popup Window

def onPopupExit(event):
    popup_window.close()
    
popup_menu_def = { 
    "Exit" : [onPopupExit, None],  # Menu item with base64-encoded icon image
}

popup_body_def = [
    [ ew.Label("Hello ezWxPython",expand=True,proportion=1,key='popup_label'), 
      { 'expand' : True, 'proportion' : 1 } ], 
]

popup_layout = {
    "body"   : popup_body_def, 
}

def onPopup(event):
    global popup_window
    popup_window = ew.WxPopup(u"Popup Window", 200, 160)
    popup_window.makeLayout(popup_layout)
    label = ew.getWxCtrl('popup_label')
    label.SetBackgroundColour(wx.Colour(200,240,240))
    popup_window.show()
    
def onMini(event):
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
    [ ew.Button("Popup Window",handler=onPopup,expand=True,proportion=1,),
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
    appWin = ew.WxApp(u"Menu Demo", 320, 240)
    appWin.makeLayout(layout)
    initCtrls()
    appWin.closeHandle(onClose)
    appWin.run()
