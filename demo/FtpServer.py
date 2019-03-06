import os
import sys
import time
import ezWxPython as ezwx

######################################################################
# Global 
######################################################################

window = None

def setStatusText(text,index=0):
    if window is not None and window.statusbar is not None:
        if index < window.statusbar.GetFieldsCount():
            window.statusbar.SetStatusText(text,index)


def getTextValue(key):
    ctrl = ezwx.getWxCtrl(key)
    if ctrl is not None:
        return ctrl.GetLineText(0)
    return None

def AppendToText(text):
    ctrl = ezwx.getWxCtrl('text')
    if ctrl is not None:
        ctrl.write( text + "\n" )
        
def printLog(text):
    AppendToText(text)

def onThread():
    from time import sleep
    while ezwx.isWxAppRun():
        ezwx.callAfter(printLog,text)
        sleep(1.0)    

######################################################################
# FTPServer
######################################################################

import logging
class logHandler(logging.Handler):
    terminator = '\n'
    def __init__(self, stream=None):
        logging.Handler.__init__(self)
    def flush(self):
        pass
    def emit(self, record):
        msg = self.format(record)
        print( 'PYLOG:' + msg)
        #print(self.terminator)
        self.flush()
    def __repr__(self):
        return "PYLOG"

def runFtpServer(host,port,user,passwd,home):
    from pyftpdlib.authorizers import DummyAuthorizer
    from pyftpdlib.handlers import FTPHandler
    from pyftpdlib.servers import FTPServer
    
    authorizer = DummyAuthorizer()
    authorizer.add_user(user,passwd,home, perm="elradfmwMT")
    authorizer.add_anonymous("D:/Temp1")
    
    handler = FTPHandler
    handler.authorizer = authorizer
    
    server = FTPServer((host,int(port)), handler)

    logger = logging.getLogger('pyftpdlib')
    logger.setLevel(logging.INFO)
    logger.addHandler(logHandler())

    server.serve_forever()

######################################################################
# Handler
######################################################################

def onExit(event):
    ezwx.WxAppClose()

def onClose(event): #return True if want to exit
    rv = ezwx.MessageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onAbout(event):
    ezwx.MessageBox("About", "Easy FTPServer\nzdiv")

def onHomeButton(event):
    folder = ezwx.DirectoryDialog()
    if folder is not None:
        ctrl = ezwx.getWxCtrl('home')
        if ctrl is not None:
            ctrl.write( folder )    

def onStartButton(event):
    host = getTextValue('host')
    port = getTextValue('port')
    user = getTextValue('user')
    passwd = getTextValue('passwd')
    home = getTextValue('home')
    ezwx.threadHandle(runFtpServer, start=True, args=(host,port,user,passwd,home))    

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
    [ ezwx.Label("IP Address: "), 
      ezwx.Text("127.0.0.1",key='host'),
      ezwx.Label("Port: "),
      ezwx.Text("21",key='port',size=(32,12)),
      ezwx.Label("Id: "), 
      ezwx.Text("user",key='user'),
      ezwx.Label("Password: "),
      ezwx.Text("1234",key='passwd',password=True),
    ],
    [ ezwx.Label("Home Folder: "), 
      ezwx.Text("",key='home',proportion=1),
      ezwx.Button("Browse",handler=onHomeButton),
      ezwx.Button("Start",handler=onStartButton),
    ],    
    [ ezwx.Text(expand=True,proportion=1,key="text"), 
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
    window = ezwx.WxApp("Easy FTPServer", 600, 480)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    window.run()
