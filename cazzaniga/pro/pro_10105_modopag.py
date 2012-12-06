# -*- coding: utf-8 -*-

from moduli import *
import pro_10114_ratapag as p10114
import pro_10108_modopag_rate as p10108
import lib_function as F
import lib_global as g

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()
        
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('modopag', meta, autoload=True)        
        s = select([t.c.id, t.c.modopag]).order_by(t.c.id)
        rs = s.execute() 
        self.fill_data(rs, [_('Codice'), _('Descrizione') ])  
         
class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):     
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'modopag', **kwargs)

        self.listcol = ('id', 'modopag')
        self.tabdel = ('ratapag', 'idmodopag')
        self.pkseq = 3
        
        self.init_controls()
        self.move_record(move)        
        
    def init_controls(self):
        self.appendctrl('id')   
        self.appendctrl('modopag')   
        self.appendctrl('ispredefinito', empty=True)   
        self.add_detail('rate', getattr(self,'get_rate'), menu_popup=getattr(self,'menu_rata'), menu_apri=getattr(self,'apri_rata'))       
        self.f_id = xrc.XRCCTRL(self.frame, 'id')
        self.f_list = xrc.XRCCTRL(self.frame, 'rate')            
        self.frame.Bind(wx.EVT_BUTTON, self.rate, id=self.get_ctrlid('btn_rate'))        
        self.frame.Bind(wx.EVT_BUTTON, self.nuovo_rata,id=self.get_ctrlid('btn_nuovo'))
        self.frame.Bind(wx.EVT_BUTTON, self.apri_rata,id=self.get_ctrlid('btn_apri'))
        self.frame.Bind(wx.EVT_BUTTON, self.elimina_rata,id=self.get_ctrlid('btn_elimina'))         
        self.f_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.apri_rata)
        self.get_ctrl('ispredefinito').Bind(wx.EVT_CHECKBOX, self.checkPredefinito)    
        
    def checkPredefinito(self, event):
        MODOPAG = Table('modopag', self.meta, autoload=True)
        val = self.get_value('ispredefinito')
        if val==True:
            s = select([MODOPAG.c.id, MODOPAG.c.modopag])
            s = s.where(MODOPAG.c.id!=self.get_value('id'))
            s = s.where(MODOPAG.c.ispredefinito==True)
            row = s.execute().fetchone()
            if row!=None:
                wx.MessageDialog(self.frame, 'Pagamento predefinito gia esistente!', 'Attenzione', wx.OK).ShowModal()            
                self.get_ctrl('ispredefinito').SetValue(False)
  
    def rate(self, event):
        x = p10108.Modifica_rate(self, self.get_value('id'))
        x.frame.Show()
        
    def get_rate(self):
        t = Table('ratapag', self.meta, autoload=True)        
        p = Table('tipopag', self.meta, autoload=True)
        p1 = Table('tiposcadenza', self.meta, autoload=True)        
        cols = [_('Id'), _('Tipo pagamento'), _('Giorni'), _('Decorrenza')]      
        s = select([t.c.id, p.c.tipopag, t.c.frequenza, p1.c.tiposcadenza],(t.c.idtipopag==p.c.id) & (t.c.idtiposcadenza==p1.c.id))        
        s = s.where(t.c.idmodopag==self.get_value('id'))
        s = s.order_by(t.c.id)
        rs = s.execute()
        ctrl = xrc.XRCCTRL(self.frame, 'rate')
        ctrl.FillData(rs, cols)

    def menu_rata(self):
        pass
    
    def apri_rata(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'rate')
        kwargs = {'pkfrom': {'idmodopag': self.get_value('id')}, 'parent_frame':self}                
        f = p10114.EditFrame(lib.g.menu.RATAPAG, _('Rata pagamento'), ctrl, ctrl.pk, lib.g.RECORD_CURRENT, {'idmodopag': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()

    def elimina_rata(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'rate')   
        recno = ctrl.GetFocusedItem()
        F.elimina_posizione(ctrl, 'rata', 'ratapag', {'idmodopag':self.get_value('id'), 'id':ctrl.pk[recno]})
    
    def nuovo_rata(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'rate')
        kwargs = {'pkfrom': {'idmodopag': self.get_value('id')}, 'parent_frame':self}                
        f = p10114.EditFrame(lib.g.menu.RATAPAG, _('Rata pagamento'), ctrl, ctrl.pk, lib.g.RECORD_APPEND, {'idmodopag': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()


    def after_move_record(self, **d):
        if self.isappend:
            flag = self.getDisableDelete()
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)           

    def getDisableDelete(self):
        FAT = Table('fattura', self.meta, autoload=True)
        s = select([FAT.c.id])
        s = s.where(FAT.c.idmodopag==self.get_value('id'))
        row = s.execute().fetchone()
        if row!=None:
            return True
        return False
