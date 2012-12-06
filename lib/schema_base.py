# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from sqlalchemy import *
import lib_db as db
import lib_global as g

#-----------------------------------------------------------------------------------------------
class sql_versione(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'versione')
        self.versione = 1

    def create_table(self):
        tb = Table("versione", self.meta,
            Column("id", Integer, Sequence("sq_versione", optional=True), primary_key=True),
            Column("versione", Integer, nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)
        self.open()
        if self.versione == 1:
            i = tb.insert()
            i.execute(versione=1)
        else:
            u = tb.update()
            u.execute(versione=self.versione)
            
#-----------------------------------------------------------------------------------------------            
class sql_utente(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'utente')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("utente", self.meta,
            Column("id", Unicode(10), nullable=False, primary_key=True),
            Column("utente", Unicode(200), nullable=True),
            Column("codice", Unicode(20), nullable=True),
            Column("password", Unicode(100), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute({ "id": "0000",
                                   "utente": u"Administrator",
                                   "codice": u"Administrator",
                                   "password" : u"",
                                   "descrizione": _("Amministratore del programma")})
            self.close()
        except Exception, e:
            print e

#-----------------------------------------------------------------------------------------------
class sql_nazione(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'nazione')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("nazione", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key=True),
        Column("nazione", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                {"id": "AD", "nazione": "Andorra"},
                {"id": "AE", "nazione": "Emirati Arabi Uniti"},
                {"id": "AF", "nazione": "Afghanistan"},
                {"id": "AG", "nazione": "Antigua e Barbuda"},
                {"id": "AI", "nazione": "Anguilla"},
                {"id": "AL", "nazione": "Albania"},
                {"id": "AM", "nazione": "Armenia"},
                {"id": "AN", "nazione": "Antille Olandesi"},
                {"id": "AO", "nazione": "Angol"},
                {"id": "AQ", "nazione": "Antartide"},
                {"id": "AR", "nazione": "Argentina"},
                {"id": "AS", "nazione": "Samoa Americane"},
                {"id": "AT", "nazione": "Austria"},
                {"id": "AU", "nazione": "Australia"},
                {"id": "AW", "nazione": "Aruba"},
                {"id": "AX", "nazione": "Isole Aland"},
                {"id": "AZ", "nazione": "Azerbaigian"},
                {"id": "BA", "nazione": "Bosnia-Erzegovina"},
                {"id": "BB", "nazione": "Barbados"},
                {"id": "BD", "nazione": "Bangladesh"},
                {"id": "BE", "nazione": "Belgio"},
                {"id": "BF", "nazione": "Burkina Faso"},
                {"id": "BG", "nazione": "Bulgaria"},
                {"id": "BH", "nazione": "Bahrain"},
                {"id": "BI", "nazione": "Burundi"},
                {"id": "BJ", "nazione": "Beninv"},
                {"id": "BL", "nazione": "Saint-Barthelemy"},
                {"id": "BM", "nazione": "Bermuda"},
                {"id": "BN", "nazione": "Brunei"},
                {"id": "BO", "nazione": "Bolivia"},
                {"id": "BR", "nazione": "Brasile"},
                {"id": "BS", "nazione": "Bahamas"},
                {"id": "BT", "nazione": "Bhutan"},
                {"id": "BV", "nazione": "Isola Bouvet"},
                {"id": "BW", "nazione": "Botswana"},
                {"id": "BY", "nazione": "Bielorussia"},
                {"id": "BZ", "nazione": "Belize"},
                {"id": "CA", "nazione": "Canada"},
                {"id": "CC", "nazione": "Isole Cocos"},
                {"id": "CD", "nazione": "Repubblica Democratica del Congo ex Zaire"},
                {"id": "CF", "nazione": "Repubblica Centrafricana"},
                {"id": "CG", "nazione": "Repubblica del Congo"},
                {"id": "CH", "nazione": "Svizzera"},
                {"id": "CI", "nazione": "Costa d'Avorio"},
                {"id": "CK", "nazione": "Isole Cook"},
                {"id": "CL", "nazione": "Cile"},
                {"id": "CM", "nazione": "Camerun"},
                {"id": "CN", "nazione": "Cina Repubblica Popolare Cinese"},
                {"id": "CO", "nazione": "Colombia"},
                {"id": "CR", "nazione": "Costa Rica"},
                {"id": "CU", "nazione": "Cuba"},
                {"id": "CV", "nazione": "Capo Verde"},
                {"id": "CX", "nazione": "Isola Christmas"},
                {"id": "CY", "nazione": "Cipro"},
                {"id": "CZ", "nazione": "Repubblica Ceca"},
                {"id": "DE", "nazione": "Germania"},
                {"id": "DJ", "nazione": "Gibuti"},
                {"id": "DK", "nazione": "Danimarca"},
                {"id": "DM", "nazione": "Dominica"},
                {"id": "DO", "nazione": "Repubblica Dominicana"},
                {"id": "DZ", "nazione": "Algeria"},
                {"id": "EC", "nazione": "Ecuador"},
                {"id": "EE", "nazione": "Estonia"},
                {"id": "EG", "nazione": "Egitto"},
                {"id": "EH", "nazione": "Sahara Occidentale ex Sahara Spagnolo"},
                {"id": "ER", "nazione": "Eritrea"},
                {"id": "ES", "nazione": "Spagna"},
                {"id": "ET", "nazione": "Etiopia"},
                {"id": "FI", "nazione": "Finlandia"},
                {"id": "FJ", "nazione": "Figi"},
                {"id": "FK", "nazione": "Isole Falkland"},
                {"id": "FM", "nazione": "Stati Federati di Micronesia"},
                {"id": "FO", "nazione": "Isole Far Oer"},
                {"id": "FR", "nazione": "Francia"},
                {"id": "GA", "nazione": "Gabon"},
                {"id": "GB", "nazione": "Regno Unito"},
                {"id": "GD", "nazione": "Grenada"},
                {"id": "GE", "nazione": "Georgia"},
                {"id": "GF", "nazione": "Guyana Francese"},
                {"id": "GG", "nazione": "Guernsey"},
                {"id": "GH", "nazione": "Ghana"},
                {"id": "GI", "nazione": "Gibilterra"},
                {"id": "GL", "nazione": "Groenlandia"},
                {"id": "GM", "nazione": "Gambia"},
                {"id": "GN", "nazione": "Guinea"},
                {"id": "GP", "nazione": "Guadalupa"},
                {"id": "GQ", "nazione": "Guinea Equatoriale"},
                {"id": "GR", "nazione": "Grecia"},
                {"id": "GS", "nazione": "Georgia del Sud e isole Sandwich meridionali"},
                {"id": "GT", "nazione": "Guatemala"},
                {"id": "GU", "nazione": "Guam"},
                {"id": "GW", "nazione": "Guinea-Bissau"},
                {"id": "GY", "nazione": "Guyana"},
                {"id": "HK", "nazione": "Hong Kong"},
                {"id": "HM", "nazione": "Isole Heard e McDonald"},
                {"id": "HN", "nazione": "Honduras"},
                {"id": "HR", "nazione": "Croazia"},
                {"id": "HT", "nazione": "Haiti"},
                {"id": "HU", "nazione": "Ungheria"},
                {"id": "ID", "nazione": "Indonesia"},
                {"id": "IE", "nazione": "Irlanda"},
                {"id": "IL", "nazione": "Israele"},
                {"id": "IM", "nazione": "Isola di Man"},
                {"id": "IN", "nazione": "India"},
                {"id": "IO", "nazione": "Territori Britannici dell'Oceano Indiano comprende Diego Garcia"},
                {"id": "IQ", "nazione": "Iraq"},
                {"id": "IR", "nazione": "Iran"},
                {"id": "IS", "nazione": "Islanda"},
                {"id": "IT", "nazione": "Italia"},
                {"id": "JE", "nazione": "Jersey"},
                {"id": "JM", "nazione": "Giamaica"},
                {"id": "JO", "nazione": "Giordania"},
                {"id": "JP", "nazione": "Giappone"},
                {"id": "KE", "nazione": "Kenya"},
                {"id": "KG", "nazione": "Kirghizistan"},
                {"id": "KH", "nazione": "Cambogia"},
                {"id": "KI", "nazione": "Kiribati"},
                {"id": "KM", "nazione": "Comore"},
                {"id": "KN", "nazione": "Saint Kitts e Nevis"},
                {"id": "KP", "nazione": "Corea del Nord"},
                {"id": "KR", "nazione": "Corea del Sud"},
                {"id": "KW", "nazione": "Kuwait"},
                {"id": "KY", "nazione": "Isole Cayman"},
                {"id": "KZ", "nazione": "Kazakistan"},
                {"id": "LA", "nazione": "Laos"},
                {"id": "LB", "nazione": "Libano"},
                {"id": "LC", "nazione": "Santa Lucia"},
                {"id": "LI", "nazione": "Liechtenstein"},
                {"id": "LK", "nazione": "Sri Lanka"},
                {"id": "LR", "nazione": "Liberia"},
                {"id": "LS", "nazione": "Lesotho"},
                {"id": "LT", "nazione": "Lituania"},
                {"id": "LU", "nazione": "Lussemburgo"},
                {"id": "LV", "nazione": "Lettonia"},
                {"id": "LY", "nazione": "Libia"},
                {"id": "MA", "nazione": "Marocco"},
                {"id": "MC", "nazione": "Monaco"},
                {"id": "MD", "nazione": "Moldavia"},
                {"id": "ME", "nazione": "Montenegro"},
                {"id": "MF", "nazione": "Saint-Martin"},
                {"id": "MG", "nazione": "Madagascar"},
                {"id": "MH", "nazione": "Isole Marshall"},
                {"id": "MK", "nazione": "Macedonia"},
                {"id": "ML", "nazione": "Mali"},
                {"id": "MM", "nazione": "Birmania Myanmar"},
                {"id": "MN", "nazione": "Mongolia"},
                {"id": "MO", "nazione": "Macao"},
                {"id": "MP", "nazione": "Isole Marianne Settentrionali"},
                {"id": "MQ", "nazione": "Martinica"},
                {"id": "MR", "nazione": "Mauritania"},
                {"id": "MS", "nazione": "Montserrat"},
                {"id": "MT", "nazione": "Malta"},
                {"id": "MU", "nazione": "Mauritius"},
                {"id": "MV", "nazione": "Maldive"},
                {"id": "MW", "nazione": "Malawi"},
                {"id": "MX", "nazione": "Messico"},
                {"id": "MY", "nazione": "Malesia"},
                {"id": "MZ", "nazione": "Mozambico"},
                {"id": "NA", "nazione": "Namibia"},
                {"id": "NC", "nazione": "Nuova Caledonia"},
                {"id": "NE", "nazione": "Niger"},
                {"id": "NF", "nazione": "Isola Norfolk"},
                {"id": "NG", "nazione": "Nigeria"},
                {"id": "NI", "nazione": "Nicaragua"},
                {"id": "NL", "nazione": "Olanda Paesi Bassi"},
                {"id": "NO", "nazione": "Norvegia"},
                {"id": "NP", "nazione": "Nepal"},
                {"id": "NR", "nazione": "Nauru"},
                {"id": "NU", "nazione": "Niue"},
                {"id": "NZ", "nazione": "Nuova Zelanda"},
                {"id": "OM", "nazione": "Oman"},
                {"id": "PA", "nazione": "Panama"},
                {"id": "PE", "nazione": "Peru"},
                {"id": "PF", "nazione": "Polinesia Francese comprende l'Isola Clipperton"},
                {"id": "PG", "nazione": "Papua Nuova Guinea"},
                {"id": "PH", "nazione": "Filippine"},
                {"id": "PK", "nazione": "Pakistan"},
                {"id": "PL", "nazione": "Polonia"},
                {"id": "PM", "nazione": "Saint Pierre e Miquelon"},
                {"id": "PN", "nazione": "Isole Pitcairn"},
                {"id": "PR", "nazione": "Porto Rico"},
                {"id": "PS", "nazione": "Territori Palestinesi Occupati ovvero, Cisgiordania e Striscia di Gaza"},
                {"id": "PT", "nazione": "Portogallo"},
                {"id": "PW", "nazione": "Palau"},
                {"id": "PY", "nazione": "Paraguay"},
                {"id": "QA", "nazione": "Qatar"},
                {"id": "RE", "nazione": "Reunion"},
                {"id": "RO", "nazione": "Romania"},
                {"id": "RU", "nazione": "Russia"},
                {"id": "RS", "nazione": "Serbia"},
                {"id": "RW", "nazione": "Ruanda"},
                {"id": "SA", "nazione": "Arabia Saudita"},
                {"id": "SB", "nazione": "Isole Salomone"},
                {"id": "SC", "nazione": "Seychelles"},
                {"id": "SD", "nazione": "Sudan"},
                {"id": "SE", "nazione": "Svezia"},
                {"id": "SG", "nazione": "Singapore"},
                {"id": "SH", "nazione": "Sant'Elena"},
                {"id": "SI", "nazione": "Slovenia"},
                {"id": "SJ", "nazione": "Svalbard e Jan Mayen"},
                {"id": "SK", "nazione": "Slovacchia"},
                {"id": "SL", "nazione": "Sierra Leone"},
                {"id": "SM", "nazione": "San Marino"},
                {"id": "SN", "nazione": "Senegal"},
                {"id": "SO", "nazione": "Somalia"},
                {"id": "SR", "nazione": "Suriname"},
                {"id": "ST", "nazione": "Sao Tome"},
                {"id": "SV", "nazione": "El Salvador"},
                {"id": "SY", "nazione": "Siria"},
                {"id": "SZ", "nazione": "Swaziland"},
                {"id": "TC", "nazione": "Isole Turks e Caicos"},
                {"id": "TD", "nazione": "Ciad"},
                {"id": "TF", "nazione": "Territori Francesi del Sud"},
                {"id": "TG", "nazione": "Togo"},
                {"id": "TH", "nazione": "Thailandia"},
                {"id": "TJ", "nazione": "Tagikistan"},
                {"id": "TK", "nazione": "Tokelau"},
                {"id": "TL", "nazione": "Timor Est"},
                {"id": "TM", "nazione": "Turkmenistan"},
                {"id": "TN", "nazione": "Tunisia"},
                {"id": "TO", "nazione": "Tonga"},
                {"id": "TR", "nazione": "Turchia"},
                {"id": "TT", "nazione": "Trinidad e Tobago"},
                {"id": "TV", "nazione": "Tuvalu"},
                {"id": "TW", "nazione": "Repubblica di Cina Taiwan"},
                {"id": "TZ", "nazione": "Tanzania"},
                {"id": "UA", "nazione": "Ucraina"},
                {"id": "UG", "nazione": "Uganda"},
                {"id": "UM", "nazione": "Isole minori esterne degli Stati Uniti"},
                {"id": "US", "nazione": "Stati Uniti d'America"},
                {"id": "UY", "nazione": "Uruguay"},
                {"id": "UZ", "nazione": "Uzbekistan"},
                {"id": "VA", "nazione": "Citta del Vaticano"},
                {"id": "VC", "nazione": "Saint Vincent e Grenadine"},
                {"id": "VE", "nazione": "Venezuela"},
                {"id": "VG", "nazione": "Isole Vergini Britanniche"},
                {"id": "VI", "nazione": "Isole Vergini Americane"},
                {"id": "VN", "nazione": "Vietnam"},
                {"id": "VU", "nazione": "Vanuatu"},
                {"id": "WF", "nazione": "Wallis e Futuna"},
                {"id": "WS", "nazione": "Samoa ex Samoa Occidentali"},
                {"id": "YE", "nazione": "Yemen"},
                {"id": "YT", "nazione": "Mayotte"},
                {"id": "ZA", "nazione": "Sudafrica"},
                {"id": "ZM", "nazione": "Zambia"},
                {"id": "ZW", "nazione": "Zimbabwe"})
            self.close()
        except: pass
#-----------------------------------------------------------------------------------------------
class sql_provincia(db.TabSchema):
    def __init__(self):
        db.TabSchema.__init__(self, 'provincia')
        self.versione = 1
        self.aggversione = 1

    def create_table(self):
        tb = Table("provincia", self.meta,
        Column("id", Unicode(10), nullable=False, primary_key=True),
        Column("provincia", Unicode(200), nullable=True))
        tb.drop(checkfirst=True)
        tb.create(checkfirst=False)

    def aggiorna(self):
        try:
            self.open()
            if self.aggversione == 1:
                i = self.table.insert()
                i.execute(
                      {"id": "AG", "provincia": "Agrigento"},
                      {"id": "AL", "provincia": "Alessandria"},
                      {"id": "AN", "provincia": "Ancona"},
                      {"id": "AO", "provincia": "Aosta"},
                      {"id": "AP", "provincia": "Ascoli Piceno"},
                      {"id": "AQ", "provincia": "L'Aquila"},
                      {"id": "AR", "provincia": "Arezzo"},
                      {"id": "AT", "provincia": "Asti"},
                      {"id": "AV", "provincia": "Avellino"},
                      {"id": "BA", "provincia": "Bari"},
                      {"id": "BG", "provincia": "Bergamo"},
                      {"id": "BI", "provincia": "Biella"},
                      {"id": "BL", "provincia": "Belluno"},
                      {"id": "BN", "provincia": "Benevento"},
                      {"id": "BO", "provincia": "Bologna"},
                      {"id": "BR", "provincia": "Brindisi"},
                      {"id": "BS", "provincia": "Brescia"},
                      {"id": "BZ", "provincia": "Bolzano"},
                      {"id": "CA", "provincia": "Cagliari"},
                      {"id": "CB", "provincia": "Campobasso"},
                      {"id": "CE", "provincia": "Caserta"},
                      {"id": "CH", "provincia": "Chieti"},
                      {"id": "CI", "provincia": "Carbonia Iglesias"},
                      {"id": "CL", "provincia": "Caltanissetta"},
                      {"id": "CN", "provincia": "Cuneo"},
                      {"id": "CO", "provincia": "Como"},
                      {"id": "CR", "provincia": "Cremona"},
                      {"id": "CS", "provincia": "Cosenza"},
                      {"id": "CT", "provincia": "Catania"},
                      {"id": "CZ", "provincia": "Catanzaro"},
                      {"id": "EN", "provincia": "Enna"},
                      {"id": "FC", "provincia": "Forli Cesena"},
                      {"id": "FE", "provincia": "Ferrara"},
                      {"id": "FG", "provincia": "Foggia"},
                      {"id": "FI", "provincia": "Firenze"},
                      {"id": "FR", "provincia": "Frosinone"},
                      {"id": "GE", "provincia": "Genova"},
                      {"id": "GO", "provincia": "Gorizia"},
                      {"id": "GR", "provincia": "Grosseto"},
                      {"id": "IM", "provincia": "Imperia"},
                      {"id": "IS", "provincia": "Isernia"},
                      {"id": "KR", "provincia": "Crotone"},
                      {"id": "LC", "provincia": "Lecco"},
                      {"id": "LE", "provincia": "Lecce"},
                      {"id": "LI", "provincia": "Livorno"},
                      {"id": "LO", "provincia": "Lodi"},
                      {"id": "LT", "provincia": "Latina"},
                      {"id": "LU", "provincia": "Lucca"},
                      {"id": "MB", "provincia": "Monza e della Brianza"},
                      {"id": "MC", "provincia": "Macerata"},
                      {"id": "ME", "provincia": "Messina"},
                      {"id": "MI", "provincia": "Milano"},
                      {"id": "MN", "provincia": "Mantova"},
                      {"id": "MO", "provincia": "Modena"},
                      {"id": "MS", "provincia": "Massa Carrara"},
                      {"id": "MT", "provincia": "Matera"},
                      {"id": "NA", "provincia": "Napoli"},
                      {"id": "NO", "provincia": "Novara"},
                      {"id": "NU", "provincia": "Nuoro"},
                      {"id": "OG", "provincia": "Ogliastra"},
                      {"id": "OR", "provincia": "Oristano"},
                      {"id": "OT", "provincia": "Olbia Tempio"},
                      {"id": "PA", "provincia": "Palermo"},
                      {"id": "PC", "provincia": "Piacenza"},
                      {"id": "PD", "provincia": "Padova"},
                      {"id": "PE", "provincia": "Pescara"},
                      {"id": "PG", "provincia": "Perugia"},
                      {"id": "PI", "provincia": "Pisa"},
                      {"id": "PN", "provincia": "Pordenone"},
                      {"id": "PO", "provincia": "Prato"},
                      {"id": "PR", "provincia": "Parma"},
                      {"id": "PT", "provincia": "Pistoia"},
                      {"id": "PU", "provincia": "Pesaro Urbino"},
                      {"id": "PV", "provincia": "Pavia"},
                      {"id": "PZ", "provincia": "Potenza"},
                      {"id": "RA", "provincia": "Ravenna"},
                      {"id": "RC", "provincia": "Reggio Calabria"},
                      {"id": "RE", "provincia": "Reggio Emilia"},
                      {"id": "RG", "provincia": "Ragusa"},
                      {"id": "RI", "provincia": "Rieti"},
                      {"id": "RM", "provincia": "Roma"},
                      {"id": "RN", "provincia": "Rimini"},
                      {"id": "RO", "provincia": "Rovigo"},
                      {"id": "SA", "provincia": "Salerno"},
                      {"id": "SI", "provincia": "Siena"},
                      {"id": "SO", "provincia": "Sondrio"},
                      {"id": "SP", "provincia": "La Spezia"},
                      {"id": "SR", "provincia": "Siracusa"},
                      {"id": "SS", "provincia": "Sassari"},
                      {"id": "SV", "provincia": "Savona"},
                      {"id": "TA", "provincia": "Taranto"},
                      {"id": "TE", "provincia": "Teramo"},
                      {"id": "TN", "provincia": "Trento"},
                      {"id": "TO", "provincia": "Torino"},
                      {"id": "TP", "provincia": "Trapani"},
                      {"id": "TR", "provincia": "Terni"},
                      {"id": "TS", "provincia": "Trieste"},
                      {"id": "TV", "provincia": "Treviso"},
                      {"id": "UD", "provincia": "Udine"},
                      {"id": "VA", "provincia": "Varese"},
                      {"id": "VB", "provincia": "Verbania"},
                      {"id": "VC", "provincia": "Vercelli"},
                      {"id": "VE", "provincia": "Venezia"},
                      {"id": "VI", "provincia": "Vicenza"},
                      {"id": "VR", "provincia": "Verona"},
                      {"id": "VS", "provincia": "Medio Campidano"},
                      {"id": "VT", "provincia": "Viterbo"},
                      {"id": "VV", "provincia": "Vibo Valentia"})
            self.close()
        except: pass
        