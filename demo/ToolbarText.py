import os
import sys
import time
import wx
import ezWxPython as ew

'''
Silk icon set 1.3 : http://www.famfamfam.com/lab/icons/silk/
'''
page_white_png = 'eJzrDPBz5+WS4mJgYOD19HAJAtICIMzBAiS3/jJ/BaRY0h19HRkY1p8wZ+16CeRLlrhGlATnp5WUJxalMjim5CelKnjmJqanBqUmplQWnky1ASra4eniGKJxvnRiNN8hBQHX5esOq71rbKud9aJd+sqPrq3+GldeO8RfmzbnYbtlop4k08VpLCfty7YwWsZwTp11Lcnp4QZ5kfBLW1i9zkvrx0TufHBD20XQs1tqln+vjGaeTohGQVKqyJblz9zaflt0bXbZm/Cn9eHLvDPN8ZbnWxv9TlqcLI59MaVrc4riwUUPTUSFRXr411xjeZwpISo2a+IBfbW61vM2rv7em267LvK+rXfbSv0ip6Fqd6k1y9EF+kZLoz+sq9zmD/QDg6ern8s6p4QmAJikcj4='
page_copy_png  = 'eJwBlwJo/YlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/YQAAAARnQU1BAACvyDcFiukAAAAZdEVYdFNvZnR3YXJlAEFkb2JlIEltYWdlUmVhZHlxyWU8AAACKUlEQVQ4y3XTPWhUQRSG4ffMzN1ssm52FX+CkkIwSSVWQYsYUYsUmkobQTClKFqJoJ2gsbCXYCEErLROJxITURIMqGWIaZKIJLjGuP937hyLu4KS3dNMM+djzjMzMnbvw8vefHTMGIqKJiCIKg2vlZ1q83mzVHo2PzVep0PJ5UeLn17dH85tloMVIKgSJwFnYXphm6XFjTff1zduzz29UG0XYIxIT6mqdmVL+fojsLyZ8Hk9Zk+XY2SoyOhI/7nc/sLdTicwCmIFsg4yVshYIZsxbG7XGNoLEycL9Pf1XO0U4ABEILKgCmqFrDPMLv8+2vAe7wPHBw9xa/pLRYLKTt2vr63VXzRLpSfzU+M1p4AgWGNaKkoISiOOuX72MFvlQGrT19OyGZhe2H6wtLgxPHpj5opThZB2IgSsQMYZkkT5WVVWthRjlNgHdmqeM4PdjAwVyWXMxZnX5cdOVRHAGTBiCApWQEnXrEtnFP3XJuLEwQKzc103DWpIgm9/xy0bJ+BaNqsl4d1qg181JXIGJ2ptw5eB4n/NnWzosogRrLUo4OJmoxKZfK6QjVEFI4JImtDORlQJQRARVMH5RL9dm/x4oOkpgNYg7c4XLBOnj+yyMQHIQLcDVcXNTJ4aazf/pYdLcRK8az2VXRXUQxBMx0+i1qU27avhy0gw4jptqNbqpcjk9+2yIR3Sml6C+qaoatuA83fev7VGBsD0gVb+2rRYJWhSLuSi7j8Xl/8bKe2kegAAAABJRU5ErkJggsgkKIY='
page_paste_png = 'eJwBvwJA/YlQTkcNChoKAAAADUlIRFIAAAAQAAAAEAgGAAAAH/P/YQAAAARnQU1BAACvyDcFiukAAAAZdEVYdFNvZnR3YXJlAEFkb2JlIEltYWdlUmVhZHlxyWU8AAACUUlEQVQYGQXBMYiWZRwA8N/zvu99npymHUFXpJVgXqEgRbZoDTa0XEPQ0hQUGQ1ODhGEjW0FLQoORRAFKQ3V0lJYgUEQRAQV3lbhWZ7yndf3vc/z//f7lcwE519+8BH8AgCAm6curO8FAAAo51564FG8hbVdy3d74Y2ztq7/AJbuOubDs6/b3roFH+HSqQvrFwFgwKVnXjmzb/mee/3z1fsyU5ttgcx04sg+S0dPysy1z86/9ywuAsCA+5dX7rP5+xUx3rb+yTtkIl3PH6W08fN3lleP7QYAgAGyzkUddfsPi1Zlpo/baS1DBHDzty3l+NNefffzvDFb+fXP9b8eu3xubXuAaKOooxhn2uw/pDaEN59btTENBZFpbGHoj/jgyubDfemvPvnaFwcHiDoTrZKhFDLpu86N2+mPjdR1aazh1nb11EM7HT+019KkW/k2208dRJ2LOtfGuahN1Ab6wuLApC8mfbE46Vzb3HboTl58Yo865oEBYpzJcS5riLGRqS2mUljoyST7YnHoXP03Tf+eeXz/DgtDZ4Coc1GbGJuoQaTIVBR91wElRSQ7eqUr+r6XGCDHJudN1CZqI4AARRH6wmTolEwRRSlFJgPUsWpjE62JsZFESwVDR1c6kfSFLjBh50BmGiDnVYxNtiZryEjQomIAAACRlSgGXN6eTk/s2rcqaxO1kYnBrE6xFwAAzOpUia4MePvrLz/djaMAcO3w8xa6A/YsjjLpSlEKUNB3d4is85KZAADg5Jnvv+m7cpBuhdyiIEFRSmSb7lla2Pk/rzVJEzgz/YUAAAAASUVORK5CYIIjiEct'

def findCtrls():
    global status, text
    status = appWin.statusbar
    text = ew.getWxCtrl('text')

def onExit(event):
    appWin.close()
    
def onClose(event):
    rv = appWin.messageYesNo("Alert", "Do you want to quit ?" )
    return rv

def onOpen(event):
    pass
    
def onAbout(event):
    appWin.messageBox("About", "ToolbarText Demo\nzdiv")

def onIdle(event):
    pass
    
def onTimer(event):
    pass

def onClear(event):
    text.Clear()
def onCopy(event):
    text.Copy()
def onPaste(event):
    text.Paste()
def onPasteHtml(event):
    text.AppendText(ew.GetClipboardHtmlText())
def onPasteFile(event):
    files = ew.GetClipboardFilenames()
    for f in files:
        text.AppendText(f + '\n')
        
menu_def = { 
    "File" : { 
        "Exit" : [onExit, wx.ART_QUIT],  
    }, 
    "Help" : { 
        "About" : [onAbout, wx.ART_HELP],
    },
}

tool_def = [ #icon, text, handler, tooltip
    [wx.ART_QUIT, onExit, "Exit" ],
    [wx.ART_HELP, onAbout, "About" ],
]

status_def = [
    ["Ready", -1],  
]

text_tool_def = [
    [page_white_png, onClear    , None, "Clear all text"],
    [page_copy_png , onCopy     , None, "Copy text to clipboard"],
    [page_paste_png, onPaste     , None, "Paste text from clipboard"],
    [page_paste_png, onPasteHtml , None, "Paste html text from clipboard"],
    [page_paste_png, onPasteFile , None, "Paste filenames from clipboard"],
]
            
body_def = [
    [ 
        ew.Notebook([
            "Default Toolbar",
            [
                [ 
                    ew.ToolbarText(expand=True,proportion=1,key="text"),
                    { 'expand' : True, 'proportion' : 1 }
                ]
            ],
            "Custom Toolbar",
            [
                [ 
                    ew.ToolbarText(tool_def=text_tool_def, expand=True,proportion=1,key="text"),
                    { 'expand' : True, 'proportion' : 1 }
                ]
            ],
        ] , expand=True, proportion=1),
        { 'expand' : True, 'proportion' : 1 }
    ],
]

layout = {
    "menu"   : menu_def, 
    "tool"   : tool_def, 
    "status" : status_def, 
    "body"   : body_def, 
}


if __name__ == "__main__":
    appWin = ew.WxApp(u"ToolbarText Demo", 480, 320)
    appWin.makeLayout(layout)
    findCtrls()
    appWin.closeHandle(onClose)
    appWin.openHandle(onOpen)
    appWin.idleHandle(onIdle)
    appWin.timerHandle(onTimer,100,start=True,key='timer')
    appWin.run()

