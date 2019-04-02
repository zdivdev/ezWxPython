import os
import sys
import time
import threading
import ezWxPython as ezwx

######################################################################
# Global 
######################################################################

title = u"Gauge Demo"
window = None

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
    ezwx.MessageBox("About", title + "\nzdiv")
   
def threadProgress(progress):
    for i in range(0,301):
        #if i % 50 == 49:
        #    progress.pulse()
        progress.update(i)
        time.sleep(0.01)

def onButton(event):
    progress = ezwx.getCtrl('progress')
    progress.setMaxValue(300)
    thread = threading.Thread(target=threadProgress, args=(progress,))
    thread.daemon = True
    thread.start()
    
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
    [ ezwx.Gauge(expand=True,proportion=1,key="progress"), ], 
    [ ezwx.Button("Show Progress",expand=True,proportion=1,handler=onButton,key="button"),
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
    window = ezwx.WxApp(title, 120, 160)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    window.run()
