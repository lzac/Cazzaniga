# -*- coding: utf-8 -*-

from moduli import *
import lib_global as g
import pro_10451_offdet as p10451
import lib_function as F
from datetime import date
import lib_file as File
import win32com.client
import lib_class as C
import subprocess


class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.showid = False
        self.get_data()
      
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('offerta', meta, autoload=True)    
        CAU = Table('causale', meta, autoload=True)    
        ANA = Table('anag', meta, autoload=True) 
        s = select([t.c.id, CAU.c.causale, t.c.data, t.c.numero,  ANA.c.anag])        
        s = s.select_from(t.outerjoin(CAU, t.c.idcausale==CAU.c.id)
                           .outerjoin(ANA, t.c.idanag==ANA.c.id))
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
        s = s.order_by(desc(t.c.data), desc(t.c.protocollo))               
        rs = s.execute() 
        self.fill_data(rs, [_('Id'), _('Causale'), _('Data'), _('Numero'), _('Ragione sociale')])
        

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'offerta', **kwargs)
        self.showid = False
        self.isdoc = True
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)       
        self.listcol = ('id', 'idcausale', 'data', 'numero', 'idanag')
        self.tabdel = ('offdet', 'idofferta')
        self.pkseq = 6                     
        self.init_controls()   
        #Ulteriori elementi della toolbar
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
        self.check_date()                  
              
    def init_controls(self):
        self.appendctrl('id')     
        self.appendctrl('idcausale')
        self.appendctrl('data', empty=True)               
        self.appendctrl('protocollo', empty=True)
        self.appendctrl('numero', empty=True)
        self.appendctrl('idanag', fillzero=6)
        self.appendctrl('recapito', empty=True)
        self.appendctrl('isrichiestatelefonica', empty=True)
        self.appendctrl('datarichiestatelefonica', empty=True)
        self.appendctrl('ismail', empty=True)
        self.appendctrl('datamail', empty=True)
        self.appendctrl('protocollomail', empty=True)
        self.appendctrl('isfax', empty=True)
        self.appendctrl('datafax', empty=True)    
        self.appendctrl('protocollofax', empty=True)
        self.appendctrl('hasdisponibilita', empty=True)
        self.appendctrl('hasmassimale', empty=True)
        self.appendctrl('noteinterne', empty=True)  
        #Lookup e calendar   
        self.appendlkp(g.menu.CAUSALE_OFFERTA, 'idcausale', **{'idtipocausale':'OFF'})
        self.appendlkp(g.menu.CLIENTE, 'idanag')  
        self.appendcalendar('data')
        self.appendcalendar('datarichiestatelefonica')
        self.appendcalendar('datamail')
        self.appendcalendar('datafax')                               
        #Detail
        self.add_detail('list_dettagli', getattr(self,'get_dettagli'))        
        self.f_descri = xrc.XRCCTRL(self.frame, 'txt_descri')                   
        #Eventi
        self.get_ctrl('idcausale').Bind(wx.EVT_CHOICE, self.evt_change_causale)
        self.frame.Bind(wx.EVT_LIST_ITEM_SELECTED, self.selected, id=self.get_ctrlid('list_dettagli'))
        self.frame.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.apri_dettaglio, id=self.get_ctrlid('list_dettagli'))       
        self.frame.Bind(wx.EVT_BUTTON, self.nuovo_dettaglio, id=self.get_ctrlid('btn_nuovodettaglio'))
        self.frame.Bind(wx.EVT_BUTTON, self.elimina_dettaglio, id=self.get_ctrlid('btn_eliminadettaglio'))
        self.frame.Bind(wx.EVT_BUTTON, self.apri_dettaglio, id=self.get_ctrlid('btn_apridettaglio'))
        
        
        
    def check_date(self):
        if self.get_ctrl('data').GetCurrValue()==None:
            v = str(datetime.date.today())
            v = v[:4]+v[5:7]+v[8:]
            self.get_ctrl('data').SetStartValue(v)     
            
            
    def after_move_record(self, **d):
        if self.isappend:
            list_not = ['idcausale', 'data']
            list_buttons = ['btn_data','btn_idanag', 'lkp_idanag', 'btn_nuovodettaglio', 'btn_apridettaglio', 'btn_eliminadettaglio',
                            'btn_datarichiestatelefonica', 'btn_datamail', 'btn_datafax']
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
            list_buttons = ['idcausale', 'data', 'btn_data', 'btn_idanag', 'lkp_idanag', 'btn_nuovodettaglio',
                            'btn_apridettaglio', 'btn_eliminadettaglio', 'list_dettagli', 'btn_datarichiestatelefonica', 'btn_datamail', 'btn_datafax']
            flag = self.get_isclosed()
            flag = not flag            
            list_ctrl = self.controls.keys()
            for ctrl in list_ctrl:
                self.get_ctrl(ctrl).Enabled=flag
            for ctrl in list_buttons:
                self.get_ctrl(ctrl).Enabled=flag   
                
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            if flag==True:
                self.set_posizioni()                 
                     
        self.get_ctrl('numero').Enabled=False   
        self.get_ctrl('protocollo').Enabled=False   
    
    
    def set_posizioni(self):
        t = Table('offdet', self.meta, autoload=True)
        i = 1
        s = select([t.c.id])
        s = s.where(t.c.idofferta==self.get_value('id'))
        s = s.order_by(t.c.id)
        rs = s.execute()
        for row in rs:
            s = t.update()
            s = s.where(t.c.id==row.id)
            s.execute({'posizione':str(i)})
            i += 1
            
        
        
    def getBlockCausaleCond(self):
        if self.get_ctrl('idcausale').GetCurrValue()==None:
            return False
        return True  
    
    
    def get_isclosed(self):
        OFF = Table('offerta', self.meta, autoload=True)
        OFFDET = Table('offdet', self.meta, autoload=True)
        """
        # Controllo che siano passati 60 giorni
        s = select([OFF.c.data])
        s = s.where(OFF.c.id==self.get_value('id'))
        row = s.execute().fetchone()        
        if row!=None:
            datafattura = date(int(row.data[:4]), int(row.data[-4:-2]), int(row.data[-2:]))
            dataodierna = date.today()
            delta = dataodierna - datafattura
            if delta.days>60:
                return True
        """
        # Controllo che tutte le posizioni siano bloccate
        tot_pos = 0
        tot_chiuse = 0
        s = select([OFFDET.c.ischiuso])
        s = s.where(OFFDET.c.idofferta==self.get_value("id"))
        rs = s.execute()
        for row in rs:
            if row.ischiuso==True:
                tot_chiuse += 1
            tot_pos += 1
        if tot_pos!=0:
            if tot_pos==tot_chiuse:
                return True
        return False                           
        
        
    def evt_change_causale(self, event):
        if self.get_ctrl('data').GetCurrValue()!=None:
            numbers_dict = lib.sql.protocollo(self.get_value('idcausale'), self.get_ctrl('data').GetCurrValue(), 'offerta')                             
            self.set_value('protocollo', numbers_dict['protocollo'])
            self.set_value('numero', numbers_dict['numero'])
            self.after_move_record(**{})
        else:
            dlg = wx.MessageDialog(None, _("Inserire data!"), _("Errore"), wx.OK)
            dlg.ShowModal()
            dlg.Destroy() 
                
                       
    def change_anag(self, event):          
        ANA = Table('anag', self.meta, autoload=True)
        s = select([ANA.c.recapito])
        s = s.where(ANA.c.id==self.get_value('idanag'))
        rs = s.execute()
        row = rs.fetchone()
        if row!=None:
            self.set_value('recapito', F.sql2str(row.recapito)) 
            
                              
    def selected(self, event):
        try:
            t = Table('offdet', self.meta, autoload=True)
            selected = self.get_ctrl('list_dettagli').GetFocusedItem()
            if selected==-1:
                selected=0
            selected_id = self.get_ctrl('list_dettagli').GetItem(selected, 0).GetText()
            s = t.select()
            s = s.where(t.c.idofferta==self.get_value('id'))
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
        DET = Table('offdet', self.meta, autoload=True)             
        cols = [_('Id'), _('Descrizione'), _('Quantita'), _(u'Prezzo')]        
        s = select([DET.c.id, 
                    DET.c.descri, 
                    DET.c.quantita,      
                    DET.c.prezzo])
        s = s.where(DET.c.idofferta==self.get_value('id'))
        s = s.order_by(DET.c.id)
        rs = s.execute()       
        ctrl.FillData(rs, cols) 


    def nuovo_dettaglio(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')
        kwargs = {'pkfrom': {'idofferta': self.get_value('id')}, 'parent_frame':self}                
        f = p10451.EditFrame(g.menu.OFFDET, _('Posizioni preventivo'), ctrl, ctrl.pk, lib.g.RECORD_APPEND, {'idofferta': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()  


    def apri_dettaglio(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')
        kwargs = {'pkfrom': {'idofferta': self.get_value('id')}, 'parent_frame':self}                
        f = p10451.EditFrame(g.menu.OFFDET, _('Posizioni preventivo'), ctrl, ctrl.pk, lib.g.RECORD_CURRENT, {'idofferta': self.get_value('id')}, **kwargs)
        f.frame.MakeModal(True)
        f.frame.Show()
        
        
    def elimina_dettaglio(self, event):
        ctrl = xrc.XRCCTRL(self.frame, 'list_dettagli')   
        recno = ctrl.GetFocusedItem()
        F.elimina_posizione(ctrl, 'posizione', 'offdet', {'idofferta':self.get_value('id'), 'id':ctrl.pk[recno]})
        self.set_posizioni()
        
    def anteprima(self, event):
        if not self.isappend:
            file = self.stampa()
            File.aprifile(self.stampa(), True)  
        else:
            wx.MessageDialog(None, _("Impossibile stampare preventivo, salvarla prima!"),  g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
    
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
            o = win32com.client.Dispatch("Outlook.Application")                          
            Msg = o.CreateItem(0)
            Msg.To = EMAIL   
            Msg.Subject = F.sql2str(self.get_ctrl('idcausale').GetStringSelection())+"  "+F.sql2str(self.get_value('numero')) 
            Msg.Attachments.Add(file)
            Msg.Display() 

        else:
            wx.MessageDialog(None, _("Impossibile stampare fattura, salvarla prima!"),  g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()  
            
            
    def stampa(self): 
        ANA = Table('anag', self.meta, autoload=True)
        OFF = Table('offerta', self.meta, autoload=True)
        CAU = Table('causale', self.meta, autoload=True)
        IVA = Table('iva', self.meta, autoload=True)
        OFFDET = Table('offdet', self.meta, autoload=True)           
        STAMPAOFF = Table('stampaofferta', self.meta, autoload=True)
        STAMPAOFFDET = Table('stampaoffdet', self.meta, autoload=True)
        STAMPAOFF.delete().execute()
        STAMPAOFFDET.delete().execute()   
        self.set_posizioni()
        noteinizio_fields = []
        notefine_fields = []
        for i in range(1, 11):    
            noteinizio_fields.append("noteinizio%s"%i)
            notefine_fields.append("notefine%s"%i)
        #TESTATA        
        s = select([ANA.c.anag,
                    ANA.c.recapito,
                    OFF.c.data,
                    CAU.c.causale,
                    OFF.c.numero,
                    OFF.c.isrichiestatelefonica,
                    OFF.c.datarichiestatelefonica,
                    OFF.c.ismail,
                    OFF.c.datamail,
                    OFF.c.protocollomail,
                    OFF.c.isfax,
                    OFF.c.datafax,
                    OFF.c.protocollofax,
                    OFF.c.hasdisponibilita,
                    OFF.c.hasmassimale])
        s = s.select_from(OFF.outerjoin(ANA, OFF.c.idanag==ANA.c.id)
                             .outerjoin(CAU, OFF.c.idcausale==CAU.c.id))                                                          
        s = s.where(OFF.c.id==self.get_value('id'))
        row = s.execute().fetchone()
        d = dict(row)
        d['data'] = F.datesql2print(d['data'])
        d['destinatario'] = F.sql2str(d['anag'])                
        d['oggetto'] = "%s %s"%(row.causale, row.numero)
        if row.hasdisponibilita==True:
            d['isdisponibilita'] = True
        if row.hasmassimale==True:
            d['ismassimale'] = True         
        if row.isrichiestatelefonica!=None or row.ismail!=None or row.isfax!=None:
            has_done_first = False
            d['intestazione'] = "Con riferimento a Vs. cortese "
            # Richiesta telefonica
            if row.isrichiestatelefonica!=None:
                d['intestazione'] += " richiesta telefonica "
                if row.datarichiestatelefonica!=None and row.datarichiestatelefonica.strip()!="":
                    d['intestazione'] += " del %s"%F.datesql2print(row.datarichiestatelefonica)
                has_done_first = True
            # Mail
            if row.ismail!=None:
                if has_done_first:
                    d['intestazione'] += ", "
                d['intestazione'] += " mail "
                if row.protocollomail!=None:
                    d['intestazione'] += " Prot. n.%s"%row.protocollomail                                
                if row.datamail!=None and row.datamail.strip()!="":
                    d['intestazione'] += " del %s"%F.datesql2print(row.datamail)
                has_done_first = True
            # Fax
            if row.isfax!=None:
                if has_done_first:
                    d['intestazione'] += ", "                
                d['intestazione'] += " fax "
                if row.protocollofax!=None:
                    d['intestazione'] += " Prot. n.%s"%row.protocollofax                 
                if row.datafax!=None and row.datafax.strip()!="":
                    d['intestazione'] += " del %s"%F.datesql2print(row.datafax)
                    
            if self.get_hasmore():
                d['intestazione'] += ", con la presente Vi sottoponiamo nostro miglior preventivo relativo ai seguenti servizi."                 
            else:
                d['intestazione'] += ", con la presente Vi sottoponiamo nostro miglior preventivo relativo al seguente servizio."
        else:
            if self.get_hasmore():
                d['intestazione'] = "Con riferimento a Vs. cortese richiesta, con la presente Vi sottoponiamo nostro miglior preventivo relativo ai seguenti servizi."                 
            else:
                d['intestazione'] = "Con riferimento a Vs. cortese richiesta, con la presente Vi sottoponiamo nostro miglior preventivo relativo al seguente servizio."                        
            
            
        STAMPAOFF.insert().execute(d)                                               
        #INSERIMENTO POSIZION
        s = select([OFFDET.c.posizione, OFFDET.c.isivato, OFFDET.c.descri, OFFDET.c.noteinizio1, OFFDET.c.noteinizio2, OFFDET.c.noteinizio3,
                    OFFDET.c.noteinizio4, OFFDET.c.noteinizio5, OFFDET.c.noteinizio6, OFFDET.c.noteinizio7, OFFDET.c.noteinizio8, OFFDET.c.noteinizio9,
                    OFFDET.c.noteinizio10, OFFDET.c.notefine1, OFFDET.c.notefine2, OFFDET.c.notefine3, OFFDET.c.notefine4, OFFDET.c.notefine5,
                    OFFDET.c.notefine6, OFFDET.c.notefine7, OFFDET.c.notefine8, OFFDET.c.notefine9, OFFDET.c.notefine10, OFFDET.c.quantita,
                    OFFDET.c.prezzo, IVA.c.iva, IVA.c.id.label('idiva'),   IVA.c.aliquota])            
        s = s.where(OFFDET.c.idofferta==self.get_value('id'))         
        s = s.select_from(OFFDET.outerjoin(IVA, OFFDET.c.idiva==IVA.c.id))        
        rs = s.execute()
        first = True
        for row in rs:
            # Divisorio fra posizioni
            if first:
                first = False
            else:
                d = dict()
                d['id'] = F.get_id_stampadet('stampaoffdet')   
                d['corpo'] = "-"*100
                STAMPAOFFDET.insert().execute(d)
            
            #Intestazione posizione
            #d = dict()
            #d['id'] = F.get_id_stampadet('stampaoffdet')   
            #d['corpo'] = "Posizione %s"%row['posizione']            
            #STAMPAOFFDET.insert().execute(d)            

            
            is_pos_inserted = False
            # Note inizio posizione
            list_noteinizio = []
            cont = 0
            last_pos = None
            for key in noteinizio_fields:
                d = dict(corpo=F.sql2str(row[key]))
                list_noteinizio.append(d)
                if d['corpo']=='':        
                    if last_pos==None:
                        last_pos = cont
                else:
                    last_pos = None
                cont+=1                
            if last_pos==None:     
                for i in range(len(list_noteinizio)):
                    d = list_noteinizio[i]
                    d['id'] = F.get_id_stampadet('stampaoffdet')
                    if not is_pos_inserted:
                        d['intestazione'] = "Pos.  %s"%row['posizione']     
                        is_pos_inserted = True
                    STAMPAOFFDET.insert().execute(d)
            else:                
                i = 0
                while i<last_pos:
                    d = list_noteinizio[i]
                    d['id'] = F.get_id_stampadet('stampaoffdet')   
                    if not is_pos_inserted:
                        d['intestazione'] = "Pos.  %s"%row['posizione']     
                        is_pos_inserted = True
                    STAMPAOFFDET.insert().execute(d)
                    i+=1           
                    
            # Posizione   
            d = dict()
            d['id'] = F.get_id_stampadet('stampaoffdet') 
            d['corpo'] = row['descri']  
            d['islineaprezzo'] = True
            if row['isivato']==True:
                val_iva = self.get_ivato(row['quantita']*row['prezzo'], row['idiva'])
                d['prezzo'] = " Eur. %s Iva inclusa %s"%(F.FormatFloat(val_iva), row['iva'])
            else:

                if row.aliquota==0 or row.aliquota==None:
                    d['prezzo'] = " Eur. %s - %s"%(F.FormatFloat(row['quantita']*row['prezzo']), row['iva'])
                else:
                    d['prezzo'] = " Eur. %s + %s"%(F.FormatFloat(row['quantita']*row['prezzo']), row['iva'])
            if not is_pos_inserted:
                d['intestazione'] = "Pos. %s"%row['posizione']     
                is_pos_inserted = True
            STAMPAOFFDET.insert().execute(d)

            # Note fine posizione
            list_notefine = []
            cont = 0
            last_pos = None
            for key in notefine_fields:
                d = dict(corpo=F.sql2str(row[key]))
                list_notefine.append(d)
                if d['corpo']=='':        
                    if last_pos==None:
                        last_pos = cont
                else:
                    last_pos = None
                cont+=1                
            if last_pos==None:     
                for i in range(len(list_notefine)):
                    d = list_notefine[i]
                    d['id'] = F.get_id_stampadet('stampaoffdet')   
                    STAMPAOFFDET.insert().execute(d)
            else:                
                i = 0
                while i<last_pos:
                    d = list_notefine[i]
                    d['id'] = F.get_id_stampadet('stampaoffdet')   
                    STAMPAOFFDET.insert().execute(d)
                    i+=1
        ##################################################################
        report = win32com.client.Dispatch("ReportMan.ReportManX")
        report.Filename = "template\\template_preventivo.rep"
        report.Preview = False
        report.ShowProgress = False
        report.ShowPrintDialog = False        
        file = os.path.dirname(tempfile.NamedTemporaryFile(delete=False).name)+'\\preventivo_cazzaniga'
        F.elimina_file(file)
        file = file+'.pdf'
        report.SaveToPDF(file, True)        
        return file       
    
    
    def get_ivato(self, importo, idiva):   
        IVA = Table('iva', self.meta, autoload=True)  
        s = select([IVA.c.aliquota])
        s = s.where(IVA.c.id==idiva)
        row = s.execute().fetchone()
        iva_val = (importo/100)*row.aliquota
        return importo+iva_val
    
    def get_hasmore(self):
        t = Table('offdet', self.meta, autoload=True)
        cont = 0  
        s = select([t.c.id])
        s = s.where(t.c.idofferta==self.get_value('id'))
        rs = s.execute()
        for row in rs:
            cont+=1
        if cont<=1:
            return False
        return True
    
    
    
    
    
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
        self.appendctrl('idcausale') 
        self.appendcalendar('datainizio')
        self.appendcalendar('datafine')    
        self.appendlkp(g.menu.CAUSALE_OFFERTA, 'idcausale', **{'idtipocausale':'OFF'})
        self.appendlkp(g.menu.CLIENTE, 'idanag') 
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

    def check_idanag(self):
        value = self.get_ctrl('idanag').GetCurrValue()
        if value!=None:
            self.page.filtro['idanag'] = value
        else:
            if 'idanag' in self.page.filtro.keys():
                del self.page.filtro['idanag']
                
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
