import os
import sys
import time
import wx
import ezWxPython as ew

def initCtrls():
    ew.getWxCtrl('top1').SetBackgroundColour(wx.Colour(200,200,240))
    ew.getWxCtrl('top2').SetBackgroundColour(wx.Colour(180,180,240))
    ew.getWxCtrl('top3').SetBackgroundColour(wx.Colour(160,160,240))
    ew.getWxCtrl('mid').SetBackgroundColour(wx.Colour(200,240,200))
    ew.getWxCtrl('bottom1').SetBackgroundColour(wx.Colour(240,200,200))
    ew.getWxCtrl('bottom21').SetBackgroundColour(wx.Colour(240,180,180))
    ew.getWxCtrl('bottom22').SetBackgroundColour(wx.Colour(240,180,180))
    ew.getWxCtrl('bottom23').SetBackgroundColour(wx.Colour(240,180,180))
    ew.getWxCtrl('bottom3').SetBackgroundColour(wx.Colour(240,160,160))

def onExit(event):
    appWin.close()
   
def onClose(event): #return True if want to exit
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    appWin.messageBox("About", "SimpleBook Demo\nzdiv")

def onBook1(event):
    effect = appWin.getSelectedText('effect')
    appWin.setBookEffect('book',effect)
    appWin.setBookPage('book',0)
    
def onBook2(event):
    effect = appWin.getSelectedText('effect')
    appWin.setBookEffect('book',effect)
    appWin.setBookPage('book',1)
    
menu_def = { 
    "File" : { 
        "Exit" : [ onExit, wx.ART_QUIT ],
    }, 
    "Help" : { 
        "About" : onAbout 
    },
}

body_def = [
    [ ew.Choice(['slide_to_left','slide_to_right','slide_to_top','slide_to_bottom',
                 'roll_to_left','roll_to_right','roll_to_top','roll_to_bottom',
                 'blend', 'expand', 'none', ], key='effect'),
      ew.Button('Book1', handler=onBook1), 
      ew.Button('Book2', handler=onBook2), 
    ],
    [ ew.Simplebook( [
        [
            [ ew.Label("Top1",expand=True,proportion=1,key='top1'),
              ew.Label("Top2",expand=True,proportion=2,key='top2'),
              ew.Label("Top3",expand=True,proportion=3,key='top3'),
              { 'expand' : True, 'proportion' : 1 }
            ], 
            [ ew.Label("Mid",expand=True,proportion=1,key='mid'),
              { 'expand' : True, 'proportion' : 2 } 
            ], 
        ],
        [
            [ ew.Label("Bottom1",expand=True,proportion=1,border=0,key='bottom1'), 
              ew.Panel( [
                [ ew.Label("Bottom21",expand=True,proportion=1,border=1, key='bottom21'), 
                  ew.Label("Bottom22",expand=True,proportion=1,border=1, key='bottom22'), 
                  ew.Label("Bottom23",expand=True,proportion=1,border=1, key='bottom23'), 
                    { 'expand' : True, 'proportion' : 1, 'border' : 0 }
                ],
                [ ew.Label("Bottom3",expand=True,proportion=1,border=0,key='bottom3'), 
                    { 'expand' : True, 'proportion' : 2, 'border' : 0 }
                ],
              ], expand=True,proportion=1, border=0),
              { 'expand' : True, 'proportion' : 3, 'border' : 0 } 
            ],
        ],
      ], expand=True, proportion=1, key='book'),
      { 'expand' : True, 'proportion' : 1, 'border' : 0 } 
    ]
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
    appWin = ew.WxApp(u"SimpleBook Demo", 320, 240)
    appWin.makeLayout(layout)
    appWin.closeHandle(onClose)
    initCtrls()
    appWin.run()
