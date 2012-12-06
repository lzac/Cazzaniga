# -*- coding: utf-8 -*-

import lib_global as g

class MenuApp():
    def __init__(self):
        self._id = []
        self._caption = []
        self._enabled = []
        self._tree = []
        self._initmenu()

    def add(self, id, caption, *args):
        self._id.append(id)
        self._caption.append(caption)
        enabled = False
        for i in args:
            if i == True:
                enabled = True
                break
        self._enabled.append(enabled)
        return id

    def label(self, id):
        i = self._id.index(id)
        return self._caption[i]

    def enabled(self, id):
        i = self._id.index(id)
        return self._enabled[i]

    def id(self, caption):
        i = self._caption.index(caption)
        return self._id[i]

    def _initmenu(self):
        self.FILE = self.add(1000, _("File"), True)
        self.FILE_NUOVO = self.add(1001, _("Nuovo"), True)
        self.FILE_APRI = self.add(1002, _("Apri"), True)
        self.FILE_CHIUDI = self.add(1003, _("Chiudi"), True)
        self.FILE_CHIUDITUTTI = self.add(1004, _("Chiudi tutti"), True)
        self.FILE_ESCI = self.add(1005, _("Esci"), True)
        self.FILE_STAMPA = self.add(1006, _("Stampa"), True)
        self.FILE_IMPORTA = self.add(1007, _("Importa"), True)
        self.FILE_IMPORTA_ABICAB = self.add(1008, _("Abi-Cab"), True)
        self.FILE_SALVA = self.add(1009, _("Salva"), True)
        self.FILE_EMAIL = self.add(1010, _("E-mail"), True)
        self.FILE_REFRESH = self.add(1011, _("Refresh"), True)    
        self.FILE_NUOVIELEMENTI = self.add(1012, _("Nuovi elementi"), True)     
        self.FILE_SELEZIONA = self.add(1013, _("Seleziona"), True)
        self.FILE_SALVACHIUDI = self.add(1014, _("Salva"), True)
        self.MODIFICA_COPIA =  self.add(1015, _("Copia"), True)
        self.MODIFICA_ELIMINA = self.add(1016, _("Elimina"), True)
        self.MODIFICA_ELIMINA_DEFINITIVA = self.add(1017, _("Eliminazione definitiva"), True)
        self.MODIFICA_PRIMO = self.add(1018, _("Primo"), True)
        self.MODIFICA_PRECEDENTE = self.add(1019, _("Precedente"), True)
        self.MODIFICA_SUCCESSIVO = self.add(1020, _("Successivo"), True)
        self.MODIFICA_ULTIMO = self.add(1021, _("Ultimo"), True)
        self.MODIFICA_DISATTIVA = self.add(1022, _("Disattiva"), True)
        self.MODIFICA_RIPRISTINA = self.add(1023, _("Ripristina"), True)
        self.MODIFICA_DUPLICA = self.add(1024, _("Duplica"), True)
        self.MODIFICA_SELEZIONATUTTO = self.add(1025, _("Seleziona tutto"), True)      
        self.TROVA_CONFERMA = self.add(1026, _("Conferma"), True)
        self.TROVA_CHIUDI = self.add(1027, _("Chiudi"), True)    
        self.FILE_SALVA_CHIUDI = self.add(1028, _("Salva e chiudi"), True)      
        self.MODIFICA = self.add(2000, _("Modifica"), True)
        self.MODIFICA_ANNULLA = self.add(2001, _("Menu"), True)
        self.VISUALIZZA = self.add(3000, _("Visualizza"), True)
        self.VISUALIZZA_AGGIORNA = self.add(3001, _("Aggiorna"), True)        
        self.VISUALIZZA_ESPLORAOGGETTI = self.add(3002, _("Esplora oggetti"), True)
        self.VISUALIZZA_PROPRIETA = self.add(3003, _("Finestra proprietà"), True)
        self.VISUALIZZA_FILTRO = self.add(3004, _("Filtra"), True)                       
        self.MANUTENZIONE = self.add(4000, _("Manutenzione tabelle"), True)       
        self.STRUMENTI = self.add(5000, _("Strumenti"), True)
        self.STRUMENTI_PROTEZIONE = self.add(5004, _("Protezione"), True)
        self.UTENTE = self.add(12000, _("Utenti"), True)
        self.GRUPPO = self.add(12001, _("Gruppi"), True)
        self.MODULO = self.add(12002, _("Moduli"), True)
        self.CONFIG = self.add(12003, _("Configurazione programma"), True)     
        self.AZIENDA = self.add(12005, _("Aziende"), True)       
        self.STRUMENTI_OPZIONE = self.add(5005, _("Opzioni"), True)
        self.STRUMENTI_AZIENDA = self.add(5006, _("Aziende"), True)
        self.STRUMENTI_AZIENDA_IMPOSTAZIONI = self.add(5007, _("Impostazioni"), True)                              
        self.AZIONI= self.add(6000, _("Azioni"), True)   
        self.STAMPE= self.add(6010, _("Stampe"), True)   
        self.PREFERITI = self.add(7000, _("Preferiti"), True)       
        self.PREFERITI_AGGIUNGI = self.add(7001, _("Aggiungi ai preferiti"), True)        
        self.PREFERITI_ORGANIZZA = self.add(7002, _("Organizza i preferiti"), True)
        self.PREFERITI_VISUALIZZA = self.add(7003, _("Visualizza i preferiti"), True)      
        self.ANAGRAFICA = self.add(8000, _("Anagrafica"), True)   
        self.DOCUMENTI = self.add(9010, _("Documenti"), True)   
        self.ARCHIVIO = self.add(8020, _("Archivio"), True)   
        self.MENU_IVA = self.add(8030, _("Iva"), True)    
        self.MENU_GESTIONE = self.add(8040, _("Gestione"), True)  
        
        
        ##################################################################################################################################
            #MODULO OFFERTA
        self.OFFERTA = self.add(10450, _("Preventivi"), True)   
        self.OFFDET = self.add(10451, _("Dettaglio preventivo"), True)
        self.ANTEPRIMA_OFFERTA = self.add(10452, _("Anteprima"), True)
        self.MAIL_OFFERTA = self.add(10453, _("Invia"), True)        
        self.EVASIONE_OFFERTA = self.add(10454, _("Fatturazione preventivi"), True)        
          
        ##################################################################################################################################
            #MODULO FATTURAZIONE
        self.FATTURA = self.add(10400, _("Fatture"), True)   
        self.FATDET = self.add(10401, _("Dettaglio fatturazione"), True)
        self.FATSPESA = self.add(10402, _("Spese fattura"), True)
        self.FATIVA = self.add(10404, _("Iva fattura"), True)
        self.RIEPILOGOFAT = self.add(10405, _("Riepilogo fatturato"), True)
        self.RIEPILOGOFATANAG = self.add(10407, _("Riepilogo fatturato per cliente"), True)
        self.RIEPILOGOFATCAUSALE = self.add(10408, _("Riepilogo fatturato per causale"), True)
        self.RIEPILOGOFATTIPOFATTURA = self.add(10409, _("Riepilogo fatturato per tipo fattura"), True)
        self.DLGSCONTI = self.add(10410, _("Sconti su conferma ordine"), True)
        self.PROSPETTO = self.add(10411, _("Prospetto fatturazione"), True)
        self.TIPOFATTURA = self.add(10406, _("Tipo fattura"), True)
        self.CAUSALE_FATTURA = self.add(10216, _("Causali fatture"), True)  
        self.CAUSALE_OFFERTA = self.add(10217, _("Causali offerte"), True)  
        self.ANTEPRIMA_FATTURA = self.add(666, _("Anteprima"), True)
        self.MAIL_FATTURA = self.add(667, _("Invia"), True)
        ##################################################
        ###################################################################################################################################        
        self.BANCHE = self.add(8050, _("Banche"), True)    
        self.NAZIONE = self.add(10101, _("Nazioni"), True)
        self.PROVINCIA = self.add(10102, _("Province"), True)     
        self.IVA = self.add(10104, _("Codici iva"), True)
        self.MODOPAG = self.add(10105, _("Modalita' di pagamento"), True)
        self.MODOPAG_RATE = self.add(10108, _("Rate pagamento"), True)
        self.TIPOPAG = self.add(10109, _("Tipologia di pagamento"), True)
        self.POSTPAG = self.add(10111, _("Posticipo pagamenti"), True)
        self.CAUSALE = self.add(10111, _("Causali"), True)
        self.NUMERAZIONE = self.add(10113, _("Numerazione movimenti"), True)
        self.RATAPAG = self.add(10114, _("Rata pagamento"), True)
        self.CAUTRASPORTO = self.add(10122, _("Causali di trasporto"), True)
        self.ARTDOC = self.add(10123, _("Articoli documenti"), True)
        self.VALIDITA = self.add(10124, _("Validità offerta"), True)
        self.ARTICOLO = self.add(10125, _("Articoli"), True)
        self.IMBALLAGGIO = self.add(10126, _("Imballaggio"), True)
        self.SPESA = self.add(10129, _("Spese"), True)
        self.CAUSALI = self.add(10209, _("Causali"), True)         
        self.BANCACC = self.add(10300, _("Banche societarie"), True)
        self.IMPORTABICAB = self.add(10301, _("Importa abi-cab"), True)
        self.CLIENTE = self.add(10502, _("Clienti"), True)
        self.ANAG_INDIRIZZO = self.add(10506, _("Indirizzo"), True)
        self.TABELLE = self.add(10799, _("Tabelle"), True)
        self.LOGIN = self.add(9000, _("login"), True)  
        self.TIPOANAGRAFICA = self.add(10120, _("Tipologia anagrafica"), True)  
        self.SCAINC = self.add(30020, _("Scadenzario incassi"), True)  
        self.SCAPAG = self.add(30021, _("Scadenzario pagamenti"), True)          
        self.MENULICENZA = self.add(200, _("Licenze"), True)  
        self.LICENZA = self.add(201, _("Visualizza licenza"), True)          
        self.AUTISTA = self.add(230, _("Autisti"), True)  
        self.VEICOLO = self.add(231, _("Veicoli"), True)  
        self.FOGLIODIVIAGGIO = self.add(232, _("Fogli di viaggio"), True)
        self.STAMPAFOGLIODIVIAGGIO = self.add(233, _("Stampa"), True)
        self.MODULOASSENZA = self.add(250, _("Modulo assenza"), True)
        self.TIPOASSENZA = self.add(251, _("Tipo di assenza"), True)
        self.STAMPAMODULOASSENZA = self.add(255, _("Stampa"), True)        
        self.PREZZOVIAGGIO = self.add(10460, _("Prezzo viaggi"), True)  
        
                         
    def _init_treepanel(self):
        self._tree.append(self.PDC)