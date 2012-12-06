# -*- coding: utf-8 -*-

from moduli import *
import lib_global as g
import pro_10401_fatdet as p10401
import pro_10402_fatspesa as p10402
import pro_30020_scainc as p30020
import pro_30021_scapag as p30021
import lib_function as F
import math
import lib_class as C
from datetime import date
import lib_file as File
import win32com.client
import subprocess
from decimal import *


class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.showid = False
        self.get_data()
      
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('fattura', meta, autoload=True)     
        CAU = Table('causale', meta, autoload=True)  
        MODOPAG = Table('modopag', meta, autoload=True)  
        ANA = Table('anag', meta, autoload=True) 
        s = select([t.c.id, CAU.c.causale, t.c.data, t.c.numero,  ANA.c.anag, MODOPAG.c.modopag, 
                           t.c.imponibile, t.c.imposta, t.c.totale]) 
        s = s.select_from(t.outerjoin(CAU, t.c.idcausale==CAU.c.id)
                                       .outerjoin(ANA, t.c.idanag==ANA.c.id)
                                       .outerjoin(MODOPAG, t.c.idmodopag==MODOPAG.c.id))   
        for k,v in self.filtro.iteritems():
            if isinstance(v, dict):
                if v['segno']=='>':
                    s = s.where(t.c[k]>=v['value'])
                elif v['segno']=='<':
                    s = s.where(t.c[k]<=v['value'])
                if v['segno']=='<>':
                    s = s.where(t.c[k].between(v['value'][0], v['value'][1]))
            elif isinstance(v, list):
                s = s.where(t.c[k].in_(v))
            elif isinstance(v, C.cFindstring):
                s = s.where(t.c[k].like('%'+v.descri+'%')) 
            else:
                s = s.where(t.c[k]==v)
        s = s.order_by(desc(t.c.data),  desc(t.c.protocollo))               
        rs = s.execute() 
        self.RightCols = [6,7,8]
        self.fill_data(rs, [_('Id'), _('Causale'), _('Data'), _('Numero'), _('Ragione sociale'), _('Mod. pagamento'), _('Imponibile'), _('Imposta'), _('Totale')])
        
    def after_fill_data(self):
        xrc.XRCCTRL(self.riepilogo, 'count').SetValue(str(self.list.GetItemCount()))
        totale = 0
        imponibile = 0
        imposta = 0
        for i in range(self.list.GetItemCount()):
            if self.list.GetItem(i, 6).GetText()!='':
                val = self.list.GetItem(i, 6).GetText()
                imponibile+=round(float(val), 2)
            if self.list.GetItem(i, 7).GetText()!='':
                val = self.list.GetItem(i, 7).GetText()
                imposta+=round(float(val), 2)
            if self.list.GetItem(i, 8).GetText()!='':
                val = self.list.GetItem(i, 8).GetText()
                totale+=round(float(val), 2)
        xrc.XRCCTRL(self.riepilogo, 'imponibile').SetValue(F.FormatFloat(imponibile)) 
        xrc.XRCCTRL(self.riepilogo, 'imposta').SetValue(F.FormatFloat(imposta))     
        xrc.XRCCTRL(self.riepilogo, 'totale').SetValue(F.FormatFloat(totale)) 

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'fattura', **kwargs)
        self.showid = False
        self.isdoc = True
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)       
        self.listcol = ('id', 'idcausale', 'data', 'numero', 'idanag', 'modopag', 'imponibile', 'imposta', 'totale')
        self.tabdel = ('fatdet', 'idfattura', 'fatspesa', 'idfattura', 'fativa', 'idfattura', 'scadenzario', 'idfattura')
        self.pkseq = 6                     
        self.init_controls()      
        #Ulteriori elementi della toolbar
        self.toolbar.AddSeparator() 
        # Fatturazione preventivi
        self.toolbar.AddLabelTool(g.menu.EVASIONE_OFFERTA, _('Preventivi'), wx.ArtProvider.GetBitmap(wx.ART_REPORT_VIEW), shortHelp=_('Fatturazione preventivi'))       
        self.frame.Bind(wx.EVT_TOOL, self.evasione, id=g.menu.EVASIONE_OFFERTA)    
        self.toolbar.AddSeparator() 
        # Anteprima
        self.toolbar.AddLabelTool(g.menu.ANTEPRIMA_FATTURA, _('Anteprima'), wx.ArtProvider.GetBitmap(wx.ART_PRINT), shortHelp= _('Anteprima')) 
        self.frame.Bind(wx.EVT_TOOL, self.anteprima, id=g.menu.ANTEPRIMA_FATTURA)     
        # Apri Mail
        self.toolbar.AddLabelTool(g.menu.MAIL_FATTURA, _('Mail'), wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE), shortHelp= _('Mail')) 
        self.frame.Bind(wx.EVT_TOOL, self.mail, id=g.menu.MAIL_FATTURA)                  
        self.toolbar.Realize()          
        #Move
        self.move_record(move) 
        self.get_ctrl('idanag').Bind(wx.EVT_TEXT, self.change_anag)      
        #Data
        self.appendcalendar('data', after_lookup='_AfterLookupData')  
        self.check_date()                  
              
    def init_controls(self):
        self.appendctrl('id')     
        self.appendctrl('idazienda', ctrl=lib.frame.VirtualTextCtrl(), default=lib.g.idazienda)
        self.appendctrl('idcausale')
        self.appendctrl('data', empty=True)               
        self.appendctrl('protocollo', empty=True)
        self.appendctrl('numero', empty=True)
        self.appendctrl('recapito', empty=True)
        self.appendctrl('idanag', fillzero=6)
        self.appendctrl('anag', empty=True)
        self.appendctrl('imponibile', empty=True)
        self.appendctrl('imposta', empty=True)
        self.appendctrl('totale', empty=True)    
        self.appendctrl('idmodopag', fillzero=3)
        self.appendctrl('descrizionebanca', empty=True)
        self.appendctrl('contoc', empty=True)
        self.appendctrl('iban', empty=True)
        self.appendctrl('idbancacc', empty=True)
        self.appendctrl('noteinterne', empty=True)
        self.appendctrl('notepiepagina', empty=True)    
        self.appendctrl('idtipoanag', ctrl=lib.frame.VirtualTextCtrl())             
        #Lookup      
        self.appendlkp(g.menu.CAUSALE_FATTURA, 'idcausale', **{'idtipocausale':'FAT'})
        self.appendlkp(g.menu.CLIENTE, 'idanag')                               
        self.appendlkp(g.menu.MODOPAG, 'idmodopag')  
        self.appendlkp(g.menu.BANCACC, 'idbancacc')      
        #detail
        self.add_detail('list_dettagli', getattr(self,'get_dettagli'))
        self.add_detail('list_spese', getattr(self,'get_spese'))  
        self.add_detail('list_iva', getattr(self, 'get_iva')) 
        self.add_detail('list_scadenzario', getattr(self, 'get_scadenzario'))
        self.f_descri = xrc.XRCCTRL(self.frame, 'txt_descri')                   
        #Eventi
        self.get_ctrl('data').Bind(wx.EVT_KILL_FOCUS, self._CheckData) 
        self.get_ctrl('idcausale').Bind(wx.EVT_CHOICE, self.evt_change_causale)
        self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selected, id=self.get_ctrlid('list_dettagli'))
        self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.apri_dettaglio, id=self.get_ctrlid('list_dettagli'))       
        self.frame.Bind(wx.EVT_BUTTON, self.nuovo_dettaglio, id=self.get_ctrlid('btn_nuovodettaglio'))
        self.frame.Bind(wx.EVT_BUTTON, self.elimina_dettaglio, id=self.get_ctrlid('btn_eliminadettaglio'))
        self.frame.Bind(wx.EVT_BUTTON, self.apri_dettaglio, id=self.get_ctrlid('btn_apridettaglio'))
        self.frame.Bind(wx.EVT_BUTTON, self.elimina_spesa, id=self.get_ctrlid('btn_eliminaspesa'))
        self.frame.Bind(wx.EVT_BUTTON, self.apri_spesa, id=self.get_ctrlid('btn_aprispesa'))          
        self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.apri_spesa, id=self.get_ctrlid('list_spese'))       
        self.frame.Bind(wx.EVT_BUTTON, self.nuova_spesa, id=self.get_ctrlid('btn_nuovaspesa'))           
        self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.apri_scadenza, id=self.get_ctrlid('list_scadenzario'))    
        self.get_ctrl('btn_createsca').Bind(wx.EVT_BUTTON, self.recreate_sca)
    
    def recreate_sca(self, event):
        self.create_values()
        
        
    def after_dont_save(self):
        if (self.isappend or self.iscopy) and not self.saved:
            self.before_delete()
            
            
    def before_delete(self):
        FATDET = Table('fatdet', self.meta, autoload=True)
        SCA = Table('scadenzario', self.meta, autoload=True)  
        # Apro posizioni offerte
        s = select([FATDET.c.idofferta, FATDET.c.idoffdet])
        s = s.where(FATDET.c.idfattura==self.get_value('id'))
        rs = s.execute()
        for row in rs: 
            if row['idofferta']!=None and row['idoffdet']!=None:
                self.open_offdet(row['idofferta'], row['idoffdet'])                    
        # Elimino scandenzario        
        s = select([SCA.c.id])
        s = s.where(SCA.c.idfattura==self.get_value('id'))
        rs = s.execute()
        for row in rs:
            s = SCA.delete()
            s = s.where(SCA.c.id==row.id)
            s.execute()     
        
    def after_move_record(self, **d):
        if self.isappend:
            list_not = ['idcausale', 'data']
            list_buttons = ['btn_idanag', 'lkp_idanag', 'btn_idmodopag', 'lkp_idmodopag',
                                     'btn_nuovodettaglio', 'btn_apridettaglio', 'btn_eliminadettaglio',
                                      'btn_nuovaspesa', 'btn_aprispesa', 'btn_eliminaspesa', 'btn_idbancacc', 'lkp_idbancacc']
            flag = self.getBlockCausaleCond()
            list_ctrl = self.controls.keys()
            for ctrl in list_ctrl:
                if ctrl not in list_not:
                    self.get_ctrl(ctrl).Enabled=flag
            for ctrl in list_buttons:
                self.get_ctrl(ctrl).Enabled=flag
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)                                    
        else:
            list_buttons = ['idcausale', 'data', 'btn_idanag', 'lkp_idanag', 'btn_idmodopag', 'lkp_idmodopag',
                                     'btn_nuovodettaglio', 'btn_apridettaglio', 'btn_eliminadettaglio',
                                      'btn_nuovaspesa', 'btn_aprispesa', 'btn_eliminaspesa', 'btn_idbancacc', 'lkp_idbancacc', 'btn_data',
                                      'list_dettagli', 'list_spese', 'list_iva']
            flag = self.get_isclosed()
            flag = not flag
            list_ctrl = self.controls.keys()
            for ctrl in list_ctrl:
                self.get_ctrl(ctrl).Enabled=flag
            for ctrl in list_buttons:
                self.get_ctrl(ctrl).Enabled=flag   
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)                    
                     
        self.get_ctrl('numero').Enabled=False   
        self.get_ctrl('protocollo').Enabled=False       
            
            
    def getBlockCausaleCond(self):
        if self.get_ctrl('idcausale').GetCurrValue()==None:
            return False
        return True
            
            
    def check_date(self):
        if self.get_ctrl('data').GetCurrValue()==None:
            v = str(datetime.date.today())
            v = v[:4]+v[5:7]+v[8:]
            self.get_ctrl('data').SetStartValue(v)   
        

    def get_isclosed(self):
        FAT = Table('fattura', self.meta, autoload=True)
        SCA = Table('scadenzario', self.meta, autoload=True)
        #Controllo se è gia stata pagata qualche rata
        s = select([SCA.c.ispagato])
        s = s.where(SCA.c.idfattura==self.get_value('id'))
        row = s.execute().fetchone()
        if row.ispagato!=None:
            return True
        # Controllo che siano passati 60 giorni
        s = select([FAT.c.data])
        s = s.where(FAT.c.id==self.get_value('id'))
        row = s.execute().fetchone()        
        if row!=None:
            datafattura = date(int(row.data[:4]), int(row.data[-4:-2]), int(row.data[-2:]))
            dataodierna = date.today()
            delta = dataodierna - datafattura
            if delta.days>60:
                return True
        return False
        
    def evt_change_causale(self, event):
        if self.get_ctrl('data').GetCurrValue()!=None:
            numbers_dict = lib.sql.protocollo(self.get_value('idcausale'), self.get_ctrl('data').GetCurrValue(), 'fattura')                             
            self.set_value('protocollo', numbers_dict['protocollo'])
            self.set_value('numero', numbers_dict['numero'])
            self.after_move_record(**{})
        else:
            dlg = wx.MessageDialog(None, _("Inserire data!"), _("Errore"), wx.OK)
            dlg.ShowModal()
            dlg.Destroy() 
                       
    def change_anag(self, event):          
        ANA = Table('anag', self.meta, autoload=True)
        BANCACC = Table('bancacc', self.meta, autoload=True)
        s = ANA.select()
        s = s.where(ANA.c.id==self.get_value('idanag'))
        rs = s.execute()
        row = rs.fetchone()
        if row!=None:
            self.set_value('idmodopag', F.sql2str(row.idmodopag)) 
            self.set_value('recapito', F.sql2str(row.recapito)) 
            self.set_value('descrizionebanca', F.sql2str(row.descrizionebanca)) 
            self.set_value('contoc', F.sql2str(row.contoc)) 
            self.set_value('iban', F.sql2str(row.iban)) 
            self.controls['idtipoanag'].SetValue(F.sql2str(row.idtipoanag))            
            s = select([BANCACC.c.id])
            s = s.where(BANCACC.c.ispredefinito==True)
            row = s.execute().fetchone()
            if row!=None:
                self.set_value('idbancacc', F.sql2str(row.id))             
                
                  
    def selected(self, event):
        try:
            t = Table('fatdet', self.meta, autoload=True)
            selected = self.get_ctrl('list_dettagli').GetFocusedItem()
            if selected==-1:
                selected=0
            selected_id = self.get_ctrl('list_dettagli').GetItem(selected, 0).GetText()
            s = t.select()
            s = s.where(t.c.idfattura==self.get_value('id'))
            s = s.where(t.c.id==selected_id)
            rs = s.execute()
            row = rs.fetchone()
            descri = ""
            if row!=None:           
                descri+= F.sql2str(row.noteinizio1)+"\n"
                descri+= F.sql2str(row.noteinizio2)+"\n"
                descri+= F.sql2str(row.noteinizio3)+"\n"
                descri+= F.sql2str(row.noteinizio4)+"\n"
                descri+= F.sql2str(row.noteinizio5)+"\n"
                descri+= F.sql2str(row.noteinizio6)+"\n"
                descri+= F.sql2str(row.noteinizio7)+"\n"
                descri+= F.sql2str(row.noteinizio8)+"\n"
                descri+= F.sql2str(row.noteinizio9)+"\n"
                descri+= F.sql2str(row.noteinizio10)+"\n"
                descri+= F.sql2str(row.notefine1)+"\n"
                descri+= F.sql2str(row.notefine2)+"\n"
                descri+= F.sql2str(row.notefine3)+"\n"
                descri+= F.sql2str(row.notefine4)+"\n"
                descri+= F.sql2str(row.notefine5)+"\n"
                descri+= F.sql2str(row.notefine6)+"\n"
                descri+= F.sql2str(row.notefine7)+"\n"
                descri+= F.sql2str(row.notefine8)+"\n"
                descri+= F.sql2str(row.notefine9)+"\n"
                descri+= F.sql2str(row.notefine10)+"\n"
            self.f_descri.SetValue(descri)
        except Exception, e:
            print e
            

    def get_dettagli(self):  
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')
        ctrl.ClearAll()              
        DET = Table('fatdet', self.meta, autoload=True)             
        cols = [_('Id'), _('Descrizione'), _('Quantita'), _(u'Prezzo'), _(u'Sconto (%)'),  _(u'Importo')]        
        s = select([DET.c.id, 
                           DET.c.descri, 
                           DET.c.quantita,      
                           DET.c.prezzo,    
                           DET.c.scontoperc,                        
                           DET.c.importo])
        s = s.where(DET.c.idfattura==self.get_value('id'))
        s = s.order_by(DET.c.id)
        rs = s.execute()       
        ctrl.FillData(rs, cols) 

        
    def get_spese(self):
        ctrl = xrc.XRCCTRL(self.frame, 'list_spese')
        ctrl.ClearAll()
        DET = Table('fatspesa', self.meta, autoload=True) 
        SPESA = Table('spesa', self.meta, autoload=True)             
        cols = [_('Pos.'), _('Spesa'), _('Iva'), _('Imponibile')]        
        s = select([DET.c.id, SPESA.c.spesa, DET.c.idiva, DET.c.imponibile])
        s = s.select_from(DET.outerjoin(SPESA, DET.c.idspesa==SPESA.c.id))
        s = s.where(DET.c.idfattura==self.get_value('id'))
        s = s.order_by(DET.c.id)
        rs = s.execute()       
        ctrl.FillData(rs, cols)
        ctrl.SetColumnWidth(0, 0) 
        
        
    def get_iva(self):
        ctrl = xrc.XRCCTRL(self.frame, 'list_iva')
        ctrl.ClearAll()
        t = Table('fativa', self.meta, autoload=True) 
        IVA = Table('iva', self.meta, autoload=True)            
        cols = [_('Posizione'),_('Iva'), _('Imponibile'), _('Imposta'), _('Totale')]        
        s = select([t.c.id, IVA.c.iva, t.c.imponibile, t.c.imposta, t.c.totale])
        s = s.select_from(t.outerjoin(IVA, t.c.idiva==IVA.c.id))
        s = s.where(t.c.idfattura==self.get_value('id'))
        s = s.order_by(t.c.id)
        rs = s.execute()           
        ctrl.FillData(rs, cols) 
        ctrl.SetColumnWidth(0, 0)        
        
        
    def get_scadenzario(self):
        ctrl = xrc.XRCCTRL(self.frame, 'list_scadenzario')
        ctrl.ClearAll()
        SCA = Table('scadenzario', self.meta, autoload=True)
        ANA = Table('anag', self.meta, autoload=True)
        TIPOPAG = Table('tipopag', self.meta, autoload=True)
        cols = [_('Posizione'), _('Cliente'), _('N° doc.'), _('Data'), _('Tipo pagamento'), _('Importo')]                
        s = select([SCA.c.id, ANA.c.anag, SCA.c.numdoc, SCA.c.data, TIPOPAG.c.tipopag, SCA.c.importo])
        s = s.select_from(SCA.outerjoin(TIPOPAG, SCA.c.idtipopag==TIPOPAG.c.id)
                                            .outerjoin(ANA, SCA.c.idanag==ANA.c.id))
        s = s.where(SCA.c.idfattura==self.get_value('id'))
        s = s.order_by(SCA.c.data)
        rs = s.execute()           
        ctrl.FillData(rs, cols) 
        for j in [0, 1, 2]:
            ctrl.SetColumnWidth(j, 0)        
        

    def nuovo_dettaglio(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')
        kwargs = {'pkfrom': {'idfattura': self.get_value('id')}, 'parent_frame':self}                
        f = p10401.EditFrame(g.menu.FATDET, _('Posizioni fattura'), ctrl, ctrl.pk, lib.g.RECORD_APPEND, {'idfattura': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()  
    
    
    def nuova_spesa(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_spese')
        kwargs = {'pkfrom': {'idfattura': self.get_value('id')}, 'parent_frame':self}                
        f = p10402.EditFrame(g.menu.FATSPESA, _('Spesa'), ctrl, ctrl.pk, lib.g.RECORD_APPEND, {'idfattura': self.get_value('id')}, **kwargs)
        f.frame.Show()      
        
    def apri_dettaglio(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')
        kwargs = {'pkfrom': {'idfattura': self.get_value('id')}, 'parent_frame':self}                
        f = p10401.EditFrame(g.menu.FATDET, _('Posizioni fattura'), ctrl, ctrl.pk, lib.g.RECORD_CURRENT, {'idfattura': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()
        
        
    def apri_spesa(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_spese')
        kwargs = {'pkfrom': {'idfattura': self.get_value('id')}, 'parent_frame':self}                
        f = p10402.EditFrame(g.menu.FATSPESA, _('Spesa'), ctrl, ctrl.pk, lib.g.RECORD_CURRENT, {'idfattura': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()
        
        
    def apri_scadenza(self, event):
        CAU = Table('causale', self.meta, autoload=True)
        s = select([CAU.c.idtiposcadenzario])
        s = s.where(CAU.c.id==self.get_value('idcausale'))
        row = s.execute().fetchone()
        # recupero tipo sacadenzario
        if row.idtiposcadenzario=='INC':
            ctrl = xrc.XRCCTRL(self.frame, 'list_scadenzario')
            kwargs = {'pkfrom': {'idfattura': self.get_value('id')}, 'parent_frame':self}                
            f = p30020.EditFrame(g.menu.SCAINC, _('Scadenza'), ctrl, ctrl.pk, lib.g.RECORD_CURRENT, {'idfattura': self.get_value('id')}, **kwargs)
            f.frame.MakeModal(True)
            f.frame.Show()      
        if row.idtiposcadenzario=='PAG':
            ctrl = xrc.XRCCTRL(self.frame, 'list_scadenzario')
            kwargs = {'pkfrom': {'idfattura': self.get_value('id')}, 'parent_frame':self}                
            f = p30021.EditFrame(g.menu.SCAPAG, _('Scadenza'), ctrl, ctrl.pk, lib.g.RECORD_CURRENT, {'idfattura': self.get_value('id')}, **kwargs)
            f.frame.MakeModal(True)
            f.frame.Show()              
          
          
    def elimina_dettaglio(self, event):
        FATDET = Table('fatdet', self.meta, autoload=True)
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')   
        recno = ctrl.GetFocusedItem()
        # Prendo riferimenti offerta
        s = select([FATDET.c.idofferta, FATDET.c.idoffdet])
        s = s.where(FATDET.c.idfattura==self.get_value('id'))
        s = s.where(FATDET.c.id==ctrl.pk[recno])
        row = s.execute().fetchone()
        idofferta = row['idofferta']
        idoffdet = row['idoffdet']
        if F.elimina_posizione(ctrl, 'posizione', 'fatdet', {'idfattura':self.get_value('id'), 'id':ctrl.pk[recno]}):
            if idofferta!=None and idoffdet!=None:
                self.open_offdet(idofferta, idoffdet)            
        self.create_values()
        
        
    def open_offdet(self, idofferta, idoffdet):        
        OFFDET = Table('offdet', self.meta, autoload=True)
        s = OFFDET.update()
        s = s.where(OFFDET.c.idofferta==idofferta)
        s = s.where(OFFDET.c.id==idoffdet)
        s.execute({'ischiuso':None})
        
            
    def elimina_spesa(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_spese')   
        recno = ctrl.GetFocusedItem()
        F.elimina_posizione(ctrl, 'spesa', 'fatspesa', {'idfattura':self.get_value('id'), 'id':ctrl.pk[recno]})
        self.create_values()
        
    def totale_values(self):
        FAT = Table('fattura', self.meta, autoload=True)
        FATIVA = Table('fativa', self.meta, autoload=True)
        s = select([func.sum(FATIVA.c.imponibile).label('imponibile'),
                           func.sum(FATIVA.c.imposta).label('imposta'),
                           func.sum(FATIVA.c.totale).label('totale')])
        s = s.where(FATIVA.c.idfattura==self.get_value('id'))
        row = s.execute().fetchone()
        if row!=None:
            insert_dict = dict(imponibile=row.imponibile, imposta=row.imposta, totale=row.totale)          
            self.get_ctrl('imponibile').Set_Value(insert_dict['imponibile'])
            self.get_ctrl('imposta').Set_Value(insert_dict['imposta'])
            self.get_ctrl('totale').Set_Value(insert_dict['totale'])
            

            print insert_dict
            
            s = FAT.update()
            s = s.where(FAT.c.id==self.get_value('id'))
            s.execute(insert_dict)

                    
    def create_values(self):
        self.set_iva()
        self.totale_values()
        self.create_scadenzario()
        self.get_iva()
        self.get_scadenzario()

                    
    def set_iva(self):
        FATDET = Table('fatdet', self.meta, autoload=True)
        FATSPESA = Table('fatspesa', self.meta, autoload=True)
        FATIVA = Table('fativa', self.meta, autoload=True)
        IVA = Table('iva', self.meta, autoload=True)
        #Elimino elementi già presenti in fativa
        s = FATIVA.delete()
        s = s.where(FATIVA.c.idfattura==self.get_value('id'))
        s.execute()
        #Raggruppo i dettagli della fattura
        s_det = select([func.sum(FATDET.c.importo).label('sum'),  FATDET.c.idiva], group_by=[FATDET.c.idiva])
        s_det = s_det.where(FATDET.c.idfattura==self.get_value('id'))
        #Raggruppo le spese della fattura
        s_spesa = select([func.sum(FATSPESA.c.imponibile).label('sum'), FATSPESA.c.idiva], group_by=[FATSPESA.c.idiva])
        s_spesa = s_spesa.where(FATSPESA.c.idfattura==self.get_value('id'))
        #Effettuo l'unione e la somma
        s = union_all(s_det, s_spesa)  
        SUM = s.alias('prova')
        s  = select([SUM.c.idiva.label('idiva'),
                            func.sum(SUM.c.sum).label('sum')], group_by=[SUM.c.idiva])
        rs = s.execute()
        #Inserimento
        for row in rs:
            #Seleziono aliquota collegata all'iva del dettaglio
            s = select([IVA.c.aliquota])
            s = s.where(IVA.c.id==row['idiva'])
            r = s.execute().fetchone()
            if r.aliquota==None:
                aliquota = 0
            else:
                aliquota = r.aliquota
            imposta = (row.sum/100)*aliquota
            totale = row.sum+imposta
            s = FATIVA.insert()  
            d = {
                 'idfattura' : self.get_value('id'),
                 'id' : self.get_pk_fativa(),
                 'imponibilefat' : row.sum,
                 'sconto' : 0,
                 'scontoperc' : 0,
                 'imponibile' : row.sum,
                 'imposta' : imposta,
                 'totale' : totale,
                 'idiva' : row.idiva,
                }
            s.execute(d)
            
    def create_scadenzario(self):
        FATIVA = Table('fativa', self.meta, autoload=True)
        RATAPAG = Table("ratapag", self.meta, autoload=True)
        SCA = Table('scadenzario', self.meta, autoload=True)
        #Elimino scadenze gia inserite
        s = SCA.delete()
        s = s.where(SCA.c.idfattura==self.get_value('id'))
        s.execute()
        #Seleziono il totale della fattura da fativa
        s = select([func.sum(FATIVA.c.totale).label('totale')])
        s = s.where(FATIVA.c.idfattura==self.get_value('id'))
        row = s.execute().fetchone()
        totale_fattura = row.totale
        #Seleziono il modo pagamento della fattura e le relative rate
        s = RATAPAG.select()
        s = s.where(RATAPAG.c.idmodopag==self.get_value('idmodopag'))
        n_rate = 0
        for k in s.execute():
            n_rate+=1
        for ratapag in s.execute():
            dict_insert = dict()
            dict_insert['idfattura'] = self.get_value('id')
            dict_insert['idanag'] = self.get_value('idanag')
            dict_insert['numdoc'] = self.get_value('numero')            
            dict_insert['id'] = self.get_pk_scadenzario()
            dict_insert['data'] = self.get_data_sca(self.get_ctrl('data').GetCurrValue(), ratapag)   
            dict_insert['idtiposcadenzario'] = self.get_tipo_scadenzario()
            dict_insert['idtipopag'] = ratapag.idtipopag  
            dict_insert['importo'] = totale_fattura/n_rate   
            dict_insert['idtipoanag'] = self.get_value('idtipoanag')
            SCA.insert().execute(dict_insert)
    
    def get_tipo_scadenzario(self):
        CAU = Table('causale', self.meta, autoload=True)
        s = select([CAU.c.idtiposcadenzario])
        s = s.where(CAU.c.id==self.get_value('idcausale'))
        row = s.execute().fetchone()
        return row.idtiposcadenzario
                           
    def get_data_sca(self, data, rata):
        POSTPAG = Table('postpag', self.meta, autoload=True)
        ANA = Table('anag', self.meta, autoload=True)
        val = str(data)                  
        datainizio = datetime.date(int(val[:4]), int(val[4:6]), int(val[6:8]))   
        if rata['frequenza']!=None:
            if rata['idtiposcadenza']=='DF':
                delta = datetime.timedelta(days=int(rata['frequenza']))
                datainizio = datainizio+delta
            elif rata['idtiposcadenza']=='FM':
                datainizio = F.AddMonths(datetime.datetime(datainizio.year, datainizio.month, 1), math.floor(int(rata['frequenza'])/28))
                datainizio = F.last_day_of_month(datainizio.year, datainizio.month) 
        if rata['giornipiu']!=None:
            delta = datetime.timedelta(days=int(rata['giornipiu']))
            datainizio = datainizio+delta
        val = str(datainizio)
        DATA = val[:4]+val[5:7]+val[8:]     
            #Seleziono ultimo giorno del mese su cui sono      
        anno = int(DATA[:4])
        mese = int(DATA[4:6])
        DATA_APP = str(F.last_day_of_month(anno, mese)).replace('-', '')
        #Controllo se esiste posticipo pagamento sull'anagrafica   
        if DATA==DATA_APP:
            MESI = {'01':'m01', '02':'m02', '03':'m03', '04':'m04',
                         '05':'m05', '06':'m06', '07':'m07', '08':'m08',
                         '09':'m09', '10':'m10', '11':'m11', '12':'m12'}
            s = select([POSTPAG.c['%s' % MESI[DATA[-4:-2]]].label('mese')])
            s = s.where(POSTPAG.c.id==ANA.c.idpostpag)
            s = s.where(ANA.c.id==self.get_value('idanag'))
            row = s.execute().fetchone()
            if row!=None:
                if row.mese!=None:
                    delta = datetime.timedelta(days=int(row.mese))
                    DATA = str(datetime.date(int(DATA[:4]), int(DATA[4:6]), int(DATA[6:8]))+delta)    
                    DATA = DATA[:4]+DATA[5:7]+DATA[8:]   
        return DATA
    
    
    def get_pk_fativa(self):
        t = Table('fativa', self.meta, autoload=True)
        s = select([func.max(t.c.id)])
        s = s.where(t.c.idfattura==self.get_value('id'))       
        rs = s.execute()
        row = rs.fetchone()
        try:
            i = int(row[0])
        except:
            i = 0
        if i == 0:
            pk = '%0*d' % (3, 1)
        else:
            pk = '%0*d' % (3, i + 1)
        return pk
    
    
    def get_pk_scadenzario(self):
        t = Table('scadenzario', self.meta, autoload=True)
        s = select([func.max(t.c.id)])
        rs = s.execute()
        row = rs.fetchone()
        try:
            i = int(row[0])
        except:
            i = 0
        if i == 0:
            pk = '%0*d' % (10, 1)
        else:
            pk = '%0*d' % (10, i + 1)
        return pk        
    
    def anteprima(self, event):
        if not self.isappend:
            file = self.stampa()
            File.aprifile(self.stampa(), True)  
        else:
            wx.MessageDialog(None, _("Impossibile stampare fattura, salvarla prima!"),  g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
    
    def mail(self, event):
        if not self.isappend:
            file = self.stampa()
            ANA = Table('anag', self.meta, autoload=True)
            T = Table('percorso', self.meta, autoload=True)
            # Recupero email cliente
            s = select([ANA.c.email])
            s = s.where(ANA.c.id==self.get_value('idanag'))
            row = s.execute().fetchone()
            EMAIL = F.sql2str(row.email)
            # Prendo percorso thunderbiurd e lo apro
            s = select([T.c.path])
            s = s.where(T.c.id=="THUNDERBIRD")
            thunderbird_path = s.execute().fetchone().path        
            subprocess.Popen("cd "+thunderbird_path, shell=True)
            titolo_mail = F.sql2str(self.get_ctrl('idcausale').GetStringSelection())+"  "+F.sql2str(self.get_value('numero')) 
            if EMAIL!=None:
                subprocess.Popen("""thunderbird -compose "to='%s',subject='%s',attachment='%s'" """%(EMAIL, titolo_mail, file), shell=True)
            else:
                subprocess.Popen("""thunderbird -compose "subject='%s',attachment='%s'" """%(titolo_mail, file), shell=True)
        else:
            wx.MessageDialog(None, _("Impossibile stampare fattura, salvarla prima!"),  g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()                
    
    def stampa(self): 
        ANA = Table('anag', self.meta, autoload=True)
        IVA = Table('iva', self.meta, autoload=True)
        CAU = Table('causale', self.meta, autoload=True)
        MODOPAG = Table('modopag', self.meta, autoload=True)
        SPESA = Table('spesa', self.meta, autoload=True)
        FAT = Table('fattura', self.meta, autoload=True)
        FATDET = Table('fatdet', self.meta, autoload=True)
        FATIVA = Table('fativa', self.meta, autoload=True)
        FATSPESA = Table('fatspesa', self.meta, autoload=True)
        SCA = Table('scadenzario', self.meta, autoload=True)    
        TIPOANAG = Table('tipoanag', self.meta, autoload=True)
        BANCACC = Table('bancacc', self.meta, autoload=True) 
        OFF = Table('offerta', self.meta, autoload=True)
        OFFDET = Table('offdet', self.meta, autoload=True)   
        STAMPAFATTURA = Table('stampafattura', self.meta, autoload=True)
        STAMPAFATDET = Table('stampafatdet', self.meta, autoload=True)
        STAMPAFATIVA = Table('stampafativa', self.meta, autoload=True)
        STAMPAFATSPESA = Table('stampafatspesa', self.meta, autoload=True)
        STAMPAFATSCA = Table('stampafatsca', self.meta, autoload=True)
        STAMPAFATTURA.delete().execute()
        STAMPAFATDET.delete().execute()
        STAMPAFATIVA.delete().execute()
        STAMPAFATSPESA.delete().execute()
        STAMPAFATSCA.delete().execute()    
        noteinizio_fields = []
        notefine_fields = []
        for i in range(1, 11):    
            noteinizio_fields.append("noteinizio%s"%i)
            notefine_fields.append("notefine%s"%i)
        #TESTATA        
        s = select([ANA.c.anag,
                    ANA.c.recapito,
                    FAT.c.numero,
                    FAT.c.data, 
                    CAU.c.causale,
                    ANA.c.codicefiscale,
                    ANA.c.codiceministeriale,                           
                    TIPOANAG.c.idtipocodice,
                    ANA.c.partitaiva,
                    MODOPAG.c.id.label('idmodopag'),
                    MODOPAG.c.modopag,
                    ANA.c.descrizionebanca,
                    ANA.c.iban,
                    BANCACC.c.bancacc,
                    BANCACC.c.iban.label('ibancc'),
                    FAT.c.imponibile,
                    FAT.c.imposta,
                    FAT.c.totale,
                    FAT.c.notepiepagina,
                    FAT.c.imponibile.label('totaleimponibile'),
                    FAT.c.imposta.label('totaleimposta'),
                    FAT.c.totale.label('totalefattura')])
        s = s.select_from(FAT.outerjoin(ANA.outerjoin(TIPOANAG, ANA.c.idtipoanag==TIPOANAG.c.id), FAT.c.idanag==ANA.c.id)
                                            .outerjoin(CAU, FAT.c.idcausale==CAU.c.id)
                                            .outerjoin(MODOPAG, FAT.c.idmodopag==MODOPAG.c.id)
                                            .outerjoin(BANCACC, FAT.c.idbancacc==BANCACC.c.id))                                                              
        s = s.where(FAT.c.id==self.get_value('id'))
        row = s.execute().fetchone()
        d = dict(row)
        d['isfiscale'] = False
        d['isministeriale'] = False
        if row.idtipocodice=="FIS":
            d['isfiscale'] = True
        elif row.idtipocodice=="MIN":
            d['isministeriale'] = True
        elif row.idtipocodice=="ALL":
            d['isfiscale'] = True
            d['isministeriale'] = True
        d['data'] = F.datesql2print(d['data'])
        d['destinatario'] = F.sql2str(d['anag'])        
        d['documento'] = F.sql2str(d['causale'])   
        d['pagamento'] = F.sql2str(d['modopag'])  
        d['totaleimponibile'] = F.FormatFloat(d['totaleimponibile'])
        d['totaleimposta'] = F.FormatFloat(d['totaleimposta'])
        d['totalefattura'] = F.FormatFloat(d['totalefattura'])
        # Recupero la banca corretta da stampare (nostra/vostra)
        tipobanca = self.GetTipoBanca(row['idmodopag'])
        if tipobanca=="VS":
            d['banca'] = F.sql2str(d['descrizionebanca'])
            d['iban'] = F.sql2str(d['iban'])
        elif tipobanca=="NS":
            d['banca'] = F.sql2str(d['bancacc'])
            d['iban'] = F.sql2str(d['ibancc'])
        STAMPAFATTURA.insert().execute(d)  
        #POSITIVI    
        s = select([func.sum(FATDET.c.importo).label('sum_pos')])
        s = s.where(FATDET.c.importo>=0)
        s = s.where(FATDET.c.idfattura==self.get_value('id'))
        Row = s.execute().fetchone()
        if Row!=None:
            if Row.sum_pos==None:
                Row.sum_pos = 0
            POS = F.sql2float(Row.sum_pos)
            s = STAMPAFATTURA.update().execute({'sum_pos':F.FormatFloat(POS)})
        else:
            POS = 0          
        #NEGATIVI    
        s = select([func.sum(FATDET.c.importo).label('sum_neg')])
        s = s.where(FATDET.c.importo<0)
        s = s.where(FATDET.c.idfattura==self.get_value('id'))
        Row = s.execute().fetchone()
        if Row!=None:
            if Row.sum_neg==None:
                NEG = 0
            else:
                NEG = abs(F.sql2float(Row.sum_neg))
            s = STAMPAFATTURA.update().execute({'sum_neg':F.FormatFloat(NEG)})
        else:
            NEG = 0    
        #NETTO
        NETTO = POS-NEG
        s = STAMPAFATTURA.update().execute({'netto':F.FormatFloat(NETTO)})
        #INSERIMENTO POSIZION
        s = select([FATDET.c.id, FATDET.c.descri,
                            FATDET.c.noteinizio1, FATDET.c.noteinizio2, FATDET.c.noteinizio3, FATDET.c.noteinizio4, FATDET.c.noteinizio5, 
                            FATDET.c.noteinizio6, FATDET.c.noteinizio7, FATDET.c.noteinizio8, FATDET.c.noteinizio9, FATDET.c.noteinizio10, 
                            FATDET.c.notefine1, FATDET.c.notefine2, FATDET.c.notefine3, FATDET.c.notefine4, FATDET.c.notefine5, 
                            FATDET.c.notefine6, FATDET.c.notefine7, FATDET.c.notefine8, FATDET.c.notefine9, FATDET.c.notefine10, 
                            FATDET.c.quantita, FATDET.c.prezzo, FATDET.c.scontoperc, FATDET.c.importo,
                            FATDET.c.idofferta, FATDET.c.idoffdet, IVA.c.id.label('iva')])
        s = s.where(FATDET.c.idfattura==self.get_value('id'))
        s = s.select_from(FATDET.outerjoin(IVA, FATDET.c.idiva==IVA.c.id))        
        s = s.order_by(FATDET.c.id)            
        rs = s.execute()
        first = True
        for row in rs:
            # Divisorio fra posizioni
            if first:
                first = False
            else:
                d = dict()
                d['id'] = F.get_id_stampadet('stampafatdet')   
                d['descrizione'] = "-"*80
                STAMPAFATDET.insert().execute(d)
            # Riferimento offerta
            if row.idofferta!=None and row.idoffdet!=None:
                s = select([OFF.c.numero, OFF.c.data.label('data_offerta'), OFFDET.c.posizione])
                s = s.where(OFFDET.c.idofferta==row.idofferta)
                s = s.where(OFFDET.c.id==row.idoffdet)                
                s = s.where(OFFDET.c.idofferta==OFF.c.id)
                r = s.execute().fetchone()
                if r!=None:
                    d = dict()
                    d['id'] = F.get_id_stampadet('stampafatdet')   
                    d['descrizione'] = "Rif. ns. preventivo num. %s del %s pos. %s "%(r.numero,
                                                                                      F.datesql2print(r.data_offerta),
                                                                                      r.posizione)
                    STAMPAFATDET.insert().execute(d)                  

            # Note inizio posizione
            list_noteinizio = []
            cont = 0
            last_pos = None
            for key in noteinizio_fields:
                d = dict(descrizione=F.sql2str(row[key]))
                list_noteinizio.append(d)
                if d['descrizione']=='':        
                    if last_pos==None:
                        last_pos = cont
                else:
                    last_pos = None
                cont+=1       
            if last_pos==None:     
                for i in range(len(list_noteinizio)):
                    d = list_noteinizio[i]
                    d['id'] = F.get_id_stampadet('stampafatdet')   
                    STAMPAFATDET.insert().execute(d)
            else:                
                i = 0
                while i<last_pos:
                    d = list_noteinizio[i]
                    d['id'] = F.get_id_stampadet('stampafatdet')   
                    STAMPAFATDET.insert().execute(d)
                    i+=1
                    
                              
            # Posizione   
            d = dict()
            d['id'] = F.get_id_stampadet('stampafatdet') 
            d['posizione'] = F.sql2str(row['id'])  
            d['descrizione'] = row['descri']
            d['quantita'] = F.FormatFloat(row['quantita'])
            d['prezzo'] = F.FormatFloat(row['prezzo'])
            d['scontoperc'] = F.FormatFloat(row['scontoperc'])
            d['importo'] = F.FormatFloat(row['importo'])
            d['iva'] = F.sql2str(row['iva'])
            STAMPAFATDET.insert().execute(d)

            # Note fine posizione
            list_notefine = []
            cont = 0
            last_pos = None
            for key in notefine_fields:
                d = dict(descrizione=F.sql2str(row[key]))
                list_notefine.append(d)
                if d['descrizione']=='':        
                    if last_pos==None:
                        last_pos = cont
                else:
                    last_pos = None
                cont+=1   
                
            if last_pos==None:     
                for i in range(len(list_notefine)):
                    d = list_notefine[i]
                    d['id'] = F.get_id_stampadet('stampafatdet')   
                    STAMPAFATDET.insert().execute(d)
            else:                
                i = 0
                while i<last_pos:
                    d = list_notefine[i]
                    d['id'] = F.get_id_stampadet('stampafatdet')   
                    STAMPAFATDET.insert().execute(d)
                    i+=1
        #FATIVA
        S = STAMPAFATIVA.insert()
        s = select([FATIVA.c.imponibile,
                    FATIVA.c.imposta,
                    FATIVA.c.idiva.label('iva'),
                    IVA.c.iva.label('descrizioneiva')])
        s = s.select_from(FATIVA.outerjoin(IVA, FATIVA.c.idiva==IVA.c.id))  
        s = s.where(FATIVA.c.idfattura==self.get_value('id'))
        rs = s.execute()
        for row in rs:
            d = dict(row)
            d['imponibile'] = F.FormatFloat(d['imponibile'])
            d['imposta'] = F.FormatFloat(d['imposta'])
            for k,v in d.iteritems():
                d[k] = F.sql2str(v)
            d['id'] = F.get_id_stampadet('stampafativa')
            S.execute(d) 
        #FATSPESA
        S = STAMPAFATSPESA.insert()
        s = select([SPESA.c.spesa,
                    FATSPESA.c.imponibile,
                    ])
        s = s.select_from(FATSPESA.outerjoin(SPESA, FATSPESA.c.idspesa==SPESA.c.id))  
        s = s.where(FATSPESA.c.idfattura==self.get_value('id'))
        rs = s.execute()
        for row in rs:
            d = dict(row)
            d['imponibile'] = F.FormatFloat(d['imponibile'])
            for k,v in d.iteritems():
                d[k] = F.sql2str(v)
            d['id'] = F.get_id_stampadet('stampafatspesa')
            S.execute(d)  
        #FATSCA
        S = STAMPAFATSCA.insert()
        s = select([SCA.c.data,
                             SCA.c.importo])
        s = s.where(SCA.c.idfattura==self.get_value('id'))
        rs = s.execute()
        print "###############"
        for row in rs:
            print row
            d = dict(row)
            d['totale'] = F.FormatFloat(d['importo'])
            for k,v in d.iteritems():
                if k=='data':
                    v = F.datesql2print(v)
                d[k] = F.sql2str(v)
            d['id'] = F.get_id_stampadet('stampafatsca')
            S.execute(d) 
        ##################################################################
        report = win32com.client.Dispatch("ReportMan.ReportManX")
        report.Filename = "template\\template_fattura.rep"
        report.Preview = False
        report.ShowProgress = False
        report.ShowPrintDialog = False        
        file = os.path.dirname(tempfile.NamedTemporaryFile(delete=False).name)+'\\fattura_cazzaniga'
        F.elimina_file(file)
        file = file+'.pdf'
        report.SaveToPDF(file, True)        
        return file
        
        
    def GetTipoBanca(self, idmodopag):
        RATAPAG = Table('ratapag', self.meta, autoload=True)
        TIPOPAG =  Table('tipopag', self.meta, autoload=True)
        ns = 0
        vs = 0
        s = select([TIPOPAG.c.idtipobanca])
        s = s.select_from(RATAPAG.outerjoin(TIPOPAG, RATAPAG.c.idtipopag==TIPOPAG.c.id))
        s = s.where(RATAPAG.c.idmodopag==idmodopag)
        rs = s.execute()
        for row in rs:
            if row['idtipobanca']=="NS":
                ns+=1
            elif row['idtipobanca']=="VS":
                vs+=1                
        if vs>ns:
            return "VS"
        else:
            return "NS"
    
    
    def evasione(self, event):
        # Controllo        
        dict_labels = dict(data="data", idcausale="causale", idanag="Cliente", idmodopag="Modalita' di pagamento")        
        validate_fields = ["data", "idcausale", "idanag", "idmodopag"]
        for ctrl in validate_fields:
            if self.get_ctrl(ctrl).GetCurrValue() == None:
                wx.MessageDialog(None, _("Inserire %s")%dict_labels[ctrl],  g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()      
                return 
        # Apertura dialog posizioni  
        EvasioneDialog("xrc\\dialog_evasione_preventivi.xrc", **{"parent_frame":self.frame,
                                                                 'idanag':self.get_ctrl('idanag').GetCurrValue(),
                                                                 'idfattura':self.get_value('id'),
                                                                 'idcausale':self.get_value('idcausale'),
                                                                 'parent4actions' : self
                                                                 })

#Dialog evasione preventivi  
#######################################################################################################################################
class EvasioneDialog(lib.dialog.CustomDialog):
    def __init__(self, frame, **kwargs):  
        lib.dialog.CustomDialog.__init__(self, frame, **kwargs)
        self.idanag = kwargs.get('idanag', None)
        self.idcausale = kwargs.get('idcausale')
        self.idfattura = kwargs.get('idfattura')
        self.parent4actions = kwargs.get('parent4actions')
        self.init_controls()
        self.fill_list()
        self.init_frame()

    def init_controls(self):
        self.appendctrl('datainizio', empty=True)  
        self.appendctrl('datafine', empty=True)  
        self.appendcalendar('datainizio')
        self.appendcalendar('datafine')  
        # Eventi bottoni
        self.get_ctrl('btn_filtra').Bind(wx.EVT_BUTTON, self.fill_list)
        self.get_ctrl('btn_annulla').Bind(wx.EVT_BUTTON, self.annulla)
        self.get_ctrl('btn_conferma').Bind(wx.EVT_BUTTON, self.conferma)                 
    
    def fill_list(self, event=None):
        #TABELLE
        ANA = Table('anag', self.meta, autoload=True)
        OFF = Table('offerta', self.meta, autoload=True)
        OFFDET = Table('offdet', self.meta, autoload=True)
        CAU = Table('causale', self.meta, autoload=True)
        # Filtri
        datainizio = self.get_ctrl('datainizio').GetCurrValue()
        datafine = self.get_ctrl('datafine').GetCurrValue()
        #
        s = select([OFF.c.id, OFFDET.c.id.label('idoffdet'),                    
                            CAU.c.causale, OFF.c.data, OFF.c.numero, ANA.c.anag, OFFDET.c.descri, OFFDET.c.quantita, OFFDET.c.prezzo, OFFDET.c.destinazione])
        s = s.select_from(OFF.outerjoin(CAU, OFF.c.idcausale==CAU.c.id)
                             .outerjoin(ANA, OFF.c.idanag==ANA.c.id))        
        s = s.where(OFF.c.id==OFFDET.c.idofferta)
        s = s.where(OFFDET.c.ischiuso==None)
        s = s.where(CAU.c.idcausalefattura==self.idcausale)        
        if self.idanag!=None:
            s = s.where(OFF.c.idanag==self.idanag)
        if datainizio!=None:
            s = s.where(OFF.c.data>=datainizio)   
        if datainizio!=None:
            s = s.where(OFF.c.data<=datafine)     
        rs = s.execute()   
        # Riempimento lista     
        self.pk = []    
        list_ctrl = self.get_ctrl('list_preventivi')   
        columns = [_('Causale'), _('Data'), _('Numero'), _('Ragione sociale'), _('Descrizione'), _('Destinazione'), _('Quantita'), _('Prezzo')]
        i = 0
        # Intestazione colonne
        for column in columns:
            list_ctrl.InsertColumn(i, column)
            i+=1
        # Riempimento righe
        for row in rs: 
            index = list_ctrl.InsertStringItem(sys.maxint, F.sql2str(row['causale']))
            list_ctrl.SetStringItem(index, 1, F.convert_datetime(row['data']))
            list_ctrl.SetStringItem(index, 2, F.sql2str(row['numero']))
            list_ctrl.SetStringItem(index, 3, F.sql2str(row['anag']))
            list_ctrl.SetStringItem(index, 4, F.sql2str(row['descri']))
            list_ctrl.SetStringItem(index, 5, F.sql2str(row['destinazione']))
            list_ctrl.SetStringItem(index, 6, F.sql2str(row['quantita']))
            list_ctrl.SetStringItem(index, 7, F.sql2str(row['prezzo']))           
            self.pk.append(dict(idofferta=row['id'], idoffdet=row['idoffdet']))
        # Dimensionamento colonne 
        for i in range(list_ctrl.GetColumnCount()):      
            list_ctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            
    def annulla(self, event=None):
        self.frame.Destroy()
    
    def conferma(self, event=None):
        OFFDET = Table('offdet', self.meta, autoload=True)
        FATDET = Table('fatdet', self.meta, autoload=True)        
        list_ctrl = self.get_ctrl('list_preventivi')  
        list_selected = list_ctrl.GetChecked()
        self.dict_close_off = dict()
        for selected_element in list_selected:
            s = OFFDET.select() 
            s = s.where(OFFDET.c.idofferta==self.pk[selected_element]['idofferta'])
            s = s.where(OFFDET.c.id==self.pk[selected_element]['idoffdet'])
            row = s.execute().fetchone()
            d = dict(row)
            d['idoffdet'] = d['id']
            d['id'] = self.get_pk_fatdet()            
            d['idfattura'] = self.idfattura    
            totale = d['quantita']*d['prezzo'] 
            d['totale'] = totale
            d['importo'] = totale 
            if d['idiva']==None:
                d['idiva'] = F.get_iva(self.idanag)                         
            FATDET.insert().execute(d)
            if self.pk[selected_element]['idofferta'] in self.dict_close_off.keys():
                self.dict_close_off[self.pk[selected_element]['idofferta']].append(self.pk[selected_element]['idoffdet'])
            else:
                self.dict_close_off[self.pk[selected_element]['idofferta']] = [self.pk[selected_element]['idoffdet']]
        self.parent4actions.create_values()
        self.parent4actions.query_save(**{'close':False})  
        # Chiusura offerte
        for idofferta in self.dict_close_off.keys():
            for idoffdet in self.dict_close_off[idofferta]:
                s = OFFDET.update()
                s = s.where(OFFDET.c.idofferta==idofferta)
                s = s.where(OFFDET.c.id==idoffdet)
                s.execute({'ischiuso':True})
        self.frame.Destroy()
            
              
    def get_pk_fatdet(self):
        t = Table('fatdet', self.meta, autoload=True)
        s = select([func.max(t.c.id)])
        s = s.where(t.c.idfattura==self.idfattura)
        rs = s.execute()
        row = rs.fetchone()
        try:
            i = int(row[0])
        except:
            i = 0
        if i == 0:
            pk = '%0*d' % (3, 1)
        else:
            pk = '%0*d' % (3, i + 1)
        return pk               
            

#######################################################################################################################################
class CustomDialog(lib.dialog.CustomDialog):
    def __init__(self, frame, **kwargs):  
        lib.dialog.CustomDialog.__init__(self, frame, **kwargs)
        self.init_controls()
        self.init_frame()
    
    def init_controls(self):
        self.appendctrl('datainizio', empty=True)   
        self.appendctrl('datafine', empty=True)  
        self.appendctrl('idanag', empty=True, fillzero=6)  
        self.appendctrl('idtipoanag', empty=True)  
        self.appendctrl('idmodopag', empty=True)
        self.appendctrl('idcausale') 
        self.appendcalendar('datainizio')
        self.appendcalendar('datafine')    
        self.appendlkp(g.menu.CAUSALE_FATTURA, 'idcausale', **{'idtipocausale':'FAT'})        
        self.appendlkp(g.menu.MODOPAG,'idmodopag') 
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
            else:
                self.set_value(k, v)
     
    def conferma(self, event):
        self.check_causale()
        self.check_idanag()
        self.check_idtipoanag()
        self.check_idmodopag()
        self.check_data()
        self.page.get_data()
        self.frame.Destroy()

    def annulla(self, event):
        for ctrl in self.datacontrols:
            try:
                self.set_value(ctrl, '') 
            except:
                self.set_value(ctrl, False)
        self.conferma(None)   

    def check_causale(self):
        value = self.get_ctrl('idcausale').GetCurrValue()
        if value!=None:
            self.page.filtro['idcausale'] = value
        else:
            if 'idcausale' in self.page.filtro.keys():
                del self.page.filtro['idcausale']


    def check_idmodopag(self):
        value = self.get_ctrl('idmodopag').GetCurrValue()
        if value!=None:
            self.page.filtro['idmodopag'] = value
        else:
            if 'idmodopag' in self.page.filtro.keys():
                del self.page.filtro['idmodopag']

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
                