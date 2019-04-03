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
    appWin.messageBox("About", "Icon Maker\nzdiv (2018.4.1)")

def guiUpdate(text):
    def textAppend():
        appWin.appendText('text',text)
    return textAppend
    
def worker(args):
    files = os.listdir(args)
    for f in files:
        name,ext = os.path.splitext(f)
        if ext != '.png':
            continue
        icon_name = f.replace('.','_') 
        icon_data = ew.encodeIconToStr(os.path.join(args,f))
        data = "%-32s = '%s'\n" % (icon_name, icon_data)
        ew.callAfter(guiUpdate(data))
            
def onMake(event):
    folder = appWin.getText('folder')
    ew.threadHandle(worker, start=True, daemon=True, args=(folder,), key='worker')    
  
def onThreadAction(arg1):
    AppendToText('[Thread] ' + str(arg1))
    

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
    [ ew.FileBrowser("Icon Folder: ", "", "Browse", key='folder', directory=True, expand=True, proportion=1 ) ],
    [ ew.Text(expand=True,proportion=1,multiline=True,readonly=True,key="text"), 
      { 'expand' : True, 'proportion': 1 }
    ], 
    [   None,
        ew.Button("Make",handler=onMake,expand=True) ],
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
    appWin = ew.WxApp("Icon Maker", 600, 480)
    appWin.makeLayout(layout)
    appWin.closeHandle(onClose)
    appWin.run()
