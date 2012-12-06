# -*- coding: utf-8 -*-

from moduli import *
import lib_global as g
import lib_function as f


class EditFrame(lib.frame.EditFrame):   
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'fatspesa', **kwargs)        
        self.listcol = ('id', 'idspesa', 'idiva', 'imponibile')
        self.pkseq = 3        
        self.init_controls()
        self.move_record(move)   
        self.change_iva(None)     

    def init_controls(self):
        #Controlli
        self.appendctrl('idfattura')        
        self.appendctrl('id')
        self.appendctrl('idspesa')
        self.appendctrl('idiva')      
        self.appendctrl('imponibile', empty=True)
        self.appendctrl('imposta', empty=True)
        self.appendctrl('totale', empty=True)
        self.appendctrl('iseliminato', ctrl=lib.frame.VirtualCheckBox())   
        #Lookup
        self.appendlkp(g.menu.SPESA, 'idspesa')
        self.appendlkp(g.menu.IVA, 'idiva')
        #Eventi
        self.get_ctrl('imponibile').Bind(wx.EVT_TEXT, self.change)
        self.get_ctrl('idiva').Bind(wx.EVT_CHOICE, self.change_iva)  
               
    def change_iva(self, event):
        IVA = Table('iva', self.meta, autoload=True)
        s = select([IVA.c.aliquota])
        s = s.where(IVA.c.id==self.get_value('idiva'))
        row = s.execute().fetchone()
        if row!=None:
            self.aliquota = row.aliquota
            if self.aliquota==None:
                self.aliquota = 0
    
    def change(self, event):
        try:
            value = self.get_ctrl('imponibile').GetCurrValue()
            imposta = (value/100)*self.aliquota
            totale = value+imposta
            self.get_ctrl('totale').Set_Value(totale)
            self.get_ctrl('imposta').Set_Value(imposta)
        except: pass
        
    def after_put_data(self):
        self.FrameParent.create_values()
                
    def after_delete(self): 
        self.FrameParent.create_values()
                                   
    def delete_fativa(self):
        self.FrameParent.after_put_data()
        
    def after_move_record(self, **d):
        if self.isappend or self.iscopy:
            iva = f.get_iva(self.FrameParent.get_value('idanag'), self.FrameParent.get_ctrl('data').GetCurrValue())
            self.set_value('idiva', iva['idiva'])
            if iva['definitive']==True:
                self.get_ctrl('idiva').Enabled=False
                self.get_ctrl('btn_idiva').Enabled=False
                self.get_ctrl('lkp_idiva').Enabled=False