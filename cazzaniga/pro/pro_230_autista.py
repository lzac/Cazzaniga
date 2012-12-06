# -*- coding: utf-8 -*-

from moduli import * 

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()

    def get_data(self):
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('autista', meta, autoload=True)
        s = select([t.c.id, t.c.autista]).order_by(t.c.id)
        rs = s.execute()
        self.fill_data(rs, [_('Codice'), _('Autista')])

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'autista', **kwargs)
        self.listcol = ('id', 'autista')
        self.pkseq = 3
        self.init_controls()
        self.move_record(move)
            
    def init_controls(self):
        self.appendctrl('id')
        self.appendctrl('autista')        
        self.appendctrl('datanascita', empty=True)
        self.appendctrl('numeropatente', empty=True)
        self.appendctrl('datainiziocollaborazione', empty=True)
        # Calendari
        self.appendcalendar('datanascita')
        self.appendcalendar('datainiziocollaborazione')