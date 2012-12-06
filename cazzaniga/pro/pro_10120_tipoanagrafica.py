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
        t = Table('tipoanag', meta, autoload=True)
        TIPOCODICE = Table('tipocodice', meta, autoload=True)
        s = select([t.c.id, t.c.tipoanag, TIPOCODICE.c.tipocodice])
        s = s.select_from(t.outerjoin(TIPOCODICE, t.c.idtipocodice==TIPOCODICE.c.id))
        s = s.order_by(t.c.id)
        rs = s.execute()
        self.fill_data(rs, [_('Codice'), _('Descrizione'), _('Tipo codice')])

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'tipoanag', **kwargs)
        self.listcol = ('id', 'tipoanag', 'idtipocodice')
        self.pkseq = 3
        self.init_controls()
        self.move_record(move)
            
    def init_controls(self):
        self.appendctrl('id')
        self.appendctrl('tipoanag')
        self.appendctrl('idtipocodice')
        self.appendlkp(wx.ID_NONE, 'idtipocodice') 