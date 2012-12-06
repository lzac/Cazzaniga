# -*- coding: utf-8 -*-

from moduli import *
import lib_menu as lib_menu
import lib_global as g
import lib_function as F
import lib_class as C
#-------------------------------------------------------------------------------------------------------------------------------------------
class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.showid = False
        self.get_data()    
        
        
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        SCA = Table('scadenzario', meta, autoload=True)   
        TIPOPAG = Table('tipopag', meta, autoload=True) 
        ANA = Table('anag', meta, autoload=True)
        s = select([SCA.c.id, 
                           ANA.c.anag,                           
                           SCA.c.numdoc,
                           SCA.c.data,
                           TIPOPAG.c.tipopag,
                           SCA.c.importo]) 
        s = s.select_from(SCA.outerjoin(ANA, SCA.c.idanag==ANA.c.id)
                                            .outerjoin(TIPOPAG, SCA.c.idtipopag==TIPOPAG.c.id))
        for k,v in self.filtro.iteritems():
            if isinstance(v, dict):
                if v['segno']=='>':
                    s = s.where(SCA.c[k]>=v['value'])
                elif v['segno']=='<':
                    s = s.where(SCA.c[k]<=v['value'])
                if v['segno']=='<>':
                    s = s.where(SCA.c[k].between(v['value'][0], v['value'][1]))
            elif isinstance(v, C.cFindstring):
                s = s.where(SCA.c[k].like('%'+v.descri+'%')) 
            else:
                s = s.where(SCA.c[k]==v)
        s = s.order_by(desc(SCA.c.data))      
        rs = s.execute() 
        self.fill_data(rs, [_('Id'),  _('CLiente'),_('Num fattura'), _('Data'),_('Tipo pagamento'), _('Importo')]) 
    
    
    def after_fill_data(self):
        xrc.XRCCTRL(self.riepilogo, 'count').SetValue(str(self.list.GetItemCount()))
        importo = 0
        for i in range(self.list.GetItemCount()):
            if self.list.GetItem(i, 5).GetText()!='':
                val = self.list.GetItem(i, 5).GetText()
                importo+=round(float(val), 2)
        xrc.XRCCTRL(self.riepilogo, 'importo').SetValue(F.FormatFloat(importo)) 

    
#-------------------------------------------------------------------------------------------------------------------------------------------
class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'scadenzario', **kwargs)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)       
        self.listcol = ('id', 'idanag', 'numdoc', 'data', 'idtipopag', 'importo')
        self.pkseq = 10                         
        self.init_controls()        
        self.move_record(move)        
    
    def init_controls(self):
        self.appendctrl('id')    
        self.appendctrl('idfattura')  
        self.appendctrl('data')    
        self.appendctrl('idanag')   
        self.appendctrl('numdoc')   
        self.appendctrl('idtipopag')
        self.appendctrl('importo', empty=True)   
        self.appendctrl('ispagato', empty=True)      
        self.appendctrl('idtipoanag', ctrl=lib.frame.VirtualTextCtrl())
        self.appendctrl('idtiposcadenzario', ctrl=lib.frame.VirtualTextCtrl(), default="PAG")
        #lookup  
        self.appendlkp(g.menu.CLIENTE, 'idanag')
        self.appendlkp(wx.ID_NONE, 'idtipopag')    
        self.appendcalendar('data')

        

#-------------------------------------------------------------------------------------------------------------------------------------------
class CustomDialog(lib.dialog.CustomDialog):
    def __init__(self, frame, **kwargs):  
        lib.dialog.CustomDialog.__init__(self, frame, **kwargs)
        self.init_controls()
        self.init_frame()

    def init_controls(self):
        self.appendctrl('idanag', empty=True, fillzero=6)  
        self.appendctrl('datainizio', empty=True)   
        self.appendctrl('datafine', empty=True)   
        self.appendctrl('numdoc', empty=True) 
        self.appendctrl('ispagato', empty=True) 
        self.appendctrl('idtipoanag', empty=True)   
        self.appendcalendar('datainizio')
        self.appendcalendar('datafine')   
        self.appendlkp(g.menu.CLIENTE, 'idanag') 
        self.appendlkp(g.menu.TIPOANAGRAFICA, 'idtipoanag') 
        self.get_ctrl('btn_conferma').Bind(wx.EVT_BUTTON, self.conferma)
        self.get_ctrl('btn_annulla').Bind(wx.EVT_BUTTON, self.annulla)
        self.get_filtro()        
            
    def get_filtro(self):
        for k,v in self.page.filtro.iteritems():
            if isinstance(v, dict):
                if k=='data':
                    if v['segno']=='>':                       
                        self.set_value('datainizio', F.datesql2print(v['value']))
                    elif v['segno']=='<':
                        self.set_value('datafine', F.datesql2print(v['value']))
                    elif v['segno']=='<>':
                        self.set_value('datainizio', F.datesql2print(v['value'][0]))
                        self.set_value('datafine', F.datesql2print(v['value'][1]))
            elif isinstance(v, C.cFindstring):
                self.set_value(k, v.descri)
            else:
                if k in self.controls:
                    self.set_value(k, v)
    
        
    def conferma(self, event):
        self.check_idanag()
        self.check_idtipoanag()
        self.check_data()
        self.check_numdoc()
        self.check_ispagato()
        self.page.get_data()
        self.frame.Destroy()

    def annulla(self, event):
        for ctrl in self.datacontrols:
            try:
                self.set_value(ctrl, '')
            except:
                self.set_value(ctrl, False)            
        self.conferma(None)   

                
    def check_numdoc(self):
        value = self.get_ctrl('numdoc').GetCurrValue()
        if value!=None:
            self.page.filtro['numdoc'] = C.cFindstring(value)
        else:
            if 'numdoc' in self.page.filtro.keys():
                del self.page.filtro['numdoc']

                
    def check_ispagato(self):
        value = self.get_ctrl('ispagato').GetCurrValue()
        if value==True:
            self.page.filtro['ispagato'] = value
        else:
            self.page.filtro['ispagato'] = None

    def check_idanag(self):
        value = self.get_ctrl('idanag').GetCurrValue()
        if value!=None:
            self.page.filtro['idanag'] = value
        else:
            if 'idanag' in self.page.filtro.keys():
                del self.page.filtro['idanag']
                
    def check_idtipoanag(self):
        value = self.get_ctrl('idtipoanag').GetCurrValue()
        if value!=None:
            self.page.filtro['idtipoanag'] = value
        else:
            if 'idtipoanag' in self.page.filtro.keys():
                del self.page.filtro['idtipoanag']

    def check_data(self):
        datainizio = self.get_ctrl('datainizio').GetCurrValue()
        datafine = self.get_ctrl('datafine').GetCurrValue()
        #Solo data inizio
        if datainizio!=None and datafine==None:
            self.page.filtro['data'] = {'segno':'>', 'value':datainizio}
        #Solo data fine
        elif datainizio==None and datafine!=None:
            self.page.filtro['data'] = {'segno':'<', 'value':datafine}
        #Data inizio e data fine
        elif datainizio!=None and datafine!=None:
            self.page.filtro['data'] = {'segno':'<>', 'value':[datainizio, datafine]}
        else:
            if 'data' in self.page.filtro.keys():
                del self.page.filtro['data']
