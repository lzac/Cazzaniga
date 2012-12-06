# -*- coding: utf-8 -*-

import wx
import wx.grid
import lib_global as g
import wx.wizard
from sqlalchemy import *
import sys
import lib_function as F
import lookup
from datetime import datetime
from wx.lib.masked import *
from wx.lib.mixins.listctrl import CheckListCtrlMixin
from wx.lib.mixins.listctrl import TextEditMixin
import wx.lib.masked as masked
import lookup as lookup
#from optparse import choices
import lib_crypto as blow
import lib_global as g
import time
import lib_crypto as crypto
import lib_class as lib_class

START_VALUE = -999999

class WizardPage(wx.wizard.PyWizardPage):
    def __init__(self):
        pre = wx.wizard.PreWizardPageSimple()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        event.Skip()

class Choice(wx.Choice):
    def __init__(self):
        self.pk = []
        self.data = []
        self.filtro = {}
        self.pkfrom = {}
        self.fillzero = 0
        self._startvalue = START_VALUE
        self.owner = None
        self.evt_choice = None
        self.after_lookup = None
        pre = wx.PreChoice()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHOICE, self.OnChoice)
        event.Skip()

    def OnChoice(self , event):
        if not self.evt_choice == None:
            m = getattr(self.owner, self.evt_choice)
            if callable(m):
                m(self.Value)
    
    def _AfterLookup(self):
        i = self.GetSelection()
        if i == wx.NOT_FOUND:
            v = None
        else:
            v = self.GetClientData(i)
        if not self.after_lookup == None:
            m = getattr(self.owner, self.after_lookup)
            if callable(m):
                m(v, None)

    def Zap(self):
        self.pk = []
        self.Clear()

    def GetValue(self):
        i = self.GetSelection()
        if i == wx.NOT_FOUND:
            return ''
        v = self.GetClientData(i)
        return v

    def GetLookupValue(self):
        return super(Choice, self).GetStringSelection()

    def GetStartValue(self):
        return self._startvalue

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = u''
            super(Choice, self).SetSelection(wx.NOT_FOUND)
            return
        isfound = False
        for i in xrange(self.GetCount()):
            if self.GetClientData(i) == v:
                super(Choice, self).SetSelection(i)
                isfound = True
                break
        if isfound == False:
            super(Choice, self).SetSelection(wx.NOT_FOUND)

    def SetValue(self, v):
        isfound = False
        for i in xrange(self.GetCount()):
            if self.GetClientData(i) == v:
                super(Choice, self).SetSelection(i)
                isfound = True
                break
        # Se non trova azzera selezione
        if isfound == False:
            super(Choice, self).SetSelection(wx.NOT_FOUND)

    def GetCurrValue(self):
        i = self.GetSelection()
        if i == wx.NOT_FOUND:
            return None
        v = self.GetClientData(i)
        if len(v) == 0:
            return None
        return v

    def Append(self, item, clientData):
        if not (item == None or clientData == None):
            super(Choice, self).Append(item, clientData)
            self.pk.append(clientData)
            self.data.append(item)

    def AppendNew(self, data):
        self.Append(data[1], data[0])

    def Update(self, recno, data):
        super(Choice, self).SetString(recno, data[1])
        super(Choice, self).SetSelection(recno)

    def InitLookup(self, *args):
        pass

    def SetItemTextColour(self, recno, col):
        pass

    def SetSelection(self, recno):
        super(Choice, self).SetSelection(recno)

class LookupTextCtrl(wx.TextCtrl):
    def __init__(self):
        self._startvalue = START_VALUE
        self.pk = []
        self.data = []
        self.owner = None
        self.filtro = {}
        self.pkfrom = {}
        self.after_lookup = None
        self.evt_kill_focus = None
        self.fillzero = 0
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            #self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEnter)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    '''
    def OnTextEnter( self , event ):
        self.Lookup()
    '''

    def OnKillFocus(self , event):
        v = self.Value.upper()
        if self.fillzero > 0 and len(v) > 0:
            v = v.zfill(self.fillzero)
        self.Value = v
        self.Lookup()

    def InitLookup(self, nome, descricontrol, lkpcodice):
        self.nome = nome
        self._descricontrol = descricontrol
        self._lkpcodice = lkpcodice

    def Zap(self):
        self.pk = []
        self.data = []

    def Append(self, data, pk):
        if not (data == None or pk == None):
            self.pk.append(pk)
            self.data.append(data)

    def SetStartValue(self, v):
        meta = MetaData()
        meta.bind = g.engine
        self._startvalue = v
        if v == None:
            v = u''
        if self._lkpcodice == True:
            t = Table('pdc', meta, autoload=True)
            s = select([t.c.codice])
            s = s.where(t.c.id == v)
            s = s.where(t.c.iseliminato == None)
            row = s.execute().fetchone()
            self._startvalue = v
            if row == None:
                v = u''
            else:
                v = row.codice
        self.Value = v
        self.Lookup()

    def SetValue(self, v):
        self.Value = v
        self.Lookup()

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        meta = MetaData()
        meta.bind = g.engine   
        v = None
        if self._lkpcodice==True:
            t = Table('pdc', meta, autoload=True)
            s = select([t.c.id])
            s = s.where(t.c.codice == self.Value)
            s = s.where(t.c.iseliminato == None)
            row = s.execute().fetchone()
            if row != None:
                v = row.id
        else:
            if self.Value==None or self.Value=='':
                v = None
            else:
                v = self.Value
        return v

    def Lookup(self):
        self._descricontrol.SetValue(u'')
        v = self.Value
        if v in self.pk:
            i = self.pk.index(v)
            self._descricontrol.SetValue(F.sql2str( self.data[i]))
            self._AfterLookup()
        else:
            self.LookupDialog()
    
    def _AfterLookup(self):
        v = self.Value
        i = self.pk.index(v)
        if not self.after_lookup == None:
            m = getattr(self.owner, self.after_lookup)
            if callable(m):
                m(self.pk[i], self.data[i])    

    def LookupDialog(self):
        v = self.Value
        if len(v) > 0:
            kwargs = {}
            kwargs['pk'] = self.pk
            kwargs['data'] = self.data
            kwargs['value'] = v
            kwargs['ctrl'] = self
            #d = lookup.LookupDialog(self.owner.frame, self.Id, **kwargs)
            #d.ShowModal()

    def GetLookupValue(self):
        v = self.Value
        if v in self.pk:
            i = self.pk.index(v)
            return self.data[i]
        return ''

    def GetSelection(self):
        try:
            v = self.Value.upper()
            i = self.pk.index(v)
            return i
        except:
            return wx.NOT_FOUND

    def SetSelection(self, recno):
        pass

    def AppendNew(self, value):
        self.Append(value[1], value[0])

    def Update(self, recno, data):
        self.data[recno] = data[1]

    def SetItemTextColour(self, recno, col):
        pass
    
class LookupNumberTextCtrl(wx.TextCtrl):
    def __init__(self):
        self._startvalue = START_VALUE     
        self.owner = None
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        event.Skip()

    def InitLookup(self, tabella):
        self._table = tabella

    def SetStartValue(self, v):
        meta = MetaData()
        meta.bind = g.engine
        self._startvalue = v
        if v == None:
            v = u''
        if self._table != None:
            t = Table(self._table, meta, autoload=True)
            s = select([t.c.numero])
            s = s.where(t.c.id == v)
            s = s.where(t.c.iseliminato == None)
            row = s.execute().fetchone()
            if row == None:
                v = u''
            else:
                v = row.numero
        self.Value = v

    def SetValue(self, v):
        self.Value = v

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        meta = MetaData()
        meta.bind = g.engine   
        v = None
        if self._table!=None:
            t = Table(self._table, meta, autoload=True)
            s = select([t.c.id])
            s = s.where(t.c.numero == self.Value)
            s = s.where(t.c.iseliminato == None)
            row = s.execute().fetchone()
            if row != None:
                v = row.id
        else:
            if self.Value==None or self.Value=='':
                v = None
            else:
                v = self.Value
        return v

    def GetLookupValue(self):
        return self.Value

class TextCtrl(wx.TextCtrl):
    def __init__(self):
        self._startvalue = START_VALUE
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def OnKillFocus(self, event):
        v = self.Value
        if self.fillzero > 0 and len(v) > 0:
            self.Value = v.zfill(self.fillzero)
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = u''
        self.Value = v

    def GetLookupValue(self):
        return self.Value

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0 or str(self.Value)=='None':
            return None
        return self.Value

    def InitLookup(self, *args):
        pass
    
    
class FindTextCtrl(wx.TextCtrl):
    def __init__(self):
        self._startvalue = START_VALUE
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
        self.Bind(wx.EVT_TEXT, self.on_write)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def OnKillFocus(self, event):
        v = self.Value
        if self.fillzero > 0 and len(v) > 0:
            self.Value = v.zfill(self.fillzero)
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = u''
        self.Value = v

    def GetLookupValue(self):
        return self.Value

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0:
            return None
        return self.Value

    def InitLookup(self, *args):
        pass
    
    def SetList(self, list):
        self.list = list
        self.lista = []
        self.load_list()
    
    def load_list(self):
        for i in range(self.list.GetItemCount()):
            a = []
            for j in range(self.list.GetColumnCount()):
                a.append(str(self.list.GetItem(i, j).GetText()))
            self.lista.append(a)
                
    def on_write(self, event):
        if self.GetValue()!='':
            delete = []
            for i in range(self.list.GetItemCount()):
                find = 0
                for j in range(self.list.GetColumnCount()):
                    app = str(self.list.GetItem(i, j).GetText()).lower()
                    if app.find(str(self.GetValue()).lower()) != -1:
                        find += 1
                if find == 0:
                    delete.append(i)
            delete.reverse()
            for i in range(len(delete)):
                self.list.DeleteItem(delete[i])
        else:
            self.list.DeleteAllItems()
            for i in range(len(self.lista)):
                app = self.lista[i]
                index = self.list.InsertStringItem(sys.maxint, str(app[0]))
                for j in xrange(len(app)):
                    self.list.SetStringItem(index, j, app[j])
    
    
class DateCtrl(wx.DatePickerCtrl):
    def __init__(self):
        self._startvalue = START_VALUE
        self.owner = None
        self.evt_kill_focus = None
        pre = wx.PreDatePickerCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def OnKillFocus(self, event):
        v = self.Value
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = wx.DateTime.Now()
            self.Value = v
        else:
            val = str(v)
            date = wx.DateTime()
            date.Set(int(val[6:8]), int(val[4:6]) - 1, int(val[:4]))
            self.Value = date

    def GetLookupValue(self):
        val = str(self.Value)
        return val[6:10] + val[3:5] + val[0:2]

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        app = str(self.Value)
        return app[6:10] + app[3:5] + app[:2]

    def InitLookup(self, *args):
        pass


class UpperTextCtrl(wx.TextCtrl):
    def __init__(self):
        self._startvalue = START_VALUE
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_TEXT, self.OnText)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = u''
        self.Value = v

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0:
            return None
        return self.Value

    def GetLookupValue(self):
        return self.Value

    def OnText(self, event):
        event.Skip()
        selection = self.GetSelection()
        value = self.GetValue().upper()
        self.ChangeValue(value)
        self.SetSelection(*selection)

class IntegerTextCtrl(wx.TextCtrl):

    def __init__(self):
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        self._startvalue = START_VALUE
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)


    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHAR, self.OnChar)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = u''
        self.Value = str(v)

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0 or str(self.Value)=='None':
            return None
        return int(self.Value)

    def GetLookupValue(self):
        return self.Value

    def OnChar(self, event):
        key = event.GetKeyCode()
        try: character = chr(key)
        except ValueError: character = "" # arrow keys will throw this error 
        acceptable_characters = "1234567890."
        # 13 = enter, 314 & 316 = arrows, 8 = backspace, 127 = del         
        if character in acceptable_characters or key == 13 or key == 314 or key == 316 or key == 8 or key == 127:
            event.Skip()
            return
        else:
            return False

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)



class PassiveFloatTextCtrl(wx.TextCtrl):

    def __init__(self):
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        self._startvalue = START_VALUE
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHAR, self.OnChar)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None or  v == 0 or  v == '' or v == 'None':
            self.value = u''
        else:
            self.Value = "%.2f" % float(v)


    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0:
            return 0
        return "%.2f" % float(self.Value)

    def GetLookupValue(self):
        return self.Value

    def OnChar(self, event):
        key = event.GetKeyCode()
        try: character = chr(key)
        except ValueError: character = "" # arrow keys will throw this error 
        acceptable_characters = "1234567890."
        if character in acceptable_characters or key == 13 or key == 314 or key == 316 or key == 8 or key == 127:
            event.Skip()
            return
        else:
            return False

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)


class ThreePassiveFloatTextCtrl(wx.TextCtrl):

    def __init__(self):
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        self._startvalue = START_VALUE
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHAR, self.OnChar)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None or  v == 0 or  v == '':
            self.value = u''
        else:
            self.Value = "%.3f" % float(v)


    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0:
            return 0
        return "%.3f" % float(self.Value)

    def GetLookupValue(self):
        return self.Value

    def OnChar(self, event):
        key = event.GetKeyCode()
        try: character = chr(key)
        except ValueError: character = "" # arrow keys will throw this error 
        acceptable_characters = "1234567890."
        # 13 = enter, 314 & 316 = arrows, 8 = backspace, 127 = del         
        if character in acceptable_characters or key == 13 or key == 314 or key == 316 or key == 8 or key == 127:
            event.Skip()
            return
        else:
            return False

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)



class FilterTextCtrl(wx.TextCtrl):

    def __init__(self):
        self.fillzero = 0
        self.owner = None
        self.evt_kill_focus = None
        self._startvalue = START_VALUE
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)


    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHAR, self.OnChar)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None or  v == 0:
            v = u''
        self.Value = str(v)

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0:
            return None
        return self.Value

    def GetLookupValue(self):
        return self.Value

    def OnChar(self, event):
        key = event.GetKeyCode()
        try: character = chr(key)
        except ValueError: character = "" # arrow keys will throw this error 
        acceptable_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijlmnopqrstuvwxyz1234567890."
        # 13 = enter, 314 & 316 = arrows, 8 = backspace, 127 = del         
        if character in acceptable_characters or key == 13 or key == 314 or key == 316 or key == 8 or key == 127:
            event.Skip()
            return
        else:
            return False

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

class PwdTextCtrl(wx.TextCtrl):

    def __init__(self):
        self.owner = None
        self.evt_kill_focus = None
        self._startvalue = START_VALUE
        pre = wx.PreTextCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHAR, self.OnChar)
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
        event.Skip()

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None or  v == u'':
            self.Value = u''
        else:
            self.Value = crypto.decrypt(str(v), g.enckey)

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if len(self.Value) == 0:
            return u''
        return crypto.encrypt(self.Value, g.enckey)

    def GetLookupValue(self):
        return self.Value

    def OnChar(self, event):
        key = event.GetKeyCode()
        try: character = chr(key)
        except ValueError: character = "" # arrow keys will throw this error 
        acceptable_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijlmnopqrstuvwxyz1234567890."
        # 13 = enter, 314 & 316 = arrows, 8 = backspace, 127 = del         
        if character in acceptable_characters or key == 13 or key == 314 or key == 316 or key == 8 or key == 127:
            event.Skip()
            return
        else:
            return False

    def dateLastMod(self):
        return str(datetime.now())[:10].replace('-', '')

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)


class SpinCtrl(wx.SpinCtrl):
    def __init__(self):
        self._startvalue = START_VALUE
        self.owner = None
        self.evt_spinctrl = None
        pre = wx.PreSpinCtrl()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHECKBOX, self.OnSpinCtrl)
        event.Skip()

    def OnSpinCtrl(self, event):
        if not self.evt_spinctrl == None:
            m = getattr(self.owner, self.evt_spinctrl)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = False
        self.Value = v

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if self.Value == False:
            return None
        return self.Value

    def GetLookupValue(self):
        return str(self.Value)

class CheckBox(wx.CheckBox):

    def __init__(self):
        self._startvalue = START_VALUE
        self.owner = None
        self.evt_checkbox = None
        pre = wx.PreCheckBox()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
            
    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        event.Skip()

    def OnCheckBox(self, event):
        if not self.evt_checkbox == None:
            m = getattr(self.owner, self.evt_checkbox)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = False
        self.Value = v

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if self.Value == False:
            return None
        return self.Value

    def GetLookupValue(self):
        return ''
    
class RadioButton(wx.RadioButton):

    def __init__(self):
        self._startvalue = START_VALUE
        self.owner = None
        pre = wx.PreRadioButton()
        self.PostCreate(pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)
            
    def OnCreate(self, event):
        event.Skip()

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            v = False
        self.Value = v

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        if self.Value == False:
            return None
        return self.Value

    def GetLookupValue(self):
        return ''
    
class ListEditable(wx.ListCtrl, TextEditMixin):
    def __init__(self):
        self.owner = None
        self.pk = []
        Pre = wx.PreListCtrl()
        self.PostCreate(Pre)
        
    def OpenEditor(self, col, row):
        cols = self.GetColumnCount()-1   
        if col == cols or col==cols-1:
            self._editing = (col, row)
            TextEditMixin.OpenEditor(self, col, row)
        if col == 0:
            flag = self.IsChecked(row) 
            self.CheckItem(row, not flag) 
        
    def CloseEditor(self, evt=None):
        cols = self.GetColumnCount()-1   
        if not self.editor.IsShown():
            return
        text = self.editor.GetValue()
        self.editor.Hide()
        self.SetFocus()
        evt = wx.ListEvent(wx.wxEVT_COMMAND_LIST_END_LABEL_EDIT, self.GetId())
        evt.m_itemIndex = self.curRow
        evt.m_col = self.curCol
        item = self.GetItem(self.curRow, self.curCol)
        evt.m_item.SetId(item.GetId()) 
        evt.m_item.SetColumn(item.GetColumn()) 
        evt.m_item.SetData(item.GetData()) 
        evt.m_item.SetText(text)
        ret = self.GetEventHandler().ProcessEvent(evt)
        if not ret or evt.IsAllowed():    
            text = text.replace(',', '.')
            try:
                float(text)
            except:
                text = ''
            if self.IsVirtual():
                self.SetVirtualData(self.curRow, self.curCol, text.replace(',', '.'))
                self.SetVirtualData(self.curRow, self.curCol, text.replace(',', '.'))    
                if self.curCol == cols:
                    self.SetVirtualData(self.curRow, cols-1, '')
                elif self.curCol == cols-1:
                    self.SetVirtualData(self.curRow, self.curCol, '')
            else:
                self.SetStringItem(self.curRow, self.curCol, text.replace(',', '.'))        
                if self.curCol == cols:
                    if self._ReturnArrFLoat(self.GetItem(self.curRow, cols).GetText())!=None:
                        self.SetStringItem(self.curRow, cols-1, '')
                elif self.curCol == cols-1:
                    if self._ReturnArrFLoat(self.GetItem(self.curRow, cols-1).GetText())!=None:
                        self.SetStringItem(self.curRow, cols, '')      
        self.RefreshItem(self.curRow)
        self.owner._EndEdit(None)
        
    def _ReturnArrFLoat(self, val):
        if val==None or val.strip()=='':
            val = None
        try:
            return round(float(val), 2)
        except:
            return None
  
    def OnChar(self, event):
        key = event.GetKeyCode()
        try:
            character = chr(key)
        except:
            character = ''
        if key == wx.WXK_TAB and event.ShiftDown():
            self.CloseEditor()
            if self.curCol-1 >= 0:
                self.OpenEditor(self.curCol-1, self.curRow)           
        elif key == wx.WXK_TAB:
            self.CloseEditor()
            if self.curCol+1 < self.GetColumnCount():
                self.OpenEditor(self.curCol+1, self.curRow)
        elif key == wx.WXK_ESCAPE:
            self.CloseEditor()
        elif key == wx.WXK_DOWN:
            self.CloseEditor()
            if self.curRow+1 < self.GetItemCount():
                self._SelectIndex(self.curRow+1)
                self.OpenEditor(self.curCol, self.curRow)
        elif key == wx.WXK_UP:
            self.CloseEditor()
            if self.curRow > 0:
                self._SelectIndex(self.curRow-1)
                self.OpenEditor(self.curCol, self.curRow)       
        else:
            acceptable_characters = "1234567890.,-"  
            if character in acceptable_characters or key == 13 or key == 314 or key == 316 or key == 8 or key == 127:
                event.Skip()

    def SetEvent(self, **kwargs):
        self.event = {}
        for k, v in kwargs.iteritems():
            self.event[k] = v

    def GetOwner(self):
        return self.owner

    def GetChecked(self):
        checkedItems = []
        for i in range(self.GetItemCount()):
            if self.IsChecked(i):
                checkedItems.append(i)
        return checkedItems

    def GetColCount(self):
        return self.GetColumnCount()

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
        
    def GetSelection(self):
        return self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

    def FillData(self, rs, cols):
        self.pk = []
        self.Freeze()
        self.ClearAll()
        for i in range(len(cols)):
            self.InsertColumn(i, cols[i])
        pos = -1
        for i in rs:
            if pos == -1:
                try:
                    k = i.keys()
                    pos = k.index('id')
                except:
                    pos = 0
            index = self.InsertStringItem(sys.maxint, str(i[0]))
            for j in range(len(i)):
                if cols[j][:4] == 'Data':
                    if i[j] == None:
                        s = u''
                    else:
                        c = time.strptime(i[j],"%Y%m%d")
                        s = time.strftime("%d/%m/%Y",c)  
                else:
                    s = F.sql2strEditable(i[j])
                self.SetStringItem(index, j, s)
            self.pk.append(i[pos])
        for i in range(len(cols)):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        self.Thaw()
        self.Select(0)


class CheckList(wx.ListCtrl, CheckListCtrlMixin):
    def __init__(self):
        self.owner = None
        self.pk = []
        Pre = wx.PreListCtrl()
        self.PostCreate(Pre)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        CheckListCtrlMixin.__init__(self)

    def SetEvent(self, **kwargs):
        self.event = {}
        for k, v in kwargs.iteritems():
            self.event[k] = v

    def GetOwner(self):
        return self.owner

    def GetChecked(self):
        checkedItems = []
        for i in range(self.GetItemCount()):
            if self.IsChecked(i):
                checkedItems.append(i)
        return checkedItems

    def GetColCount(self):
        return self.GetColumnCount()

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
        
    def GetSelection(self):
        return self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

    def FillData(self, rs, cols):
        self.pk = []
        self.Freeze()
        self.ClearAll()
        for i in range(len(cols)):
            self.InsertColumn(i, cols[i])
        pos = -1
        for i in rs:
            if pos == -1:
                try:
                    k = i.keys()
                    pos = k.index('id')
                except:
                    pos = 0
            index = self.InsertStringItem(sys.maxint, str(i[0]))
            for j in range(len(i)):
                if i[j] == 0:
                    s = ''
                else:             
                    if cols[j][:4] == 'Data':
                        if i[j] == None:
                            s = u''
                        else:
                            c = time.strptime(i[j],"%Y%m%d")
                            s = time.strftime("%d/%m/%Y",c)        
                    else:
                        s = F.sql2str(i[j])
                self.SetStringItem(index, j, s)
            self.pk.append(i[pos])
        for i in range(len(cols)):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        self.Thaw()

class MoveListCtrl(wx.ListCtrl):
    def __init__(self):
        self.owner = None
        self.pk = []
        self.cols = []
        self.items = []
        c = wx.PreListCtrl()
        self.PostCreate(c)

    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()

    def Fill(self, cols, list):
        self.items = list
        self.cols = cols
        
        for p in range(len(cols)):
            self.InsertColumn(p, cols[p])

        self.DeleteAllItems()

        for line in list:
            index = self.InsertStringItem(sys.maxint, line[0])
            for i in range(len(cols)):
                self.SetStringItem(index, i, line[i])
        
        for p in range(len(cols)):
            self.SetColumnWidth(p, wx.LIST_AUTOSIZE_USEHEADER)

    def WriteItems(self, items):
        self.DeleteAllItems()
        for line in items:
            index = self.InsertStringItem(sys.maxint, line[0])
            for i in range(len(self.cols)):
                self.SetStringItem(index, i, line[i])
        for p in range(len(self.cols)):
            self.SetColumnWidth(p, wx.LIST_AUTOSIZE_USEHEADER)
            
    def GetOwner(self):
        return self.owner

    def GetSelection(self):
        return self.GetNextItem(-1, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)

    def DelSelItems(self):
        l = []
        idx = -1
        while True: 
            idx = self.GetNextItem(idx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if idx == -1 or idx == 0:
                break
            l.append(self.getItemInfo(idx))
        l.reverse()
        for i in l:
            pos = self.FindItem(i[0], i[2])
            self.DeleteItem(pos)
            
    def GetSelItems(self):
        l = []
        idx = -1
        while True: 
            idx = self.GetNextItem(idx, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if idx == -1 or idx == 0:
                break
            l.append(self.getItemInfo(idx))
        return l
        
    def GetNextSelected(self, current):
        return self.GetNextItem(current,
                                wx.LIST_NEXT_ALL,
                                wx.LIST_STATE_SELECTED)
    
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
    
    def getItemInfo(self, idx):
        """Collect all relevant data of a listitem, and put it in a list"""
        l = []
        l.append(idx) # We need the original index, so it is easier to eventualy delete it
        l.append(self.GetItemData(idx)) # Itemdata
        l.append(self.GetItemText(idx)) # Text first column
        for i in range(1, self.GetColumnCount()): # Possible extra columns
            l.append(self.GetItem(idx, i).GetText())
        return l
    
    def ShowId(self, f):
        if not f:
            self.SetColumnWidth(0,0)
            return
        else:
            self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)


class DetListCtrl(wx.ListCtrl):
    def __init__(self):
        self.owner = None
        self.pk = []
        c = wx.PreListCtrl()
        self.PostCreate(c)

    def SetEvent(self, **kwargs):
        self.event = {}
        for k, v in kwargs.iteritems():
            self.event[k] = v

    def GetOwner(self):
        return self.owner

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

    def FillData(self, rs, cols):
        
        self.pk = []
        self.Freeze()
        self.ClearAll()
        for i in range(len(cols)):
            self.InsertColumn(i, cols[i])
        pos = -1
        for i in rs:
            if pos == -1:
                try:
                    k = i.keys()
                    pos = k.index('id')
                except:
                    pos = 0
            index = self.InsertStringItem(sys.maxint, str(i[0]))
            for j in range(len(i)):
                if i[j] == 0:
                    s = ''
                else:             
                    if cols[j][:4] == 'Data':
                        if i[j] == None:
                            s = u''
                        else:
                            c = time.strptime(i[j],"%Y%m%d")
                            s = time.strftime("%d/%m/%Y",c)        
                    else:
                        s = F.sql2str(i[j])
                self.SetStringItem(index, j, s)
            self.pk.append(i[pos])
        for i in range(len(cols)):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
        self.Thaw()
        self.Select(0)

    def Fill(self, numcols, list):    
        self.DeleteAllItems()

        for line in list:
            index = self.InsertStringItem(sys.maxint, str(line[0]))
            for i in range(numcols):
                if line[i] is not None:
                    self.SetStringItem(index, i, line[i])
                
        for i in range(numcols):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)

    def ShowId(self, f):
        if not f:
            self.SetColumnWidth(0, 0)
            return
        else:
            self.SetColumnWidth(0, wx.LIST_AUTOSIZE_USEHEADER)

    def DoColumns(self, cols):
        for p in range(len(cols)):
            self.InsertColumn(p, cols[p])
        for i in range(len(cols)):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE_USEHEADER)
            
    def getItemText(self, idx):
        l = []
        l.append(idx) # We need the original index, so it is easier to eventualy delete it
        l.append(self.GetItemData(idx)) # Itemdata
        l.append(self.GetItemText(idx)) # Text first column
        for i in range(1, self.GetColumnCount()): # Possible extra columns
            l.append(self.GetItem(idx, i).GetText())
        return l    
    
    def getColumnText(self, index, col):
        item = self.GetItem(index, col)
        return item.GetText()
        
    def GetImageList(self):
        imagelist = []
        ncols = self.GetColumnCount()
        for x in range(self.GetItemCount()):
            app = []
            for i in range(ncols):
                app.append(self.getColumnText(x, i))
            imagelist.append(app)
        return imagelist
       
    def WriteItems(self, items):
        self.DeleteAllItems()
        for line in items:
            index = self.InsertStringItem(sys.maxint, line[0])
            for i in range(self.GetColumnCount()):
                self.SetStringItem(index, i, line[i])
        for p in range(self.GetColumnCount()):
            self.SetColumnWidth(p, wx.LIST_AUTOSIZE_USEHEADER)
     
    def EqualWidthCol(self):
        numcols = self.GetColumnCount()
        totwidth = sum([self.GetColumnWidth(i) for i in range(numcols)]) 
        eqw = totwidth / numcols
        for i in range(numcols):
            self.SetColumnWidth(i, eqw)
     
class GridCtrl(wx.grid.Grid):
    def __init__(self):
        self.owner = None
        self.pk = []
        c = wx.grid.PreGrid()
        self.PostCreate(c)
            #DATABASE
        self.meta = MetaData()
        self.meta.bind = g.engine
            #CONTROLLO CHE QUANTITA CONFERMATA DEVE ESSERE<=DI QUELLA CALCOLATA
        self.PREZZI = True
        self.ANAG = None
        self.ANAGSEDE = None
        self.CHECKANAG = True
        self.QUANTITA = True
        self.PARAM = None
        self.LIST = []
        self.FATTI = []
        #Eventi sulla grid
        self.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.change)  
        self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.RightClick)
    
    def RightClick(self,event):
        i = event.GetRow()
        self.table.data[i][0] = self.table.data[i][1]
        self.table.data[i][self.GetNumberCols()-1] = 1
        if i not in self.LIST:
            self.LIST.append(i)
        colour = wx.GREEN
        attr = wx.grid.GridCellAttr()
        attr.SetBackgroundColour(colour)
        self.SetRowAttr(i, attr)
        self.ForceRefresh()

    def Set_Table(self, cols, types, s):
        self.table = lib_class.CustomDataTable(cols, types, s)
        self.SetTable(self.table, True)
               
    def set_readonly(self):
        COLS = self.GetNumberCols()-1
        ROWS = self.GetNumberRows()-1
        for i in range(ROWS):
            for j in range(COLS):     
                if j!=0:             
                    self.SetReadOnly(i, j, True)
        self.ForceRefresh()
    
    def select(self, all):
        self.LIST = []
        for i in range(self.GetNumberRows()-1):
            if all:
                self.table.data[i][0] = self.table.data[i][1]
                self.table.data[i][self.GetNumberCols()-1] = 1
                colour = wx.GREEN
                self.LIST.append(i)
            else:
                self.table.data[i][0] = 0
                self.table.data[i][self.GetNumberCols()-1] = 0  
                colour = wx.WHITE
            attr = wx.grid.GridCellAttr()
            attr.SetBackgroundColour(colour)
            self.SetRowAttr(i, attr)
            self.ForceRefresh()
            self.ForceRefresh()
    
    def change(self, event):    
        col = event.GetCol()
        if col==0:
            numcols = self.GetNumberCols()        
            QTACONF = self.table.data[event.GetRow()][0]
            if QTACONF.strip()=='' or QTACONF==None:
                QTACONF = 0
            QTA = self.table.data[event.GetRow()][1]
            #SE VA IN ERRORE NON E INSERITO UN NUMERO
            try:
                QTACONF = round(float(QTACONF), 2)
                if QTACONF>=QTA:
                    if col==0:
                        #SE NON PUO AVERE QUANTITA CONFERMATA MAGGIORE DELLA QUANTITA
                        if self.QUANTITA:
                            self.table.data[event.GetRow()][0] = self.table.data[event.GetRow()][1]   
                        self.table.data[event.GetRow()][numcols-1] = 1
                        self.RemoveFromList(event.GetRow(), True)
                    else:
                        self.table.data[event.GetRow()][numcols-1] = 1
                    colour = wx.GREEN
                #SE INSERISCO 0 COME QUANTITA
                elif QTACONF==0:
                    self.table.data[event.GetRow()][numcols-1] = 0
                    colour = wx.WHITE
                    self.RemoveFromList(event.GetRow(), False)
                #ALTRIMENTI
                else:
                    self.table.data[event.GetRow()][0] = round(float(QTACONF), 2)
                    if event.GetCol()!=numcols-1:
                        self.table.data[event.GetRow()][numcols-1] = 0
                    colour = wx.GREEN
                    self.RemoveFromList(event.GetRow(), True)           
            except:
                self.table.data[event.GetRow()][0] = 0
                colour = wx.WHITE
                self.RemoveFromList(event.GetRow(), False)
            #COLORO LA RIGA VERDE SE  SELEZIONATA      
            attr = wx.grid.GridCellAttr()
            attr.SetBackgroundColour(colour)
            self.SetRowAttr(event.GetRow(), attr)
            self.ForceRefresh()
    
    def RemoveFromList(self, val, insert):
        if insert:
            if val not in self.LIST:
                self.LIST.append(val)
        else:
            if val in self.LIST:
                self.LIST.remove(val)
    
    def CheckAnag(self):
        #CONTROLLO ANAGRAFICA
        count = 0
        list = []
        for element in self.LIST:
            val = self.table.IDLIST[element]['idpadre']
            if not val in list:   
                list.append(val)
        t = Table(self.PARAM['EVPADRE'], self.meta, autoload=True)
        s = select([t.c.idanag, t.c.idanagsede]).distinct()
        s = s.where(t.c.id.in_(list))
        s = s.where(t.c.iseliminato==None)
        rs = s.execute()
        for row in rs:
            count+=1
        if count<=1:
            self.ANAG = row.idanag
            self.ANAGSEDE = row.idanagsede
            return True
        else:
            wx.MessageDialog(None, "Impossibile evadere documenti con anagrafica diversa", g.appname ,wx.OK | wx.ICON_QUESTION).ShowModal()
            return False
        
    def conferma(self): 
        OK = True
        if self.CHECKANAG:
            if not self.CheckAnag():
                OK = False
                return False
        if OK:
            self.go()
        return True
    
    def go(self):
        #ASSEGNAZIONE TABELLE DI PARTENZA E ARRIVO EVASIONE
        EVDET = Table(self.PARAM['EVDET'], self.meta, autoload=True)
        DET = Table(self.PARAM['DET'], self.meta, autoload=True)
        #CAMPI PER PADRE E POSIZIONE DA EVADERE     (ESEMPIO offerta,offdet)  
        FLD_PADRE = 'id'+self.PARAM['EVPADRE']
        FLD_DET = 'id'+self.PARAM['EVDET']
        #ESECUZIONE
        for POS in self.LIST:
            #SELEZIONO RIGA DI PARTENZA PER EVASIONE
            s = EVDET.select() 
            s = s.where(EVDET.c[FLD_PADRE] == self.table.IDLIST[POS]['idpadre'])
            s = s.where(EVDET.c.id == self.table.IDLIST[POS]['id'])
            s = s.where(EVDET.c.iseliminato==None)
            row = s.execute().fetchone()   
            #SE ESISTE CONVERTO IN DIZIONARIO E SALVO
            if row!=None:     
                d = dict(row)
                d['id'+self.PARAM['PADRE']] = self.PARAM['IDPADRE']
                d['id'] = self.get_pk_det(POS)
                d['quantita'] = round(float(self.table.data[POS][0]), 2)
                #GESTIONE PREZZI E SCONTI------------------------------
                if 'prezzo' in d.keys(): 
                    totale = round(d['quantita']*row['prezzo'], 2)
                    if 'scontoperc' in d.keys():
                        if d['scontoperc']!=0:
                            sconto = round((totale/100)*d['scontoperc'], 2)
                        else:
                            sconto = 0
                        importo = round(totale-sconto, 2)
                    else:
                        importo = totale
                    d['totale'] = totale
                    d['importo'] = importo
                #------------------------------------------------------       
                d[FLD_PADRE] = row[FLD_PADRE]
                d[FLD_DET] = row.id
                if not self.PREZZI:
                    d['prezzo'], d['sconto'], d['scontoperc'], d['totale'], d['importo'], d['impsconto'] = 0, 0, 0, 0, 0, 0
                #ESECUZIONE
                s = DET.insert()
                s.execute(d)    
                self.FATTI.append(d['id'])
                #CHIUSURA
                s = EVDET.update()   
                s = s.where(EVDET.c[FLD_PADRE] == self.table.IDLIST[POS]['idpadre'])
                s = s.where(EVDET.c.id == self.table.IDLIST[POS]['id'])
                s = s.where(EVDET.c.iseliminato==None) 
                val = self.table.data[POS][self.GetNumberCols()-1]
                if not val:
                    val = None
                s.execute({self.PARAM['field']:val})   
    
    def get_pk_det(self, pos):
        t = Table(self.PARAM['DET'], self.meta, autoload = True)
        FLD_PADRE = 'id'+self.PARAM['PADRE']
        s = select([func.max(t.c.id)])      
        s = s.where(t.c[FLD_PADRE]==self.PARAM['IDPADRE'])
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
   
    def seleziona(self, pos):
        DET = Table(self.PARAM['EVDET'], self.meta, autoload=True)
        #CAMPI PER PADRE E POSIZIONE DA EVADERE     (ESEMPIO offerta,offdet)  
        FLD_PADRE = 'id'+self.PARAM['EVPADRE']
        #ESECUZIONE 
        new = ''
        if pos!=self.GetNumberRows()-1:
            s = select([DET.c.descri, DET.c.descri2, DET.c.descri3, DET.c.descri4, DET.c.descri5,
                        DET.c.descri6, DET.c.descri7, DET.c.descri8, DET.c.descri9, DET.c.descri10])
            s = s.where(DET.c[FLD_PADRE]==self.table.IDLIST[pos]['idpadre'])
            s = s.where(DET.c.id==self.table.IDLIST[pos]['id'])
            s = s.where(DET.c.iseliminato==None)
            rs = s.execute()
            for row in rs:
                for string in row:
                    if ( (string!=None) and (string!='')):
                        new = new+string+'\n'
        return new
              
              
class FrameButton(wx.Button):
    def __init__(self):
        self.owner = None
        c = wx.PreButton()
        self.PostCreate(c)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_BUTTON, self.OnButton)
        event.Skip()

    def InitLookup(self, owner, id, ctrl):
        self.owner = owner
        self.id = id
        self.ctrl = ctrl

    def OnButton(self, event):
        self.owner.apri(self.id, self.ctrl)

class LookupButton(wx.BitmapButton):
    def __init__(self):
        self.owner = None
        c = wx.PreBitmapButton()
        self.PostCreate(c)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_BUTTON, self.OnButton)
        event.Skip()

    def InitLookup(self, owner, id, ctrl):
        self.owner = owner
        self.id = id
        self.ctrl = ctrl

    def OnButton(self, event):
        kwargs = {}
        kwargs['pk'] = self.ctrl.pk
        kwargs['data'] = self.ctrl.data
        kwargs['value'] = self.ctrl.GetValue()
        kwargs['ctrl'] = self.ctrl
        d = lookup.LookupDialog(self.owner.frame, self.id, **kwargs)
        d.ShowModal()


class TimeTextCtrl(masked.textctrl.PreMaskedTextCtrl):
    def OnCreate(self, event):
        self._startvalue = START_VALUE
        if self is event.GetEventObject():
            masked.textctrl.PreMaskedTextCtrl.OnCreate(self, event)
            self.evt_kill_focus = None
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            self.SetCtrlParameters(autoformat='24HRTIMEHHMM', useFixedWidthFont=False)

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        if v == None:
            self.Value = u'  :  '
        else:
            self.Value = v[:2] + ":" + v[-2:]

    def GetLookupValue(self):
        return self.Value

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        v = self.GetPlainValue()
        if len(v.strip()) == 0:
            return None
        return v

    def InitLookup(self, *args):
        pass

class OraTextCtrl(masked.textctrl.PreMaskedTextCtrl):
    def OnCreate(self, event):
        if self is event.GetEventObject():
            PreMaskedTextCtrl.OnCreate(self, event)
            self.evt_kill_focus = None
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            self.SetCtrlParameters(mask="##.##", formatcodes="F_,R", useFixedWidthFont=False)
            self.SetFieldParameters(1, choices=g.smincen, choiceRequired=True)


    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)

    def SetStartValue(self, v):
        self._startvalue = v
        self.Value = F.min2msk(v)

    def GetStartValue(self):
        return self._startvalue

    def InitLookup(self, *args):
        pass

    def GetCurrValue(self):
        v = self.GetPlainValue()
        if len(v.strip()) == 0:
            return None
        return F.str2min(v)

    def GetLookupValue(self):
        return self.Value
    
################################################################################################################# 
class FloatTextCtrl(masked.textctrl.PreMaskedTextCtrl):
    def OnCreate(self, event):
        self._startvalue = u'.00'
        if self is event.GetEventObject():
            masked.textctrl.PreMaskedTextCtrl.OnCreate(self, event)
            self.evt_kill_focus = None
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            self.Bind(wx.EVT_LEFT_DOWN, self.left_down)
            self.SetCtrlParameters(mask="#{9}.#{2}", formatcodes="F_-R", useParensForNegatives=False)
            self.SetFieldParameters(0, formatcodes='r<', validRequired=True)
            self.SetFieldParameters(1, defaultValue='00')

    def OnKillFocus(self, event):
        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)
        else:
            self.SetValue("%.2f" % self.GetCurrValue())

    def left_down(self, event):
        self.SetFocus()
        self.SetInsertionPoint(self.GetLastPosition() - 3)

    def SetStartValue(self, v):
        try:
            self._startvalue = round(v, 2)
        except:
            self._startvalue = round(0, 2)
        if v == None:
            self.SetValue('%.2f' % 0.00)
        else:
            self.SetValue('%.2f' % v)

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        v = self.GetValue()
        if len(v.strip()) == 0:
            return 0
        return round(float("%.2f" % round(float(v), 2)), 2)

    def Set_Value(self, v):
        self.SetValue("%.2f" % round(float(v), 2))

    def GetLookupValue(self):
        return "%.2f" % round(float(self.Value), 2)
#################################################################################################################
class DateTextCtrl(masked.textctrl.PreMaskedTextCtrl):
    def OnCreate(self, event):
        self.after_lookup = None
        self._startvalue = START_VALUE
        self._format = -1
        self.sep = g.formdata[2]
        if self is event.GetEventObject():
            masked.textctrl.PreMaskedTextCtrl.OnCreate(self, event)
            self.evt_kill_focus = None
            self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
            if g.formdata == 'gg/mm/aaaa':
                self.format = 1
                self.SetCtrlParameters(autoformat='EUDATEDDMMYYYY/', useFixedWidthFont=True)
            elif g.formdata == 'gg.mm.aaaa':
                self.format = 3
                self.SetCtrlParameters(autoformat='EUDATEDDMMYYYY.', useFixedWidthFont=True)
            elif g.formdata == 'gg/mm/aa' or g.formdata == 'gg.mm.aa':
                self.format = 2
                self.SetCtrlParameters(mask='##' + self.sep + '##' + self.sep + '##', formatcodes='F',
                                       validRegex='^' + wx.lib.masked.maskededit.days + self.sep + wx.lib.masked.maskededit.months,
                                       useFixedWidthFont=True)
            elif g.formdata == 'mm/gg/aaaa' or g.formdata == 'mm.gg.aaaa':
                self.format = 5
                self.SetCtrlParameters(mask='##' + self.sep + '##' + self.sep + '####', formatcodes='F',
                                       validRegex='^' + wx.lib.masked.maskededit.months + self.sep + wx.lib.masked.maskededit.days + self.sep + '\d{4}',
                                       useFixedWidthFont=True)

    def OnKillFocus(self, event):
        sep = self.GetValue()[2]
        v = string.split(self.GetValue(), sep)
        anno = string.strip(v[2], ' ')
        strepoch = str(g.epoch)
        if self.format in [2, 3]:
            if len(anno) == 1:
                self.SetValue(v[0] + self.sep + v[1] + self.sep + string.strip(anno) + '0')
        else:
            try:
                if len(anno) == 2:
                    if anno < strepoch[-2:]:
                        self.SetValue(v[0] + self.sep + v[1] + self.sep + str(g.epoch + 50 + int(anno)))
                    else:
                        self.SetValue(v[0] + self.sep + v[1] + self.sep + string.strip(str(str(g.epoch)[:2] + anno), ' '))
                if len(anno) == 1:
                    self.SetValue(v[0] + self.sep + v[1] + self.sep + str(g.epoch + 50 + int(anno)))
            except: pass

        if not self.evt_kill_focus == None:
            m = getattr(self.owner, self.evt_kill_focus)
            if callable(m):
                m(self.Value)
        self._AfterLookup()
                
    def _AfterLookup(self):
        if not self.after_lookup == None:
            m = getattr(self.owner, self.after_lookup)
            if callable(m):
                m(self.Value, None)
                
    def SetStartValue(self, v):
        self._startvalue = v
        if v == None or int(v) == 0:
            #GG MM AA
            if self.format == 2 or self.format == 4:
                self.Value = u'  ' + self.sep + '  ' + self.sep + '  '
            #GG MM AAAA o MM GG AAAA
            else:
                self.Value = u'  ' + self.sep + '  ' + self.sep + '    '
        #SE NON E' VUOTA
        else:
            #GG MM AA
            if self.format == 2 or self.format == 4:
                self.Value = v[-2:] + self.sep + v[4:6] + self.sep + v[2:4]
            #GG MM AAAA
            elif self.format == 1 or self.format == 3:
                self.Value = v[-2:] + self.sep + v[4:6] + self.sep + v[:4]
            #MM GG AAAA
            else:
                self.Value = v[4:6] + self.sep + v[-2:] + self.sep + v[:4]

    def GetLookupValue(self):
        return self.Value

    def GetStartValue(self):
        return self._startvalue

    def GetCurrValue(self):
        v = self.GetPlainValue()
        if len(v.strip()) == 0:
            return None
        #GG MM AA
        if self.format == 2 or self.format == 4:
            strepoch = str(g.epoch)
            s = string.split(self.GetValue(), self.sep)
            anno = v[-2:6]
            mese = s[1]
            giorno = s[0]
            #SE ANNO < EPOCH es. 30 -> 2030
            if anno < strepoch[-2:4]:
                anno = str(int(strepoch[:2]) + 1) + anno
            #SE ANNO > EPOCH es. 80 -> 2080
            else:
                anno = str(strepoch[:2]) + anno
        #GG MM AAAA
        elif self.format == 1 or self.format == 3:
            anno = v[-4:]
            mese = v[2:4]
            giorno = v[:2]
        else:
        #MM GG AAAA
            anno = v[-4:]
            mese = v[:2]
            giorno = v[2:4]
        return anno + mese + giorno

    def InitLookup(self, *args):
        pass

    def get_day(self):
        return self.GetDate().GetDay()

    def get_month(self):
        return self.GetDate().GetMonth()

    def get_year(self):
        return self.GetDate().GetYear()

    def GetDate(self):
        IsEmpty = lambda x: x.strip() == '' and True or False
        v = self.GetPlainValue()
        d = wx.DateTime.Today()
        s = string.split(self.GetValue(), self.sep)
        if not IsEmpty(v):
            #SE GG MM AA          
            if self.format == 2 or self.format == 4:
                strepoch = str(g.epoch)
                anno = v[-2:6]
                mese = v[2:4]
                giorno = v[:2]
                #SE ANNO < EPOCH es. 30 -> 2030
                if anno < strepoch[-2:4]:
                    anno = str(int(strepoch[:2]) + 1) + anno
                #SE ANNO > EPOCH es. 80 -> 2080
                else:
                    anno = str(strepoch[:2]) + anno
            #SE FORMATO gg mm aaaa
            elif self.format == 1 or self.format == 3:
                anno = v[-4:]
                mese = v[2:4]
                giorno = v[:2]
            #SE FORMATO mm gg aaaa            
            else:
                anno = v[-4:]
                mese = v[:2]
                giorno = v[2:4]
            d.Set(int(giorno), int(mese) - 1, int(anno))
        return d


    def SetDate(self, d):
        dd = '%0*d' % (2, d.GetDay())
        mm = '%0*d' % (2, d.GetMonth() + 1)
        yyyy = '%0*d' % (4, d.GetYear())
        #SE GG MM AA
        if self.format == 2 or self.format == 4:
            self.Value = dd + self.sep + mm + self.sep + yyyy[-2:]
        #SE GG MM AAAA
        elif self.format == 1 or self.format == 3:
            self.Value = dd + self.sep + mm + self.sep + yyyy
        #SE MM GG AAAA
        else:
            self.Value = mm + self.sep + dd + self.sep + yyyy
        return d

    def GetPos(self):
        txtdatePt = self.GetPosition()
        txtdatePt = self.GetParent().ClientToScreen(txtdatePt)
        return wx.Point(txtdatePt.x, txtdatePt.y + self.GetSize().y)


class CalendarButton(wx.BitmapButton):
    def __init__(self):
        self.owner = None
        c = wx.PreBitmapButton()
        self.PostCreate(c)
        self.Bind(wx.EVT_WINDOW_CREATE, self.OnCreate)

    def OnCreate(self, event):
        if self is event.GetEventObject():
            self.Bind(wx.EVT_BUTTON, self.OnButton)
        event.Skip()

    def InitLookup(self, owner, ctrl):
        self.owner = owner
        self.ctrl = ctrl

    def OnButton(self, event):
        kwargs = {}
        kwargs['data'] = self.ctrl.GetDate()
        kwargs['ctrl'] = self.ctrl
        win = lookup.CalendarPopup(self.owner.frame, wx.NO_BORDER, **kwargs)
        #ASSEGNA COME 0,0 LA POSIZIONE REL. DEL BUTT               
        pos = self.ClientToScreen((self.GetSize().x, -self.GetSize().y))
        sz = self.ctrl.GetSize()
        win.Position(pos, (0, sz[1]))
        win.Popup()
