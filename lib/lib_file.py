# -*- coding: utf-8 -*-

import os
import sys
import wx
import lib_global as g
import time


def aprifile(nomefile,msg):
    time.sleep(2.5)
    if _cercafile(nomefile,  msg):
        if os.name == "nt": 
            os.startfile("%s" % nomefile)
        
def stampafile(nomefile,msg):
    if _cercafile(nomefile,msg):    
        if os.name == "nt": 
            os.startfile("%s" % nomefile, "print") 
 
def _cercafile(nomefile, msg):
    if not os.path.exists(nomefile):
        if msg:
            dlg = wx.MessageDialog(None, ("Impossibile trovare %s") % nomefile, (g.appname), wx.OK)
            dlg.ShowModal() 
            dlg.Destroy()
        return False
    return True
       
if __name__ == "__main__":
    appname = "Oikos"
    app = wx.App(redirect=False)
    aprifile("c:\\temp\\nazioni.pdf",True)
    
    