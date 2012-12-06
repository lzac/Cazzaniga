# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from sqlalchemy import * 
import lib_db as db

#------------------------------------------------------------------------------------------------------             
class sql_bancacc(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'bancacc')
        self.versione = 3

    def create_table(self):
        tb = Table("bancacc", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key=True),
        Column('bancacc', Unicode(200), nullable=True ),
        Column("contoc", Unicode(12), nullable=True),
        Column("iban", Unicode(27), nullable=True),
        Column("ispredefinito", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

#------------------------------------------------------------------------------------------------------        
class sql_causale(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'causale')
        self.versione = 5

    def create_table(self):
        tb = Table("causale", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key=True),
        Column("causale", Unicode(200), nullable=True),
        Column("codice", Unicode(1), nullable=True),
        Column('idtipocausale', Unicode(10), nullable=True),
        Column('idcausalefattura', Unicode(10), nullable=True),
        Column('idtiposcadenzario', Unicode(10), nullable=True)) 
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False) 
        
class sql_tipocausale(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipocausale')
        self.versione = 5
        self.aggversione = 5

    def create_table(self):
        tb = Table("tipocausale", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("tipocausale", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 5:
                i = self.table.insert()
                i.execute(
                      {"id": "OFF", "tipocausale": "Offerta"},
                      {"id": "FAT", "tipocausale": "Fattura"})
            self.close()
        except: pass          
        
        
         

#------------------------------------------------------------------------------------------------------      
class sql_fatdet(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'fatdet')
        self.versione = 8

    def create_table(self):
        tb = Table("fatdet", self.meta,
            Column("idfattura", Unicode(10), nullable=False, primary_key = True),
            Column("id", Unicode(10), nullable=False, primary_key=True),    
            Column("idofferta", Unicode(10), nullable=True),
            Column("idoffdet", Unicode(10), nullable=True),            
            Column("descri", Unicode(100), nullable=True),
            Column("noteinizio1", Unicode(100), nullable=True),
            Column("noteinizio2", Unicode(100), nullable=True),
            Column("noteinizio3", Unicode(100), nullable=True),
            Column("noteinizio4", Unicode(100), nullable=True),
            Column("noteinizio5", Unicode(100), nullable=True),
            Column("noteinizio6", Unicode(100), nullable=True),
            Column("noteinizio7", Unicode(100), nullable=True),
            Column("noteinizio8", Unicode(100), nullable=True),
            Column("noteinizio9", Unicode(100), nullable=True),
            Column("noteinizio10", Unicode(100), nullable=True),
            Column("notefine1", Unicode(100), nullable=True),
            Column("notefine2", Unicode(100), nullable=True),
            Column("notefine3", Unicode(100), nullable=True),
            Column("notefine4", Unicode(100), nullable=True),
            Column("notefine5", Unicode(100), nullable=True),
            Column("notefine6", Unicode(100), nullable=True),
            Column("notefine7", Unicode(100), nullable=True),
            Column("notefine8", Unicode(100), nullable=True),
            Column("notefine9", Unicode(100), nullable=True),
            Column("notefine10", Unicode(100), nullable=True),            
            Column("quantita", Numeric(10, 2), PassiveDefault('0')),
            Column("prezzo", Numeric(10, 2), PassiveDefault('0')),
            Column("scontoperc", Numeric(10, 2), PassiveDefault('0')),
            Column("importo", Numeric(10, 2), PassiveDefault('0')),            
            Column('idiva', Unicode(10), nullable=True))                      
        tb.drop(checkfirst=True)        
        tb.create(checkfirst=False)
#------------------------------------------------------------------------------------------------------        
class sql_fativa(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'fativa')
        self.versione = 8

    def create_table(self):
        tb = Table("fativa", self.meta,
            Column("idfattura", Unicode(10), nullable=False, primary_key = True),
            Column("id", Unicode(10), nullable=False, primary_key=True),        
            Column('imponibilefat', Numeric(10, 2),PassiveDefault('0')),
            Column('scontoperc', Numeric(10, 2),PassiveDefault('0')),
            Column('sconto', Numeric(10, 2),PassiveDefault('0')),    
            Column('imponibile', Numeric(10, 2),PassiveDefault('0')),                                
            Column('idiva', Unicode(10), nullable=True),
            Column('imposta', Numeric(10, 2),PassiveDefault('0')),
            Column('totale', Numeric(10, 2),PassiveDefault('0')))
        tb.drop(checkfirst=True)        
        tb.create(checkfirst=False)
#------------------------------------------------------------------------------------------------------           
class sql_fatspesa(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'fatspesa')
        self.versione = 8

    def create_table(self):
        tb = Table("fatspesa", self.meta,
            Column("idfattura", Unicode(10), nullable=False, primary_key = True),
            Column("id", Unicode(10), nullable=False, primary_key=True),        
            Column("idspesa", Unicode(10), nullable=True),
            Column('imponibile', Numeric(10, 2),PassiveDefault('0')),
            Column('idiva', Unicode(10), nullable=True),
            Column('imposta', Numeric(10, 2),PassiveDefault('0')),
            Column('totale', Numeric(10, 2),PassiveDefault('0')))
        tb.drop(checkfirst=True)        
        tb.create(checkfirst=False)
#------------------------------------------------------------------------------------------------------        
class sql_fattura(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'fattura')
        self.versione = 8

    def create_table(self):
        tb = Table("fattura", self.meta,
            Column("id", Unicode(10), nullable=False, primary_key=True),
            Column("idcausale", Unicode(10), nullable=True),
            Column("data", Unicode(8), nullable=True),
            Column("protocollo", Integer, nullable=True),
            Column("numero", Unicode(50), nullable=True),
            Column("idanag", Unicode(10), nullable=True),     
            Column("idtipoanag", Unicode(10), nullable=True),  
            Column("recapito", UnicodeText(), nullable=True),
            
        
            Column("imponibile", Numeric(10, 2), PassiveDefault('0')),
            Column("imposta", Numeric(10, 2), PassiveDefault('0')),
            Column("totale", Numeric(10, 2), PassiveDefault('0')),

            
            Column("idmodopag", Unicode(10), nullable=True),   
            Column("idbancacc", Unicode(10), nullable=True),   
            Column("descrizionebanca", Unicode(2000), nullable=True),       
            Column("contoc", Unicode(12), nullable=True),
            Column("iban", Unicode(27), nullable=True),  
            Column("noteinterne", UnicodeText(), nullable=True),
            Column("notepiepagina", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

#------------------------------------------------------------------------------------------------------       
class sql_iva(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'iva')
        self.versione = 1

    def create_table(self):
        tb = Table("iva", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key=True),
        Column("iva", Unicode(200), nullable=True),
        Column("codice", Unicode(10), nullable=True),
        Column("idtipoiva", Unicode(10), nullable=True),
        Column("aliquota", Integer, nullable=True),
        Column("ispredefinito", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

#------------------------------------------------------------------------------------------------------        
class sql_modopag(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'modopag')
        self.versione = 1

    def create_table(self):
        tb = Table("modopag", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),      
        Column("modopag", Unicode(200), nullable=True),
        Column("numrate", Integer, nullable=True),
        Column("ispredefinito", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

#------------------------------------------------------------------------------------------------------        
class sql_postpag(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'postpag')
        self.versione = 1

    def create_table(self):
        tb = Table("postpag", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("postpag", Unicode(200), nullable=True),
        Column("m01", Integer, nullable=True),        
        Column("m02", Integer, nullable=True),
        Column("m03", Integer, nullable=True),
        Column("m04", Integer, nullable=True),
        Column("m05", Integer, nullable=True),        
        Column("m06", Integer, nullable=True),
        Column("m07", Integer, nullable=True),
        Column("m08", Integer, nullable=True),
        Column("m09", Integer, nullable=True),        
        Column("m10", Integer, nullable=True),
        Column("m11", Integer, nullable=True),
        Column("m12", Integer, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)



#------------------------------------------------------------------------------------------------------                
class sql_ratapag(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'ratapag')
        self.versione = 1

    def create_table(self):
        tb = Table("ratapag", self.meta,
        Column("idmodopag", Unicode(10), nullable=False, primary_key = True),
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("idtipopag", Unicode(10), nullable=True),
        Column("frequenza", Integer, nullable=True),
        Column("idtiposcadenza", Unicode(10), nullable=True),
        Column("giornipiu", Integer, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

#------------------------------------------------------------------------------------------------------        
class sql_spesa(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'spesa')
        self.versione = 1

    def create_table(self):
        tb = Table("spesa", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),      
        Column("spesa", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)


#------------------------------------------------------------------------------------------------------        
class sql_tipobanca(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipobanca')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("tipobanca", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("tipobanca", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "NS", "tipobanca": "Nostra banca"},
                      {"id": "VS", "tipobanca": "Vostra banca"})
            self.close()
        except: pass


#------------------------------------------------------------------------------------------------------
class sql_tipoiva(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipoiva')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("tipoiva", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("tipoiva", Unicode(200), nullable=True),
        Column("isaliquota", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "00", "tipoiva": "Imponibile", "isaliquota": True },
                      {"id": "01", "tipoiva": "Non imponibile", "isaliquota": False },            
                      {"id": "02", "tipoiva": "Esente", "isaliquota": False },
                      {"id": "03", "tipoiva": "Escluso", "isaliquota": False },
                      {"id": "04", "tipoiva": "Fuori campo", "isaliquota": False })
            self.close()
        except: pass            

#------------------------------------------------------------------------------------------------------
class sql_tipopag(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipopag')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("tipopag", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("tipopag", Unicode(200), nullable=True),  
        Column("idtipobanca", Unicode(10), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "RB", "tipopag": "Ricevuta Bancaria", "idtipobanca":"VS"},
                      {"id": "BO", "tipopag": "Bonifico", "idtipobanca":"NS"},
                      {"id": "RD", "tipopag": "Rimessa Diretta", "idtipobanca":"NS"},
                      {"id": "AS", "tipopag": "Assegno", "idtipobanca":"NS"},
                      {"id": "RI", "tipopag": "Rid", "idtipobanca":"NS"},
                      {"id": "TR", "tipopag": "Tratta", "idtipobanca":"NS"})
            self.close()
        except: pass

#------------------------------------------------------------------------------------------------------
class sql_tiposcadenza(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tiposcadenza')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("tiposcadenza", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("tiposcadenza", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)      
        tb.create(checkfirst=False)
     
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "DF", "tiposcadenza": "Data fattura"},
                      {"id": "FM", "tiposcadenza": "Fine mese"})
            self.close()
        except: pass

             
#------------------------------------------------------------------------------------------------------
class sql_anag(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'anag')
        self.versione = 1

    def create_table(self):
        tb = Table("anag", self.meta,
            Column("id", Unicode(10), nullable=False, primary_key = True),
            Column("anag", Unicode(200), nullable=True),            
            Column("partitaiva", Unicode(13), nullable=True),
            Column("codicefiscale", Unicode(16), nullable=True),
            Column("codiceministeriale", Unicode(25), nullable=True),
            Column("sitoweb", Unicode(200), nullable=True),
            Column("descrizionebanca", Unicode(2000), nullable=True),    
            Column("contoc", Unicode(12), nullable=True),
            Column("iban", Unicode(27), nullable=True),       
            Column("idtipoanag", Unicode(10), nullable=True),
            Column("recapito", Unicode(2000), nullable=True),        
            Column("indirizzo", Unicode(200), nullable=True),
            Column("cap", Unicode(5), nullable=True),
            Column("localita", Unicode(200), nullable=True, default=""),
            Column("idprovincia", Unicode(10), nullable=True),
            Column("idnazione", Unicode(10), nullable=True),
            Column("telefono", Unicode(200), nullable=True, default=""),
            Column("cellulare", Unicode(200), nullable=True, default=""),
            Column("fax", Unicode(200), nullable=True, default=""),
            Column("email", Unicode(200), nullable=True, default=""),
            Column("idmodopag", Unicode(10), nullable=True),
            Column("idpostpag", Unicode(10), nullable=True),
            Column("idiva", Unicode(10), nullable=True),     
            Column("note", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)        
        tb.create(checkfirst=False)
        
        
# Tipo anagrafica
class sql_tipoanag(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipoanag')
        self.versione = 1
    
    def create_table(self):
        tb = Table("tipoanag", self.meta,
            Column("id", Unicode(10), nullable=False, primary_key = True),     
            Column("tipoanag", Unicode(200), nullable=True),
            Column("idtipocodice", Unicode(10), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)     
        
# Tipo codice
class sql_tipocodice(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipocodice')
        self.versione = 1
        self.aggversione = 1
    
    def create_table(self):
        tb = Table("tipocodice", self.meta,
            Column("id", Unicode(200), nullable=False, primary_key = True),
            Column("tipocodice", Unicode(200), nullable=True))            
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)   
           
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "FIS", "tipocodice": "Codice fiscale"},
                      {"id": "MIN", "tipocodice": "Codice ministeriale"},
                      {"id": "ALL",  "tipocodice": "Entrambi"})
            self.close()
        except: pass   
    
        
        
        
        
# Scadenzario
class sql_scadenzario(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'scadenzario')
        self.versione = 9
    
    def create_table(self):
        tb = Table("scadenzario", self.meta,
            Column("id", Unicode(200), nullable=False, primary_key = True),
            Column("idfattura", Unicode(10), nullable=False),
            Column("idanag", Unicode(10), nullable=True),
            Column("idtipoanag", Unicode(10), nullable=True),  
            Column("numdoc", Unicode(15), nullable=True),            
            Column("data", Unicode(10), nullable=True),
            Column("idtipopag", Unicode(10), nullable=True),
            Column('idtiposcadenzario', Unicode(10), nullable=True),
            Column("importo", Numeric(10, 2), PassiveDefault('0')),
            Column("ispagato", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
#Tipo scadenzario
class sql_tiposcadenzario(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tiposcadenzario')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("tiposcadenzario", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("tiposcadenzario", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
         
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "INC", "tiposcadenzario": "Incasso"},
                      {"id": "PAG", "tiposcadenzario": "pagamento"})
            self.close()
        except: pass
        
        
        
        
        
        
        
        
#------------------------------------------------------------------------------------------------------     
# Tabelle per stampe
#------------------------------------------------------------------------------------------------------
class sql_stampafattura(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampafattura')
        self.versione = 2

    def create_table(self):
        tb = Table("stampafattura", self.meta,   
        Column("destinatario", UnicodeText(), nullable=True),
        Column("recapito", UnicodeText(), nullable=True),
        Column("numero", UnicodeText(), nullable=True),
        Column("data", UnicodeText(), nullable=True),
        Column("documento", UnicodeText(), nullable=True),
         Column("isfiscale", Boolean, nullable=True),
        Column("codicefiscale", UnicodeText(), nullable=True),     
         Column("isministeriale", Boolean, nullable=True),
        Column("codiceministeriale", UnicodeText(), nullable=True),     
        Column("partitaiva", UnicodeText(), nullable=True), 
        Column("pagamento", UnicodeText(), nullable=True),  
        Column("banca", UnicodeText(), nullable=True),
        Column("iban", UnicodeText(), nullable=True),
        Column("totaleimponibile", UnicodeText(), nullable=True),
        Column("totaleimposta", UnicodeText(), nullable=True),
        Column("totalefattura", UnicodeText(), nullable=True),
        Column("sum_pos", UnicodeText(), nullable=True),
        Column("sum_neg", UnicodeText(), nullable=True),
        Column("netto", UnicodeText(), nullable=True),      
        Column("notepiepagina", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)


class sql_stampafatdet(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampafatdet')
        self.versione = 3

    def create_table(self):
        tb = Table("stampafatdet", self.meta,
        Column('id', Unicode(10), nullable=False, primary_key = True),
        Column("posizione", UnicodeText(), nullable=True),
        Column("descrizione", UnicodeText(), nullable=True),
        Column("quantita", UnicodeText(), nullable=True),
        Column("prezzo", UnicodeText(), nullable=True),
        Column("scontoperc", UnicodeText(), nullable=True),
        Column("importo", UnicodeText(), nullable=True),
        Column("iva", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)


class sql_stampafativa(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampafativa')
        self.versione = 2

    def create_table(self):
        tb = Table("stampafativa", self.meta,
        Column('id', Unicode(10), nullable=False, primary_key = True),
        Column('imponibile', Unicode(10), nullable=False, primary_key = True),
        Column("iva", UnicodeText(), nullable=True),
        Column("descrizioneiva", UnicodeText(), nullable=True),
        Column("imposta", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)


class sql_stampafatspesa(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampafatspesa')
        self.versione = 2

    def create_table(self):
        tb = Table("stampafatspesa", self.meta,
        Column('id', Unicode(10), nullable=False, primary_key = True),
        Column("spesa", UnicodeText(), nullable=True),
        Column("imponibile", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)


class sql_stampafatsca(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampafatsca')
        self.versione = 2

    def create_table(self):
        tb = Table("stampafatsca", self.meta,
        Column('id', Unicode(10), nullable=False, primary_key = True),
        Column('data', Unicode(10), nullable=False, primary_key = True),
        Column("totale", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

#########################
class sql_percorso(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'percorso')
        self.versione = 2
        self.aggversione = 2

    def create_table(self):
        tb = Table("percorso", self.meta,
        Column("id", Unicode(50), nullable=False, primary_key = True),
        Column("path", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 2:
                i = self.table.insert()
                i.execute(
                      {"id":"THUNDERBIRD", "path": "C:\\Program Files\\Mozilla Thunderbird"})
            self.close()
        except: pass
        
        
        
# Autista
class sql_autista(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'autista')
        self.versione = 10

    def create_table(self):
        tb = Table("autista", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),      
        Column("autista", Unicode(200), nullable=True),        
        Column("datanascita", Unicode(8), nullable=True),
        Column("numeropatente", Unicode(200), nullable=True),
        Column("datainiziocollaborazione", Unicode(8), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
# Veicolo
class sql_veicolo(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'veicolo')
        self.versione = 4

    def create_table(self):
        tb = Table("veicolo", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),      
        Column("veicolo", Unicode(200), nullable=True),
        Column("targa", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
        
#------------------------------------------------------------------------------------------------------        
#OFFERTE
#------------------------------------------------------------------------------------------------------        
class sql_offerta(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'offerta')
        self.versione = 5

    def create_table(self):
        tb = Table("offerta", self.meta,
            Column("id", Unicode(10), nullable=False, primary_key=True),
            Column("idcausale", Unicode(10), nullable=True),
            Column("data", Unicode(8), nullable=True),
            Column("protocollo", Integer, nullable=True),
            Column("numero", Unicode(50), nullable=True),
            Column("idanag", Unicode(10), nullable=True),     
            Column("recapito", UnicodeText(), nullable=True),                                             
            Column("isrichiestatelefonica", Boolean, nullable=True),
            Column("datarichiestatelefonica", Unicode(8), nullable=True),            
            Column("ismail", Boolean, nullable=True),
            Column("datamail", Unicode(8), nullable=True),   
            Column("protocollomail", Unicode(50), nullable=True),           
            Column("isfax", Boolean, nullable=True),
            Column("datafax", Unicode(8), nullable=True),
            Column("protocollofax", Unicode(50), nullable=True),  
            Column("hasdisponibilita", Boolean, nullable=True),
            Column("hasmassimale", Boolean, nullable=True),
            Column("noteinterne", UnicodeText(), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
             
class sql_offdet(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'offdet')
        self.versione = 8

    def create_table(self):
        tb = Table("offdet", self.meta,
            Column("idofferta", Unicode(10), nullable=False, primary_key = True),
            Column("id", Unicode(10), nullable=False, primary_key=True), 
            Column("posizione", Unicode(100), nullable=True),   
            Column("isivato", Boolean, nullable=True),
            Column("ischiuso", Boolean, nullable=True),
            Column("descri", Unicode(100), nullable=True),
            Column("destinazione", Unicode(100), nullable=True),
            Column("noteinizio1", Unicode(100), nullable=True),
            Column("noteinizio2", Unicode(100), nullable=True),
            Column("noteinizio3", Unicode(100), nullable=True),
            Column("noteinizio4", Unicode(100), nullable=True),
            Column("noteinizio5", Unicode(100), nullable=True),
            Column("noteinizio6", Unicode(100), nullable=True),
            Column("noteinizio7", Unicode(100), nullable=True),
            Column("noteinizio8", Unicode(100), nullable=True),
            Column("noteinizio9", Unicode(100), nullable=True),
            Column("noteinizio10", Unicode(100), nullable=True),
            Column("notefine1", Unicode(100), nullable=True),
            Column("notefine2", Unicode(100), nullable=True),
            Column("notefine3", Unicode(100), nullable=True),
            Column("notefine4", Unicode(100), nullable=True),
            Column("notefine5", Unicode(100), nullable=True),
            Column("notefine6", Unicode(100), nullable=True),
            Column("notefine7", Unicode(100), nullable=True),
            Column("notefine8", Unicode(100), nullable=True),
            Column("notefine9", Unicode(100), nullable=True),
            Column("notefine10", Unicode(100), nullable=True),            
            Column("quantita", Numeric(10, 2), PassiveDefault('0')),
            Column("prezzo", Numeric(10, 2), PassiveDefault('0')),         
            Column('idiva', Unicode(10), nullable=True))                      
        tb.drop(checkfirst=True)        
        tb.create(checkfirst=False)     
        
        
class sql_stampaofferta(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampaofferta')
        self.versione = 5

    def create_table(self):
        tb = Table("stampaofferta", self.meta,   
        Column("destinatario", UnicodeText(), nullable=True),
        Column("recapito", UnicodeText(), nullable=True),
        Column("data", UnicodeText(), nullable=True),
        Column("oggetto", UnicodeText(), nullable=True),
        Column("intestazione", UnicodeText(), nullable=True),
        Column("isdisponibilita", Boolean, nullable=True),
        Column("ismassimale", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)


class sql_stampaoffdet(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampaoffdet')
        self.versione = 9

    def create_table(self):
        tb = Table("stampaoffdet", self.meta,
        Column('id', Unicode(10), nullable=False, primary_key = True),
        Column("corpo", UnicodeText(), nullable=True),
        Column("prezzo", UnicodeText(), nullable=True),
        Column("intestazione", UnicodeText(), nullable=True),
        Column("islineaprezzo", Boolean, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)        
        
                         
        

# Foglio di viaggio       
class sql_fogliodiviaggio(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'fogliodiviaggio')
        self.versione = 5

    def create_table(self):
        tb = Table("fogliodiviaggio", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True), 
        Column("data", Unicode(8), nullable=True),
        Column("dataritorno", Unicode(8), nullable=True),
        Column("numero", Unicode(10), nullable=True),        
        Column("idautista1", Unicode(10), nullable=True),
        Column("autista1", Unicode(200), nullable=True),
        Column("idautista2", Unicode(10), nullable=True),
        Column("autista2", Unicode(200), nullable=True),
        Column("idveicolo", Unicode(10), nullable=True),
        Column("veicolo", Unicode(200), nullable=True),
        Column("targa", Unicode(200), nullable=True),
        Column("idcommittente", Unicode(10), nullable=True),
        Column("committente", Unicode(200), nullable=True),
        Column("oraeluogo", Unicode(200), nullable=True),
        Column("destinazione", Unicode(200), nullable=True),        
        Column("veicolo", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
        
# STampa foglio di viaggio
class sql_stampafogliodiviaggio(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampafogliodiviaggio')
        self.versione = 5

    def create_table(self):
        tb = Table("stampafogliodiviaggio", self.meta,   
        Column("numero", UnicodeText(), nullable=True),
        Column("data", UnicodeText(), nullable=True),
        Column("dataritorno", UnicodeText(), nullable=True),
        Column("autista1", UnicodeText(), nullable=True),
        Column("autista2", UnicodeText(), nullable=True),
        Column("veicolo", UnicodeText(), nullable=True),
        Column("targa", UnicodeText(), nullable=True),
        Column("committente", UnicodeText(), nullable=True),     
        Column("oraeluogo", UnicodeText(), nullable=True),
        Column("destinazione", UnicodeText(), nullable=True))        
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
        
        
# Modulo assenza
class sql_moduloassenza(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self,  'moduloassenza')
        self.versione = 10

    def create_table(self):
        tb = Table("moduloassenza", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True), 
        Column("data", Unicode(8), nullable=True),    
        Column("idautista", Unicode(10), nullable=True),                
        Column("datainizio", Unicode(8), nullable=True),
        Column("orainizio", Unicode(5), nullable=True),
        Column("datafine", Unicode(8), nullable=True),
        Column("orafine", Unicode(5), nullable=True),
        Column("idtipoassenza", Unicode(10), nullable=True))                        
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
# STampa foglio di viaggio
class sql_stampamoduloassenza(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'stampamoduloassenza')
        self.versione = 10

    def create_table(self):
        tb = Table("stampamoduloassenza", self.meta,   
        Column("data", UnicodeText(), nullable=True),
        Column("autista", UnicodeText(), nullable=True),
        Column("datanascita", UnicodeText(), nullable=True),
        Column("numeropatente", UnicodeText(), nullable=True),
        Column("datainiziocollaborazione", UnicodeText(), nullable=True),
        Column("datainizio", UnicodeText(), nullable=True),
        Column("orainizio", UnicodeText(), nullable=True),
        Column("datafine", UnicodeText(), nullable=True),
        Column("orafine", UnicodeText(), nullable=True),
        Column("idtipoassenza", Unicode(10), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
class sql_tipoassenza(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'tipoassenza')
        self.versione = 10
        self.aggversione = 10

    def create_table(self):
        tb = Table("tipoassenza", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key = True),
        Column("numero", Unicode(5), nullable=True),
        Column("tipoassenza", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        
    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 10:
                i = self.table.insert()
                i.execute(
                      {"id": "01", "tipoassenza": "Era assente per malattia", "numero":"14"},
                      {"id": "02", "tipoassenza": "Era in ferie", "numero":"15"},
                      {"id": "03", "tipoassenza": "Era in congedo o in recupero", "numero":"16"},
                      {"id": "04", "tipoassenza": "Era alla guida di un veicolo non rientrante nell'ambito di applicazione del regolamento (CE) n. 561/2006 o dell'accordo AETS", "numero":"17"},
                      {"id": "05", "tipoassenza": "Eseguiva un lavoro diverso dalla guida", "numero":"18"},
                      {"id": "06", "tipoassenza": "Era disponibile", "numero":"19"},                      
                      )
            self.close()
        except: pass    

        