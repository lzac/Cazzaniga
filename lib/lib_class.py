# -*- coding: utf-8 -*-

import wx.grid as gridlib
import mod_lib as m
import wx
import lib_global as g
#import mod_pro as pro
import lib_menu
import sys
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import MetaData
from sqlalchemy import exc
import time
import lib_function as F

class CustomDataTable(gridlib.PyGridTableBase):
    def __init__(self, cols, types, s):   
        NOT = ['idpadre', 'quantita', 'somma']
        self.IDLIST = []
        gridlib.PyGridTableBase.__init__(self)
        self.colLabels = cols            
        self.dataTypes = types
        self.rs = s.execute()     
        self.data=[]
        for row in self.rs:   
            if row.somma==None:
                somma = 0
            else:
                somma = row.somma
            somma = round(row.quantita-somma, 2)
            if somma>0:
                self.IDLIST.append({'idpadre':row.idpadre, 'id':row.iddet})             
                app = [0, somma]      
                for k in row.keys():
                    if k not in NOT:
                        if k[:4]=='data':
                            c = time.strptime(row[k],"%Y%m%d")
                            app.append(time.strftime("%d/%m/%Y", c))
                        elif k=='anag':
                            app.append(F.sql2str(row[k]))           
                        else:
                            app.append(F.sql2str(row[k]))   
                app.append(0)
                self.data.append(app)

    def GetNumberRows(self):
        return len(self.data) + 1

    def GetNumberCols(self):
        try:
            return len(self.data[0])
        except: pass

    def IsEmptyCell(self, row, col):
        try:
            return not self.data[row][col]
        except IndexError:
            return True

    def GetValue(self, row, col):
        try:
            return self.data[row][col]
        except IndexError:
            return ''

    def SetValue(self, row, col, value):
        try:
            self.data[row][col] = value
        except IndexError:
            pass

    def GetColLabelValue(self, col):
        return self.colLabels[col]

    def GetTypeName(self, row, col):
        return self.dataTypes[col]


class StaticLinkCtrl():
    def __init__(self, p1, p2, p3):
        self.panel = p1
        self.data = p2
        self.stringa = p3
        self.ctrl = wx.StaticText(self.panel, wx.ID_ANY, self.stringa, wx.DefaultPosition, wx.DefaultSize, 0)
        self.ctrl.Bind(wx.EVT_LEFT_DOWN, self.OnLink)
        self.ctrl.SetForegroundColour("BLACK")
        self.ctrl.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, "Arial")) # 74, 93, 92, False, "Arial"))
        cursor = wx.StockCursor(wx.CURSOR_HAND)
        self.ctrl.SetCursor(cursor)

    def OnLink(self, event):
        a = evento(self.get_data())
        if a.Id == g.menu.FILE_NUOVO:
            g.mainframe.menu_nuovo(None)
        elif a.Id == g.menu.FILE_APRI:
            g.mainframe.menu_apri(None)
        elif a.Id == g.menu.MODIFICA_ELIMINA:
            g.mainframe.menu_elimina(None)
        elif a.Id == g.menu.PDC:
            g.mainframe.menu_tree(a)
        else:
            g.mainframe.menu_lista(a)

    def get_data(self):
        return self.data


class FoldBarPanel(wx.Panel):
    def __init__(self, parent, list_fpitem, list_fpmenu, image,
                 id, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.NO_BORDER | wx.TAB_TRAVERSAL):
        wx.Panel.__init__(self, parent)
        self.list_fpitem = list_fpitem
        self.list_fpmenu = list_fpmenu
        self.image = image
        self.CreateControls()
        self.GetSizer().Fit(self)
        self.GetSizer().SetSizeHints(self)
        self.GetSizer().Layout()

    def CreateControls(self):
            # Sizer della finestra
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        subpanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.NO_BORDER | wx.TAB_TRAVERSAL)
        sizer.Add(subpanel, 1, wx.GROW | wx.ADJUST_MINSIZE, 5)
            # Flexible sizer
        subsizer = wx.FlexGridSizer(2, 2, 0, 0)
        subsizer.AddGrowableCol(1)
        subsizer.SetFlexibleDirection(wx.BOTH)
        subsizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        subpanel.SetSizer(subsizer)
        i = 0
            # Inserimento righe della flexgridsizer
        for k in self.list_fpitem:
            item = wx.StaticBitmap(subpanel, wx.ID_ANY, wx.Bitmap(self.image, wx.BITMAP_TYPE_ANY))
            subsizer.Add(item, 1, wx.GROW | wx.ALL, 5)
            a = StaticLinkCtrl(subpanel, self.list_fpmenu[i], self.list_fpitem[i])
            item = a.ctrl
            subsizer.Add(item, 1, wx.GROW | wx.ALL, 5)
            i = i + 1
        subpanel.SetBackgroundColour('WHITE')

class Panel_Table(wx.Panel):
    def __init__(self, parent, **kwargs):
        self.kwargs = kwargs
        #Recupero kwargs
        self.table = kwargs.get('table', None)
        self.meta = MetaData()
        self.meta.bind = g.engine
        self.list_data = []
        self.list_elements = []
        wx.Panel.__init__  (self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(500, 300), style=wx.TAB_TRAVERSAL)
        self.init_layout()
        self.set_record()
        self.fill_data()
        self.set_eventi()
        self.check.SetValue(True)
        self.select(None)

    def set_record(self):
        self.filtro = {}
        if self.table == 'pdc':
            self.ListCols = ['Id', 'Codice', 'Descrizione']
            self.ListElements = ['id', 'codice', 'pdc']
        elif self.table == 'anag':
            if self.kwargs.get('iscliente', None) == True:
                self.filtro['iscliente'] = True
            elif self.kwargs.get('isfornitore', None) == True:
                self.filtro['isfornitore'] = True
            elif self.kwargs.get('isvettore', None) == True:
                self.filtro['isvettore'] = True
            self.ListCols = ['Codice', 'Descrizione']
            self.ListElements = ['id', 'anag']
        elif self.table == 'causale':
            self.filtro['idtipodoc'] = self.kwargs.get('idtipodoc', None)
            self.filtro['idtipomov'] = self.kwargs.get('idtipomov', None)
            self.ListCols = ['Codice', 'Descrizione']
            self.ListElements = ['id', 'causale']
        elif self.table == 'azienda':
            self.ListCols = ['Id', 'Azienda', 'Sigla']
            self.ListElements = ['id', 'azienda', 'sigla']
        elif self.table == 'filiale':
            self.ListCols = ['Id', 'Filiale']
            self.ListElements = ['id', 'filiale']
        elif self.table == 'divisione':
            self.ListCols = ['Id', 'Divisione']
            self.ListElements = ['id', 'divisione']
        elif self.table == 'reparto':
            self.ListCols = ['Id', 'Reparto']
            self.ListElements = ['id', 'reparto']
        elif self.table == 'cdc':
            self.ListCols = ['Id', 'Cdc']
            self.ListElements = ['id', 'cdc']
        elif self.table == 'funzione':
            self.ListCols = ['Id', 'Funzione']
            self.ListElements = ['id', 'funzione']
        elif self.table == 'mansione':
            self.ListCols = ['Id', 'Mansione']
            self.ListElements = ['id', 'mansione']
        elif self.table == 'catmatri':
            self.ListCols = ['Id', 'Categoria']
            self.ListElements = ['id', 'catmatri']
        elif self.table == 'qualifica':
            self.ListCols = ['Id', 'Qualifica']
            self.ListElements = ['id', 'qualifica']
        elif self.table == 'livello':
            self.ListCols = ['Id', 'Livello']
            self.ListElements = ['id', 'livello']
        elif self.table == 'contrass':
            self.ListCols = ['Id', 'Contratto']
            self.ListElements = ['id', 'contrass']

    def fill_data(self):
        t = Table(self.table, self.meta, autoload=True)
        s = select([t.c['%s' % self.ListElements[i]] for i in range(len(self.ListElements))])
        for k, v in self.filtro.iteritems():
            s = s.where(t.c[k] == v)
        s = s.where(t.c.iseliminato == None)
        rs = s.execute()
        #Fill data
        self.list.ClearAll()
        for i in range(len(self.ListCols)):
            self.list.InsertColumn(i, self.ListCols[i])
        for i in rs:
            index = self.list.InsertStringItem(sys.maxint, str(i[0]))
            for j in range(len(i)):
                self.list.SetStringItem(index, j, str(i[j]))
        for i in range(len(self.ListCols)):
            self.list.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        self.create_list_data()

    def create_list_data(self):
        for i in range(self.list.GetItemCount()):
            a = []
            for j in range(self.list.GetColumnCount()):
                a.append(str(self.list.GetItem(i, j).GetText()))
            self.list_data.append(a)

    def init_layout(self):
        #Sizer principale
        SIZER = wx.BoxSizer(wx.VERTICAL)
        #Flex sizer contentente check e find
        flex_sizer = wx.FlexGridSizer(2, 2, 0, 0)
        flex_sizer.AddGrowableCol(1)
        flex_sizer.SetFlexibleDirection(wx.BOTH)
        flex_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)
        #Check box e casella di testo di ricerca
        self.check = wx.CheckBox(self, wx.ID_ANY, u"Seleziona tutti", wx.DefaultPosition, wx.DefaultSize, 0)
        flex_sizer.Add(self.check, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
        self.find = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        flex_sizer.Add(self.find, 0, wx.ALL | wx.EXPAND, 5)
        SIZER.Add(flex_sizer, 0, wx.EXPAND, 5)
        #Check list ctrl
        self.list = CheckListCtrl(self)
        SIZER.Add(self.list, 1, wx.ALL | wx.EXPAND, 0)
        #Settaggio layout
        self.SetSizer(SIZER)
        self.Layout()

    def set_eventi(self):
        self.list.OnCheckItem = self.OnCheckItem
        self.find.Bind(wx.EVT_TEXT, self.trova)
        self.check.Bind(wx.EVT_CHECKBOX, self.select)

    def OnCheckItem(self, index, flag):
        value = self.list.GetItem(index).GetText()
        if flag == False:
            if value in self.list_elements:
                self.list_elements.remove(value)
        else:
            self.list_elements.append(value)

    def trova(self, event):
        if self.find.GetValue() != '':
            delete = []
            for i in range(self.list.GetItemCount()):
                find = 0
                for j in range(self.list.GetColumnCount()):
                    app = str(self.list.GetItem(i, j).GetText()).lower()
                    if app.find(str(self.find.GetValue()).lower()) != -1:
                        find += 1
                if find == 0:
                    delete.append(i)
            delete.reverse()
            for i in range(len(delete)):
                self.list.DeleteItem(delete[i])
        else:
            self.list.DeleteAllItems()
            for i in range(len(self.list_data)):
                app = self.list_data[i]
                index = self.list.InsertStringItem(sys.maxint, str(app[0]))
                for j in xrange(len(app)):
                    self.list.SetStringItem(index, j, app[j])
            for i in range(self.list.GetItemCount()):
                self.list.CheckItem(i, True)

    def select(self, event):
        if self.check.GetValue() == True:
            for i in range(self.list.GetItemCount()):
                self.list.CheckItem(i)
        else:
            for i in range(self.list.GetItemCount()):
                self.list_elements = []
                self.list.CheckItem(i, False)


class CheckListCtrl(wx.ListCtrl, CheckListCtrlMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        CheckListCtrlMixin.__init__(self)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated)

    def OnItemActivated(self, evt):
        self.ToggleItem(evt.m_itemIndex)


class evento():
    def __init__(self, p1):
        self.Id = p1
                    
class cFindstring():
    def __init__(self, p1):
        self.descri = p1