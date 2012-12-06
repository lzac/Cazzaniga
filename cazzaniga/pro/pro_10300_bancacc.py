# -*- coding: utf-8 -*-

from moduli import *

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()

    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('bancacc', meta, autoload=True)    
        s = select([t.c.id, t.c.bancacc, t.c.iban]) 
        rs = s.execute() 
        self.fill_data(rs, [_('Id'), _('Descrizione'),  _('Iban')])     


class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'bancacc', **kwargs)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        self.listcol = ('id', 'bancacc', 'iban')
        self.pkseq = 2              
        self.init_controls()
        self.move_record(move)
        
    def init_controls(self):        
        self.appendctrl('id')  
        self.appendctrl('bancacc')  
        self.appendctrl('contoc')      
        self.appendctrl('iban')   
        self.appendctrl('ispredefinito', empty=True) 
        self.get_ctrl('ispredefinito').Bind(wx.EVT_CHECKBOX, self.checkPredefinito)      
        
    def checkPredefinito(self, event):
        t = Table('bancacc', self.meta, autoload=True)
        val = self.get_value('ispredefinito')
        if val==True:
            s = select([t.c.id])
            s = s.where(t.c.id!=self.get_value('id'))
            s = s.where(t.c.ispredefinito==True)
            row = s.execute().fetchone()
            if row!=None:
                wx.MessageDialog(self.frame, 'Banca predefinita gia esistente!', 'Attenzione', wx.OK).ShowModal()            
                self.get_ctrl('ispredefinito').SetValue(False)                    