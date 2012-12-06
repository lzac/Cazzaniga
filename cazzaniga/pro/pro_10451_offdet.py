# -*- coding: utf-8 -*-

from moduli import *
import lib_function as f
import lib_global as g

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'offdet', **kwargs)
        self.listcol = ('id', 'descri','quantita', 'prezzo')
        self.pkseq = 3    
        self.init_controls()
        #Move
        self.move_record(move)    
         
    def init_controls(self):
        #Controlli
        self.appendctrl('idofferta')        
        self.appendctrl('id')    
        self.appendctrl('posizione', empty=True)    
        self.appendctrl('descri')
        self.appendctrl('destinazione', empty=True)
        self.appendctrl('ischiuso', empty=True)
        self.appendctrl('noteinizio1', empty=True)
        self.appendctrl('noteinizio2', empty=True)
        self.appendctrl('noteinizio3', empty=True)
        self.appendctrl('noteinizio4', empty=True)
        self.appendctrl('noteinizio5', empty=True)
        self.appendctrl('noteinizio6', empty=True)
        self.appendctrl('noteinizio7', empty=True)
        self.appendctrl('noteinizio8', empty=True)
        self.appendctrl('noteinizio9', empty=True)
        self.appendctrl('noteinizio10', empty=True)        
        self.appendctrl('notefine1', empty=True)
        self.appendctrl('notefine2', empty=True)
        self.appendctrl('notefine3', empty=True)
        self.appendctrl('notefine4', empty=True)
        self.appendctrl('notefine5', empty=True)
        self.appendctrl('notefine6', empty=True)
        self.appendctrl('notefine7', empty=True)
        self.appendctrl('notefine8', empty=True)
        self.appendctrl('notefine9', empty=True)
        self.appendctrl('notefine10', empty=True)
        self.appendctrl('isivato', empty=True)
        self.appendctrl('idiva', empty=True)
        self.appendctrl('quantita')
        self.appendctrl('prezzo')    
        #Lookup
        self.appendlkp(g.menu.IVA, 'idiva')  
                      
        
    def after_move_record(self, **d):
        if self.isappend or self.iscopy:
            iva = f.get_iva(self.FrameParent.get_value('idanag'))            
            if iva!=None:            
                self.set_value('idiva', f.sql2str(iva))
        else:
            list_buttons = ['btn_idiva', 'lkp_idiva']
            flag = self.get_value('ischiuso')            
            if flag!=True:
                flag = False
            flag = not flag                                    
            list_ctrl = self.controls.keys()
            list_not = ["idofferta", "id", "posizione","ischiuso"]
            for ctrl in list_ctrl:
                if ctrl not in list_not:
                    self.get_ctrl(ctrl).Enabled=flag
            for ctrl in list_buttons:
                if ctrl not in list_not:
                    self.get_ctrl(ctrl).Enabled=flag     
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag) 
                        
    def after_put_data(self):
        self.FrameParent.set_posizioni()
                
    def after_delete(self): 
        self.FrameParent.set_posizioni()                                    
            
            
                