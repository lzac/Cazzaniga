# -*- coding: utf-8 -*-

from moduli import *
import lib_global as g
import pro_10451_offdet as p10451
import lib_function as F
from datetime import date
import lib_file as File
import win32com.client
import lib_class as C
import subprocess


class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.showid = False        
        self.get_data()    
      
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        OFF = Table('offerta', meta, autoload=True)    
        OFFDET = Table('offdet', meta, autoload=True)   
        CAU = Table('causale', meta, autoload=True)    
        ANA = Table('anag', meta, autoload=True) 
        s = select([CAU.c.causale, OFF.c.data, OFF.c.numero, OFFDET.c.posizione, ANA.c.anag, OFFDET.c.descri, OFFDET.c.destinazione, OFFDET.c.quantita, OFFDET.c.prezzo])        
        s = s.select_from(OFF.outerjoin(CAU, OFF.c.idcausale==CAU.c.id)
                             .outerjoin(ANA, OFF.c.idanag==ANA.c.id))
        s = s.where(OFF.c.id==OFFDET.c.idofferta)
        if self.filtro.has_key('destinazione'):
            s = s.where(OFFDET.c.destinazione.like('%'+self.filtro['destinazione']+'%'))        
            s = s.order_by(ANA.c.anag)               
            rs = s.execute() 
        else:
            rs = []        
        self.fill_data(rs, [_('Causale'), _('Data'), _('Numero'), _('Pos.'),_('Ragione sociale'), _('Descrizione'), _('Destinazione'),_('Quantita'), _('Prezzo')])
        
        
        
class CustomDialog(lib.dialog.CustomDialog):
    def __init__(self, frame, **kwargs):  
        lib.dialog.CustomDialog.__init__(self, frame, **kwargs)
        self.init_controls()
        self.init_frame()
    
    def init_controls(self):
        self.appendctrl('destinazione', empty=True)   
        self.get_ctrl('btn_conferma').Bind(wx.EVT_BUTTON, self.conferma)
        self.get_ctrl('btn_annulla').Bind(wx.EVT_BUTTON, self.annulla)
        self.get_filtro()
    
    def get_filtro(self):
        for k,v in self.page.filtro.iteritems():
            self.set_value(k, v)
     
    def conferma(self, event):
        self.check_destinazione()
        self.page.get_data()
        self.frame.Destroy()
        
        
    def check_destinazione(self):
        value = self.get_ctrl('destinazione').GetCurrValue()
        if value!=None:
            self.page.filtro['destinazione'] = value
        else:
            if 'destinazione' in self.page.filtro.keys():
                del self.page.filtro['destinazione']        


    def annulla(self, event):
        for ctrl in self.datacontrols:
            try:
                self.set_value(ctrl, '') 
            except:
                self.set_value(ctrl, False)
        self.conferma(None)   


       
