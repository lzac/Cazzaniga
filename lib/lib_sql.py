# -*- coding: utf-8 -*-

from sqlalchemy import *
import lib_global as g
import wx
import lib_function as F
import datetime
import lib_file as FILE

def controllo_dicintento():
    meta = MetaData()
    meta.bind = g.engine
    TAB = Table('dicintento', meta, autoload=True)
    s = select([TAB.c.datafine, TAB.c.numero],TAB.c.idtipointento=='03')
    s = s.where(TAB.c.iseliminato==None)
    rs = s.execute()
    for i in rs:
        today=str(wx.DateTime.Now())[:10]
        anno=today[6:10]
        mese=today[3:5]
        giorno=today[:2]
        today=anno+mese+giorno
        if today>i[0]:
            wx.MessageDialog(None,_(u'Dichiarazione di intento numero '+i[1]+' scaduta' ), 'Oikos', wx.OK | wx.ICON_INFORMATION).ShowModal()

def elimina_record(tabella, tabelle, pk):
    meta = MetaData()
    meta.bind = g.engine    
    for i in range(0, len(tabelle), 2):       
        tab = tabelle[i]
        key = tabelle[i+1]   
        tb = Table(tab, meta, autoload=True)
        r = tb.delete().where(tb.c['%s' % key]==pk)
        r.execute()       
    s = tabella.delete()
    s = s.where(tabella.c.id==pk)
    s.execute()
    
def fill_idtipoanag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoanag', meta, autoload=True)
    s = t.select().order_by(t.c.tipoanag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoanag,row.id)

def fill_idnazione(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('nazione', meta, autoload=True)
    s = t.select().order_by(t.c.nazione)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.nazione,row.id)
        
        
def fill_idautista(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('autista', meta, autoload=True)
    s = t.select().order_by(t.c.autista)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.autista,row.id)
        
        
def fill_idtipoassenza(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoassenza', meta, autoload=True)
    s = t.select().order_by(t.c.tipoassenza)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoassenza, row.id)
        
def fill_idtipocodice(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipocodice', meta, autoload=True)
    s = t.select().order_by(t.c.tipocodice)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipocodice,row.id)
        
def fill_idtipofattura(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipofattura', meta, autoload=True)
    s = t.select().order_by(t.c.tipofattura)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipofattura, row.id)

def fill_idprofilo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('profilo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty: ctrl.append('', '')
    for row in rs:
        ctrl.Append(row.profilo, row.id)
        
def fill_idtiposcadenzario(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiposcadenzario', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tiposcadenzario, row.id)
        
def fill_idfunzione(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('funzione', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.funzione, row.id)
        
def fill_idutente(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('utente', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.utente,row.id)
        
def fill_idstatoofficina(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('statoofficina', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.statoofficina, row.id)
        
def fill_idmese(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('mese', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.mese,row.id)
        
def fill_idmeseinizio(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('mese', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.mese,row.id)
        
        
def fill_idmesefine(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('mese', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.mese,row.id)
        
def fill_idtipoliquidazioneiva(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoliquidazioneiva', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoliquidazioneiva, row.id)
        
def fill_idtipogiornale(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipogiornale', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipogiornale, row.id)
        
def fill_idtipoaggancio(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoaggancio', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoaggancio, row.id)
        

def fill_idtimcampo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('timcampo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.timcampo,row.id)
        
def fill_idtipobanca(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipobanca', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipobanca, row.id)
        
def fill_idtipostatodoc(ctrl, **kwargs):
    empty = kwargs.get('empty', True)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipostatodoc', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipostatodoc, row.id)
        
def fill_idtipobancaacq(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipobanca', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipobanca,row.id)
        
def fill_idricmer(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('ricmer', meta, autoload=True)
    ANA = Table('anag', meta, autoload=True)
    s = select([t.c.numero, t.c.id, ANA.c.anag], group_by=[t.c.numero, t.c.id, ANA.c.anag])
    s = s.select_from(t.outerjoin(ANA, t.c.idanag==ANA.c.id))
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(F.sql2str(row.numero)+' - '+F.sql2str(row.anag), row.id)
        
def fill_idordven(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('ordven', meta, autoload=True)
    ANA = Table('anag', meta, autoload=True)
    s = select([t.c.numero, t.c.id, ANA.c.anag], group_by=[t.c.numero, t.c.id, ANA.c.anag])
    s = s.select_from(t.outerjoin(ANA, t.c.idanag==ANA.c.id))
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(F.sql2str(row.numero)+' - '+F.sql2str(row.anag), row.id)
        
def fill_idcab(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    abi = kwargs.get('abi', None)    
    if not abi == None:
        ctrl.filtro =  kwargs.get('filtro', {})
        ctrl.pkfrom = kwargs.get('pkfrom', {}) 
        meta = MetaData()
        meta.bind = g.engine
        t = Table('cab', meta, autoload=True)
        s = t.select().where(t.c.iseliminato==None)
        s = s.where(t.c.idabi==abi)
        s = s.order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        ctrl.Zap()        
        if empty == True: ctrl.Append('','')        
        for row in rs:
            ctrl.Append(row.cab,row.id)
            
def fill_idsede(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    idanag = kwargs.get('idanag', None)  
    ctrl.Clear()  
    if not idanag == None:
        ctrl.filtro =  kwargs.get('filtro', {})
        ctrl.pkfrom = kwargs.get('pkfrom', {}) 
        meta = MetaData()
        meta.bind = g.engine
        t = Table('anagsede', meta, autoload=True)
        s = t.select().where(t.c.iseliminato==None)
        s = s.where(t.c.idanag==idanag)
        s = s.order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        ctrl.Zap()        
        if empty == True: ctrl.Append('','')        
        for row in rs:       
            ctrl.Append(row.anagsede, row.id)
        
def fill_idricmerdet(ctrl, **kwargs):
    meta = MetaData()
    meta.bind = g.engine
    empty = kwargs.get('empty', False)
    idricmer = kwargs.get('idricmer', None)
    if not idricmer==None:
        ctrl.filtro =  kwargs.get('filtro', {})
        ctrl.pkfrom = kwargs.get('pkfrom', {}) 
        t = Table('ricmerdet', meta, autoload=True)
        s = t.select()
        s = s.where(t.c.idricmer==idricmer)
        s = s.where(t.c.iseliminato==None)
        s = s.order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        ctrl.Zap()
        if empty == True: ctrl.Append('','')    
        for row in rs:
            ctrl.Append(F.sql2str(row.descri), row.id)
            
def fill_idordvendet(ctrl, **kwargs):
    meta = MetaData()
    meta.bind = g.engine
    empty = kwargs.get('empty', False)
    idordven = kwargs.get('idordven', None)
    if not idordven==None:
        ctrl.filtro =  kwargs.get('filtro', {})
        ctrl.pkfrom = kwargs.get('pkfrom', {}) 
        t = Table('ordvendet', meta, autoload=True)
        s = t.select()
        s = s.where(t.c.idordven==idordven)
        s = s.where(t.c.iseliminato==None)
        s = s.order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        ctrl.Zap()
        if empty == True: ctrl.Append('','')    
        for row in rs:
            ctrl.Append(F.sql2str(row.descri), row.id)
        
def fill_idordfor(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('ordfor', meta, autoload=True)
    ANA = Table('anag', meta, autoload=True)
    s = select([t.c.id, ANA.c.anag])
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag, row.id)
        
def fill_idtipowhere(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipowhere', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipowhere,row.id)
        
def fill_idubicazione(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('ubicazione', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.ubicazione, row.id)
               
def fill_idtipodataprotocollo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipodataprotocollo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipodataprotocollo,row.id)
        
def fill_idcauportaf(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    s = s.where(t.c.idtipomov=='POR')
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causale,row.id)

def fill_causto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causto, row.id)

def fill_segno(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    if empty: ctrl.Append('', '')
    for segno in ['+', '-']:
        ctrl.Append(segno, segno)

def fill_oregg(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    if empty == True: ctrl.Append('','')
    for row, id in zip([_('Ore'), _('Giorni')], ['H', 'G']):
        ctrl.Append(row, id)
    
def fill_idtipoeffetto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoeffetto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoeffetto, row.id)
        
def fill_idprotocolloiva(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    empty = True
    meta = MetaData()
    meta.bind = g.engine
    t = Table('protocollo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.protocollo,row.id)
     
def fill_idtipoflex(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoflex', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')
    for row in rs:
        ctrl.Append(row.tipoflex,row.id)
        
def fill_idtiposenso(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiposenso', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')
    for row in rs:
        ctrl.Append(row.tiposenso,row.id)
        
def fill_idarro(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('arro', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')
    for row in rs:
        ctrl.Append(row.arro,row.id)
        
def fill_idcaucol(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.idtipodoc=='CON')
    s = s.where(t.c.idtipomov=='PNO')
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causale,row.id)

def fill_idmatricola(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('matricola', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.matricola,row.id)     
    
def fill_idmaggio(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('maggio', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.maggio,row.id)      
        
def fill_idstatocivile(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('statocivile', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.statocivile,row.id)   
        
def fill_idtipocontod(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoconto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoconto,row.id) 
        
def fill_idtipocontoa(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoconto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoconto,row.id)  
        
def fill_idtipoconto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoconto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoconto, row.id)  
        
def fill_idtipocontocontropartita(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoconto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoconto, row.id)   

def fill_idtipoarro(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoarro', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoarro,row.id)   

def fill_idtipogestiva(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipogestiva', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipogestiva,row.id)
        
def fill_idtipotemplate(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipotemplate', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipotemplate, row.id)
        
def fill_idtiporegiva(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiporegiva', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tiporegiva,row.id)
        
def fill_idtipopnota(ctrl, **kwargs):
    empty = kwargs.get('emty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipopnota', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipopnota,row.id)

def fill_idpdccontoc(ctrl, **kwargs):
    empty = kwargs.get('empty', False)  
    meta = MetaData()
    meta.bind = g.engine
    t = Table('pdc', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.isultimo==True)
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.pdc, row.codice)
        
def fill_idpdcsbf(ctrl, **kwargs):
    empty = kwargs.get('empty', False)  
    meta = MetaData()
    meta.bind = g.engine
    t = Table('pdc', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.isultimo==True)
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.pdc, row.codice)
   
def fill_idcontropartita(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('caupnota', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.idcausale==ctrl.owner.get_value('idcausale'))
    s = s.where(t.c.id!=ctrl.owner.get_value('id'))
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.caupnota, row.id)
        
def fill_idconto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    tipoconto = kwargs.get('tipoconto', None)  
    meta = MetaData()
    meta.bind = g.engine  
    if not tipoconto == None:
        ctrl.Zap()
        if tipoconto == 'C':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.iscliente==1)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.CLIENTE, 'idconto')
        elif tipoconto == 'F':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.isfornitore==True)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()
            row = rs.fetchall        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.FORNITORE, 'idconto')
        elif tipoconto == 'P':
            t = Table('pdc', meta, autoload=True)
            s = t.select()
            s = s.where(t.c.isultimo==True)
            s = s.where(t.c.iseliminato==None)
            s = s.order_by(t.c.id)
            rs = s.execute()
            row = rs.fetchall         
            if empty == True: ctrl.Append('','')    
            for row in rs:
                ctrl.Append(row.pdc, row.codice)
            kwargs = {'lkp_codice' : True} 
            ctrl.owner.appendlkp(g.menu.PDC, 'idconto', **kwargs)

def fill_idcontocontropartita(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    tipoconto = kwargs.get('tipocontocontropartita', None)  
    meta = MetaData()
    meta.bind = g.engine  
    if not tipoconto == None:
        if tipoconto == 'C':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.iscliente==1)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.CLIENTE, 'idcontocontropartita')
        elif tipoconto == 'F':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.isfornitore==True)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()
            row = rs.fetchall        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.FORNITORE, 'idcontocontropartita')
        elif tipoconto == 'P':
            t = Table('pdc', meta, autoload=True)
            s = t.select()
            s = s.where(t.c.isultimo==True)
            s = s.where(t.c.iseliminato==None)
            s = s.order_by(t.c.id)
            rs = s.execute()
            row = rs.fetchall
            ctrl.Zap()
            if empty == True: ctrl.Append('','')    
            for row in rs:
                ctrl.Append(row.pdc, row.codice)
            kwargs = {'lkp_codice' : True} 
            ctrl.owner.appendlkp(g.menu.PDC, 'idcontocontropartita', **kwargs)
    
def fill_idcontod(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    tipocontod = kwargs.get('tipocontod', None)  
    meta = MetaData()
    meta.bind = g.engine  
    if not tipocontod == None:
        if tipocontod == 'C':          
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.iscliente==True)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.CLIENTE, 'idcontod')
        elif tipocontod == 'F':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.isfornitore==True)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()
            row = rs.fetchall        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.FORNITORE, 'idcontod')
        elif tipocontod == 'P':
            t = Table('pdc', meta, autoload=True)
            s = t.select()
            s = s.where(t.c.isultimo==True)
            s = s.where(t.c.iseliminato==None)
            s = s.order_by(t.c.id)
            rs = s.execute()
            row = rs.fetchall
            ctrl.Zap()
            if empty == True: ctrl.Append('','')    
            for row in rs:
                ctrl.Append(row.pdc, row.codice)
            kwargs = {'lkp_codice' : True} 
            ctrl.owner.appendlkp(g.menu.PDC, 'idcontod', **kwargs)

def fill_idcontoa(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    tipocontoa = kwargs.get('tipocontoa', None)  
    meta = MetaData()
    meta.bind = g.engine  
    if not tipocontoa == None:
        ctrl.Zap()
        if tipocontoa == 'C':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.iscliente==1)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.CLIENTE, 'idcontoa')
        elif tipocontoa == 'F':
            t = Table('anag', meta, autoload=True)
            s = select([t.c.anag, t.c.id])
            s = s.where(t.c.isfornitore==True)
            s = s.where(t.c.iseliminato==None)
            rs = s.execute()
            row = rs.fetchall        
            if empty == True: ctrl.Append('','')        
            for row in rs:
                ctrl.Append(row.anag, row.id)
            ctrl.owner.appendlkp(g.menu.FORNITORE, 'idcontoa')
        elif tipocontoa == 'P':
            t = Table('pdc', meta, autoload=True)
            s = t.select()
            s = s.where(t.c.isultimo==True)
            s = s.where(t.c.iseliminato==None)
            s = s.order_by(t.c.id)
            rs = s.execute()
            row = rs.fetchall
            ctrl.Zap()
            if empty == True: ctrl.Append('','')    
            for row in rs:
                ctrl.Append(row.pdc, row.codice)
            kwargs = {'lkp_codice' : True} 
            ctrl.owner.appendlkp(g.menu.PDC, 'idcontoa', **kwargs)
            
def fill_uteazi():
    azi = {}
    meta = MetaData()
    meta.bind = g.engine
    t = Table('azienda', meta, autoload=True)
    s = t.select().where(t.c.iseliminato == None) 
    uteazi = Table('uteazi', meta, autoload=True)
    if g.idutente == g.USR_ADMINISTRATOR:
        s = select([t.c.id , t.c.azienda])
        s = s.where(t.c.iseliminato == None)
        s = s.order_by(t.c.azienda)
    else:
        s = select([t.c.id , t.c.azienda])
        s = s.select_from(uteazi.join(t, uteazi.c.idazienda == t.c.id))
        s = s.where(uteazi.c.idutente == g.idutente)
        s = s.where(t.c.iseliminato == None)
        s = s.order_by(t.c.azienda)
               
    rs = s.execute()
    row = rs.fetchall
    for row in rs:
        azi[row.id]=row.azienda
    return azi
              
def fill_idtipocausto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipocausto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipocausto,row.id)

def fill_idtipogiorno(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipogiorno', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipogiorno,row.id)

    
def fill_idpadre(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('pdc', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.pdc,row.id)


def fill_idtipodataciclo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipodataciclo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipodataciclo,row.id)

        
def fill_idclienti(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.iscliente==True)
    s = s.where(t.c.ischiuso==None)
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)
        
def fill_idfornitori(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.isfornitore==True)
    s = s.where(t.c.ischiuso==None)
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)

def fill_idciclo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('ciclo', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.ciclo,row.id)
               
def fill_idtipodoc(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipodoc', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipodoc,row.id)
        
def fill_idtipomov(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    empty = True
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipomov', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipomov,row.id)
        
def fill_idmacchina(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('macchina', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.macchina,row.id)
        
def fill_idazienda(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('azienda', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.azienda,row.id)

def fill_idtipooralavo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipooralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipooralavo,row.id)    
        
def fill_idtiposesso(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiposesso', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tiposesso,row.id)
        
def fill_idtipoposlav(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoposlav', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoposlav,row.id)
        
def fill_idcittadinanza(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('cittadinanza', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.cittadinanza,row.id)
        
def fill_idprovincianascita(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('provincia', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.provincia)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.provincia,row.id)
        
def fill_idnazionenascita(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('nazione', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.nazione,row.id)
        
def fill_idspesa(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('spesa', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.spesa,row.id)

def fill_idcausca(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.idtipodoc=="SCA")
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causale,row.id)
        

        
def fill_idvocemag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('vocemag', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.vocemag,row.id)
        
def fill_idbancacc(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('bancacc', meta, autoload=True)
    s = t.select()
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.bancacc, row.id)
        
def fill_idtipospesa(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipospesa', meta, autoload=True)
    s = t.select()
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipospesa, row.id)
        
def fill_idcaumag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('caumag', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.caumag,row.id)
        
def fill_idcaumagcoll(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.idtipodoc=='MAG')
    s = s.where(t.c.idtipomov=='MAG')
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causale,row.id)
        
def fill_idcaupnota(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.idtipomov=='PNO')
    s = s.where(t.c.idtipodoc=='CON')
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causale,row.id)
        
def fill_idmagazzino(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('magazzino', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.magazzino,row.id)
        
def fill_idmagazzinocoll(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('magazzino', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.magazzino,row.id)
        
        
def fill_idfase(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('fase', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.fase,row.id)
        
def fill_idstato(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('stato', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.stato,row.id)
        
def fill_idstatoprecedente(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('stato', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.stato,row.id)
        
def fill_idstatoparziale(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('stato', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.stato,row.id)
        
def fill_idmatri(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('matri', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.matri,row.id)
        
def fill_idartclasse(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('artclasse', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.artclasse,row.id)
        
def fill_idartdia(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('artdia', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.artdia,row.id)
        
def fill_idarttipo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('arttipo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.arttipo,row.id)
        
def fill_idoralavo1(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo2(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo3(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo4(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo5(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo6(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo7(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo8(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo9(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idoralavo10(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('oralavo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.oralavo,row.id)
        
def fill_idmateriale(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('materiale', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.materiale,row.id)
        
def fill_idanagsede(ctrl, **kwargs):
    idanag =  kwargs.get('idanag', None)
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anagsede', meta, autoload=True)
    s = t.select().where(t.c.idanag==idanag)
    s = s.where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anagsede, row.id)
        
        
def fill_idcausalefattura(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.idtipocausale=="FAT")
    s = s.order_by(t.c.causale)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causale, row.id)        
        
def fill_idcausaletrasporto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causaletrasporto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causaletrasporto,row.id)
        
def fill_idddt(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    idanag = kwargs.get('idanag', None)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('ddt', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    if idanag!=None:
        s = s.where(t.c.idanag==idanag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.numero,row.id)
        
def fill_idtrasportocura(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('trasportocura', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.trasportocura,row.id)
        
def fill_idaspettobene(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('aspettobene', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.aspettobene,row.id)
        
def fill_idporto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('porto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.porto,row.id)
                
def fill_idcolata(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('colata', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.colata,row.id)
        
        
def fill_idacciaieria(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('acciaieria', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.acciaieria,row.id)
        
def fill_idnormat(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('normat', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.normat,row.id)

def fill_idvisdim(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('visdim', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.visdim,row.id)
        
def fill_idtrater(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('trater', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.trater,row.id)
        
def fill_idforno(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('forno', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.forno,row.id)
        
def fill_idofferta(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('offerta', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.numero,row.id)
        
def fill_idoffdet(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('offdet', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.idarticolo,row.id)
        
def fill_idpagamento(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('modopag', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.modopag,row.id)
        
def fill_idimballaggio(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('imballaggio', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.imballaggio,row.id)

def fill_idcausto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causto', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.causto,row.id)
        
def fill_idresamerce(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('resamerce', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.resamerce,row.id)
            
def fill_idmodopag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('modopag', meta, autoload=True)
    s = t.select().order_by(t.c.modopag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.modopag,row.id)
        
def fill_idarticolo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('articolo', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.articolo)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.articolo,row.id)
        
def fill_idagente(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('agente', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.agente)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.agente, row.id)
        
def fill_idsettore(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('settore', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.settore)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.settore, row.id)
       

def fill_idpostpag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('postpag', meta, autoload=True)
    s = t.select().order_by(t.c.postpag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.postpag,row.id)
  
def fill_idprovincia(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('provincia', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.provincia,row.id)
        

def fill_idiva(ctrl,  **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('iva', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.iva,row.id)
       
def fill_idtiposede(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiposede', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.tiposede)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tiposede,row.id)
        
def fill_idvalidita(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('validita', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.validita)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.validita,row.id)

def fill_idtipoiva(ctrl,  **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoiva', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoiva,row.id)
        
def fill_idtipoart(ctrl,  **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoart', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoart,row.id)

def fill_idabi(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('abi', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.abi,row.id)
           
def fill_idtiposcadenza(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiposcadenza', meta, autoload=True)
    s = t.select().order_by(t.c.tiposcadenza)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tiposcadenza,row.id)
        
def fill_idanag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)   
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = select([t.c.id, t.c.anag])
    s = s.order_by(t.c.anag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True:
        ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag, row.id)
    
                         
def fill_idcliente(ctrl, **kwargs):
    empty = kwargs.get('empty', False)   
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.iscliente==True)
    s = s.where(t.c.ischiuso==None)
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.anag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)
        
def fill_idfornitore(ctrl, **kwargs):
    empty = kwargs.get('empty', False)   
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select()
    s = s.where(t.c.iscliente==True)
    s = s.where(t.c.ischiuso==None)
    s = s.where(t.c.iseliminato==None)
    s = s.order_by(t.c.anag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)
        
def fill_idvettore(ctrl, **kwargs):
    empty = kwargs.get('empty', False)   
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.anag)
    s = s.where(t.c.isvettore==True)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)
        
def fill_idvettore2(ctrl, **kwargs):
    empty = kwargs.get('empty', False)   
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.anag)
    s = s.where(t.c.isvettore==True)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)

def fill_idtipoimporto(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipoimporto', meta, autoload=True)
    s = t.select().order_by(t.c.tipoimporto)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipoimporto,row.id)

def fill_idtipopag(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipopag', meta, autoload=True)
    s = t.select().order_by(t.c.tipopag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipopag,row.id)
       
def fill_idprotocollo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('protocollo', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.protocollo,row.id)
        
def fill_idnumerazione(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('numerazione', meta, autoload=True)
    s = t.select().order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.numerazione,row.id)
                
            
def fill_idcommessa(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    open = kwargs.get('open', None)
    idanag = kwargs.get('idanag', None)    
    meta = MetaData()
    meta.bind = g.engine
    ANA = Table('anag', meta, autoload=True)
    STATO = Table('stato', meta, autoload=True)
    t = Table('commessa', meta, autoload=True)
    s = t.select()
    if idanag!=None:
        S = select([ANA.c.iscliente])
        S = S.where(ANA.c.id==idanag)
        row = S.execute().fetchone()
        if row!=None:
            if row.iscliente==True:
                s = s.where(t.c.idanag==idanag)
    s = s.order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        if open:
            s = select([STATO.c.isfinale])
            s = s.where(STATO.c.id==row.idstato)
            s = s.where(STATO.c.iseliminato==None)
            r = s.execute().fetchone()
            if r!=None:
                if not r.isfinale:
                    ctrl.Append(F.sql2str(row.numero)+' - '+F.sql2str(row.commessa), row.id)        
        else:
            ctrl.Append(F.sql2str(row.numero)+' - '+F.sql2str(row.commessa), row.id)
            
            
def fill_idcomdet(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    commessa = kwargs.get('commessa', None)  
    open = kwargs.get('open', None)
    if not commessa == None:
        ctrl.filtro =  kwargs.get('filtro', {})
        ctrl.pkfrom = kwargs.get('pkfrom', {}) 
        meta = MetaData()
        meta.bind = g.engine
        t = Table('comdet', meta, autoload=True)
        STATO = Table('stato', meta, autoload=True)
        s = t.select().where(t.c.iseliminato==None)
        s = s.where(t.c.idcommessa==commessa)
        s = s.order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        ctrl.Zap()        
        if empty == True: ctrl.Append('','')        
        for row in rs:
            if open:
                s = select([STATO.c.isfinale])
                s = s.where(STATO.c.id==row.idstato)
                s = s.where(STATO.c.iseliminato==None)
                r = s.execute().fetchone()
                if r!=None:
                    if not r.isfinale:
                        ctrl.Append(F.sql2str(row.descri), row.id)   
            else:
                ctrl.Append(F.sql2str(row.descri), row.id)
            
            
def fill_idcomfase(ctrl, **kwargs):
    meta = MetaData()
    meta.bind = g.engine
    open = kwargs.get('open', None)
    t = Table('comfase', meta, autoload=True)
    STATO = Table("stato", meta, autoload=True)
    FASE = Table('fase', meta, autoload=True)
    empty = kwargs.get('empty', False)    
    commessa = kwargs.get('commessa', None)  
    comdet = kwargs.get('comdet', None) 
    if not commessa==None and not comdet==None:
        ctrl.filtro =  kwargs.get('filtro', {})
        ctrl.pkfrom = kwargs.get('pkfrom', {}) 
        s = select([t.c.id, FASE.c.fase, t.c.idstato])
        s = s.where(FASE.c.id==t.c.idfase)
        s = s.where(t.c.idcommessa==commessa)
        s = s.where(t.c.idcomdet==comdet)
        s = s.where(and_(t.c.flag==True, t.c.iseliminato==None))
        s = s.order_by(t.c.id)
        rs = s.execute()
        row = rs.fetchall
        ctrl.Zap()        
        if empty == True: ctrl.Append('','')        
        for row in rs:
            if open:
                s = select([STATO.c.isfinale])
                s = s.where(STATO.c.id==row.idstato)
                s = s.where(STATO.c.iseliminato==None)
                r = s.execute().fetchone()
                if r!=None:
                    if not r.isfinale:
                        ctrl.Append(F.sql2str(row.fase), row.id)      
            else:
                ctrl.Append(F.sql2str(row.fase), row.id)
            
def fill_idcausale(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    idtipocausale = kwargs.get('idtipocausale', None)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('causale', meta, autoload=True) 
    s = t.select()
    if idtipocausale!=None:
        s = s.where(t.c.idtipocausale==idtipocausale)
    s = s.order_by(t.c.causale)        
    rs = s.execute()
    ctrl.Zap()        
    if empty == True: ctrl.Append('','')        
    for row in rs:
        ctrl.Append(row.causale, row.id)
        
def fill_idtipointento(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tipointento', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tipointento,row.id)

def fill_idtiponum(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tiponum', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.tiponum,row.id)
        
def fill_idunimis(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('unimis', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.unimis,row.id)
        
def fill_idcatart(ctrl, **kwargs):
    empty = kwargs.get('empty', False)    
    meta = MetaData()
    meta.bind = g.engine
    t = Table('catart', meta, autoload=True)
    s = t.select().where(t.c.iseliminato==None).order_by(t.c.id)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()    
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.catart,row.id)

def protocollo(idcausale, datadoc, tabella):
    meta = MetaData()
    meta.bind = g.engine
    t = Table(tabella, meta, autoload=True)
    CAU = Table('causale', meta, autoload=True)
    datainizio = "%s0101"%datadoc[:4]
    datafine = "%s1231"%datadoc[:4]
    codecausale = getCodeCausale(idcausale)
    s = select([CAU.c.idtipocausale])
    s = s.where(CAU.c.id==idcausale)
    row = s.execute().fetchone()
    idtipocausale = row.idtipocausale
    s = select([func.max(t.c.protocollo).label('protocollo')])
    if idtipocausale!="FAT":
        s = s.where(t.c.idcausale==idcausale)
    s = s.where(t.c.data>=datainizio)
    s = s.where(t.c.data<=datafine)
    row = s.execute().fetchone()
    if row.protocollo==None:
        protocollo = 0
    else:
        protocollo = row.protocollo
    protocollo+=1    
    return_dict = dict(protocollo="%s"%protocollo)
    if codecausale!=None:
        return_dict['numero'] = "%s  %s/%s"%(codecausale, protocollo, datadoc[:4])
    else:
        return_dict['numero'] = "%s/%s"%(protocollo, datadoc[:4])
    return return_dict

def getCodeCausale(idcausale):
    meta = MetaData()
    meta.bind = g.engine
    CAU = Table('causale', meta, autoload=True)
    s = select([CAU.c.codice])
    s = s.where(CAU.c.id==idcausale)
    row = s.execute().fetchone()
    if row!=None:
        return row.codice
    return None
  
def check_field(v, l):
    if v==None:
        v = ' '
    if l==None:
        return v
    else:
        if len(v)>l:
            return v[:l]
        elif len(v)<l:
            return v+(' '*(l-len(v)))
        elif len(v)==l:
            return v

def get_allids(nometab):
    meta = MetaData()
    meta.bind = g.engine
    try:
        t = Table(nometab, meta, autoload=True)
        s = select([t.c.id]).where(t.c.iseliminato == None)
        rs = s.execute()
    except: 
        return None
    return [row.id for row in rs]  
        





def fill_idcommittente(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('anag', meta, autoload=True)
    s = t.select().order_by(t.c.anag)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.anag,row.id)


def fill_idautista1(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('autista', meta, autoload=True)
    s = t.select().order_by(t.c.autista)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.autista,row.id)
        
def fill_idautista2(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('autista', meta, autoload=True)
    s = t.select().order_by(t.c.autista)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.autista,row.id)
        
def fill_idveicolo(ctrl, **kwargs):
    empty = kwargs.get('empty', False)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('veicolo', meta, autoload=True)
    s = t.select().order_by(t.c.veicolo)
    rs = s.execute()
    row = rs.fetchall
    ctrl.Zap()
    if empty == True: ctrl.Append('','')    
    for row in rs:
        ctrl.Append(row.veicolo, row.id)
