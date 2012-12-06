# -*- coding: utf-8 -*-

from moduli import *
import lib_global as g

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()
        
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('iva', meta, autoload=True)
        s = select([t.c.id, t.c.iva])
        rs = s.execute() 
        self.fill_data(rs, [_('Id'), _('Descrizione')])     

class EditFrame(lib.frame.EditFrame):
    
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'iva', **kwargs)  
        self.listcol = ('id', 'iva')
        self.pkseq = 0       
        self.init_controls()
        self.move_record(move)        

    def init_controls(self):    
        self.appendctrl('id')   
        self.appendctrl('iva')
        self.appendctrl('ispredefinito', empty=True)
        self.appendctrl('idtipoiva', default='00')
        self.appendctrl('aliquota', empty=True)               
        self.appendlkp(wx.ID_NONE, 'idtipoiva')    
        self.get_ctrl('ispredefinito').Bind(wx.EVT_CHECKBOX, self.checkPredefinito)                  

    def checkPredefinito(self, event):
        IVA = Table('iva', self.meta, autoload=True)
        val = self.get_value('ispredefinito')
        if val==True:
            s = select([IVA.c.id, IVA.c.iva])
            s = s.where(IVA.c.id!=self.get_value('id'))
            s = s.where(IVA.c.ispredefinito==True)
            row = s.execute().fetchone()
            if row!=None:
                wx.MessageDialog(self.frame, 'Iva predefinita gia esistente!', 'Attenzione', wx.OK).ShowModal()            
                self.get_ctrl('ispredefinito').SetValue(False)
                              
    def after_move_record(self, **d):
        if self.isappend:
            flag = self.getDisableDelete()
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)           

    def getDisableDelete(self):
        FATIVA = Table('fativa', self.meta, autoload=True)
        s = select([FATIVA.c.id])
        s = s.where(FATIVA.c.id==self.get_value('id'))
        row = s.execute().fetchone()
        if row!=None:
            return True
        return False
    
                
                