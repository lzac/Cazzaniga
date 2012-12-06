# -*- coding: utf-8 -*-

import sys
import  wx
import  wx.lib.mixins.listctrl  as  listmix
import wx.calendar
import lib_global as g
import  images
import wx.xrc as xrc

class LookupListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)

class LookupPanel(wx.Panel, listmix.ColumnSorterMixin):
    def __init__(self, parent, **kwargs):
        wx.Panel.__init__(self, parent, -1)

        self.pk = kwargs.get('pk')
        self.data = kwargs.get('data')
        self.value = kwargs.get('value')
        self.ctrl = kwargs.get('ctrl')
        self.datalist = {}

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.il = wx.ImageList(16, 16)
        self.sm_up = self.il.Add(images.SmallUpArrow.GetBitmap())
        self.sm_dn = self.il.Add(images.SmallDnArrow.GetBitmap())

        self.text = wx.SearchCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)

        sizer.Add(self.text, 0, wx.ALL | wx.EXPAND, 5)
        self.text.Bind(wx.EVT_TEXT, self.search)

        self.list = LookupListCtrl(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, style=wx.LC_REPORT | wx.LC_SORT_ASCENDING)
        self.list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_list_item_activated)
        self.list.SetImageList(self.il, wx.IMAGE_LIST_SMALL)
        sizer.Add(self.list, 1, wx.ALL | wx.EXPAND, 5)

        self.PopulateList()

        self.itemDataMap = self.datalist
        listmix.ColumnSorterMixin.__init__(self, 2)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)

    def on_list_item_activated(self, event):
        val = self.list.GetFocusedItem()
        if val==-1:
            val=0
        self.ctrl.SetValue(self.list.GetItemText(val))  
        self.ctrl._AfterLookup()
        try:
            if self.ctrl==xrc.XRCCTRL(self.ctrl.owner.frame, 'idcausale'):
                f = getattr(self.ctrl.owner, 'evt_change_causale')
                if callable(f):
                    f(None)
        except: pass
        self.Parent.Close()

    def search(self, event):
        self.list.Freeze()
        self.list.ClearAll()

        self.list.InsertColumn(0, _('id'))
        self.list.InsertColumn(1, _('Descrizione'))
        self.datalist = {}

        for i in xrange(len(self.pk)):
            
            #if ((self.pk[i].lower().startswith(self.text.GetValue().lower()) == True) |
            #    (self.data[i].lower().startswith(self.text.GetValue().lower()) == True)):
            
            if ( (self.text.GetValue().lower() in self.pk[i].lower()) |
                 (self.text.GetValue().lower() in self.data[i].lower())):
                self.datalist[i] = (self.pk[i], self.data[i])

        for key, data in self.datalist.iteritems():
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetItemData(index, key)

        self.list.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.list.Thaw()
        self.list.Select(0)


    def PopulateList(self):

        self.list.Freeze()
        self.list.ClearAll()

        self.list.InsertColumn(0, _('id'))
        self.list.InsertColumn(1, _('Descrizione'))
        
        for i in xrange(len(self.pk)):
            self.datalist[i] = (self.pk[i], self.data[i])

        for key, data in self.datalist.iteritems():
            index = self.list.InsertStringItem(sys.maxint, data[0])
            self.list.SetStringItem(index, 1, data[1])
            self.list.SetItemData(index, key)

        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.list.SetColumnWidth(1, wx.LIST_AUTOSIZE_USEHEADER)
        self.list.Thaw()
        self.list.Select(0)

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self.list

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetSortImages(self):
        return (self.sm_dn, self.sm_up)


class LookupDialog(wx.Dialog):
    def __init__(self, *args, **kwargs):
        wx.Dialog.__init__(self, *args, title=_('Elenco'), style=(wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER))
        self.Panel = LookupPanel(self, **kwargs)
        self.Fit()
        self.SetSize((640, 500))
        self.SetMinSize((640, 500))


class CalendarPopup(wx.PopupTransientWindow):
    def __init__(self, parent, style, **kwargs):
        wx.PopupTransientWindow.__init__(self, parent, style)
        # title=_('Calendario'), style=(wx.DEFAULT_DIALOG_STYLE))
        p = wx.Panel(self, -1, style=wx.BORDER_DOUBLE)
        self.ctrl = kwargs.get('ctrl')
        self.cal = wx.calendar.CalendarCtrl(p, style=wx.calendar.CAL_SHOW_HOLIDAYS | wx.NO_BORDER | wx.calendar.CAL_SEQUENTIAL_MONTH_SELECTION | wx.calendar.CAL_SHOW_HOLIDAYS | wx.calendar.CAL_MONDAY_FIRST)
        self.cal.SetDate(kwargs.get('data'))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.cal, 1, wx.EXPAND)
        p.SetSizerAndFit(sizer)
        sz = p.GetBestSize()        
        self.SetSize((sz.width, sz.height))
        self.cal.Bind(wx.calendar.EVT_CALENDAR, self.on_calendar) 
        self.cal.SetHighlightColours(g.font_selected_day, g.background_selected_day)
        self.cal.SetHeaderColours(g.background_header, g.font_header)
        
                
    def on_calendar(self, event):
        self.ctrl.SetDate(self.cal.GetDate())
        self.ctrl._AfterLookup()
        self.Destroy()