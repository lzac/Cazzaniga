# -*- coding: utf-8 -*-

from moduli import *

import lib_function as f
import lib_menu as menu
import lib_global as g
import lib_sql as libsql

import datetime
import calendar

class DetailFrame():
    def __init__(self, cols, tabfiglia, tabpadre, tabass, idpadre, app, listpadre, **kwargs):
        self.xrc = "xrc\\frm_det.xrc"
        self.default = {}
        self.meta = MetaData()
        self.meta.bind = g.engine
        self.controls = {}
        self.datacontrols = {}
        self.lkpcontrols = {}        
        self.detcontrols = {}
        self.detmethods = {}        
        self.emptycontrols = {} 
        self.cols = cols
        self.persnomecol = kwargs.get('persnomecol', None)
        if self.persnomecol:
            self.cols = [_('Id'), _(self.persnomecol)]
        self.desc_det = {}
        self.idapp = app
        self.tabfiglia = tabfiglia
        self.tabass = tabass
        self.tabpadre = tabpadre
        self.idpadre = idpadre
        # lista id per associarli all'itemdata
        self.ids = []
        # numero di 0 nell'id
        self.zerid = 0
        #kwargs
        self.FrameParent = kwargs.get('parent_frame', None)    
        self.isappend = kwargs.get('new', None)       
        self.id = kwargs.get('id', None)   
        self.iselim = kwargs.get('iselim', True)
        self.listpadre = listpadre     
        self.init_frame()
  
    def init_frame(self):
        self.res = xrc.XmlResource(self.xrc)
        self.frame = self.res.LoadFrame(None, "frame")  
        #controllo lista
        self.lista = self.appendctrl('list')
        #controlli bottoni
        self.aggiungi = self.appendctrl('aggiungi')
        self.annulla = self.appendctrl('annulla')
        self.seltutto = self.appendctrl('seltutto')
        #Creazione toolbar
        self.toolbar = self.frame.CreateToolBar(style=wx.TB_FLAT|wx.TB_TEXT)       
        self.toolbar.Realize()
        #Eventi 
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        self.aggiungi.Bind(wx.EVT_BUTTON, self.aggiungi_elementi)
        self.seltutto.Bind(wx.EVT_TOGGLEBUTTON, self.seldesel)
        self.annulla.Bind(wx.EVT_BUTTON, self.on_close)
        #Popola lista
        self.get_dett()
        self.frame.Show()
    
    def seldesel(self, event):
        if self.seltutto.GetValue():
            for i in range(self.lista.GetItemCount()):
                self.lista.CheckItem(i)
            return
        for i in range(self.lista.GetItemCount()):
                self.lista.CheckItem(i, False)
    
    def alertNone(self):
        dlg = wx.MessageDialog(None, "ATTENZIONE\n"
                                  "Non hai spuntato nessun elemento.\n",            
                                  "ATTENZIONE", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
    
    def GetApp(self):
        return self.idapp
    
    def aggiungi_elementi(self, event):
        checked = self.lista.GetChecked()
        if not checked:
            self.alertNone()
        else:
            self.on_close(None)
        for i in range(self.lista.GetItemCount()):
            if i in checked:
                # aggiungi dettaglio alla lista padre
                nidagg = self.lista.GetItemData(i)
                idagg = '%0*d' % (self.zerid+1, nidagg)
                index = self.listpadre.InsertStringItem(sys.maxint, idagg)      
                self.listpadre.SetStringItem(index, 1, self.desc_det[idagg])
                t = Table(self.tabass, self.meta, autoload=True)
                s = t.insert()  
                d = {
                     'id'+self.tabpadre : self.idpadre,
                     'id'+self.tabfiglia : idagg
                    }
                s.execute(d)
                self.idapp.append(idagg)
                
    def get_dett(self, **kwargs):
        for i in range(len(self.cols)):      
            self.lista.InsertColumn(i, _(self.cols[i]))
        t = Table(self.tabfiglia, self.meta, autoload=True)   
        s = select([t.c.id, t.c['%s' % self.tabfiglia]])
        if self.iselim:
            s = s.where(t.c.iseliminato==None)       
        rs = s.execute()     
        for row in rs:     
            self.desc_det[row.id] = row[self.tabfiglia]
            if row.id not in self.idapp:   
                self.ids.append(row.id)
                self.lista.InsertStringItem(sys.maxint, row[self.tabfiglia]) 
        for a in range(self.lista.GetColumnCount()):
            self.lista.SetColumnWidth(a, wx.LIST_AUTOSIZE_USEHEADER)    
        
        # calcolo numero di zeri dell'id
        count = 0
        try:
            for pos in self.ids[0]:
                if pos == '0':
                    count = count + 1
            self.zerid = count
        except IndexError:
            return
        # associo ad ogni item l'id     
        for p in range(self.lista.GetItemCount()):
            self.lista.SetItemData(p, int(self.ids[p]))
                
        for a in range(self.lista.GetColumnCount()):
            self.lista.SetColumnWidth(a, wx.LIST_AUTOSIZE_USEHEADER)
            # focus su aggiungi e nascondo Id
            self.aggiungi.SetFocus()
            
                                                 
    def on_close(self, event):
        self.frame.Destroy()  
        
    def get_value(self, id):
        return self.controls[id].GetValue()

    def get_ctrl(self, nome):
        try:
            ctrl = self.controls[nome]
        except:
            ctrl = xrc.XRCCTRL(self.frame, nome)
        return ctrl

    def get_ctrlid(self, nome):
        return xrc.XRCID(nome)    
    
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
    
    