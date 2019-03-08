import os
import sys
import time
import ezWxPython as ezwx

######################################################################
# Global 
######################################################################

window = None
web = None
addr = None

def findControls():
    global web
    global addr
    web = ezwx.getWxCtrl('web')
    addr = ezwx.getWxCtrl('addr')
    
def setStatusText(text,index=0):
    if window is not None and window.statusbar is not None:
        if index < window.statusbar.GetFieldsCount():
            window.statusbar.SetStatusText(text,index)

######################################################################
# Handler
######################################################################

def onExit(event):
    ezwx.WxAppClose()

def onClose(event): #return True if want to exit
    rv = ezwx.MessageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    ezwx.MessageBox("About", "StyledTextCtrl Demo\nzdiv")

def onHome(event):
    global web
    web.GoHome()    

def onBack(event):
    global web
    if web.CanGoBack():
        web.GoBack()

def onForward(event):
    global web
    if web.CanGoForward():
        web.GoForward()

def onGo(event):
    global web, addr
    web.LoadUrl(addr.GetValue())
      
######################################################################
# Layout
######################################################################

menu_def = { 
    "File" : { 
        "Exit" : onExit,
        }, 
    "Help" : { 
        "About" : onAbout 
        },
}

status_def = [
    ["Ready", -1],
]

body_def = [
    [ ezwx.Button('Home',handler=onHome),
      ezwx.Button('Back',handler=onBack),
      ezwx.Button('Forward',handler=onForward),
    ],
    [ ezwx.Label('Address: '),
      ezwx.Text('https://www.google.com',proportion=1,key='addr'),
      ezwx.Button('Go',handler=onGo),
    ],
    [ ezwx.Web("https://www.google.com",expand=True,proportion=1,key="web"),
      { 'expand' : True, 'proportion' : 1 } ], 
]

layout = {
    "menu"   : menu_def,
    "status" : status_def, 
    "body"   : body_def, 
}

######################################################################
# Main
######################################################################

if __name__ == "__main__":
    window = ezwx.WxApp(u"wxPython Template", 600, 480)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    findControls()
    window.run()
