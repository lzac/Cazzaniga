# -*- coding: utf-8 -*-

from sqlalchemy.orm import sessionmaker
from moduli import *
import myxrc
import lib_sql as lib_sql
import lib_global as g
import lib_sql as libsql
import lib_class as C

CHOICE = 1
LIST = 2
TEXT = 3

class EditFrame():
    def __init__(self, id, titolo, list, pk, filtro, tabella, **kwargs):
        self.BLOCCO = True
        self.list_ModCtrls = []
        self.asc = True
        self.INSERIMENTO = True
        self.PROTOCOLLOMOD = False
        self.OwnCheck = False
        self.listcol = ()
        self.tabdel = ()
        self.pkseq = 0
        self.default = {}
        
        self.doc_evasi = []
        self.filtro_evasi = {}
        
        for k, v in filtro.iteritems():
            self.default[k] = v
        self.filtro = filtro
        self.id = id
        self.list = list
        self.pk = pk
        self.saved = False
        self.isdoc = False
        self.isprotocolloiva = False
        self.det_buttons = []
        self.pkfrom = kwargs.get('pkfrom', {})
        self.idpk2 = kwargs.get('idpk2', None)
        self.pk2 = kwargs.get('pk2', None)
        self.showid = kwargs.get('showid', None)
        self.FrameParent = kwargs.get('parent_frame', None)
        self.pnota_fields = True

        self.meta = MetaData()
        self.meta.bind = g.engine
        self.tabella = tabella
        self.table = Table(tabella, self.meta, autoload=True)
        
        self.metastampa = MetaData()
        self.metastampa.bind = g.stampengine
        
        self.controls = {}
        self.datacontrols = {}
        self.lkpcontrols = {}
        self.detcontrols = {}
        self.detmethods = {}
        self.emptycontrols = {}

        if isinstance(list, wx.Choice):
            self.parent = CHOICE
            self.lookup = True
        elif isinstance(list, wx.ListCtrl):
            self.parent = LIST
            self.lookup = False
        elif isinstance(list, wx.TextCtrl):
            self.parent = TEXT
            self.lookup = True
        self.reccount = len(self.pk)
        if self.list!=None:
            self.recno = self.list.GetSelection()
        else:
            self.recno = None
        self.init_frame(titolo)

    def init_frame(self, titolo):
        self.res = xrc.XmlResource("xrc\\frm_%s.xrc" % (self.id))
        self.frame = self.res.LoadFrame(None, "frame")
        self.frame.Title = titolo
        #
        self.menubar = wx.MenuBar()
        menu0 = wx.Menu()
        menu0.Append(g.menu.FILE_NUOVO, _('Nuovo'))
        menu0.AppendSeparator()
        menu0.Append(g.menu.FILE_SELEZIONA, _('Seleziona'))
        menu0.AppendSeparator()
        menu0.Append(g.menu.FILE_SALVA_CHIUDI, _('Salva e chiudi'))
        menu0.Append(g.menu.FILE_SALVA, _('Salva'))
        menu0.AppendSeparator()
        menu0.Append(g.menu.FILE_CHIUDI, _('Chiudi'))
        #
        self. menubar.Append(menu0, _('File'))
        menu0 = wx.Menu()
        menu0.Append(g.menu.MODIFICA_ANNULLA, _('Annulla'))
        menu0.AppendSeparator()
        menu0.Append(g.menu.MODIFICA_ELIMINA_DEFINITIVA, _('Elimina'))
        self.menubar.Append(menu0, _('Modifica'))
        menu0 = wx.Menu()
        menu0.Append(g.menu.MODIFICA_PRECEDENTE, _('Precedente'))
        menu0.Append(g.menu.MODIFICA_SUCCESSIVO, _('Successivo'))
        menu0.AppendSeparator()
        menu0.Append(g.menu.MODIFICA_PRIMO, _('Primo'))
        menu0.Append(g.menu.MODIFICA_ULTIMO, _('Ultimo'))
        self.menubar.Append(menu0, _('Vai'))
        self.frame.SetMenuBar(self.menubar)

        self.toolbar = self.frame.CreateToolBar(style=wx.TB_FLAT | wx.TB_TEXT)
        self.toolbar.AddLabelTool(g.menu.FILE_NUOVO, _('Nuovo'), wx.ArtProvider.GetBitmap(wx.ART_NEW), shortHelp=_('Crea nuova scheda'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(g.menu.FILE_SALVA_CHIUDI, _('Salva/chiudi'), wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE), shortHelp=_('Salva e chiudi'))
        self.toolbar.AddLabelTool(g.menu.FILE_SALVA, _('Salva'), wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE), shortHelp=_('Salva'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(g.menu.MODIFICA_ANNULLA, _('Annulla'), wx.ArtProvider.GetBitmap(wx.ART_UNDO), shortHelp=_('Annulla modifiche'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, _('Elimina'), wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK), shortHelp=_('Elimina scheda'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(g.menu.MODIFICA_PRECEDENTE, _('Precedente'), wx.ArtProvider.GetBitmap(wx.ART_GO_UP), shortHelp=_('Scheda precedente'))
        self.toolbar.AddLabelTool(g.menu.MODIFICA_SUCCESSIVO, _('Successivo'), wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN), shortHelp=_('Scheda successiva'))
        self.toolbar.AddSeparator()
        self.toolbar.AddLabelTool(g.menu.FILE_REFRESH, _('Refresh'), wx.ArtProvider.GetBitmap(wx.ART_REDO), shortHelp=_('Aggiorna'))
        self.toolbar.AddSeparator()
        if self.lookup:
            self.toolbar.AddLabelTool(g.menu.FILE_SELEZIONA, _('Seleziona'), wx.ArtProvider.GetBitmap(wx.ART_EXECUTABLE_FILE), shortHelp=_('Seleziona scheda'))
        else:
            self.toolbar.AddLabelTool(g.menu.FILE_CHIUDI, _('Chiudi'), wx.ArtProvider.GetBitmap(wx.ART_QUIT), shortHelp=_('Chiudi scheda'))
        self.toolbar.Realize()
        #EVENTI
            #MENU
        self.frame.Bind(wx.EVT_MENU, self.menu_salva, id=g.menu.FILE_SALVA)
        self.frame.Bind(wx.EVT_MENU, self.menu_salva_chiudi, id=g.menu.FILE_SALVA_CHIUDI)
        self.frame.Bind(wx.EVT_MENU, self.menu_nuovo, id=g.menu.FILE_NUOVO)
        self.frame.Bind(wx.EVT_MENU, self.menu_refresh, id=g.menu.FILE_REFRESH)
        self.frame.Bind(wx.EVT_MENU, self.menu_chiudi, id=g.menu.FILE_CHIUDI)
        self.frame.Bind(wx.EVT_MENU, self.menu_annulla, id=g.menu.MODIFICA_ANNULLA)
        self.frame.Bind(wx.EVT_MENU, self.menu_elimina_definitiva, id=g.menu.MODIFICA_ELIMINA_DEFINITIVA)
        self.frame.Bind(wx.EVT_MENU, self.menu_copia, id=g.menu.MODIFICA_COPIA)
        self.frame.Bind(wx.EVT_MENU, self.menu_primo, id=g.menu.MODIFICA_PRIMO)
        self.frame.Bind(wx.EVT_MENU, self.menu_ultimo, id=g.menu.MODIFICA_ULTIMO)
        self.frame.Bind(wx.EVT_MENU, self.menu_seleziona, id=g.menu.FILE_SELEZIONA)
        self.frame.Bind(wx.EVT_MENU, self.menu_precedente, id=g.menu.MODIFICA_PRECEDENTE)
        self.frame.Bind(wx.EVT_MENU, self.menu_successivo, id=g.menu.MODIFICA_SUCCESSIVO)
            #TOOLBAR
        self.frame.Bind(wx.EVT_TOOL, self.menu_nuovo, id=g.menu.FILE_NUOVO)
        self.frame.Bind(wx.EVT_TOOL, self.menu_chiudi, id=g.menu.FILE_CHIUDI)    
        self.frame.Bind(wx.EVT_TOOL, self.menu_salva, id=g.menu.FILE_SALVA)
        self.frame.Bind(wx.EVT_TOOL, self.menu_salva_chiudi, id=g.menu.FILE_SALVA_CHIUDI)
        self.frame.Bind(wx.EVT_TOOL, self.menu_annulla, id=g.menu.MODIFICA_ANNULLA)
        self.frame.Bind(wx.EVT_MENU, self.menu_elimina_definitiva, id=g.menu.MODIFICA_ELIMINA_DEFINITIVA)
        self.frame.Bind(wx.EVT_TOOL, self.menu_copia, id=g.menu.MODIFICA_COPIA)
        self.frame.Bind(wx.EVT_TOOL, self.menu_primo, id=g.menu.MODIFICA_PRIMO)
        self.frame.Bind(wx.EVT_TOOL, self.menu_ultimo, id=g.menu.MODIFICA_ULTIMO)
        self.frame.Bind(wx.EVT_TOOL, self.menu_precedente, id=g.menu.MODIFICA_PRECEDENTE)
        self.frame.Bind(wx.EVT_TOOL, self.menu_successivo, id=g.menu.MODIFICA_SUCCESSIVO)
        self.frame.Bind(wx.EVT_TOOL, self.menu_seleziona, id=g.menu.FILE_SELEZIONA)
        self.frame.Bind(wx.EVT_CLOSE, self.on_close)
        self.frame.Bind(wx.EVT_TEXT_MAXLEN, self._MaxChar)
        

    def add_detail(self, nome, method, **kwargs):
        self.detmethods[nome] = method
        self.detcontrols[nome] = xrc.XRCCTRL(self.frame, nome)
    
    def _AfterLookupData(self, v, p2):
        self._CheckData(None)
        
    def _CheckData(self, event):
        if (self.isappend or self.iscopy) and not self.saved:
            data = self.get_ctrl('data').GetCurrValue()
            s = select([func.max(self.table.c.data).label('data')])
            row = s.execute().fetchone()
            if row!=None:
                if not data>=row.data:
                    wx.MessageDialog(None, _("Data inserita inferiore all'ultima inserita"), g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()                 
                    v = str(datetime.date.today())
                    v = v[:4]+v[5:7]+v[8:]
                    self.get_ctrl('data').SetStartValue(v) 
                    self.get_ctrl('data').SetFocus()
        try:
            f = getattr(self, 'after_check_data')
            if callable(f):
                f()
        except: pass   
        
    def _MaxChar(self, event):
        wx.MessageDialog(None, _('Numero massimo di caratteri raggiunto'), 'Attenzione', wx.CANCEL | wx.ICON_QUESTION).ShowModal()        
                    
    def move_record(self, move):
        if self.recno == wx.NOT_FOUND:
            if self.reccount > 0:
                move = g.RECORD_FIRST
            else:
                move = g.RECORD_APPEND

        self.isappend = False
        self.iscopy = False

        if move == g.RECORD_FIRST:
            self.recno = 0
            if self.pk[0] == '':
                self.recno = 1
        elif move == g.RECORD_PREV:
            self.recno -= 1
            if self.recno == 1 and self.pk[0] == '':
                self.recno = 1
        elif move == g.RECORD_NEXT:
            self.recno += 1
        elif move == g.RECORD_LAST:
            self.recno = self.reccount - 1
        elif move == g.RECORD_APPEND:
            self.recno = self.recno
            self.isappend = True
            self.saved=False
        elif move == g.RECORD_COPY:
            self.recno = self.recno
            self.iscopy = True
            self.saved=False
        elif move == g.RECORD_CURRENT:
            if self.recno == 0 and self.reccount > 1 and self.pk[0] == '':
                self.recno = 1
        self.move_record_parent()
        self.get_data()
        if move==g.RECORD_APPEND or move==g.RECORD_COPY:
            self.insert()
        self.set_layout()
        #Blocco causale
        if self.isdoc:
            if not self.isappend and not self.iscopy:
                flag = False
            else:
                flag = True
            self.get_ctrl('btn_idcausale').Enabled = flag
            self.get_ctrl('lkp_idcausale').Enabled = flag
            self.get_ctrl('idcausale').Enabled = flag   
        self.check_doc_evasi()  
        try:
            d = {'move':move}
            f = getattr(self, 'after_move_record')
            if callable(f):
                f(**d)
        except: pass
    
    def check_doc_evasi(self):  
        if not self.OwnCheck:
            if self.BLOCCO: 
                NotCtrls = ['da', 'a', 'vsrif', 'note', 'noteinterne', 'numdoc', 'datadoc', 'dataconsegna']
                count = 0
                for tabella in self.doc_evasi:
                    t = Table(tabella, self.meta, autoload=True)
                    s = select([func.count(t.c.id).label('numero')])
                    for k, v in self.filtro_evasi.iteritems():
                        s = s.where(t.c[k]==self.get_value(v))
                    row = s.execute().fetchone()
                    count += row.numero
                if count>0:
                    list_ctrl = self.controls.keys()
                    for ctrl in list_ctrl:
                        if ctrl not in NotCtrls:
                            self.get_ctrl(ctrl).Enabled=False
                            try:
                                self.get_ctrl('btn_'+ctrl).Enabled=False
                                self.get_ctrl('lkp_'+ctrl).Enabled=False
                            except: pass   
                    for ctrl in self.det_buttons:
                        self.get_ctrl(ctrl).Enabled=False
                    self.toolbar.EnableTool(g.menu.FILE_NUOVO, False)
                    self.toolbar.EnableTool(g.menu.MODIFICA_COPIA, False)    
                    self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, False)  
                    self.toolbar.EnableTool(g.menu.MODIFICA_COPIA, False)             
                    self.menubar.Enable(g.menu.FILE_NUOVO, False)
                    self.menubar.Enable(g.menu.MODIFICA_COPIA, False)    
                    self.menubar.Enable(g.menu.MODIFICA_ELIMINA_DEFINITIVA, False) 
        else:
            try:
                f = getattr(self, '_CheckDoc')
                if callable(f):
                    f()
            except: pass
        
    def get_data(self):
        if self.isappend:
            for v in self.datacontrols.itervalues():
                v.SetStartValue(None)
            self.set_startvalue('id', self.get_pk())
            for k, v in self.default.iteritems():
                if not isinstance(v, dict):
                    self.set_startvalue(k, v)
        else:
            if isinstance(self.pk, list):
                s = self.table.select(self.table.c.id == self.pk[self.recno])
                if not self.idpk2 == None:
                    s = s.where(self.table.c[self.idpk2] == self.pk2[self.recno])
                for k,v in self.filtro.iteritems():
                            if isinstance(v, dict):
                                if v['segno']=='>':
                                    s = s.where(self.table.c[k]>=v['value'])
                                elif v['segno']=='<':
                                    s = s.where(self.table.c[k]<=v['value'])
                                if v['segno']=='<>':
                                    s = s.where(self.table.c[k].between(v['value'][0], v['value'][1]))
                            elif isinstance(v, list):
                                s = s.where(self.table.c[k].in_(v))
                            elif isinstance(v, C.cFindstring):
                                s = s.where(self.table.c[k].like('%'+v.descri+'%')) 
                            else:
                                s = s.where(self.table.c[k]==v) 
            else:
                s = self.table.select(self.table.c.id == self.pk)
            rs = s.execute()
            row = rs.fetchone()
            try:
                for i in row.items():
                    if i[0] in self.datacontrols:
                        self.datacontrols[i[0]].SetStartValue(i[1])
                if self.iscopy:
                    if self.pkseq == 0:
                        self.set_startvalue('id', None)
                    else:
                        self.set_startvalue('id', self.get_pk())
            except AttributeError:
                pass

        for v in self.detmethods.itervalues():
            v()

        if self.isappend or self.iscopy:
            if self.pkseq == 0:
                self.datacontrols['id'].Enabled = True
            else:
                self.datacontrols['id'].Enabled = False
            if not self.idpk2 == None:
                self.datacontrols[self.idpk2].Enabled = True
            for k in self.pkfrom.iterkeys():
                self.datacontrols[k].Enabled = False
            self.datacontrols['id'].SetFocus()
        else:
            self.datacontrols['id'].Enabled = False
            if not self.idpk2 == None:
                self.datacontrols[self.idpk2].Enabled = False
            for k in self.pkfrom.iterkeys():
                self.datacontrols[k].Enabled = False
        
    def put_data(self, **kwargs):
        try:
            f = getattr(self, 'before_put_data')
            if callable(f):
                f()
        except: pass
        d = {}
        for k, v in self.datacontrols.iteritems():
            if k == 'id' or k == self.idpk2 or k in self.pkfrom:
                if self.isappend or self.iscopy:
                    d[k] = v.GetCurrValue()
            else:
                d[k] = v.GetCurrValue()
        if self.isdoc==True:
            if (self.isappend or self.iscopy) and (not self.saved):                
                numbers_dict = lib_sql.protocollo(self.get_value('idcausale'), self.get_ctrl('data').GetCurrValue(), self.tabella)                             
                d['protocollo'] = numbers_dict['protocollo']
                d['numero'] = numbers_dict['numero']
                self.set_value('protocollo', d['protocollo'])
                self.set_value('numero', d['numero'])
                #In prima nota per protocollo iva          
        if self.check_insert():
            r = self.table.insert()
        else:
            r = self.table.update()
            r = r.where(self.table.c.id == self.get_value('id'))
            for k, v in self.pkfrom.iteritems():
                r = r.where(self.table.c[k] == v)
            if not self.idpk2 == None:
                r = r.where(self.table.c[self.idpk2] == self.get_value(self.idpk2))
        try:
            r.execute(d)
            self.saved = True  
        except: pass   
        try:
            f = getattr(self, 'after_put_data')
            if callable(f):
                f()
        except Exception, e:
            print e
        
        if self.INSERIMENTO==True:
            if isinstance(self.pk, list):
                self.put_data_list(**kwargs)
        else:
            close = kwargs.get('close', False)
            if close==True:
                self.chiudi()
        return True
    
    def check_insert(self):
        r = select([self.table.c.id])
        r = r.where(self.table.c.id == self.get_value('id'))
        for k, v in self.pkfrom.iteritems():
            r = r.where(self.table.c[k] == v)
        if not self.idpk2 == None:
            r = r.where(self.table.c[self.idpk2] == self.get_value(self.idpk2))
        row = r.execute().fetchone()
        if row==None:
            return True
        else:
            return False
                  
    def get_pk(self):
        if self.pkseq == 0:
            return None
        s = select([func.max(self.table.c.id)])
        for k, v in self.pkfrom.iteritems():
            s = s.where(self.table.c[k] == v)
        rs = s.execute()
        row = rs.fetchone()
        try:
            i = int(row[0])
        except:
            i = 0
        if i == 0:
            pk = '%0*d' % (self.pkseq, 1)
        else:
            pk = '%0*d' % (self.pkseq, i + 1)
        return pk

    def put_data_list(self, **kwargs):
        close = kwargs.get('close', False)
        if self.isappend or self.iscopy:
            self.reccount += 1
            self.recno = self.reccount - 1     
  
        try: 
            self.list.parent.get_data()
            self.list.parent.after_fill()
        except:      
            data = []
            for i in self.listcol:
                data.append(xrc.XRCCTRL(self.frame, i).GetLookupValue())
            if self.isappend or self.iscopy:
                self.list.AppendNew(data)
                self.isappend = False
                self.iscopy = False
                try:
                    self.list.Select(self.list.GetItemCount()-1)
                except:
                    pass
            else:
                self.list.Update(self.recno, data)
                try:
                    self.list.Select(self.recno)    
                except: pass  
            for i in range(len(self.listcol)):
                try:
                    self.list.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
                except:
                    pass
            if self.showid == False:
                self.list.SetColumnWidth(0, 0) 
        if self.datacontrols['id'].GetValue() not in self.pk:
            self.pk.append(self.datacontrols['id'].GetValue()) 

        try:                             
            self.list.Select(self.recno)    
        except:
            pass     
        if self.showid == False:
            self.list.SetColumnWidth(0, 0)
        #self.destroy_tablelock()
        if close==True:
            self.chiudi()
        else:
            self.move_record(g.RECORD_CURRENT)
            
    def insert(self):
        if self.pkseq>0:
            d = {}
            for k, v in self.default.iteritems():
                if not isinstance(v, dict):
                    d[k] = v
            d['id'] = self.get_value('id')
            d['datainsert'] = datetime.datetime.now()
            s = self.table.insert()
            s.execute(d)
                    
    def move_record_parent(self):
        if self.recno >= 0:
            self.list.SetSelection(self.recno)

    def set_layout(self):
        prev = False
        next = False
        first = False
        last = False
        if self.reccount > 1:
            if self.recno <= 0:
                next = True
                last = True
            elif self.recno == (self.reccount - 1):
                prev = True
                first = True
            else:
                prev = True
                next = True
                first = True
                last = True

        if self.recno == 1 and self.pk[0] == '':
            prev = False
            first = False

        self.toolbar.EnableTool(g.menu.MODIFICA_PRECEDENTE, prev)
        self.toolbar.EnableTool(g.menu.MODIFICA_SUCCESSIVO, next)
        self.toolbar.EnableTool(g.menu.MODIFICA_ANNULLA, True)
        self.toolbar.EnableTool(g.menu.MODIFICA_ELIMINA_DEFINITIVA, True)
        self.toolbar.EnableTool(g.menu.FILE_SELEZIONA, True)

        self.menubar.GetMenu(2).FindItemById(g.menu.MODIFICA_PRIMO).Enable(first)
        self.menubar.GetMenu(2).FindItemById(g.menu.MODIFICA_ULTIMO).Enable(last)
        self.menubar.GetMenu(2).FindItemById(g.menu.MODIFICA_PRECEDENTE).Enable(prev)
        self.menubar.GetMenu(2).FindItemById(g.menu.MODIFICA_SUCCESSIVO).Enable(next)
        self.menubar.GetMenu(1).FindItemById(g.menu.MODIFICA_ANNULLA).Enable(True)
        self.menubar.GetMenu(1).FindItemById(g.menu.MODIFICA_ELIMINA_DEFINITIVA).Enable(True)
        self.menubar.GetMenu(0).FindItemById(g.menu.FILE_SELEZIONA).Enable(self.lookup)

        # Abilita / disabilita gli oggetti 
        for i in self.frame.GetChildren():
            i.Enabled = True
        try:
            f = getattr(self, 'after_set_layout')
            if callable(f):
                f()
        except: pass
        self.set_ctrls_moduli()
        
    def set_ctrls_moduli(self):
        for element in self.list_ModCtrls:
            for k, v in element.iteritems():
                if not g.modulo.abilitato(k):
                    for ctrl in v:
                        self.get_ctrl(ctrl).Hide()
        

    def save_data(self):
        try:
            f = getattr(self, 'before_save_data')
            if callable(f):
                d = f() 
            if d['flag']==False:
                wx.MessageDialog(None,_(d['msg']), lib.g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
                return False
        except: pass
        for k, v in self.datacontrols.iteritems():           
            if not str(v.GetCurrValue()) == str(v.GetStartValue()):
                return True   
        return False

    def menu_nuovo(self, event):
        if self.query_save():
            try:
                f = getattr(self, 'before_menu_nuovo')
                if callable(f):
                    f()
            except: pass
            self.move_record(g.RECORD_APPEND)
            try:
                f = getattr(self, 'after_menu_nuovo')
                if callable(f):
                    f()
            except: pass
    
    def menu_refresh(self, event=None):
        if (self.isappend or self.iscopy) and not self.saved:
            d = wx.MessageDialog(None, 'Salvare posizione? (Altrimenti tutte le modifiche andranno perse)', lib.g.appname ,wx.YES_NO | wx.CANCEL |wx.ICON_QUESTION)
            r = d.ShowModal()
            if r == wx.ID_YES:
                self.put_data() 
                self.move_record(g.RECORD_LAST)
            else:
                self.move_record(g.RECORD_CURRENT)
        else:
            self.move_record(g.RECORD_CURRENT)

    def menu_elimina_definitiva(self, event):
        self.delete_record()

    def menu_copia(self, event):
        if self.query_save():
            try:
                f = getattr(self, 'before_menu_copy')
                if callable(f):
                    f()
            except: pass
            self.move_record(g.RECORD_COPY)

    def menu_annulla(self, event):
        self.move_record(g.RECORD_CURRENT)

    def menu_primo(self, event):
        if self.query_save():
            try:
                f = getattr(self, 'before_menu_first')
                if callable(f):
                    f()
            except: pass
            self.move_record(g.RECORD_FIRST)

    def menu_ultimo(self, event):
        if self.query_save():
            try:
                f = getattr(self, 'before_menu_last')
                if callable(f):
                    f()
            except: pass
            self.move_record(g.RECORD_LAST)

    def menu_seleziona(self, event):
        if self.query_save():
            self.list.SetValue(self.pk[self.recno])
            try:
                if self.list.owner==xrc.XRCCTRL(self.frame, 'idcausale'):
                    f = getattr(self.list.owner, 'evt_change_causale')
                    if callable(f):
                        f(None)
            except: pass
        self.chiudi()

    def menu_precedente(self, event):
        if self.query_save():
            try:
                f = getattr(self, 'before_menu_prev')
                if callable(f):
                    f()
            except: pass
            self.move_record(g.RECORD_PREV)

    def menu_successivo(self, event):
        if self.query_save():
            try:
                f = getattr(self, 'before_menu_next')
                if callable(f):
                    f()
            except: pass
            self.move_record(g.RECORD_NEXT)

    def menu_chiudi(self, event):
        if self.save_data() == True:
            if self.query_close() == True:
                self.chiudi()
        else:
            self.delete_notsaved()
            self.chiudi()
    
    def chiudi(self):  
        self.frame.MakeModal(False) 
        if self.FrameParent!=None:
            self.FrameParent.frame.MakeModal(True)
        else:
            g.mainframe.MakeModal(True)
        self.frame.Destroy()
        
    def menu_salva(self, event):
        kwargs = {'close':False}
        self.query_save(**kwargs)

    def menu_salva_chiudi(self, event):
        kwargs = {'close':True}
        self.query_save(**kwargs)
        

    def on_close(self, event):
        try:
            #Per salvare altri elementi tipo ordinamenti listctrl
            f = getattr(self, 'save_others')
            if callable(f):
                f()
        except: pass
        if self.save_data() == True:
            if self.query_close() == True: 
                self.chiudi()
            self.delete_notsaved()
        else:
            self.delete_notsaved()
            self.chiudi()
        #self.destroy_tablelock()
    
    def delete_notsaved(self):
        if not self.saved and (self.isappend or self.iscopy):
            if self.pkseq!=0:
                s = self.table.delete()
                s = s.where(self.table.c.id==self.get_value('id'))
                for k, v in self.pkfrom.iteritems():
                    s = s.where(self.table.c[k] == v)
                s.execute()  
        
    def destroy_tablelock(self):
        t = Table('tablelock', self.meta, autoload=True)
        s = t.delete()
        s = s.where(t.c.tabella==str(self.table))
        s = s.where(t.c.idutente==g.utecod)
        s.execute()

    def query_save(self, **kwargs):
        if self.iscopy:
            self.put_data(**kwargs)
        if self.valid_data() == False:
            return False
        if self.save_data() == False:
            close = kwargs.get('close', False)
            if close:
                self.chiudi()
            return True
        try:
            f = getattr(self, 'valid_controls')
        except AttributeError:
            pass
        else:
            if f() == False:
                return False
        if self.put_data(**kwargs) == False:
            return False
        return True

    def query_close(self):
        d = wx.MessageDialog(None, _('Salvare le modifiche?'), 'Info', wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
        r = d.ShowModal()
        if r == wx.ID_YES:
            if self.valid_data() == True and self.put_data() == True:
                return True
        elif r == wx.ID_NO:
            try:
                f = getattr(self, 'after_dont_save')
                if callable(f):
                    f()
            except: pass
            if (self.isappend or self.iscopy) and not self.saved:
                try:
                    f = getattr(self, 'after_dont_save_notsaved')
                    if callable(f):
                        f()
                except: pass
            self.delete_children() 
            self.delete_notsaved()
            return True
        return False

    def delete_children(self):
            # eleimina i record di dettaglio se sono in insert e non confermo
            if (self.isappend or self.iscopy) and not self.saved and len(self.detcontrols) > 0:
                for v in self.detcontrols.values():
                    if v.GetItemCount() > 0:
                        libsql.elimina_record(self.table, self.tabdel, self.get_value('id'))
        
    def delete_record(self):
        if self.isappend or self.iscopy:
            self.move_record(g.RECORD_CURRENT)
        else:
            msg = _('Confermi eliminazione ?')
            d = wx.MessageDialog(None, msg, g.appname , wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
            r = d.ShowModal()
            if r == wx.ID_YES:
                try:
                    f = getattr(self, 'before_delete')
                    if callable(f):
                        f()
                except: pass
                #Elimina record
                r = self.table.delete()
                r = r.where(self.table.c.id == self.get_value('id'))
                for k, v in self.pkfrom.iteritems():
                    r = r.where(self.table.c[k] == v)
                if not self.idpk2 == None:
                    r = r.where(self.table.c[self.idpk2] == self.get_value(self.idpk2))
                r.execute()
                # elimina le tabelle collegate        
                if len(self.tabdel) > 0:
                    libsql.elimina_record(self.table, self.tabdel, self.pk[self.recno])
                # Metodo da eseguire dopo eliminazione del record
                try:
                    f = getattr(self, 'after_delete')
                    if callable(f):
                        f()
                except: pass
                self.list.DeleteItem(self.recno)
                self.pk.remove(self.pk[self.recno])
                self.frame.MakeModal(False)
                self.frame.Destroy()

    def elimina(self, d):
        return d

    def get_value(self, id):
        return self.controls[id].GetValue()

    def get_currvalue(self, id):
        return self.controls[id].GetCurrValue()

    def get_startvalue(self, id):
        return self.controls[id].GetStartValue()

    def set_value(self, id, v):
        return self.controls[id].SetValue(v)

    def set_startvalue(self, id, v):
        return self.controls[id].SetStartValue(v)

    def get_ctrl(self, nome):
        try:
            ctrl = self.controls[nome]
        except:
            ctrl = xrc.XRCCTRL(self.frame, nome)
        return ctrl

    def get_ctrlid(self, nome):
        return xrc.XRCID(nome)

    def appendctrl(self, nome, **kwargs):
        if 'ctrl' in kwargs:
            empty = True
        else:
            empty = kwargs.get('empty', False)
        ctrl = kwargs.get('ctrl', xrc.XRCCTRL(self.frame, nome))
        ctrl.owner = self
        data = kwargs.get('data', True)
        self.controls[nome] = ctrl
        if data:
            self.datacontrols[nome] = ctrl
            if empty == False:
                self.emptycontrols[nome] = ctrl
        if 'default' in kwargs:
            if not nome in self.default:
                self.default[nome] = kwargs.get('default')
        if 'fillzero' in kwargs:
            ctrl.fillzero = kwargs.get('fillzero')
        if 'evt_kill_focus' in kwargs:
            ctrl.evt_kill_focus = kwargs.get('evt_kill_focus')
        return ctrl

    def appendlkp(self, id, nome, **kwargs):
        ctrl = self.get_ctrl(nome)
        lkpcodice = kwargs.get('lkp_codice', False)
        self.lkpcontrols[nome] = ctrl
        ctrl.InitLookup(nome, self.get_ctrl(nome[2:]), lkpcodice)
        f = getattr(libsql, 'fill_' + nome)
        if callable(f):
            f(ctrl, **kwargs)
        if 'after_lookup' in kwargs:
            ctrl.after_lookup = kwargs.get('after_lookup')
        if not id == wx.ID_NONE:
            btn = xrc.XRCCTRL(self.frame, 'btn_' + nome)
            lkp = xrc.XRCCTRL(self.frame, 'lkp_' + nome)
            #btn
            btn.InitLookup(self, id, ctrl)
            #lkp
            lkp.InitLookup(self, id, ctrl)

    def appendcalendar(self, nome, **kwargs):
        ctrl = self.get_ctrl(nome)
        if 'after_lookup' in kwargs:
            ctrl.after_lookup = kwargs.get('after_lookup')
        btn = xrc.XRCCTRL(self.frame, 'btn_' + nome)
        btn.InitLookup(self, ctrl)
        
    def appendnumber(self, nome, **kwargs):
        ctrl = self.get_ctrl(nome)
        table = nome[2:]
        ctrl.InitLookup(table)

    def apri(self, id, ctrl):
        titolo = g.menu.label(id)
        m = g.mainframe.appmod.moduli['p%s' % (id)]
        d = {}
        if len(ctrl.pkfrom) > 0:
            d['pkfrom'] = ctrl.pkfrom
        d['parent_frame'] = self
        f = m.EditFrame(id, titolo, ctrl , ctrl.pk, g.RECORD_CURRENT, ctrl.filtro, **d)
        f.frame.MakeModal(True)
        f.frame.Show()

    def lookup(self, id, cnt):
        pass

    def valid_data(self):
        try:
            f = getattr(self, 'before_valid_data')
            if callable(f):
                f()
        except: pass
        for k, v in self.emptycontrols.iteritems():
            if isinstance(v, myxrc.FloatTextCtrl):
                value = float(v.GetCurrValue())
                if value==0:
                    wx.MessageDialog(None, _(u'Campo obbligatorio: ' + k), g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
                    v.SetFocus()
                    return False          
            if len(v.GetValue()) == 0:
                wx.MessageDialog(None, _(u'Campo obbligatorio: ' + k), g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
                v.SetFocus()
                return False
            if isinstance(v, myxrc.DateTextCtrl):
                value = v.GetCurrValue()
                if value==None:
                    wx.MessageDialog(None, _(u'Campo obbligatorio: ' + k), g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
                    v.SetFocus()
                    return False   
        for k, v in self.lkpcontrols.iteritems():
            if not len(v.GetValue()) == 0:
                if v.GetSelection() == wx.NOT_FOUND:
                    wx.MessageDialog(None, _(u'Valore inserito non valido. ' + k + '=' + v.GetValue()), g.appname, wx.OK | wx.ICON_INFORMATION).ShowModal()
                    v.SetFocus()
                    return False
        return True


#--------------------------------------------------------------------------------------------------------------------------------------
class VirtualCheckBox():
    def __init__(self):
        self._startvalue = g.START_VALUE
        self.Value = g.START_VALUE
        self.fillzero = 0

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = False
        self.Value = v

    def SetValue(self, v):
        self.Value = v
        return v

    def GetStartValue(self):
        return self._startvalue

    def GetValue(self):
        return self.Value

    def GetCurrValue(self):
        if self.Value == False:
            return None
        return self.Value

    def GetLookupValue(self):
        return ''

class VirtualTextCtrl():
    def __init__(self):
        self._startvalue = g.START_VALUE
        self.Value = g.START_VALUE
        self.fillzero = 0

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = u''
        self.Value = v

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        return self.Value

    def GetValue(self):
        return self.Value

    def SetValue(self, v):
        self.Value = v
        return v

    def GetLookupValue(self):
        return self.Value
    
class evento():
    def __init__(self, p1):
        self.Id = p1