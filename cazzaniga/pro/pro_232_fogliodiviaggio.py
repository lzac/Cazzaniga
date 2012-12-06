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
        t = Table('fogliodiviaggio', meta, autoload=True)
        s = select([t.c.id, t.c.numero, t.c.data, t.c.committente]).order_by(t.c.id)
        rs = s.execute()
        self.fill_data(rs, [_('Id'),  _('Numero'), _('Data'), _('Committente')])

class EditFrame(lib.frame.EditFrame):
    def __init__(self, id, titolo, list, pk, move, filtro, **kwargs):
        lib.frame.EditFrame.__init__(self, id, titolo, list, pk, filtro, 'fogliodiviaggio', **kwargs)
        self.showid = False
        self.listcol = ('id', 'numero', 'data', 'committente')
        self.pkseq = 6
        self.init_controls()
        self.move_record(move)
        #Ulteriori elementi della toolbar
        self.toolbar.AddSeparator() 
        self.toolbar.AddLabelTool(g.menu.STAMPAFOGLIODIVIAGGIO, _('Stampa'), wx.ArtProvider.GetBitmap(wx.ART_PRINT), shortHelp= _('Stampa')) 
        self.frame.Bind(wx.EVT_TOOL, self.stampa, id=g.menu.STAMPAFOGLIODIVIAGGIO)    
        self.toolbar.Realize()           
            
    def init_controls(self):
        self.appendctrl('id')
        self.appendctrl('numero')
        self.appendctrl('data')
        self.appendctrl('dataritorno', empty=True)
        self.appendctrl('idautista1', empty=True)
        self.appendctrl('autista1', empty=True)
        self.appendctrl('idautista2', empty=True)
        self.appendctrl('autista2', empty=True)
        self.appendctrl('idveicolo', empty=True)
        self.appendctrl('veicolo', empty=True)
        self.appendctrl('targa', empty=True)
        self.appendctrl('idcommittente', empty=True)
        self.appendctrl('committente', empty=True)
        self.appendctrl('oraeluogo', empty=True)
        self.appendctrl('destinazione', empty=True)
        #Calendar e lookup
        self.appendcalendar('data')
        self.appendcalendar('dataritorno')
        self.appendlkp(g.menu.CLIENTE, 'idcommittente')
        self.appendlkp(g.menu.AUTISTA, 'idautista1') 
        self.appendlkp(g.menu.AUTISTA, 'idautista2') 
        self.appendlkp(g.menu.VEICOLO, 'idveicolo')
        # Eventi
        self.get_ctrl('idveicolo').Bind(wx.EVT_TEXT, self.change_veicolo)
        
        
    def after_move_record(self, **d):
        today = datetime.date.today()
        today+=datetime.timedelta(days=1)
        if self.isappend:
            # Imposto data odierna
            if self.get_ctrl('data').GetCurrValue()==None:
                v = str(today)
                v = v[:4]+v[5:7]+v[8:]
                self.get_ctrl('data').SetStartValue(v)     
            # Imposto il numero
            datainizio = "%s0101"%today.year
            datafine = "%s1231"%today.year
            t = Table('fogliodiviaggio', self.meta, autoload=True)        
            s = select([t.c.id, t.c.numero])
            s = s.where(t.c.data>=datainizio)
            s = s.where(t.c.data<=datafine)
            rs = s.execute()
            max_num = 0
            for row in rs:
                if int(row.numero)>max_num:
                    max_num = int(row.numero)                    
            max_num = '%0*d' % (3, max_num+1)                     
            self.get_ctrl('numero').SetStartValue(max_num)     
    
    
    def change_veicolo(self, event):
        t = Table('veicolo', self.meta, autoload=True)
        s = select([t.c.targa])
        s = s.where(t.c.id==self.get_value('idveicolo'))      
        row = s.execute().fetchone()
        if row!=None:
            if row.targa!=None:
                self.set_value('targa', F.sql2str(row.targa))


    def stampa(self, event): 
        T = Table('stampafogliodiviaggio', self.meta, autoload=True)
        T.delete().execute()
        insert_dict = dict()
        for key in ['numero', 'data', 'dataritorno', 'autista1', 'autista2', 'veicolo', 'targa', 'committente', 'oraeluogo', 'destinazione']:
            insert_dict[key] = F.sql2str(self.get_value(key))
            
        if self.get_ctrl('dataritorno').GetCurrValue()==None:
            insert_dict['dataritorno'] = "NULL"

            
        T.insert().execute(insert_dict)  
        ##################################################################
        report = win32com.client.Dispatch("ReportMan.ReportManX")
        report.Filename = "template\\template_fogliodiviaggio.rep"
        report.Preview = False
        report.ShowProgress = False
        report.ShowPrintDialog = False        
        file = os.path.dirname(tempfile.NamedTemporaryFile(delete=False).name)+'\\fogliodiviaggio_%s'%self.get_value('numero')
        F.elimina_file(file)
        file = file+'.pdf'
        report.SaveToPDF(file, True)        
        File.aprifile(file, True)  

