import os
import sys
import time
import wx
import ezWxPython as ew

def onExit(event):
    appWin.close()
   
def onClose(event): #return True if want to exit
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    if rv is True:
        appWin.setTickerStop('ticker')
    return rv
   
def onAbout(event):
    appWin.messageBox("About", "Ticker Demo\nzdiv")

def onTextApply(event):
    text = appWin.getText('deftext')
    appWin.setTickerText('ticker',text)
  
def onPPFApply(event):
    text = appWin.getText('ppf')
    appWin.setTickerPPF('ticker',int(text))
  
def onFPSApply(event):
    text = appWin.getText('fps')
    appWin.setTickerFPS('ticker',int(text))
    
def onFont(event):
    font = ew.getWxCtrl('font')
    appWin.setTickerFont('ticker',font.GetSelectedFont())
    
def onStart(event):
    appWin.setTickerStart('ticker')
  
def onStop(event):
    appWin.setTickerStop('ticker')

def onRight(event):
    appWin.setTickerDirection('ticker','right')

def onLeft(event):
    appWin.setTickerDirection('ticker','left')
    
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Ticker(text="Default Ticker Text",fgcolor=wx.BLACK,bgcolor=wx.WHITE,key='ticker',expand=True,proportion=1,) ],
    [ ew.Line() ],
    [ ew.Text('New Ticker Value', expand=True,proportion=1,key='deftext'), 
      ew.Button("Apply",handler=onTextApply), ],
    [ ew.Label("PPF: "),
      ew.Text('2', expand=True,key='ppf',size=(32,-1)), 
      ew.Button("Apply",handler=onPPFApply,size=(64,-1)), 
      ew.Label("FPS: "),
      ew.Text('20', expand=True,key='fps',size=(64,-1)), 
      ew.Button("Apply",handler=onFPSApply,size=(64,-1)), 
      ew.Label("Font: "),
      ew.FontPicker(handler=onFont,key='font'), 
      ],
    [ None,
      ew.Button("Start",handler=onStart),
      ew.Button("Stop",handler=onStop),
      ew.Button("L > R",handler=onRight),
      ew.Button("L < R",handler=onLeft),
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
    appWin = ew.WxApp(u"Ticker Demo", 480, 240)
    appWin.makeLayout(layout)
    appWin.closeHandle(onClose)
    appWin.run()
