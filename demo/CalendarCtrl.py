import os
import sys
import time
import wx
import ezWxPython as ew

def initCtrls():
    global cal
    cal = ew.getWxCtrl('cal')
    cal.SetBackgroundColour(wx.Colour(200,200,240))
    
def onExit(event):
    appWin.close()
   
def onClose(event): #return True if want to exit
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    appWin.messageBox("About", "Menu Demo\nzdiv")

def onCalendar(event):
    appWin.appendText('text', appWin.getCalendarDate('cal') + '\n')
    
def onGetDate(event):
    date = cal.GetDate()
    appWin.appendText('text', date.Format('[%Y-%m-%d]\n'))
    
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Calendar(handler=onCalendar,expand=True,proportion=1,key='cal'), ],
    [ ew.Button('GetDate',handler=onGetDate,expand=True,proportion=1), ],
    [ ew.Text("",multiline=True,expand=True,proportion=1,key='text'), 
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
    appWin = ew.WxApp(u"Menu Demo", 320, 480)
    appWin.makeLayout(layout)
    initCtrls()
    appWin.closeHandle(onClose)
    appWin.run()
