# -*- coding: utf-8 -*-

import wx
from wx import xrc
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.orm import sessionmaker
from moduli import *
import lib_sql as lib_sql

import lib_function as lib
import lib_menu as menu
import lib_global as g
import lib_sql as libsql

import myxrc

import datetime
import calendar

CHOICE = 1
LIST = 2
TEXT = 3

class PanelFiltro():
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)   
        self.ListPanel = kwargs.get('ListPanel', None) 
        res = xrc.XmlResource("xrc\\flt_%s.xrc" % (self.id))
        self.panel = res.LoadPanel(g.mainframe, "panel")
        
        self.controls = {}
        self.datacontrols = {}
        self.lkpcontrols = {}
        self.detcontrols = {}
        self.detmethods = {}
        self.emptycontrols = {}
        self.list = self.ListPanel.datalist


    def appendctrl(self, nome, **kwargs):
        if 'ctrl' in kwargs:
            empty = True
        else:
            empty = kwargs.get('empty', False)
        ctrl = kwargs.get('ctrl', xrc.XRCCTRL(self.panel, nome))
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
    
    def get_ctrl(self, nome):
        try:
            ctrl = self.controls[nome]
        except:
            ctrl = xrc.XRCCTRL(self.panel, nome)
        return ctrl