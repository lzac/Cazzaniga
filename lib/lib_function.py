# -*- coding: utf-8 -*-

from moduli import *
import lib_global as g
import lib_config as cfg
import lib_file as File
import re
import lib_sql as SQL
import locale


def elimina_posizione(ctrl, descri, table, fields):
    meta = MetaData()
    meta.bind = g.engine     
    t = Table(table, meta, autoload=True)    
    recno = ctrl.GetFocusedItem()         
    d = wx.MessageDialog(None, 'Eliminare '+descri+'?', g.appname ,wx.YES_NO | wx.CANCEL |wx.ICON_QUESTION)
    r = d.ShowModal()  
    if r == wx.ID_YES:             
        s = t.delete()
        for k,v in fields.iteritems():
            s = s.where(t.c['%s' % k]==v)
        s.execute()
        ctrl.pk.remove(ctrl.pk[recno])
        ctrl.DeleteItem(recno)
        return True
    return False

def FormatFloat(v):
    locale.setlocale(locale.LC_ALL, '')
    v = sql2float(v)
    if v!=0:
        return locale.format("%0.2f", v, grouping=True)
    else:
        return ''
    
def Sn2Bool(v):
    if v=='S' or v=='s':
        return True
    else:
        return None

def FormatString(v):
    val = v.replace(".", "").replace(",", ".")
    try:
        return round(float(val), 2)
    except:
        return round(float(0), 2)

def get_anag(IDANAG, DATA):
    meta = MetaData()
    meta.bind = g.engine
    ANA = Table('anag', meta, autoload=True)
    ANAGEDIT = Table("anagedit", meta, autoload=True)
    ANAG = ''
    s = select([ANA.c.anag])
    s = s.where(ANA.c.id==IDANAG)
    s = s.where(ANA.c.iseliminato==None)
    ROW = s.execute().fetchone()
    if ROW!=None:
        ANAG = ROW.anag
        s = select([ANAGEDIT.c.id, ANAGEDIT.c.anagedit, func.max(ANAGEDIT.c.data).label('data')],
                   group_by=[ANAGEDIT.c.id, ANAGEDIT.c.anagedit])
        s = s.where(DATA<ANAGEDIT.c.data)
        s = s.where(ANAGEDIT.c.idanag==IDANAG)
        s = s.where(ANAGEDIT.c.iseliminato==None)
        date = '99999999'
        id = None
        anag = None
        for r in s.execute():
            if r.data<date:
                date = r.data
                id = r.id
                anag = r.anagedit
        if id!=None:
            ANAG = anag
    return ANAG 
        
def last_day_of_month(year, month):
        last_days = [31, 30, 29, 28, 27]
        for i in last_days:
                try:
                        end = datetime.datetime(year, month, i)
                except ValueError:
                        continue
                else:
                        return end.date()
        return None
    
def AddMonths(d,x):
    x = int(x)
    
    newmonth = ((( d.month - 1) + x ) % 12 ) + 1
    newyear  = d.year + ((( d.month - 1) + x ) // 12 ) 
    return datetime.date( newyear, newmonth, d.day)
   
def elimina_file(file):
    if os.path.exists(file):
        os.remove(file)

def get_iva(idanag):      
    meta = MetaData()
    meta.bind = g.engine  
    ANA = Table('anag', meta, autoload=True)
    record = None
    #Iva anagrafica
    s = select([ANA.c.idiva])
    s = s.where(ANA.c.id==idanag)
    row = s.execute().fetchone()
    if row!=None:
        record = row.idiva
    return record

def int2sql(v):
    '''
    trasforma intero in dato sql
    '''
    if v == '' or v == None:
        return None
    return int(v)

def sql2strEditable(v):
    if v == None:
        return u''
    if isinstance(v, int):
        return unicode(v)
    if isinstance(v, float):
        if v == None or v == '':
            return 0
        else:
            return "%.2f" % v
    return unicode(v)

def sql2int(v):
    if v == '':
        return None
    return sql2str(v)

def sql2str(v):
    if v == None or v == 0:
        return u''
    if isinstance(v, int):
        return unicode(v)
    if isinstance(v, float):
        if v == None or v == '':
            return 0
        else:
            return "%.2f" % v
    return unicode(v)

def str2float(v):
    if v == None or v == '':
        return 0
    else:
        return float(v)
    
def date2print(d):
    s = str(d)
    if not d:
        return ''
    y = s[:4]
    m = s[5:7]
    g = s[8:10]
    return g + '/' + m + '/' + y

def sql2float(v):
    if v == None or v == '':
        return 0
    else:
        return v

def sql2sconto(v):
    if v == None or v == '' or v == 0:
        return ''
    else:
        return str(v) + '%'

def sql2bool(v):
    if v == None:
        return False
    return bool(v)

def str2sql(v):
    '''
    Trasforma stringa in valore valore sql
    '''
    if v == '' or v == None:
        return None
    return v

def str2int(v):
    '''
    trasforma stringa in numero intero
    '''
    if v == '' or v == None:
        return 0
    return int(v)

def index(list, value):
    try:
        i = list.index(value)
    except:
        i = -1
    return i

def Str2Bool(v):
    if v=='True':
        return True
    return False

def convert_date(v):
    if v == None:
        return None
    v = str(v)[:8]
    return str(v[6:8]) + "/" + str(v[4:6]) + "/" + str(v[0:4])

def convert_datetime(v):
    if v == None:
        return u''
    else:
        v = str(v)
        year = v[:4]
        month = v[4:6]
        day = v[-2:]
        v = day + '/' + month + '/' + year
        return v

def datectrl2sql(v):
    v = str(v)
    if v == None:
        return u''
    else:
        v = str(v)[:10].replace(u'/', '')
        return unicode(v[4:] + v[2:4] + v[:2])


def strdate2list(v):
    v = str(v)
    if v == None:
        return u''
    #<<<<<<< .mine
    #else: return unicode(v[-2:] + '/' + v[4:6] + '/' + v[0:4])
    #== == == =
    else:
        return [int(v[6:8]), int(v[4:6]) , int(v[0:4])]
    #>>>>>>> .r1051


def datesql2print(v):
    if v == None or v == '':
        return u''
    else:
        v = str(v)
        return unicode(v[-2:] + '/' + v[4:6] + '/' + v[0:4])
    
def timesql2print(v):
    if v == None or v == '':
        return u''
    else:
        v = str(v)
        return unicode(v[:2]+':'+v[-2:])

def date2sql(v):
    if v == None:
        return None
    v = str(v)[0:10]
    return str(str(v[6:10]) + str(v[3:5]) + str(v[0:2]))

def sql2date(v):
    if v == None:
        return datetime.datetime.now()
    return str(wx.DateTimeFromDMY(v.day, v.month - 1, v.year))

def min2cent(min):
    min = int(min)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tabconv', meta, autoload=True)
    s = select([t.c.min, t.c.cent])
    rs = s.execute()
    a = {}
    for row in rs:
        if len(str(row['cent'])) == 1:
            v = '00' + str(row['cent'])
        elif len(str(row['cent'])) == 2:
            v = '0' + str(row['cent'])
        else:
            v = str(row['cent'])
        a[row['min']] = v
    return str(a.get(min))

def oracent2min(ora):
    h = ora[:2]
    c = ora[2:5]
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tabconv', meta, autoload=True)
    s = select([t.c.min, t.c.cent])
    rs = s.execute()
    a = {}
    for row in rs:
        if len(str(row['cent'])) == 1:
            v = '00' + str(row['cent'])
        elif len(str(row['cent'])) == 2:
            v = '0' + str(row['cent'])
        else:
            v = str(row['cent'])
        a[v] = row['min']
    return int(h) * 60 + a.get(str(c))

def oramin2cent(orainminuti):
    resto = orainminuti % 60
    ora = int(orainminuti / 60)
    if len(str(ora)) == 1:
        sora = '0' + str(ora)
    else:
        sora = str(ora)
    meta = MetaData()
    meta.bind = g.engine
    t = Table('tabconv', meta, autoload=True)
    s = select([t.c.min, t.c.cent])
    rs = s.execute()
    a = {}
    for row in rs:
        if len(str(row['cent'])) == 1:
            v = '00' + str(row['cent'])
        elif len(str(row['cent'])) == 2:
            v = '0' + str(row['cent'])
        else:
            v = str(row['cent'])
        a[row['min']] = v
    if a.get(resto) == None:
        a = sora + '.' + '000'
    else:
        a = sora + '.' + str(a.get(resto))
    return a

def cent2min(cent):
    b = 0
    return b

def del_reply(seq):
    keys = {}
    for e in seq:
        keys[e] = 1
    return keys.keys()

def calcola_cin(abi , cab, ccc):
        abi = fill_zero(abi, 5)
        cab = fill_zero(cab, 5)
        ccc = fill_zero(ccc, 12)
        if len(abi) + len(cab) + len(ccc) < 22:
            return ''
        pesi = {"0":(0, 1), "1":(1, 0), "2":(2, 5), "3":(3, 7), "4":(4, 9), "5":(5, 13), "6":(6, 15), \
        "7":(7, 17), "8":(8, 19), "9":(9, 21), "A":(0, 1), "B":(1, 0), "C":(2, 5), "D":(3, 7), \
        "E":(4, 9), "F":(5, 13), "G":(6, 15), "H":(7, 17), "I":(8, 19), "J":(9, 21), "K":(10, 2), \
        "L":(11, 4), "M":(12, 18), "N":(13, 20), "O":(14, 11), "P":(15, 3), "Q":(16, 6), "R":(17, 8), \
        "S":(18, 12), "T":(19, 14), "U":(20, 16), "V":(21, 10), "W":(22, 22), "X":(23, 25), "Y":(24, 24), \
        "Z":(25, 23), "-":(26, 27), ".":(27, 28), " ":(28, 26)}
        bban = abi + cab + ccc
        tot = 0
        for i in range(22):
                tot = tot + pesi[bban[i]][(i + 1) % 2]
        return "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[tot % 26]

def  calcola_iban(naz, cin, abi, cab, ccc):

    abi = fill_zero(abi, 5)
    cab = fill_zero(cab, 5)
    ccc = fill_zero(ccc, 12)
    if len(cin) == 0: cin = '0'
    if len(naz) == 0: naz = 'IT'

    p1 = naz + '00' + cin + abi + cab + ccc
    if len(p1) <> 27:
        return ''

    codice = p1
    codice_girato = codice[4:] + codice[:4]
    codice_numerico = ''
    resto = 0
    i = 0
    
    while i < len(codice_girato):
        carattere = codice_girato[i]
        if str(carattere) == '0':
            codice_numerico = codice_numerico + '0'
        elif str(carattere) == '1':
            codice_numerico = codice_numerico + '1'
        elif str(carattere) == '2':
            codice_numerico = codice_numerico + '2'
        elif str(carattere) == '3':
            codice_numerico = codice_numerico + '3'
        elif str(carattere) == '4':
            codice_numerico = codice_numerico + '4'
        elif str(carattere) == '5':
            codice_numerico = codice_numerico + '5'
        elif str(carattere) == '6':
            codice_numerico = codice_numerico + '6'
        elif str(carattere) == '7':
            codice_numerico = codice_numerico + '7'
        elif str(carattere) == '8':
            codice_numerico = codice_numerico + '8'
        elif str(carattere) == '9':
            codice_numerico = codice_numerico + '9'
        elif str(carattere) == 'A':
            codice_numerico = codice_numerico + '10'
        elif str(carattere) == 'B':
            codice_numerico = codice_numerico + '11'
        elif str(carattere) == 'C':
            codice_numerico = codice_numerico + '12'
        elif str(carattere) == 'D':
            codice_numerico = codice_numerico + '13'
        elif str(carattere) == 'E':
            codice_numerico = codice_numerico + '14'
        elif str(carattere) == 'F':
            codice_numerico = codice_numerico + '15'
        elif str(carattere) == 'G':
            codice_numerico = codice_numerico + '16'
        elif str(carattere) == 'H':
            codice_numerico = codice_numerico + '17'
        elif str(carattere) == 'I':
            codice_numerico = codice_numerico + '18'
        elif str(carattere) == 'J':
            codice_numerico = codice_numerico + '19'
        elif str(carattere) == 'K':
            codice_numerico = codice_numerico + '20'
        elif str(carattere) == 'L':
            codice_numerico = codice_numerico + '21'
        elif str(carattere) == 'M':
            codice_numerico = codice_numerico + '22'
        elif str(carattere) == 'N':
            codice_numerico = codice_numerico + '23'
        elif str(carattere) == 'O':
            codice_numerico = codice_numerico + '24'
        elif str(carattere) == 'P':
            codice_numerico = codice_numerico + '25'
        elif str(carattere) == 'Q':
            codice_numerico = codice_numerico + '26'
        elif str(carattere) == 'R':
            codice_numerico = codice_numerico + '27'
        elif str(carattere) == 'S':
            codice_numerico = codice_numerico + '28'
        elif str(carattere) == 'T':
            codice_numerico = codice_numerico + '29'
        elif str(carattere) == 'U':
            codice_numerico = codice_numerico + '30'
        elif str(carattere) == 'V':
            codice_numerico = codice_numerico + '31'
        elif str(carattere) == 'W':
            codice_numerico = codice_numerico + '32'
        elif str(carattere) == 'X':
            codice_numerico = codice_numerico + '33'
        elif str(carattere) == 'Y':
            codice_numerico = codice_numerico + '34'
        elif str(carattere) == 'Z':
            codice_numerico = codice_numerico + '35'
        i += 1
    resto = int(codice_numerico) % 97
    cod = (98 - resto) % 97
    codice = codice[:2] + str(cod) + codice[4:]
    return codice


def fill_zero(v, n):
    if len(v) == 0:
        v = 0
    else:
        v = int(v)
    return '%0*d' % (n, v)




#--------------------------------------------------------------------------------------------------------------------------------------------
def par_mincen(value=None):
    if not g.app == g.APP_INFOS:
        return

    g.nmincen = []
    g.smincen = []

    if g.mincen == "M":
        for i in range(60):
            g.nmincen.append(i)
            g.smincen.append('%0*d' % (2, i))
    else:
        g.nmincen = [ 0, 2, 3, 5, 7, 8, 10, 12, 14, 15,
                     16, 18, 20, 22, 24, 25, 28, 29, 30, 31,
                     32, 34, 36, 38, 40, 42, 44, 46, 48, 49,
                     50, 52, 53, 55, 57, 58, 60, 62, 63, 65,
                     67, 68, 70, 72, 73, 75, 78, 79, 80, 81,
                     82, 84, 86, 88, 90, 92, 94, 96, 98, 99]
        for i in range(60):
            g.smincen.append('%0*d' % (2, g.nmincen[i]))

def min2str(minuti):
    if minuti == None or int(minuti) == 0:
        return '    '
    hh = '%0*d' % (2, minuti / 60)
    mc = g.smincen[minuti % 60]
    return hh + mc

def min2msk(minuti):
    hhmc = min2str(minuti)
    return hhmc[:2] + "." + hhmc[-2:]

def str2min(hhmc):
    if int(hhmc) == 0:
        return 0
    minuti = int(hhmc[:2]) * 60
    minuti += g.nmincen[int(hhmc[-2:])]
    return minuti

def msk2min(hhmc):
    hhmc = hhmc[:2] + hhmc[-2:]
    return str2min(hhmc)    







































def get_id_stampadet(table):
    meta = MetaData()
    meta.bind = g.engine  
    t = Table(table, meta, autoload=True)
    s = select([func.max(t.c.id)])
    rs = s.execute()
    row = rs.fetchone()
    try:
        i = int(row[0])
    except:
        i = 0
    if i == 0:
        pk = '%0*d' % (10, 1)
    else:
        pk = '%0*d' % (10, i + 1)
    return pk 

def get_pdf_name(idcausale, numero):
    meta = MetaData()
    meta.bind = g.engine
    val = ''
    CAU = Table('causale', meta, autoload=True)
    s = select([CAU.c.idtipodoc, CAU.c.idtipomov])
    s = s.where(and_(CAU.c.id==idcausale,CAU.c.iseliminato==None))
    row = s.execute().fetchone()
    if row!=None:
        d = dict(row)
        for k, v in d.iteritems():
            if v!=None:
                val+=sql2str(v)+'_'          
    val+=sql2str(numero)
    val = val.replace(' ', '')
    val = val.replace('/', '_')
    return val.replace(' ', '')
    

