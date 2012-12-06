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
        t = Table('causale', meta, autoload=True)    
        s = select([t.c.id, t.c.causale])
        s = s.where(t.c.idtipocausale=="OFF")
        s = s.order_by(t.c.id)
        rs = s.execute() 
        self.fill_data(rs, [_('Id'), _('Causale')])  
      

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'causale', **kwargs)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        self.listcol = ('id', 'causale')
        self.pkseq = 2          
        self.init_controls()
        self.move_record(move)
        
    def init_controls(self):
        self.appendctrl('id')        
        self.appendctrl('causale')
        self.appendctrl('codice')
        self.appendctrl('idcausalefattura')        
        self.appendctrl('idtipocausale', ctrl=lib.frame.VirtualTextCtrl(), default='OFF')
        self.appendlkp(wx.ID_NONE, 'idcausalefattura')   