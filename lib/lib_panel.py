# -*- coding: utf-8 -*-

import wx
import os
from sqlalchemy import *
import sys
from lib_function import *
import time
import lib_class as c
import images
import lib_sql as libsql
import myxrc
#-----------------------------------------------------------------------------------------------------------------------------     
class TestListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.CheckListCtrlMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, **kwargs):
        self.parent = parent
        self.list_checked = []
        self.IsCheck = kwargs.get('IsCheck', False)    
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)   
        if self.IsCheck==True:
            d = {}
            listmix.CheckListCtrlMixin.__init__(self, **d)             
                        
    def OnCheckItem(self, index, flag):
        value = self.GetItem(index, 0).GetText()
        if flag==False:
            if value in self.list_checked:
                self.list_checked.remove(value)
        if flag==True:
            if value not in self.list_checked:
                self.list_checked.append(value)
  
    def GetSelection(self):
        return self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

    def AppendNew(self, data):
        x = self.InsertStringItem(sys.maxint, data[0])
        for i in range(1, len(data)):
            self.SetStringItem(x, i, data[i])
    
    def Update(self, recno, data):        
        for i in range(1, len(data)):
            self.SetStringItem(recno, i, data[i])

    def SetSelection(self, recno):
        self.Select(recno)        
        self.EnsureVisible(recno)
#-----------------------------------------------------------------------------------------------------------------------------     
class ListPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args)
        self.RightCols = []
        self.id = args[1]
        self.data = kwargs.get('data')
        self.filtro = kwargs.get('filtro', {})
        self.idpk2 = kwargs.get('idpk2', None)   
        self.parent = kwargs.get('parent', {})  
        self.ShowAzioni = kwargs.get('ShowAzioni', True)     
        self.CheckPanel = kwargs.get('CheckPanel', False)
        self.init_panel()      
        self.pk = []
        self.pk2 = []
        self.datalist = {}
        self.ListColumn = []
        self.COLUMNSORTER = False
        self.showid = True
        self.text_list = []
        self.init_menu()
        self.init_riepilogo()
        
    def init_riepilogo(self):
        if os.path.exists("xrc\\rpl_%s" % (self.id)+'.xrc'):   
            res = xrc.XmlResource("xrc\\rpl_%s" % (self.id)+'.xrc')
            self.riepilogo = res.LoadPanel(g.mainframe, "panel")
        else:   
            self.riepilogo = PanelRiepilogo(g.mainframe)        
                      
    def init_panel(self):
        #Inizializzazione lista elementi
        #wx.LC_HRULES|wx.LC_VRULES
        kwargs = {}
        kwargs['IsCheck'] = self.CheckPanel
        self.list = TestListCtrl(self, wx.ID_ANY, style=wx.LC_REPORT|wx.LC_SINGLE_SEL, **kwargs)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.Parent.menu_apri)
        self.list.ClearAll()
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list, 1, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.EXPAND,0 )
        self.SetSizerAndFit(sizer)
        self.OnSortOrderChanged = self.pk_refresh
        
    def init_menu(self):
        #import app_lista       
        self.menu = wx.Menu()
        self.menu.Append(g.menu.FILE_NUOVO, _("Nuovo"))
        self.menu.Append(g.menu.FILE_APRI, _("Apri"))
        self.menu.AppendSeparator()
        self.menu.Append(g.menu.MODIFICA_ELIMINA, _("Elimina"))
        self.menu.AppendSeparator()
        self.Bind(wx.EVT_MENU, self.Parent.menu_nuovo, id=g.menu.FILE_NUOVO)
        self.Bind(wx.EVT_MENU, self.Parent.menu_apri, id=g.menu.FILE_APRI)
        self.Bind(wx.EVT_MENU, self.Parent.menu_elimina, id=g.menu.MODIFICA_ELIMINA)
        try:
            f = getattr(self, 'after_init_menu')
            if callable(f):
                f()
        except: pass
    
    def SetColumnSorter(self, cols):
        if not self.COLUMNSORTER:
            listmix.ColumnSorterMixin.__init__(self, len(cols))
            self.COLUMNSORTER = True
    
    def fill_data(self, rs, cols, **kwargs):  
        lastfloat=False 
        self.datalist = {}
        self.ListColumn = []
        self.list.ClearAll()            
        self.pk = []
        self.pk2 = []
        self.list.Freeze()      
        for i in range(len(cols)):
            if not i in self.RightCols:
                self.list.InsertColumn(i, cols[i])
            else:
                self.list.InsertColumn(i, cols[i], wx.LIST_FORMAT_RIGHT)
                if i==len(cols)-1:
                    lastfloat=True
        if lastfloat:
            cols.append(_(""))
            self.list.InsertColumn(len(cols), _(""), wx.LIST_FORMAT_RIGHT)
                
        pos = -1
        for i in rs:    
            list = []    
            if pos == -1:
                k = i.keys()
                try:
                    pos = k.index('id')
                except: pos=0
                if not self.idpk2 == None: pos2 = k.index(self.idpk2)
            index = self.list.InsertStringItem(sys.maxint, str(i[0]))
            list.append(str(i[0]))
            for j in xrange(len(i)):
                if i[j] == 0:
                    s = ''
                else:      
                    if isinstance(i[j], float):
                        s = FormatFloat(i[j])
                    elif cols[j]=='Privacy':
                        if i[j]==True:
                            s = 'SI'
                        else:
                            s = 'NO'
                    elif cols[j][:4] == 'Data':
                        if i[j] == None:
                            s = u''
                        else:
                            try:
                                c = time.strptime(i[j],"%Y%m%d")
                                s = time.strftime("%d/%m/%Y",c)      
                            except:
                                s = sql2str(i[j])
                    else:
                        s = sql2str(i[j])
                self.list.SetStringItem(index, j, s)
                list.append(s)
            self.ListColumn.append(list)            
            self.pk.append(i[pos])
            
            self.list.SetItemData(index, len(self.pk)-1)    
            
            if not self.idpk2 == None: self.pk2.append(i[pos2])

        for i in range(len(cols)):
            if i==0:
                if self.showid == False:
                    self.list.SetColumnWidth(0, 0)        
            else:
                self.list.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER) 

        for i in xrange(self.list.GetItemCount()):
            COLS_NUMBER = [ 'totale', 'importo', 'imponibile', 'imposta']
            a=[]
            for j in range(len(cols)):
                val = self.list.GetItem(i, j).GetText()
                if cols[j].lower() in COLS_NUMBER:
                    if val.strip()=='' or val==None:
                        val = 0
                    else:
                        val = float(filter(lambda x: x.isdigit(), val))
                a.append(val)
            self.datalist[i] = a
        self.list.Thaw()     
        self.itemDataMap = self.datalist      
        self.SetColumnSorter(cols)
        self.after_fill()
        
    def after_fill(self):
        try:
            self.riepilogo.count.SetValue(str(self.list.GetItemCount()))
        except:      
            try:
                f = getattr(self, 'after_fill_data')
                if callable(f):
                    f()
            except: pass
                
    def GetListCtrl(self):
        return self.list
    
    def pk_refresh(self):
        self.pk = []
        for i in xrange(self.list.GetItemCount()):
            self.pk.append(self.list.GetItem(i).GetText())
#-----------------------------------------------------------------------------------------------------------------------------                 
class PanelRiepilogo ( wx.Panel ): 
    def __init__( self, parent ):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.TAB_TRAVERSAL )
        
        mainsizer = wx.BoxSizer( wx.VERTICAL )
        
        self.panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        flexsizer = wx.FlexGridSizer( 2, 4, 0, 0 )
        flexsizer.AddGrowableCol( 1 )
        flexsizer.AddGrowableCol( 3 )
        flexsizer.SetFlexibleDirection( wx.BOTH )
        flexsizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
        
        self.m_staticText1 = wx.StaticText( self.panel, wx.ID_ANY, u"Numero Elementi:", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        self.m_staticText1.SetFont( wx.Font( 10, 74, 90, 92, False, "Tahoma" ) )
        
        flexsizer.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.count = wx.TextCtrl( self.panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_RIGHT )
        self.count.Enable( False )
        flexsizer.Add( self.count, 0, wx.ALL, 5 )
        
        self.panel.SetSizer( flexsizer )
        self.panel.Layout()
        flexsizer.Fit( self.panel )
        mainsizer.Add( self.panel, 1, wx.EXPAND |wx.ALL, 0 )
        
        self.SetSizer( mainsizer )
        self.Layout()