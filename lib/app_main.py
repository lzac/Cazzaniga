# -*- coding: utf-8 -*-

import wx
import sys
import wx.lib.agw.aui as aui
import gettext
import lib_function as F
import lib_global as g
import lib_menu as menu
import os
import lib_sql as sql
import datetime
import thread
import tempfile
import password
import config
import wx.lib.agw.flatmenu as FM
from wx.lib.agw.fmresources import FM_OPT_SHOW_CUSTOMIZE
import lib_file as FILE
from sqlalchemy import MetaData, Table, select, and_
import lib_config
import lib_class as C
try:
    from agw import hyperlink as hl
except ImportError: # if it's not there locally, try the wxPython lib.
    import wx.lib.agw.hyperlink as hl

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwargs):   
        wx.Frame.__init__(self, *args, **kwargs)
        #
        self.Label = g.appname
        self.appmod = None
        # lingua
        wx.Locale(wx.LANGUAGE_DEFAULT)
        if g.lingua != 'IT':
            lan = gettext.translation(g.appname, "./locale", languages=[g.lingua])
            lan.install()   
        self.aziende = None
        self.mbar = None
        self.tbar = None
        self.tbar2 = None
        self.nb = None
        self.rp = None
        self.fp = None
        self.lp = None       
        self.current_riepilogo = None
        self.auimgr = aui.AuiManager()
        self.auimgr.SetManagedWindow(self)
          
    def postinit(self):
        # imposta frame   
        #if config.LoadConfig():
        g.menu = menu.MenuApp()
        self.lista = []
        self._menu()
        self._toolbar()
        self._aui()   
        self.Bind(wx.EVT_CLOSE, self.file_esci)
        info = self.auimgr.GetPane(_("lp"))
        info.Show(False)

    def _aui(self):
            #Pannello in alto per gestire ricerca con casella di testo
        self.hp = wx.Panel(self,-1, size=wx.Size(100, -1))
        info = aui.AuiPaneInfo()
        info = info.Name(_("p2"))
        info = info.CaptionVisible(False)
        info = info.Center()
        info.dock_proportion = 11
        self.auimgr.AddPane(self.hp, info) 
        sizer = wx.BoxSizer( wx.HORIZONTAL ) 
        self.filtro = wx.SearchCtrl(self.hp, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(-1, 205), style=wx.TE_PROCESS_ENTER)
        self.filtro.ShowCancelButton(True)
        sizer.Add( self.filtro, 1, wx.ALL|wx.EXPAND, 0 )       
        self.hp.SetSizer( sizer )
        self.hp.Layout()     
        self.filtro.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.ricerca)
        self.filtro.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.cancel)     
        self.filtro.Bind(wx.EVT_TEXT_ENTER, self.ricerca)   
            #Notebook centrale
        self.nb = aui.AuiNotebook(self, style=aui.AUI_NB_TOP |
                                  aui.AUI_NB_TAB_SPLIT |
                                  aui.AUI_NB_TAB_MOVE |
                                  aui.AUI_NB_SCROLL_BUTTONS |
                                  aui.AUI_NB_CLOSE_ON_ACTIVE_TAB | wx.NO_BORDER)
        info = aui.AuiPaneInfo()
        info = info.Name("cp")
        info = info.CaptionVisible(False)
        info = info.Center()
        info.dock_proportion = 300
        self.auimgr.AddPane(self.nb, info)
        self.nb.SetArtProvider(aui.tabart.ChromeTabArt())
        self.nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.change_page)
        self.nb.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.change_page)
            #Pannello centrale sottostante per avere il riepilogo del contenuto della pagina notebook aperta 
        self.info_down = aui.AuiPaneInfo()
        self.info_down = self.info_down.Name(_("bp"))
        self.info_down = self.info_down.CaptionVisible(False)
        self.info_down = self.info_down.Center()
        self.info_down.Position(1)
        self.info_down = self.info_down.CloseButton(False)
        self.info_down.dock_proportion = 35   
            #Pannello di sinistra per la gestione dei preferiti  
             
        # Aggiorna layout
        self.mbar.PositionAUI(self.auimgr)
        self.auimgr.AddPane(self.tbar, aui.AuiPaneInfo().Name("self.tbar").Caption("").ToolbarPane().Top().Row(1).Dockable(False))
        self.auimgr.AddPane(self.tbar2, aui.AuiPaneInfo().Name("self.tbar2").Caption("").ToolbarPane().Top().Row(1).Dockable(False))                    
        self.auimgr.Update()   
        
    def cancel(self, event):
        self.filtro.SetValue('')
        page = self.nb.GetCurrentPage()
        page.get_data()
        page.pk = []
        for i in range(page.list.GetItemCount()):
            page.pk.append(str(page.list.GetItem(i, 0).GetText()))
        
    def ricerca(self, event):
        page = self.nb.GetCurrentPage()
        page.get_data()
        value = str(self.filtro.GetValue()).lower()
        delete = []
        if value != '':
            k = 0
            for list in page.ListColumn:
                find = 0
                for element in list:
                    app = element.lower()
                    if app.startswith(value) == True:
                        find += 1
                if find == 0:                    
                    delete.append(k)
                k+=1
            delete.reverse()
            for i in range(len(delete)):
                page.list.DeleteItem(delete[i])
                page.pk.pop(delete[i])
            page.after_fill()
        else:
            self.cancel(None)
     
    def _menu(self):          
        self.mbar = FM.FlatMenuBar(self, wx.ID_ANY, 16, 1, options = FM_OPT_SHOW_CUSTOMIZE)
        self.mbar.Bind(wx.EVT_MENU, self.menu_lista)       
        ##############################################################################################################################                  
        #File
        menu_file = FM.FlatMenu()
        #Esci
        item = FM.FlatMenuItem(menu_file, g.menu.FILE_ESCI, g.menu.label(g.menu.FILE_ESCI), "", wx.ITEM_NORMAL)
        menu_file.AppendItem(item)            
        self.mbar.Append(menu_file, g.menu.label(g.menu.FILE))
        ##################################################################################################################  
        # Anagrafica
        menu_anagrafica = FM.FlatMenu()
        # Clienti
        item = FM.FlatMenuItem(menu_anagrafica, g.menu.CLIENTE, g.menu.label(g.menu.CLIENTE), "", wx.ITEM_NORMAL)
        menu_anagrafica.AppendItem(item)
        menu_anagrafica.AppendSeparator()  
        #Autisti
        item = FM.FlatMenuItem(menu_anagrafica, g.menu.AUTISTA, g.menu.label(g.menu.AUTISTA), "", wx.ITEM_NORMAL)
        menu_anagrafica.AppendItem(item)
        menu_anagrafica.AppendSeparator()             
        # Banche
        item = FM.FlatMenuItem(menu_anagrafica, g.menu.BANCACC, g.menu.label(g.menu.BANCACC), "", wx.ITEM_NORMAL)
        menu_anagrafica.AppendItem(item)
        menu_anagrafica.AppendSeparator()     
        # Cerca prezzo destinazione
        item = FM.FlatMenuItem(menu_anagrafica, g.menu.PREZZOVIAGGIO, g.menu.label(g.menu.PREZZOVIAGGIO), "", wx.ITEM_NORMAL)
        menu_anagrafica.AppendItem(item)
        menu_anagrafica.AppendSeparator()          
        
                        
        self.mbar.Append(menu_anagrafica, g.menu.label(g.menu.ANAGRAFICA))  
        ##################################################################################################################
        #DOCUMENTI
        CONT = 0
        menu_documenti = FM.FlatMenu() 
        #Fogli di viaggio
        item = FM.FlatMenuItem(menu_documenti, g.menu.FOGLIODIVIAGGIO, g.menu.label(g.menu.FOGLIODIVIAGGIO), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)          
        #Fogli di viaggio
        item = FM.FlatMenuItem(menu_documenti, g.menu.MODULOASSENZA, g.menu.label(g.menu.MODULOASSENZA), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)               
        # Separatore                
        menu_documenti.AppendSeparator()                   
        #OFFERTE
        item = FM.FlatMenuItem(menu_documenti, g.menu.OFFERTA, g.menu.label(g.menu.OFFERTA), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)     
               
        #FATTURA
        item = FM.FlatMenuItem(menu_documenti, g.menu.FATTURA, g.menu.label(g.menu.FATTURA), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)
        menu_documenti.AppendSeparator()  
        #SCADENZARIO INCASSI
        item = FM.FlatMenuItem(menu_documenti, g.menu.SCAINC, g.menu.label(g.menu.SCAINC), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)
        #SCADENZARIO PAGAMENTI
        item = FM.FlatMenuItem(menu_documenti, g.menu.SCAPAG, g.menu.label(g.menu.SCAPAG), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)   
        menu_documenti.AppendSeparator()  
        #CAUSALI OFFERTE
        item = FM.FlatMenuItem(menu_documenti, g.menu.CAUSALE_OFFERTA, g.menu.label(g.menu.CAUSALE_OFFERTA), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)                    
        #CAUSALI FATTURE
        item = FM.FlatMenuItem(menu_documenti, g.menu.CAUSALE_FATTURA, g.menu.label(g.menu.CAUSALE_FATTURA), "", wx.ITEM_NORMAL)
        menu_documenti.AppendItem(item)        
        self.mbar.Append(menu_documenti, g.menu.label(g.menu.DOCUMENTI)) 
        ##################################################################################################################
        # MANUTENZIONE TABELLE
        menu_manutenzione = FM.FlatMenu()
        #Nazioni
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.TIPOANAGRAFICA, g.menu.label(g.menu.TIPOANAGRAFICA), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)   
        menu_manutenzione.AppendSeparator()        
        #Nazioni
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.NAZIONE, g.menu.label(g.menu.NAZIONE), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)   
        #Province
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.PROVINCIA, g.menu.label(g.menu.PROVINCIA), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)      
        menu_manutenzione.AppendSeparator()
        #Tipologia pagamento
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.TIPOPAG, g.menu.label(g.menu.TIPOPAG), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)       
        #Modalita pagamento
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.MODOPAG, g.menu.label(g.menu.MODOPAG), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)    
        #Posticipo pagamenti
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.POSTPAG, g.menu.label(g.menu.POSTPAG), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)                     
        menu_manutenzione.AppendSeparator()        
        #Tipo assenza
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.TIPOASSENZA, g.menu.label(g.menu.TIPOASSENZA), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)   
        #Veicoli
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.VEICOLO, g.menu.label(g.menu.VEICOLO), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)   
        #Iva
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.IVA, g.menu.label(g.menu.IVA), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)
        menu_manutenzione.AppendSeparator()          
        #Spesa
        item = FM.FlatMenuItem(menu_manutenzione, g.menu.SPESA, g.menu.label(g.menu.SPESA), "", wx.ITEM_NORMAL)
        menu_manutenzione.AppendItem(item)      
        self.mbar.Append(menu_manutenzione, g.menu.label(g.menu.MANUTENZIONE))  
        ##################################################################################################################
        # MENU LICENZA
        menu_licenza = FM.FlatMenu()
        item = FM.FlatMenuItem(menu_licenza, g.menu.LICENZA, g.menu.label(g.menu.LICENZA), "", wx.ITEM_NORMAL)
        menu_licenza.AppendItem(item)   
        self.mbar.Append(menu_licenza, g.menu.label(g.menu.MENULICENZA))  
       
              
    def _toolbar(self):       
        #Toolbar azioni 
        self.tbar = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize, agwStyle=aui.AUI_TB_DEFAULT_STYLE | aui.AUI_TB_TEXT | aui.AUI_TB_HORZ_TEXT |aui.AUI_TB_PLAIN_BACKGROUND )
        self.tbar.SetToolBitmapSize(wx.Size(16, 16))        

        bmp = wx.Bitmap("pic\\document-new-2.png", wx.BITMAP_TYPE_PNG)        
        self.tbar.AddSimpleTool(g.menu.FILE_NUOVO, g.menu.label(g.menu.FILE_NUOVO), bmp,  g.menu.label(g.menu.FILE_NUOVO))
        self.Bind(wx.EVT_TOOL, self.menu_nuovo, id=g.menu.FILE_NUOVO)
        self.tbar.AddSeparator()
        
        bmp = wx.Bitmap("pic\\view-refresh-4.png", wx.BITMAP_TYPE_PNG)
        self.tbar.AddSimpleTool(g.menu.VISUALIZZA_AGGIORNA, g.menu.label(g.menu.VISUALIZZA_AGGIORNA), bmp, g.menu.label(g.menu.VISUALIZZA_AGGIORNA))
        self.Bind(wx.EVT_TOOL, self.menu_refresh, id=g.menu.VISUALIZZA_AGGIORNA)
        self.tbar.AddSeparator()
        
        
        bmp = wx.Bitmap("pic\\filter.png", wx.BITMAP_TYPE_PNG)
        self.tbar.AddSimpleTool(g.menu.VISUALIZZA_FILTRO, g.menu.label(g.menu.VISUALIZZA_FILTRO), bmp, g.menu.label(g.menu.VISUALIZZA_FILTRO))
        self.Bind(wx.EVT_TOOL, self.run_filtro, id=g.menu.VISUALIZZA_FILTRO)
        self.tbar.AddSeparator()
        self.tbar.Realize()        

        
    def OnDropDownToolbarItem(self, event):
        if event.IsDropDownClicked():
            tb = event.GetEventObject()
            tb.SetToolSticky(event.GetId(), True)
            # create the popup menu
            menu0 = wx.Menu()
            menu0.Append(g.menu.CLIENTE, _("Cliente"))
            # line up our menu with the button
            rect = tb.GetToolRect(event.GetId())
            pt = tb.ClientToScreen(rect.GetBottomLeft())
            pt = self.ScreenToClient(pt)
            pt = self.ScreenToClient(pt)
            self.PopupMenu(menu0, pt)
            # make sure the button is "un-stuck"
            tb.SetToolSticky(event.GetId(), False)
        
    def menu_refresh(self, event):
        page = self.nb.GetCurrentPage()
        try:
            self.filtro.SetValue("")
            page.get_data()
        except:
            wx.MessageDialog(None, _("Aggiornamento non disponibile!"), _("Attenzione"), wx.OK).ShowModal()
        
    def run_filtro(self, event):
        page = self.nb.GetCurrentPage()
        if page!=None:
            if os.path.exists("xrc\\flt_%s" % (page.Id)+'.xrc'):      
                kwargs = {'page':page}
                m = self.appmod.moduli['p%s' % (page.Id)]
                m.CustomDialog("xrc\\flt_%s" % (page.Id)+'.xrc', **kwargs)
            else:
                dlg = wx.MessageDialog(None, _("Nessun filtro avanzato disponibile!"), _("Attenzione"), wx.OK)
                dlg.ShowModal()
            
    def preferiti_visualizza(self, event):
        info = self.auimgr.GetPane(_("lp"))
        info.Show()
        self.auimgr.Update()

    def _aziende(self):
        self.aziende = wx.ListCtrl(self, -1)
        sql.fill_uteazi(self.aziende)
        isfound = False
        for i in xrange(self.aziende.GetCount()):
            if self.aziende.GetClientData(i) == g.idazienda:
                self.aziende.SetSelection(i)
                isfound = True
                break
        if isfound == False:
            self.aziende.SetSelection(wx.NOT_FOUND)
        self.aziende.Bind(wx.EVT_CHOICE, self.choice_aziende)

    def choice_aziende(self, event):
        pos = self.aziendw.GetSelection()
        g.idazienda = self.aziendw.GetClientData(pos)

    def on_searchctrl_cancel_btn(self, event):
        self.filtro.SetValue('')

    def on_searchctrl_text(self, event):
        try:
            page = self.nb.GetCurrentPage()
            delete = []
            if self.filtro.GetValue() != '':
                for i in range(page.list.GetItemCount()):
                    find = 0
                    for j in range(page.list.GetColumnCount()):
                        app = str(page.list.GetItem(i, j).GetText()).lower()
                        if app.find(str(self.filtro.GetValue()).lower()) != -1:
                            find += 1
                    if find == 0:
                        delete.append(i)
                delete.reverse()
                for i in range(len(delete)):
                    page.list.DeleteItem(delete[i])
            else:
                page.list.DeleteAllItems()
                for i in range(len(self.lista)):
                    app = self.lista[i]
                    index = page.list.InsertStringItem(sys.maxint, str(app[0]))
                    for j in xrange(len(app)):
                        page.list.SetStringItem(index, j, app[j])
            page.pk = []
            for i in range(page.list.GetItemCount()):
                page.pk.append(str(page.list.GetItem(i, 0).GetText()))
        except:
            pass
        
    def menu_nuovo(self, event):
        page = self.nb.GetCurrentPage()
        m = self.appmod.moduli['p%s' % (page.Id)]                
        # Se prezzo viaggio riapro il filtro
        if page.Id==g.menu.PREZZOVIAGGIO:
            self.run_filtro(None)
        # Per tutti gli altri
        else:        
            if page.Id in g.TREES:
                kwargs = {'parent_frame': page, 'new' : True}
                f = m.StandardFrame("xrc\\frm_%s" % (page.Id)+'.xrc', **kwargs)  
            else:
                page.list.Select(0)
                titolo = g.menu.label(page.Id)
                m = self.appmod.moduli['p%s' % (page.Id)]
                d = {'idpk2': page.idpk2, 'pk2': page.pk2}
                page.filtro = {}
                f = m.EditFrame(page.Id, titolo, page.list, page.pk, g.RECORD_APPEND, page.filtro, **d)
            f.frame.MakeModal(True) 
            f.frame.Show()

    def menu_lista(self, event, **kwargs):  
            #CHIUDI PAGINA CORRENTE
        if event.Id==g.menu.FILE_CHIUDI:    
            pass
            #CHIUDI TUTTE LE PAGINE
        elif event.Id==g.menu.FILE_CHIUDITUTTI:
            pass
            #ESCI
        elif event.Id==g.menu.FILE_ESCI:
            pass
            # Visualizza licenza
        elif event.Id==g.menu.LICENZA:
            FILE.aprifile("LICENSE.txt", True)
        else:
            self.menu_lista_ListPanel(event, **kwargs)
    
    def menu_lista_ListPanel(self, event, **kwargs):   
        data = str(datetime.date.today())
        data = data[:4]+data[5:7]+'01'    
        titolo = g.menu.label(event.Id)
        m = self.appmod.moduli['p%s' % (event.Id)]
        filtro = {}
        kwargs = {}
        idpk2 = ''
        #Impostazione filtri e pannelli
        if event.Id == g.menu.SCAINC:
            filtro['idtiposcadenzario'] = "INC"
            filtro['ispagato'] = None
        elif event.Id == g.menu.SCAPAG:
            filtro['idtiposcadenzario'] = "PAG"
            filtro['ispagato'] = None
            #FILTRO FATTURA
        if event.Id == g.menu.OFFERTA:
            filtro['data'] = {'segno':'>', 'value':data}
        if event.Id == g.menu.FATTURA:
            filtro['data'] = {'segno':'>', 'value':data}            
            
        if len(filtro) > 0:
            kwargs['filtro'] = filtro
        if len(idpk2):
            kwargs['idpk2'] = idpk2
        kwargs['parent'] = self
        kwargs['titolo'] = titolo
        #Apertura lista
        p = m.ListPanel(self, event.Id, **kwargs)
        self.nb.AddPage(p, titolo, select=True)
        page = self.nb.GetCurrentPage()
        self.lista = []
        for i in range(page.list.GetItemCount()):
            a = []
            for j in range(page.list.GetColumnCount()):
                a.append(str(page.list.GetItem(i, j).GetText()))
            self.lista.append(a)
        page.list.Select(0)
        if event.Id in [g.menu.PREZZOVIAGGIO]:
            self.run_filtro(None)        

    def menu_apri(self, event):
        try:
            page = self.nb.GetCurrentPage()
            ind = self.nb.GetPageIndex(page)
            m = self.appmod.moduli['p%s' % (page.Id)]
            d = {'idpk2': page.idpk2, 'pk2': page.pk2}
            f = m.EditFrame(page.Id, self.nb.GetPageText(ind), page.list, page.pk, g.RECORD_CURRENT, page.filtro, **d)
            f.frame.MakeModal(True)        
            f.frame.Show()   
        except Exception, e:
            print e    

    def menu_elimina(self, event):
        pass

    def file_esci(self, event=None):
        d = wx.MessageDialog(None, 'Sei sicuro di uscire dal programma?', g.appname , wx.YES_NO | wx.ICON_QUESTION)
        r = d.ShowModal()  
        if r == wx.ID_YES:   
            self.auimgr.UnInit()
            self.Destroy()
            
    def change_page(self, event):
        page = self.nb.GetCurrentPage()
        self.auimgr.DetachPane(self.current_riepilogo)    
        self.auimgr.ClosePane(self.info_down)  
        if page!=None:
            #Abilito/disabilito bottone nuovo della toolbar
            if page.Id==g.menu.GRUPPO or page.Id==g.menu.MODULO or page.Id==g.menu.CONFIG:
                self.tbar.EnableTool(g.menu.FILE_NUOVO, False)
            else:
                self.tbar.EnableTool(g.menu.FILE_NUOVO, True)
            #Gestisco layout nel cambio pagina     
            if page.riepilogo!=None:
                self.auimgr.AddPane(page.riepilogo, self.info_down)
                self.current_riepilogo = page.riepilogo
                self.info_down.Show()   
        self.auimgr.Update()

