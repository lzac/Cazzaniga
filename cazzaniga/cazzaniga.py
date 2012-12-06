# -*- coding: iso-8859-1 -*-

import wx
import lib_global as g
import gettext
import locale
import cazzaniga_moduli
import schema_base
import cazzaniga_schema
import app_main
import login
import sys
locale.setlocale(locale.LC_ALL, '')
gettext.install("infos", "./locale", unicode=True)

class Cazzaniga(app_main.MainFrame): 
    def __init__(self, *args, **kwargs):
        app_main.MainFrame.__init__(self, *args, **kwargs)
        self.appmod = cazzaniga_moduli   
        
if __name__ == '__main__':    
    #Decommentare quando si crea l'eseguibile       
    #sys.setdefaultencoding('iso-8859-1')    
    #sys.stdout = open('oikos.exe.log', 'w')
    #sys.stderr = open('oikos.exe.log', 'w') 
    app = wx.App(redirect=False)
    g.appname = "Fatturazione Autoservizi"  
    g.dbversion = 10
    g.dbschema = (schema_base, cazzaniga_schema)
    wx.DefaultSize
    Log = login.Login()
    if Log.result == wx.ID_OK:
        g.mainframe = Cazzaniga(None)    
        g.mainframe.postinit()
        g.mainframe.MakeModal(True)
        g.mainframe.Show()
        g.mainframe.Maximize()   
        app.MainLoop()
