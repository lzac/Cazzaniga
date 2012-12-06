# -*- coding: utf-8 -*-

import lib_global as g
import os
from moduli import *
import fileinput
import lib_crypto as crypto
import lib_function as F

enckey = "afellay"


def LoadConfig():
    meta = MetaData()
    meta.bind = g.engine
    CONFIG = Table("config", meta, autoload=True)
    MODULO = Table("modulo", meta, autoload=True)
    #Se esiste il file lo carico
    if os.path.exists("config.cfg"):
        L = []
        # Eliminazione
        CONFIG.delete().execute()
        # Inserimento nuova configurazione
        RowPos = 0
        for line in fileinput.input("config.cfg"):
            L.append(crypto.decrypt(line.rstrip('\n'), g.Dkeyref[RowPos]))
            RowPos+=1
            # Tabella config
        dconfig = {}
        dconfig['id'] = '001'
        dconfig['config'] = L[0]
        dconfig['isrete'] = L[1]
        dconfig['isaziendale'] = L[2]
        dconfig['data'] = crypto.encrypt(str(datetime.date.today()+datetime.timedelta(days=60)).replace("-", ""), enckey)
        CONFIG.insert().execute(dconfig)
            # Righe ulteriori: MODULI VARI
        for i in range(3, len(L)):
            s = MODULO.update()
            s = s.where(MODULO.c.id=='%0*d' % (4, i-3))
            s.execute({'abilitato':F.Str2Bool(L[i])})
        os.remove("config.cfg")
    else:
        #Se non esiste il file controllo che sia primo avvio e nel caso faccio azienda demo, altrimenti controllo data
        s = CONFIG.select()
        s = s.where(CONFIG.c.iseliminato==None)
        row = s.execute().fetchone()
        if row==None:
            #Inserisco azienda demo in config
            dconfig = {}
            dconfig['id'] = '001'
            dconfig['config'] = 'Azienda demo'
            dconfig['isrete'] = True
            dconfig['isaziendale'] = True
            dconfig['data'] = crypto.encrypt(str(datetime.date.today()).replace("-", ""), enckey)
            CONFIG.insert().execute(dconfig)
            #Abilito tutti i moduli
            s = MODULO.update()
            s.execute({'abilitato':True})
        else:
            s = select([CONFIG.c.data])
            s = s.where(CONFIG.c.iseliminato==None)
            row = s.execute().fetchone()
            row_data = crypto.decrypt(row.data, enckey)
            data = str(datetime.date.today()).replace("-", "")
            if data>row_data:
                return False
    return True
        

        
class Config:
    def __init__(self):
        self._config = {}
        self._init_config()
        
    def _init_config(self):
        self._config[g.CFG_LICENZA] = "VULCANO"
        self._config[g.CFG_AZIENDE] = 1 
        self._config[g.CFG_POSTAZIONI] = 1

    def licenza(self):
        return self._config[g.CFG_LICENZA]    

    def aziende(self):
        return self._config[g.CFG_AZIENDE]

    def postazioni(self):
        return self._config[g.CFG_POSTAZIONI]
    
    def multiaziendale(self):
        if self._config[g.CFG_POSTAZIONI]>1:
            return True
        return False

class Modulo():
    def __init__(self):
        self._modulo = {}
        self._init_modulo()
         
    def _init_modulo(self):
        self._modulo[g.MOD_OFFERTA] = True
        self._modulo[g.MOD_ROFFERTA] = True
        self._modulo[g.MOD_ORDVEN] = True
        self._modulo[g.MOD_ORDFOR] = True
        self._modulo[g.MOD_DDT] = True
        self._modulo[g.MOD_MAGAZZINO] = True
        self._modulo[g.MOD_FATTURA] = True
        self._modulo[g.MOD_CONTABILITA] = True
        self._modulo[g.MOD_DDT_VENDITE] = True
        self._modulo[g.MOD_DDT_CLAVORO] = True
        self._modulo[g.MOD_TERZISTI] = True
        self._modulo[g.MOD_COMMESSA] = True
        self._modulo[g.MOD_CERCOL] = True
        self._modulo[g.MOD_OFFICINA] = True
        
    def enabled(self, *args):
        for i in args:
            if self._modulo[i] == True:
                return True
        return False