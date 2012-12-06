# -*- coding: utf-8 -*-

import wx
import wx.lib.agw.genericmessagedialog as GMD
import images
import lib_global as g

def InfoBox(parent, message):
    btnStyle = wx.OK
    dlgStyle = wx.ICON_INFORMATION
    dlg = GMD.GenericMessageDialog(parent, message, g.appname, btnStyle | dlgStyle)
    dlg.ShowModal()
    dlg.Destroy()

def ErrorBox(parent, message):
    btnStyle = wx.OK
    dlgStyle = wx.ICON_ERROR
    dlg = GMD.GenericMessageDialog(parent, message, g.appname, btnStyle | dlgStyle)
    dlg.ShowModal()
    dlg.Destroy()

def WarningBox(parent, message):
    btnStyle = wx.OK
    dlgStyle = wx.ICON_WARNING
    dlg = GMD.GenericMessageDialog(parent, message, g.appname, btnStyle | dlgStyle)
    dlg.ShowModal()
    dlg.Destroy()

def YesNoBox(parent, message):
    btnStyle = wx.YES_NO
    dlgStyle = wx.ICON_QUESTION
    dlg = GMD.GenericMessageDialog(parent, message, g.appname, btnStyle | dlgStyle)
    #dlg.SetIcon(images.Mondrian.GetIcon())
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

def YesNoCancel(parent, message):
    btnStyle = wx.YES_NO | wx.CANCEL
    dlgStyle = wx.ICON_QUESTION
    dlg = GMD.GenericMessageDialog(parent, message, g.appname, btnStyle | dlgStyle)
    #dlg.SetIcon(images.morecontrols.GetIcon())
    result = dlg.ShowModal()
    dlg.Destroy()
    return result

def OkCancel(parent, message, caption=g.appname):
    btnStyle = wx.OK | wx.CANCEL
    dlgStyle = wx.ICON_QUESTION
    dlg = GMD.GenericMessageDialog(parent, message, caption, btnStyle | dlgStyle)
    result = dlg.ShowModal()
    dlg.Destroy()
    return result
