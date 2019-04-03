import os
import sys
import time
import wx
import ezWxPython as ew

window = None

def findCtrls():
    global status, addr, video, url, progress, volume, timer, time
    status = window.statusbar
    addr = ew.getWxCtrl('addr')
    video = ew.getWxCtrl('media')
    video.SetVolume(0.5)
    url = ew.getWxCtrl('url')
    progress = ew.getWxCtrl('progress')
    progress.SetRange(0,1000)
    progress.SetValue(0)
    volume = ew.getWxCtrl('volume')
    volume.SetRange(0,100)
    volume.SetValue(100*video.GetVolume())
    time = ew.getWxCtrl('time')
    
def onExit(event):
    ew.WxAppClose()
    
def onClose(event):
    rv = ew.MessageYesNo("Alert", "Do you want to quit ?" )
    if rv == True:
        window.timerStop('timer')
    return rv

def onAbout(event):
    ew.MessageBox("About", "MediaCtrl Demo\nzdiv")

def onIdle(event):
    pass
    
def onTimer(event):
    state = video.GetState()
    if state == wx.media.MEDIASTATE_PLAYING:        
        length = video.Length()
        if length != 0:
            tell = video.Tell()
            ss = tell / 1000;
            hh = ss / 3600
            mm = (ss % 3600) / 60
            ss = ss % 60
            time.SetLabel("%02d:%02d.%02d" % (hh, mm, ss))
            progress.SetValue(1000*tell/length)

def onProgress(event):
    length = video.Length()
    p = progress.GetValue()
    video.Seek(p*length/1000)
    
def onHome(event):
    state = video.GetState()
    if state != wx.media.MEDIASTATE_STOPPED:
        video.Stop()
        status.SetStatusText("Stopped")

def onBack(event):
    state = video.GetState()
    if state == wx.media.MEDIASTATE_PLAYING:
        video.Pause()
        status.SetStatusText("Paused")

def onForward(event):
    state = video.GetState()
    if state != wx.media.MEDIASTATE_PLAYING:
        video.Play()
        status.SetStatusText("Playing")

def onLoad(event):
    video.Load(url.GetValue())
   
menu_def = { 
    "File" : { 
        "Exit" : [onExit, wx.ART_QUIT],  
    }, 
    "Help" : { 
        "About" : [onAbout, wx.ART_HELP],
    },
}

tool_def = [ #icon, text, handler
    [wx.ART_GO_HOME, onHome, "Stop" ],
    [wx.ART_GO_BACK, onBack, "Pause" ],
    [wx.ART_GO_FORWARD, onForward, "Play" ],
]

status_def = [
    ["Ready", -1],  
]

def_url = r'D:/video.wmv'

body_def = [
    [ ew.Label ("Address: "), 
      ew.Text  (def_url,expand=True,proportion=1,key="url"),
      ew.Button("Load",handler=onLoad),
    ],
    [ ew.Media(def_url,expand=True,proportion=1,key='media'),
      { 'expand':True, 'proportion':1 }
    ],
    [ ew.Label("00:00:00", key='time'), ew.Slider(expand=True,proportion=1,handler=onProgress,key='progress'),
      ew.Label("Volume: "), ew.Slider(expand=True,key='volume'),
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
    findCtrls()
    window.closeHandle(onClose)
    window.idleHandle(onIdle)
    window.timerHandle(onTimer,100,start=True,key='timer')
    window.run()

