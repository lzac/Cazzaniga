# -*- coding: utf-8 -*-

from moduli import * 
import images
import datetime
import lib_file as File

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.get_data()

    def get_data(self):
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('nazione', meta, autoload=True)
        s = select([t.c.id, t.c.nazione]).order_by(t.c.id)
        rs = s.execute()
        self.fill_data(rs, [_('Sigla'), _('Nazione')])

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'nazione', **kwargs)
        self.listcol = ('id', 'nazione')
        self.pkseq = 0
        self.init_controls()
        self.move_record(move)
            
    def init_controls(self):
        self.appendctrl('id')
        self.appendctrl('nazione')