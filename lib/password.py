# -*- coding: utf-8 -*-

import ConfigParser
from sqlalchemy import *
from sqlalchemy import MetaData
import lib_db
import lib_global as g
import wx.xrc as xrc
import lib_msg as msg
import lib_crypto as crypto
import os
import wx

class Password(wx.Panel):
    def __init__(self, parent, var):
        self.schema = None
        self.active = True
        self.parent = parent
        self.var = var
        self.res = xrc.XmlResource('xrc\\frm_password.xrc')
        self.dlg = self.res.LoadDialog(self.parent, 'password')
        self.dlg.SetBackgroundColour(g.login_bkg_color)   
        # Bottoni
        self.f_ok = self.dlg.FindWindowByName('ok')
        self.f_cancel = self.dlg.FindWindowByName('cancel')
        self.f_ok.SetId(wx.ID_OK)
        self.f_cancel.SetId(wx.ID_CANCEL)
        # Campi
        self.f_pwd = self.dlg.FindWindowByName('pwd')
        # Eventi
        self.dlg.Bind(wx.EVT_CLOSE, self.chiudi)
        self.f_cancel.Bind(wx.EVT_BUTTON, self.chiudi)
        self.f_ok.Bind(wx.EVT_BUTTON, self.btn_ok)
        self.dlg.ShowModal()

    def btn_ok(self, event):
        if self.valid_connection():
            if self.valid_login():
                self.result = wx.ID_OK
                self.dlg.Destroy()
            else:
                self.result = wx.ID_CANCEL
                self.f_pwd.SetFocus()
                
    def chiudi(self, event):
        self.result = wx.ID_CANCEL
        self.dlg.Destroy()

    def valid_connection(self):
        g.db = lib_db.Dbase(g.dbschema)
        return g.db.is_connect

    def valid_login(self):
        pwd = crypto.decrypt(self.f_pwd.GetValue(), g.enckey)
        if pwd==self.var:
            return True
        else:
            msg.WarningBox(self.dlg, _("Password errata!"))
            return False   