# -*- coding: utf-8 -*-

import lib_crypto as crypto


#CHIAVE PASSWORD BLOWFISH
enckey = '12345678'
password = crypto.decrypt('oikospwd', enckey)
anagpassword = crypto.decrypt('basilepwd', enckey)

working = True
release = '1.0'
lingua = 'IT'
engine = None
stampengine = None
idazienda = '001'
codiceazienda = ''
azides = u'BASILE'
utecod = u'0000'
aziende = None

idutente = None
config = None
modulo = None
#PARAMETRI COLORI CALENDAR POPUP
font_selected_day = 'WHITE'
background_selected_day = '#68D9FF'
font_header = '#68D9FF'
background_header = 'WHITE'

vulcano = "VULCANO info@vulcanos.it"
keycritto = "12345"
#PARAMETRI COLORI LOGIN
login_bkg_color = '#E7F5FE'

utegrp = u'00'
utedes = u'Administrator'
vulcano = u"VULCANO info@vulcanos.it"
chiave = u"chiave database basile"
dicintento = '50'

template = "template\\"
report = "rpt\\"
mainframe = None
START_VALUE = -999999
menu = None




#DATABASE
dbms = None
dbversion = None
dbstampeversion = None
dbschema = None
dbstampe_schema = None
db = None
dbstampe = None
#MOVE RECORD
RECORD_FIRST = -4
RECORD_PREV = -3
RECORD_NEXT = -2
RECORD_LAST = -1
RECORD_CURRENT = 0
RECORD_APPEND = 1
RECORD_COPY = 2
RECORD_DELETE = 3
RECORD_UPDATE = 4
#
# Minuti e centesimi
#
mincen = 'M'
nmincen = []
smincen = []

epoch = 1950
formdata = "gg/mm/aaaa"
#
# percorsi
#
localpath = None
userpath = None
serverpath = None
temppath = None
rptpath = None
localcfg = None
oopath = None
picpath = None

#
# applicazione
#
APP_INFOS = 1
APP_OIKOS = 2
appname = None
app = None

TREES = [
         30001, #Piano dei conti
         ]

WIZARDS = [
           30032, #Contabilizza fatture
           30033, #Creazione riba
           30042, #Contabilizza effetti  
           30052,  #Contabilizza RIBA,
           30031  #Creazione effetti portafoglio   
          ]

DIALOGS = [30055, #STAMPA GIORNALE
           10517, #STAMPE REGISTRO COMMESSE
           ]

FRAMES = [
          30050, #Stampa brogliaccio
          30051, #Stampa mastrino
          30053, #Stampa saldi
          30054, #Stampa registro iva
          30056, #Stampa scadenzario
          30080, #Pagamento scadenza
          10506, #Riepilogo anagrafica
          10518, #Gestione commessa da officina
          10607, #Creazione guidata nuovo esercizio
          10405, #RIEPILOGO FATTURATO
          10411, #PROSPETTO FATTURATO
          10520, #PROSPETTO FATTURATO
          10407, #Riepilogo fatturato per cliente
          10408, #riepilogo fatturato per causale
          10409, #Riepilogo fatturato per tipo fatturato
          40080, #Import Archivi
          40060, #Ricerca note
          40050, #Ricerca mail
          40040, #Ricerca nominativi
          40030, #Ricerche in corso
          40020, #Avviso di chiamata
          40070  #Invio mail
         ]

#TABELLE PER CONTROLLO PROTOCOLLO
TABLES_TIPODOC = {
                  'CER':['cercol'],
                  'COL':['colata'],
                  'COM':['commessa'],
                  'CON':['pnota'],
                  'DDI':['dicintento'],
                  'DDT':['ddt'],
                  'EFF':['portaf'],
                  'FAT':['fattura'],
                  'MAG':['mag'],
                  'OFF':['offerta', 'rofferta'],
                  'ORD':['ordven', 'ordfor'],
                  'RIB':['riba'],
                  'RIC':['ricmer'],
                  'SCA':['sca']
                 }

Dkeyref = {
            0:"5da7c4wa",
            1:"c8s4r1gh",
            2:"v7fr4hj4",
            3:"2dsa5866",
            4:"vf874g6r",
            5:"4rew8rew",
            6:"few75f55",
            7:"we7vs5a2",
            8:"82c9ceer",
            9:"1984dc1d",
            10:"gfg5dsae",
            11:"87rew45d",
            12:"54reyhtr",
            13:"05erwa8r",
            14:"rew8fds5",
            15:"kjh7yt5r",
            16:"bvcb54rc",
            17:"w,xti545",
       }