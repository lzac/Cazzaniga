# -*- coding: utf-8 -*-

import lib_global as g
from sqlalchemy import *
from sqlalchemy import MetaData
import os
import ConfigParser

class Modulo():
    def __init__(self):
        self.meta = MetaData()
        self.meta.bind = g.engine
        self._gruppi = []  
        self._moduli = {}       
        UTEGRP = Table('utegrp', self.meta, autoload=True) 
        GRPMOD = Table('grpmod', self.meta, autoload=True)        
        MODULO = Table('modulo', self.meta, autoload=True)
        #Prendo tutti i moduli e li assegno inizialmente falsi
        s = select([MODULO.c.id]).distinct()
        s = s.where(MODULO.c.iseliminato==None)
        rs = s.execute()
        for row in rs:
            self._moduli[row.id] = False     
        # leggo gruppi di appartenenza
        s = select([UTEGRP.c.idgruppo]).distinct()
        s = s.where(and_(UTEGRP.c.idutente==g.idutente, UTEGRP.c.iseliminato==None))
        rs = s.execute()
        for row in rs:
            self._gruppi.append(row.idgruppo)     
        # controllo abilitazioni per gruppo
        s = select([GRPMOD.c.idmodulo, MODULO.c.abilitato]).distinct()
        s = s.where(GRPMOD.c.idgruppo.in_(self._gruppi))
        s = s.where(GRPMOD.c.idmodulo==MODULO.c.id)
        s = s.where(GRPMOD.c.iseliminato==None)
        rs = s.execute()
        for row in rs:
            self._moduli[row.idmodulo] = row.abilitato      
    
    def abilitato(self, id):
        m = self._moduli[id]
        return m

class Config():
    def __init__(self):
        meta = MetaData()
        meta.bind = g.engine
        t = Table('config', meta, autoload=True)
        s = t.select().order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        for row in rs:
            self._config[row.id] = row.config

    def value(self, id):
        m = self._config[id]
        return m[0]


class LocalCfg():
    def __init__(self):
        self.cfgfile = 'appdata\\'+ g.appname + ".cfg"

    def put_user(self, user):
        config = ConfigParser.RawConfigParser()
        config.add_section('Start')
        config.set('Start', 'user', user)
        with open(self.cfgfile, 'wb') as configfile:
            config.write(configfile)

    def get_user(self):
        try:
            if  os.path.isfile(self.cfgfile):
                config = ConfigParser.RawConfigParser()
                config.read(self.cfgfile)
                user = config.get("Start", "User")
            else:
                user = os.getenv("USERNAME", "Administrator")
        except:
            user = os.getenv("USERNAME", "Administrator")
        return user

    def get_sqlserver(self):
        try:
            if os.path.isfile(self.cfgfile):
                config = ConfigParser.RawConfigParser()
                config.read(self.cfgfile)
                dsn = config.get("SqlServer", "dsn")
            else:
                dsn = g.appname
        except:
            dsn = g.appname
        return dsn

    def put_sqlserver(self, dsn):
        config = ConfigParser.RawConfigParser()
        config.add_section("SqlServer")
        config.set("SqlServer", "dsn", dsn)
        with open(self.cfgfile, 'wb') as configfile:
            config.write(configfile)