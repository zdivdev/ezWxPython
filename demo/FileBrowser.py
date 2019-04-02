import os
import sys
import time
import ezWxPython as ew

######################################################################
# Handler
######################################################################

def onExit(event):
    appWin.close()

def onClose(event):
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    appWin.messageBox("About", "TextFileBrowser Demo\nzdiv")

def onFileBrowse(filename):
    browser = ew.getWxCtrl('file')
    text = ew.getWxCtrl('text')
    text.AppendText(browser.GetValue() + "\n")
    text.AppendText(filename + "\n")

def onDirBrowse(filename):
    browser = ew.getWxCtrl('dir')
    text = ew.getWxCtrl('text')
    text.AppendText(browser.GetValue() + "\n")
    text.AppendText(filename + "\n")
    
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
    [ ew.FileBrowser("Input File: ", "", "Open", handler=onFileBrowse, key='file', save=False, expand=True, proportion=1, border=1 ) ],
    [ ew.FileBrowser("Output Folder: ", "", "Browse", handler=onDirBrowse, key='dir', directory=True, expand=True, proportion=1, border=0 ) ],
    [ ew.Text(expand=True,proportion=1,multiline=True,readonly=True,key="text"), 
      { 'expand' : True, 'proportion': 1 }
    ], 
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
    appWin = ew.WxApp("TextFileBrowser Demo", 600, 480)
    appWin.makeLayout(layout)
    appWin.closeHandle(onClose)
    appWin.run()
