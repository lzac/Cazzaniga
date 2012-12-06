# -*- coding: utf-8 -*-

from moduli import * 
import lib_global as g
import lib_function as F
import win32com.client
import lib_file as File

class ListPanel(lib.panel.ListPanel):
    def __init__(self, *args, **kwargs):
        lib.panel.ListPanel.__init__(self, *args, **kwargs)
        self.showid = False
        self.get_data()

    def get_data(self):
        meta = MetaData()
        meta.bind = lib.g.engine
        t = Table('moduloassenza', meta, autoload=True)
        AUT = Table('autista', meta, autoload=True)           
        ASS = Table('tipoassenza', meta, autoload=True)                     
        s = select([t.c.id,  t.c.data, AUT.c.autista, ASS.c.tipoassenza])
        s = s.where(t.c.idautista==AUT.c.id)                
        s = s.where(t.c.idtipoassenza==ASS.c.id)                
        s = s.order_by(t.c.data)
        rs = s.execute()
        self.fill_data(rs, [_('Id'),  _('Data'), _('Autista'), _('Tipo assenza')])

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'moduloassenza', **kwargs)
        self.showid = False
        self.listcol = ('id',  'data', 'autista', 'idtipoassenza')
        self.pkseq = 6
        self.init_controls()
        self.move_record(move)
        #Ulteriori elementi della toolbar
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(g.menu.STAMPAMODULOASSENZA, _('Stampa'), wx.ArtProvider.GetBitmap(wx.ART_PRINT), shortHelp= _('Stampa')) 
        self.frame.Bind(wx.EVT_TOOL, self.stampa, id=g.menu.STAMPAMODULOASSENZA)    
        self.toolbar.Realize()           
            
    def init_controls(self):
        self.appendctrl('id')        
        self.appendctrl('data')        
        self.appendctrl('idautista')
        self.appendctrl('datainizio')
        self.appendctrl('datafine')
        self.appendctrl('orainizio')
        self.appendctrl('orafine')
        self.appendctrl('idtipoassenza')
        #Calendar e lookup
        self.appendcalendar('data')
        self.appendcalendar('datainizio')
        self.appendcalendar('datafine')                                
        self.appendlkp(g.menu.AUTISTA, 'idautista')
        self.appendlkp(g.menu.TIPOASSENZA, 'idtipoassenza') 
        
    def after_move_record(self, **d):
        today = datetime.date.today()
        today+=datetime.timedelta(days=1)
        if self.isappend:
            # Imposto data odierna
            if self.get_ctrl('data').GetCurrValue()==None:
                v = str(today)
                v = v[:4]+v[5:7]+v[8:]
                self.get_ctrl('data').SetStartValue(v)         
    
    
    def stampa(self, event): 
        MOD = Table('moduloassenza', self.meta, autoload=True)
        AUT = Table('autista', self.meta, autoload=True)                
        T = Table('stampamoduloassenza', self.meta, autoload=True)
        # Svuotamento tabella
        T.delete().execute()
        # Recupero campi
        s = select([MOD.c.data,
                            AUT.c.autista,
                            AUT.c.datanascita,
                            AUT.c.numeropatente,
                            AUT.c.datainiziocollaborazione,
                            MOD.c.datainizio,
                            MOD.c.orainizio,
                            MOD.c.datafine,
                            MOD.c.orafine,
                            MOD.c.idtipoassenza])
        s = s.where(MOD.c.id==self.get_value("id"))
        s = s.where(MOD.c.idautista==AUT.c.id)
        row = s.execute().fetchone()        
        insert_dict = dict(row)                
        for key in insert_dict.keys():
            if key in ["data", "datanascita", "datainizio", "datafine"]:
                insert_dict[key] = F.datesql2print(insert_dict[key])    
            else:            
                insert_dict[key] = F.sql2str(insert_dict[key])     
        T.insert().execute(insert_dict)  
        ##################################################################
        report = win32com.client.Dispatch("ReportMan.ReportManX")
        report.Filename = "template\\template_moduloassenza.rep"
        report.Preview = False
        report.ShowProgress = False
        report.ShowPrintDialog = False        
        file = os.path.dirname(tempfile.NamedTemporaryFile(delete=False).name)+'\\moduloassenza'
        F.elimina_file(file)
        file = file+'.pdf'
        report.SaveToPDF(file, True)        
        File.aprifile(file, True)  
        