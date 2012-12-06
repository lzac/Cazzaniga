# -*- coding: utf-8 -*-

from moduli import *

class Modifica_rate():

    def __init__(self, owner, idmodopag):
        self.owner = owner
        self.idmodopag = idmodopag
        self.init_frame()
        self.init_data()
        
    
    def init_frame(self):     
        self.meta = MetaData()
        self.meta.bind = lib.g.engine         
        
        self.table = Table('ratapag', self.meta, autoload=True)
        
        self.res = xrc.XmlResource("xrc\\frm_10105a.xrc")
        self.frame = self.res.LoadFrame(None, "frame")          
        self.f_numrate = xrc.XRCCTRL(self.frame, 'numrate')
        self.f_idtipopag = xrc.XRCCTRL(self.frame, 'idtipopag')
        self.f_prima_frequenza = xrc.XRCCTRL(self.frame, 'prima_frequenza')
        self.f_frequenza_successiva=xrc.XRCCTRL(self.frame,'frequenza_successiva')
        self.f_idtiposcadenza = xrc.XRCCTRL(self.frame,'idtiposcadenza')
        self.f_idtipoimporto = xrc.XRCCTRL(self.frame,'idtipoimporto')

                
        t = Table('tipopag', self.meta, autoload=True)
        s = t.select().order_by(t.c.tipopag)
        rs = s.execute()
        row = rs.fetchall
        for row in rs:
            self.f_idtipopag.Append(row.tipopag,row.id)                                              
        
        t = Table('tiposcadenza', self.meta, autoload=True)
        s = t.select().order_by(t.c.tiposcadenza)
        rs = s.execute()
        row = rs.fetchall
        for row in rs:
            self.f_idtiposcadenza.Append(row.tiposcadenza,row.id)                        
                                     
        self.frame.Bind(wx.EVT_BUTTON, self.btn_conferma, id=xrc.XRCID('cmd_conferma'))
        self.frame.Bind(wx.EVT_BUTTON, self.btn_annulla,  id=xrc.XRCID('cmd_annulla'))               
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
                       
    def init_data(self):        
        self.f_numrate.SetValue('')
        self.f_idtipopag.SetValue('')
        self.f_idtiposcadenza.SetValue('FM')
               
    def btn_conferma(self, event):
        if self.valid_data():
            self.conferma()
            self.chiudi()        

    def btn_annulla(self, event):
        self.chiudi()
    
    def on_close(self, event):
        self.chiudi()    
               
    def conferma(self):
        f = lib.func.str2int(self.f_prima_frequenza.GetValue())
        r = lib.func.str2int(self.f_numrate.GetValue())
        for k in range(1, r+1):
            d = {}
            d['idmodopag'] = self.idmodopag
            d['id'] = '%0*d' % (3, k)
            d['frequenza'] = f
            d['idtipopag'] = self.f_idtipopag.GetValue() 
            d['idtiposcadenza'] = self.f_idtiposcadenza.GetValue()
            f += lib.func.str2int(self.f_frequenza_successiva.GetValue())
            r = self.table.insert()
            r.execute(d)
        self.owner.get_rate()

    def valid_data(self):
        freq1 = lib.func.str2int(self.f_prima_frequenza.GetValue())
        freq2 = lib.func.str2int(self.f_frequenza_successiva.GetValue())
        tiposca = self.f_idtiposcadenza.GetValue()
        tipopag = self.f_idtipopag.GetValue()
        rate = lib.func.str2int(self.f_numrate.GetValue())

        if rate == 0:
            wx.MessageDialog(None,_(u'Inserire numero rate'), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
            self.f_numrate.SetFocus()
            return False
        if tipopag == '':                
            wx.MessageDialog(None,_(u'Inserire tipo pagamento'), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
            self.f_idtipopag.SetFocus()
            return False
        if freq1 == 0:
            wx.MessageDialog(None,_(u'Inserire giorni prima rata'), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
            self.f_prima_frequenza.SetFocus()
            return False
        if rate == 1:
            self.f_frequenza_successiva.SetValue('')
        if rate > 1 and freq2 == 0:
            wx.MessageDialog(None,_(u'Inserire giorni rete successive'), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
            self.f_frequenza_successiva.SetFocus()
            return False
        if tiposca == '':                
            wx.MessageDialog(None,_(u'Inserire tipo scadenza'), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
            self.f_idtiposcadenza.SetFocus()
            return False
        return True
            
    def chiudi(self):
        self.frame.Destroy()