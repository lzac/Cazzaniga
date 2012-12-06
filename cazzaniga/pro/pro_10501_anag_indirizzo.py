# -*- coding: utf-8 -*-

from moduli import *

class Modifica_indirizzo():
    def __init__(self, parent):               
        self.parent = parent 
        self.init_frame()
        self.get_data()
        
    def init_frame(self):     
        self.meta = MetaData()
        self.meta.bind = lib.g.engine        
        self.res = xrc.XmlResource("xrc\\frm_10501.xrc")
        self.frame = self.res.LoadFrame(None, "frame")   
        self.f_indirizzo = xrc.XRCCTRL(self.frame, 'indirizzo')
        self.f_cap = xrc.XRCCTRL(self.frame, 'cap')
        self.f_localita = xrc.XRCCTRL(self.frame, 'localita')
        self.f_idprovincia = xrc.XRCCTRL(self.frame,'idprovincia')
        self.frame.Bind(wx.EVT_BUTTON, self.btn_ok, id=xrc.XRCID('btn_ok'))
        self.frame.Bind(wx.EVT_BUTTON, self.btn_annulla, id=xrc.XRCID('btn_annulla'))
        self.frame.Bind(wx.EVT_CLOSE, self.btn_annulla)
        #self.frame.Bind(wx.EVT_BUTTON, self.btn_idprovincia, id=xrc.XRCID('btn_idprovincia'))
        ctrl = self.f_idprovincia
        ctrl.InitLookup('idprovincia', xrc.XRCCTRL(self.frame, 'provincia'), None)
        lib.sql.fill_idprovincia(ctrl)
        xrc.XRCCTRL(self.frame, 'btn_idprovincia').InitLookup(self, lib.g.menu.PROVINCIA, ctrl) 
        xrc.XRCCTRL(self.frame, 'lkp_idprovincia').InitLookup(self, lib.g.menu.PROVINCIA, ctrl)
        
    def apri(self, id, ctrl):
        pass
               
    def get_data(self):
        self.f_indirizzo.SetValue(self.parent.controls['indirizzo'].GetValue())
        self.f_cap.SetValue(self.parent.controls['cap'].GetValue())                                       
        self.f_localita.SetValue(self.parent.controls['localita'].GetValue())        
        self.f_idprovincia.SetValue(self.parent.controls['idprovincia'].GetValue())

    def btn_annulla(self,event):
        self.frame.MakeModal(False)
        self.frame.Destroy()

    def btn_ok(self, event):   
        self.parent.controls['recapito'].SetValue(
                            self.f_indirizzo.GetValue()+'\n'+
                            self.f_cap.GetValue()+' '+
                            self.f_localita.GetValue()+' '+
                            self.f_idprovincia.GetValue())
        
        self.parent.controls['indirizzo'].SetValue(self.f_indirizzo.GetValue())
        self.parent.controls['cap'].SetValue(self.f_cap.GetValue())
        self.parent.controls['localita'].SetValue(self.f_localita.GetValue())
        self.parent.controls['idprovincia'].SetValue(self.f_idprovincia.GetValue())    
        self.btn_annulla(None)