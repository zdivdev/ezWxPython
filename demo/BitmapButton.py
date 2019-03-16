
wx_addr = None
wx_output = None
wx_text = None

def onExit(event):
    ew.WxAppClose()
    
def onClose(event): 
    return ew.MessageYesNo("Alert", "Do you want to quit ?" )

def onAbout(event):
    ew.MessageBox("About", "eezWxPython Demo\nzdiv")

def onGo(event):
    url = wx_addr.GetValue()
    output_dir = wx_output.GetValue()
    ew.threadHandle(saveTookKor, args=(home_url, url, output_dir), key='thread')    
    ew.threadStart('thread')
    saveTookKor()

def onFolder(event):
    folder = ew.DirectoryDialog()
    if wx_output is not None and folder is not None:
        wx_output.Clear()
        wx_output.write(folder)  

def AppendToText(text):
    if wx_text is not None:
        wx_text.AppendText( str(text) )
        wx_text.AppendText( '\r\n' )
        lines = wx_text.GetNumberOfLines()
        wx_text.ScrollLines( lines + 1 )
        

def printf(text):
    if gui_enabled is True:
        ew.callAfter(AppendToText,text)
    else:
        print(text)
        
def findCtrls():
    global wx_addr, wx_output, wx_text
    wx_addr = ew.getWxCtrl('addr')
    wx_output = ew.getWxCtrl('output')
    wx_text = ew.getWxCtrl('text')
    
menu_def = { 
    "File" : { 
        "Exit" : [onExit, wx.ART_QUIT],  
    }, 
    "Help" : { 
        "About" : [onAbout, wx.ART_HELP],
    },
}

tool_def = [ #icon, text, handler
    [wx.ART_QUIT, onExit, "Exit" ],
]

status_def = [
    ["Ready", -1],  
]

body_def = [
    [ ew.Label ("Address: "), 
      ew.Text  ("https://gogle.com",key="addr",expand=True,proportion=1),
      ew.Button(wx.ART_GO_FORWARD,handler=onGo),
    ],
    [ ew.Label ("Output Folder: "), 
      ew.Text  ("D:/",key="output",expand=True,proportion=1),
      ew.Button(wx.ART_FOLDER_OPEN,handler=onFolder),
    ],
    [ ew.StyledText(key='text',expand=True,proportion=1),
      { 'expand':True, 'proportion':1 }
    ]
]

layout = {
    "menu"   : menu_def, 
    "tool"   : tool_def, 
    "status" : status_def, 
    "body"   : body_def, 
}


if __name__ == "__main__":
    gui_enabled = True
    window = ew.WxApp(u"ezwxApp", 900, 620)
    window.makeLayout(layout)
    window.closeHandle(onClose)
    findCtrls()
    window.run()



