# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy  import types
from sqlalchemy.sql import text
import lib_global as g
import wx
import lib_msg as msg
import subprocess
import pyodbc
import os

class Dbase():
    def __init__(self, schema):
        self.is_connect = True 
        g.engine = create_engine("mysql://root:sapwd@localhost/fatturazione", pool_size=200, max_overflow=0, pool_recycle=3600)
 
        if len(g.engine.name)==0:
            self.is_connect = False
                 
        if self.is_connect:
            self.versione = 0
            self.schema = schema
            self.get_versione()
            if self.versione >= 0 and  self.versione < g.dbversion:
                self.update_schema()

    def get_versione(self):
        if self.versione == 0:
            if not self.is_nuovo():
                self.ver = 0
                try:
                    meta = MetaData()
                    meta.bind = g.engine
                    tb = Table("versione", meta, autoload=True)
                    s = select([tb.c.versione])
                    rs = s.execute()
                    row = rs.fetchone()
                    self.versione = row["versione"]
                except:
                    msg.WarningBox(g.mainframe, _("Errore inizializzazione infos"))
                    self.versione = -1
        return self.versione

    def is_nuovo(self):
        s = text("""SELECT COUNT(*) AS c1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='versione';""")
        conn = g.engine.connect()
        result = conn.execute(s)
        for row in result:
            if row["c1"] == 0:
                return True
        return False


    def update_schema(self):
        for m in self.schema:
            list = dir(m)
            for t in list:
                if t[:4] == "sql_":
                    f = getattr(m, t)
                    if callable(f):
                        tab = f()
                        if tab.versione > self.versione:
                            if self.versione == 0:
                                tab.create(False)
                            else:
                                tab.create(True)
                        if tab.aggversione > self.versione:
                            tab.aggiorna()
        # aggiorna tabella versione            
        meta = MetaData()
        meta.bind = g.engine
        t = Table('versione', meta, autoload=True)
        i = t.update()
        i.execute({"versione": g.dbversion})
      
class TabSchema():
    def __init__(self, nome):
        self.nome = nome
        self.table = None
        self.meta = MetaData()
        self.meta.bind = g.engine
        self.versione = 0
        self.aggversione = 0

    def exist(self):
        return g.engine.has_table(self.nome)

    def create(self, bkpres):
        rows = self.before_create(bkpres)
        self.create_table()
        self.meta.clear()
        self.after_create(rows)

    def before_create(self, bkpres):
        rows = []
        if bkpres == True and self.exist():
            self.open()
            s = self.table.select()
            rs = s.execute()
            rp = rs.fetchall()
            for row in rp:
                rows.append(row)
            self.close()
        return rows

    def after_create(self, rows):
        if len(rows) > 0:
            self.open()
            i = self.table.insert()
            i.execute(rows)
            self.close()

    def open(self):
        self.table = Table(self.nome, self.meta, autoload=True)

    def close(self):
        self.meta.clear()