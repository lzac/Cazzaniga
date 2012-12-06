# -*- coding: utf-8 -*-

from moduli import *
import lib_function as f
import lib_global as g

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'fatdet', **kwargs)
        self.listcol = ('id', 'descri','quantita', 'prezzo', 'scontoperc','importo')
        self.pkseq = 3    
        self.init_controls()
        #Move
        self.move_record(move)    
         
    def init_controls(self):
        #Controlli
        self.appendctrl('idfattura')        
        self.appendctrl('id')
        self.appendctrl('descri', empty=True)
        self.appendctrl('noteinizio1', empty=True)
        self.appendctrl('noteinizio2', empty=True)
        self.appendctrl('noteinizio3', empty=True)
        self.appendctrl('noteinizio4', empty=True)
        self.appendctrl('noteinizio5', empty=True)
        self.appendctrl('noteinizio6', empty=True)
        self.appendctrl('noteinizio7', empty=True)
        self.appendctrl('noteinizio8', empty=True)
        self.appendctrl('noteinizio9', empty=True)
        self.appendctrl('noteinizio10', empty=True)        
        self.appendctrl('notefine1', empty=True)
        self.appendctrl('notefine2', empty=True)
        self.appendctrl('notefine3', empty=True)
        self.appendctrl('notefine4', empty=True)
        self.appendctrl('notefine5', empty=True)
        self.appendctrl('notefine6', empty=True)
        self.appendctrl('notefine7', empty=True)
        self.appendctrl('notefine8', empty=True)
        self.appendctrl('notefine9', empty=True)
        self.appendctrl('notefine10', empty=True)
        self.appendctrl('idiva')
        self.appendctrl('quantita')
        self.appendctrl('prezzo', empty=True)
        self.appendctrl('scontoperc', empty=True)
        self.appendctrl('importo', empty=True)    
        self.appendctrl('idofferta', ctrl=lib.frame.VirtualTextCtrl())
        self.appendctrl('idoffdet', ctrl=lib.frame.VirtualTextCtrl())
         
        #Lookup
        self.appendlkp(g.menu.IVA, 'idiva')  
        #Eventi
        self.get_ctrl('prezzo').Bind(wx.EVT_TEXT, self.on_killfocus)        
        self.get_ctrl('quantita').Bind(wx.EVT_TEXT, self.on_killfocus)
        self.get_ctrl('scontoperc').Bind(wx.EVT_TEXT, self.on_killfocus)
                
    def on_killfocus(self, event):    
        scontoperc =  self.get_ctrl('scontoperc').GetCurrValue()
        tot = self.get_ctrl('quantita').GetCurrValue()*self.get_ctrl('prezzo').GetCurrValue()
        if scontoperc==0:
            self.get_ctrl('importo').Set_Value(tot)  
        else:
            sconto = round((tot/100)*scontoperc, 2)
            self.get_ctrl('importo').Set_Value(tot-sconto)  
    
    def after_put_data(self):
        self.FrameParent.create_values()
                
    def after_delete(self): 
        self.FrameParent.open_offdet(self.get_value('idofferta'), self.get_value('idoffdet'))
        self.FrameParent.create_values()                                 
        
    def after_move_record(self, **d):
        if self.isappend or self.iscopy:
            iva = f.get_iva(self.FrameParent.get_value('idanag'))            
            if iva!=None:            
                self.set_value('idiva', f.sql2str(iva))
