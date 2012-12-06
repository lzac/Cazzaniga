# -*- coding: utf-8 -*-

from moduli import *

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'ratapag', **kwargs)
        
        self.listcol = ('id', 'idtipopag', 'frequenza', 'idtiposcadenza')
        self.pkseq = 3
        
        self.init_controls()
        self.move_record(move)        


    def init_controls(self):
        self.appendctrl('idmodopag')        
        self.appendctrl('id')
        self.appendctrl('idtipopag')        
        self.appendctrl('frequenza', empty=True, )
        self.appendctrl('idtiposcadenza')
        self.appendctrl('giornipiu', empty=True)
        self.appendlkp(lib.g.menu.TIPOPAG, 'idtipopag')
        self.appendlkp(wx.ID_NONE, 'idtiposcadenza')                                 