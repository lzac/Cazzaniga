# -*- coding: utf-8 -*-

from moduli import *

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()
                
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('spesa', meta, autoload=True)    
        s = select([t.c.id, t.c.spesa]).order_by(t.c.id)
        rs = s.execute() 
        self.fill_data(rs, [_('Codice'), _('Spesa')])        
    
class EditFrame(lib.frame.EditFrame):
    
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'spesa', **kwargs)
        self.listcol = ('id', 'spesa')
        self.pkseq = 2     
        self.init_controls()
        self.move_record(move)

    def init_controls(self):
        self.appendctrl('id')   
        self.appendctrl('spesa')   
                                