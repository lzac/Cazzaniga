# -*- coding: utf-8 -*-

import wx
import os
import wx.xrc as xrc
import wx.lib.mixins.listctrl as listmix
from sqlalchemy import *
import sys
from lib_function import *
import time
import wx.lib.agw.foldpanelbar as fpb
import lib_class as c
import wx.html as  html
import images
import lib_sql as libsql
import wx.gizmos as gizmos

class CustomDialog():
    def __init__(self, frame, **kwargs): 
        self.Frame = frame   
        self.notoolb = kwargs.get('notoolb', False)
        self.xrc = xrc
        self.default = {}
        self.meta = MetaData()
        self.meta.bind = g.engine
        self.metastampa = MetaData()
        self.metastampa.bind = g.stampengine
        self.controls = {}
        self.datacontrols = {}
        self.lkpcontrols = {}        
        self.detcontrols = {}
        self.detmethods = {}        
        self.emptycontrols = {} 
        self.FrameParent = kwargs.get('parent_frame', None)    
        self.isappend = kwargs.get('new', None)       
        self.table = kwargs.get('table', None)
        self.id = kwargs.get('id', None)   
        self.list = kwargs.get('list', None)   
        self.frame = self.buildDialog(self.Frame, 'dialog')  
        self.page = kwargs.get('page')
    
    def init_frame(self):      
        try:
            result = self.runDialog(self.frame, True)
        finally:
            self.frame.Destroy()
        return result
    
    def buildDialog(self, filePath, resourceName, *mayCancel, **defaults):
        res = xrc.XmlResource(filePath)
        dlg = res.LoadDialog(self.FrameParent, resourceName)
        assert isinstance(dlg, wx.Dialog)
        return dlg

    def runDialog(self, dlg, mayCancel, *itemNames):
        while True:
            if dlg.ShowModal() == wx.ID_OK:
                result = tuple((dlg.FindWindowByName(name).GetValue()
                                for name in itemNames))
                break
            elif mayCancel:
                result = None
                break
            else:
                wx.Bell()
        return result
    
    def add_detail(self, nome, method, **kwargs):
        self.detmethods[nome] = method
        self.detcontrols[nome] = xrc.XRCCTRL(self.frame, nome)                   

    def get_value(self, id):
        return self.controls[id].GetValue()

    def get_currvalue(self, id):
        return self.controls[id].GetCurrValue()

    def get_startvalue(self, id):
        return self.controls[id].GetStartValue()

    def set_value(self, id, v):
        if v==None:
            v = False
        return self.controls[id].SetValue(v)

    def set_startvalue(self, id, v):
        return self.controls[id].SetStartValue(v)

    def get_ctrl(self, nome):
        try:
            ctrl = self.controls[nome]
        except:
            ctrl = xrc.XRCCTRL(self.frame, nome)
        return ctrl

    def get_ctrlid(self, nome):
        return xrc.XRCID(nome)    
    
    def appendcalendar(self, nome, **kwargs):
        ctrl = self.get_ctrl(nome)
        if 'after_lookup' in kwargs:
            ctrl.after_lookup = kwargs.get('after_lookup')
        btn = xrc.XRCCTRL(self.frame, 'btn_' + nome)
        btn.InitLookup(self, ctrl)
    
    def appendctrl(self, nome, **kwargs):
        if 'ctrl' in kwargs:
            empty = True
        else:
            empty = kwargs.get('empty', False)
        ctrl = kwargs.get('ctrl', xrc.XRCCTRL(self.frame, nome))
        ctrl.owner = self
        data = kwargs.get('data', True)
        self.controls[nome] = ctrl
        if data:
            self.datacontrols[nome] = ctrl
            if empty == False:
                self.emptycontrols[nome] = ctrl
        if 'default' in kwargs:
            if not nome in self.default:
                self.default[nome] = kwargs.get('default')
        if 'fillzero' in kwargs:
            ctrl.fillzero = kwargs.get('fillzero')
        if 'evt_kill_focus' in kwargs:
            ctrl.evt_kill_focus = kwargs.get('evt_kill_focus')
        return ctrl
    
    def appendlkp(self, id, nome, **kwargs):
        ctrl = self.get_ctrl(nome)
        lkpcodice = kwargs.get('lkp_codice', False)
        self.lkpcontrols[nome] = ctrl
        ctrl.InitLookup(nome, self.get_ctrl(nome[2:]), lkpcodice)
        f = getattr(libsql, 'fill_' + nome)
        if callable(f):
            f(ctrl, **kwargs)
        if 'after_lookup' in kwargs:
            ctrl.after_lookup = kwargs.get('after_lookup')
        if not id == wx.ID_NONE:
            btn = xrc.XRCCTRL(self.frame, 'btn_' + nome)
            lkp = xrc.XRCCTRL(self.frame, 'lkp_' + nome)
            #btn
            btn.InitLookup(self, id, ctrl)
            #lkp
            lkp.InitLookup(self, id, ctrl)

    def lookup(self, id, cnt):
        pass

    def apri(self, id, ctrl):
        flag = id == 30001
        try:
            titolo = g.mainframe.MenuBar.FindItemById(id).GetItemLabelText()
        except: titolo=''
        m = g.mainframe.appmod.moduli['p%s' % (id)]
        d = {}
        if not flag:
            if len(ctrl.pkfrom) > 0:
                d = {'pkfrom': ctrl.pkfrom}
            f = m.EditFrame(id, titolo, ctrl , ctrl.pk, g.RECORD_CURRENT, ctrl.filtro, **d)
        else:
            if ctrl.GetValue() != '':
                t = Table('pdc', self.meta, autoload=True)
                s = t.select()
                s = s.where(t.c.codice == ctrl.GetValue())
                s = s.where(t.c.iseliminato == None)
                row = s.execute().fetchone()
                if row != None:
                    id = row.id
                    kwargs = {'new' : False}
                    f = m.StandardFrame('xrc\\frm_30001.xrc', **kwargs)
                    f.get_data(id)
            else:
                kwargs = {'new' : True}
                f = m.StandardFrame('xrc\\frm_30001.xrc', **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()
    
    def chiudi(self, event):
        self.frame.Destroy()