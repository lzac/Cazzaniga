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

class Login(wx.Panel):
    def __init__(self):
        self.schema = None
        self.active = True
        self.res = xrc.XmlResource('xrc\\frm_login.xrc')
        self.dlg = self.res.LoadDialog(None, 'Login')
        self.dlg.SetBackgroundColour(g.login_bkg_color)
        # Bottoni
        self.f_img = self.dlg.FindWindowByName('wxID_STATIC')
        self.f_ok = self.dlg.FindWindowByName('ok')
        self.f_cancel = self.dlg.FindWindowByName('cancel')
        self.f_ok.SetId(wx.ID_OK)
        self.f_cancel.SetId(wx.ID_CANCEL)
        # Campi
        self.f_user = self.dlg.FindWindowByName('user')
        self.f_pwd = self.dlg.FindWindowByName('password')
        # Eventi
        self.dlg.Bind(wx.EVT_CLOSE, self.chiudi)
        self.f_cancel.Bind(wx.EVT_BUTTON, self.chiudi)
        self.f_ok.Bind(wx.EVT_BUTTON, self.btn_ok)
        self.dlg.SetTitle(_("Connetti a ") + g.appname)
        self.dlg.ShowModal()

    def btn_ok(self, event):
        if self.valid_connection():
            if self.valid_login():
                self.result = wx.ID_OK
                self.dlg.Destroy()
            else:
                self.f_user.SetFocus()

    def chiudi(self, event):
        self.result = wx.ID_CANCEL
        self.dlg.Destroy()

    def valid_connection(self):
        g.db = lib_db.Dbase(g.dbschema)
        #g.dbstampe = stampe.Dbase(g.dbstampe_schema)
        return g.db.is_connect

    def valid_login(self):
        if len(self.f_user.GetValue()) == 0:
            msg.WarningBox(self.dlg, _("Inserire utente"))
            return False
        meta = MetaData()
        meta.bind = g.engine
        t = Table('utente', meta, autoload=True)
        s = select([func.count(t.c.id)])
        s = s.where(t.c.codice == self.f_user.GetValue())
        row = s.execute().fetchone()
        if row[0] == 0:
            msg.WarningBox(self.dlg, _("Utente non valido"))
            return False
        t = Table('utente', meta, autoload=True)
        s = select([t.c.password, t.c.id])
        s = s.where(t.c.codice == self.f_user.GetValue())
        row = s.execute().fetchone()
        pwd = crypto.decrypt(row[0], g.enckey)
        if not pwd == self.f_pwd.GetValue():
            msg.WarningBox(self.dlg, _("Password non valida"))
            return False
        self.set_idutente()
        return True
    
    def set_idutente(self):
        meta = MetaData()
        meta.bind = g.engine
        t = Table('utente', meta, autoload=True)
        s = select([t.c.id])
        s = s.where(t.c.codice == self.f_user.GetValue())    
        row = s.execute().fetchone()
        g.idutente = row.id
        