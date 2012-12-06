# -*- coding: utf-8 -*-

from moduli import *

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()
                
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('postpag', meta, autoload=True)    
        s = select([t.c.id, t.c.postpag]).order_by(t.c.id)
        rs = s.execute() 
        self.fill_data(rs, [_('Codice'), _('Posticipo pagamento')])   
        

class EditFrame(lib.frame.EditFrame):
    
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'postpag', **kwargs)

        self.listcol = ('id', 'postpag')
        self.pkseq = 2

        self.init_controls()
        self.move_record(move)
               
    def init_controls(self):
        self.appendctrl('id')   
        self.appendctrl('postpag')   
        self.appendctrl('m01', empty=True)        
        self.appendctrl('m02', empty=True)
        self.appendctrl('m03', empty=True)
        self.appendctrl('m04', empty=True)
        self.appendctrl('m05', empty=True)
        self.appendctrl('m06', empty=True)
        self.appendctrl('m07', empty=True)
        self.appendctrl('m08', empty=True)
        self.appendctrl('m09', empty=True)
        self.appendctrl('m10', empty=True)
        self.appendctrl('m11', empty=True)
        self.appendctrl('m12', empty=True)                    
        