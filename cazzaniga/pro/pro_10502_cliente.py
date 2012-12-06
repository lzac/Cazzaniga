# -*- coding: utf-8 -*-

from moduli import *
import pro_10501_anag_indirizzo as p10501
import lib_class as c
import lib_file as File
import lib_function as F
import lib_global as g
import password

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.showid = False
        self.get_data()
        
    def get_data(self):    
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('anag', meta, autoload=True) 
        IVA = Table('iva', meta, autoload=True)
        PAG = Table('modopag', meta, autoload=True)
        TIPOANAG = Table('tipoanag', meta, autoload=True)
        s = select([t.c.id,
                           t.c.anag, 
                           TIPOANAG.c.tipoanag,
                           t.c.partitaiva,
                           IVA.c.iva,
                           PAG.c.modopag])
        s = s.select_from(t.outerjoin(PAG,t.c.idmodopag==PAG.c.id).outerjoin(IVA, t.c.idiva==IVA.c.id).outerjoin(TIPOANAG, t.c.idtipoanag==TIPOANAG.c.id))       
        s = s.order_by(t.c.anag)    
        rs = s.execute() 
        self.fill_data(rs, [_('Id'), _('Ragione sociale'), _('Tipologia'),_('Partita iva'), _('Iva'), _('Modo pag.')])
        

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'anag', **kwargs)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)      
        self.listcol = ('id', 'anag', 'idtipoanag','partitaiva',  'idiva', 'idmodopag')
        self.pkseq = 6                  
        self.init_controls()
        self.move_record(move)
              
    def init_controls(self):       
        self.appendctrl('id')        
        self.appendctrl('anag')
        self.appendctrl('partitaiva', empty=True)
        self.appendctrl('codicefiscale', empty=True)
        self.appendctrl('codiceministeriale', empty=True)
        self.appendctrl('sitoweb', empty=True)
        self.appendctrl('descrizionebanca', empty=True)
        self.appendctrl('contoc', empty=True, fillzero=12)
        self.appendctrl('iban', empty=True)
        self.appendctrl('idtipoanag', empty=True)
        self.appendctrl('recapito')
        self.appendctrl('indirizzo', ctrl=lib.frame.VirtualTextCtrl())
        self.appendctrl('cap', ctrl=lib.frame.VirtualTextCtrl())
        self.appendctrl('localita', ctrl=lib.frame.VirtualTextCtrl())
        self.appendctrl('idprovincia', ctrl=lib.frame.VirtualTextCtrl())        
        self.appendctrl('idnazione', empty=True, default='IT')
        self.appendctrl('telefono', empty=True)
        self.appendctrl('cellulare', empty=True)
        self.appendctrl('fax', empty=True)
        self.appendctrl('email', empty=True)
        self.appendctrl('idmodopag', empty=True)   
        self.appendctrl('idpostpag', empty=True)
        self.appendctrl('idiva', empty=True)
        self.appendctrl('note', empty=True)
        #lookup
        self.appendlkp(lib.g.menu.NAZIONE, 'idnazione')
        self.appendlkp(lib.g.menu.MODOPAG, 'idmodopag', after_lookup='on_killfocus_modopag')                        
        self.appendlkp(lib.g.menu.POSTPAG, 'idpostpag')                       
        self.appendlkp(lib.g.menu.IVA, 'idiva') 
        self.appendlkp(lib.g.menu.TIPOANAGRAFICA, 'idtipoanag') 
        #Eventi
        self.frame.Bind(wx.EVT_BUTTON, self.btn_indirizzo,id=self.get_ctrlid('btn_indirizzo')) 
        self.frame.Bind(wx.EVT_BUTTON, self.btn_verifica_partitaiva, id=self.get_ctrlid('btn_verifica_partitaiva'))
        self.get_ctrl('recapito').Bind(wx.EVT_CHAR, self.OnCharRecapito)     
        
        
    def after_move_record(self, **d):
        if self.isappend:
            self.get_predefiniti()
            flag = self.getDisableDelete()
            self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)   
            self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, flag)           
        
        
    def get_predefiniti(self):
        IVA = Table('iva', self.meta, autoload=True)
        MODOPAG = Table('modopag', self.meta, autoload=True)
        # Iva
        s = IVA.select()
        s = s.where(IVA.c.ispredefinito==True)
        row = s.execute().fetchone()
        if row!=None:
            self.set_value('idiva', F.sql2str(row.id))
        # Modopag
        s = MODOPAG.select()
        s = s.where(MODOPAG.c.ispredefinito==True)
        row = s.execute().fetchone()
        if row!=None:
            self.set_value('idmodopag', F.sql2str(row.id))
            
    def getDisableDelete(self):
        FAT = Table('fattura', self.meta, autoload=True)
        SCA = Table('fattura', self.meta, autoload=True)
        s = select([FAT.c.id])
        s = s.where(FAT.c.idanag==self.get_value('id'))
        row = s.execute().fetchone()
        if row!=None:
            return True
        s = select([SCA.c.id])
        s = s.where(SCA.c.idanag==self.get_value('id'))
        row = s.execute().fetchone()
        if row!=None:
            return True
        return False
 
 
    def OnCharRecapito(self, event):
        ctrl =  self.get_ctrl('recapito')
        for i in range(7, ctrl.GetNumberOfLines()):
            ctrl.Remove(0, ctrl.GetLineLength(i)) 
        event.Skip() 
  
  
    def on_killfocus_modopag(self, p1, p2):
        self.change_modopag(None)
                        
    def btn_indirizzo(self,event):
        self.calcola_indirizzo(self.get_value('recapito'))        
        x = p10501.Modifica_indirizzo(self)
        x.frame.MakeModal(True)
        x.frame.Show()
         
         
    def calcola_indirizzo(self, recapito):
        i = 0
        for x in recapito.splitlines(): 
            if i == 0:
                self.set_value('indirizzo',x)
            elif i == 1:                
                self.set_value('cap', x[:5])
                self.set_value('idprovincia', x[-2:])                    
                self.set_value('localita', x[6:len(x)-3])
            i += 1


    def btn_verifica_partitaiva(self, event):
        wx.MessageDialog(None,Check_PIVA(self.get_value('partitaiva')), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
                       
      


def Check_PIVA(p1):
    pi = p1
    if (pi[0]==0):
        return "";
    if (len(pi)!=11):
        return "La lunghezza della partita IVA non e' corretta."
    for i in range(11):
        if(pi[i].isdigit()==False):
            return "La partita IVA contiene dei caratteri non ammessi, deve contenere solo cifre"
    s = 0
    for i in range(0,9,2):
        s += int(pi[i])  
    for i in range(1,10,2):
        c = 2*(int(pi[i]))
        if (c > 9 ):
            c = c - 9
        s += c
    r=s%10
    if r==0:
        c=0
    else:
        c=10-r
    if int(pi[-1:])==c:
        return "Partita iva corretta"
    else:
        return "Il codice di controllo della partita iva non e' corretto" 