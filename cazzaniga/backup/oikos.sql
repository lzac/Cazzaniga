-- MySQL dump 10.13  Distrib 5.5.19, for Win32 (x86)
--
-- Host: localhost    Database: oikos
-- ------------------------------------------------------
-- Server version	5.5.19

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `anag`
--

use oikos;

DROP TABLE IF EXISTS `anag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `anag` (
  `id` varchar(10) NOT NULL,
  `anag` varchar(200) DEFAULT NULL,
  `partitaiva` varchar(13) DEFAULT NULL,
  `codicefiscale` varchar(16) DEFAULT NULL,
  `codiceministeriale` varchar(25) DEFAULT NULL,
  `sitoweb` varchar(200) DEFAULT NULL,
  `descrizionebanca` varchar(2000) DEFAULT NULL,
  `contoc` varchar(12) DEFAULT NULL,
  `iban` varchar(27) DEFAULT NULL,
  `idtipoanag` varchar(10) DEFAULT NULL,
  `recapito` varchar(2000) DEFAULT NULL,
  `indirizzo` varchar(200) DEFAULT NULL,
  `cap` varchar(5) DEFAULT NULL,
  `localita` varchar(200) DEFAULT NULL,
  `idprovincia` varchar(10) DEFAULT NULL,
  `idnazione` varchar(10) DEFAULT NULL,
  `telefono` varchar(200) DEFAULT NULL,
  `cellulare` varchar(200) DEFAULT NULL,
  `fax` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `idmodopag` varchar(10) DEFAULT NULL,
  `idpostpag` varchar(10) DEFAULT NULL,
  `idiva` varchar(10) DEFAULT NULL,
  `note` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `anag`
--

LOCK TABLES `anag` WRITE;
/*!40000 ALTER TABLE `anag` DISABLE KEYS */;
INSERT INTO `anag` VALUES ('000001','AAAA',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'Via Cantu 86\n23890 Barzago LC','Via Cantu 86','23890','Barzago','LC','IT',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('000002','CONSORZIO BRIANTEO PER L\'ISTRUZIONE SCUOLA MEDIA SUPERIORE','01385870132','85001680132',NULL,NULL,'Banca popolare di milano - ag Barzago',NULL,'IT77Q0558489260000000000498',NULL,'Via Monte Grappa, 21\n23876 Monticello LC','','','','','IT',NULL,NULL,NULL,NULL,NULL,NULL,'10',NULL);
/*!40000 ALTER TABLE `anag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `autista`
--

DROP TABLE IF EXISTS `autista`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `autista` (
  `id` varchar(10) NOT NULL,
  `autista` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `autista`
--

LOCK TABLES `autista` WRITE;
/*!40000 ALTER TABLE `autista` DISABLE KEYS */;
/*!40000 ALTER TABLE `autista` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bancacc`
--

DROP TABLE IF EXISTS `bancacc`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bancacc` (
  `id` varchar(10) NOT NULL,
  `bancacc` varchar(200) DEFAULT NULL,
  `contoc` varchar(12) DEFAULT NULL,
  `iban` varchar(27) DEFAULT NULL,
  `ispredefinito` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bancacc`
--

LOCK TABLES `bancacc` WRITE;
/*!40000 ALTER TABLE `bancacc` DISABLE KEYS */;
/*!40000 ALTER TABLE `bancacc` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `causale`
--

DROP TABLE IF EXISTS `causale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `causale` (
  `id` varchar(10) NOT NULL,
  `causale` varchar(200) DEFAULT NULL,
  `codice` varchar(1) DEFAULT NULL,
  `idtipocausale` varchar(10) DEFAULT NULL,
  `idcausalefattura` varchar(10) DEFAULT NULL,
  `idtiposcadenzario` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `causale`
--

LOCK TABLES `causale` WRITE;
/*!40000 ALTER TABLE `causale` DISABLE KEYS */;
INSERT INTO `causale` VALUES ('01','FATTURA DI VENDITA','F','FAT',NULL,'INC'),('02','OFFERTA DI VENDITA','O','OFF','01',NULL);
/*!40000 ALTER TABLE `causale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fatdet`
--

DROP TABLE IF EXISTS `fatdet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fatdet` (
  `idfattura` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `idofferta` varchar(10) DEFAULT NULL,
  `idoffdet` varchar(10) DEFAULT NULL,
  `descri` varchar(100) DEFAULT NULL,
  `noteinizio1` varchar(100) DEFAULT NULL,
  `noteinizio2` varchar(100) DEFAULT NULL,
  `noteinizio3` varchar(100) DEFAULT NULL,
  `noteinizio4` varchar(100) DEFAULT NULL,
  `noteinizio5` varchar(100) DEFAULT NULL,
  `noteinizio6` varchar(100) DEFAULT NULL,
  `noteinizio7` varchar(100) DEFAULT NULL,
  `noteinizio8` varchar(100) DEFAULT NULL,
  `noteinizio9` varchar(100) DEFAULT NULL,
  `noteinizio10` varchar(100) DEFAULT NULL,
  `notefine1` varchar(100) DEFAULT NULL,
  `notefine2` varchar(100) DEFAULT NULL,
  `notefine3` varchar(100) DEFAULT NULL,
  `notefine4` varchar(100) DEFAULT NULL,
  `notefine5` varchar(100) DEFAULT NULL,
  `notefine6` varchar(100) DEFAULT NULL,
  `notefine7` varchar(100) DEFAULT NULL,
  `notefine8` varchar(100) DEFAULT NULL,
  `notefine9` varchar(100) DEFAULT NULL,
  `notefine10` varchar(100) DEFAULT NULL,
  `quantita` decimal(10,2) DEFAULT '0.00',
  `prezzo` decimal(10,2) DEFAULT '0.00',
  `scontoperc` decimal(10,2) DEFAULT '0.00',
  `importo` decimal(10,2) DEFAULT '0.00',
  `idiva` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idfattura`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fatdet`
--

LOCK TABLES `fatdet` WRITE;
/*!40000 ALTER TABLE `fatdet` DISABLE KEYS */;
INSERT INTO `fatdet` VALUES ('000001','001','000001','001','dahdadasdas+','dasdas',NULL,NULL,NULL,'dasdas',NULL,NULL,NULL,NULL,NULL,'das',NULL,'das',NULL,NULL,NULL,NULL,NULL,NULL,NULL,2.00,100.00,0.00,200.00,'21'),('000001','002','000001','002','gfdgfd','gfdgfd',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,50.00,10.00,0.00,500.00,'21'),('000002','001','','','GENNAIO - FEBBRAIO 2012',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1.00,10421.50,0.00,10421.50,'10'),('000003','001','','','fsdfdsfds',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1.00,50.00,0.00,50.00,'10');
/*!40000 ALTER TABLE `fatdet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fativa`
--

DROP TABLE IF EXISTS `fativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fativa` (
  `idfattura` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `imponibilefat` decimal(10,2) DEFAULT '0.00',
  `scontoperc` decimal(10,2) DEFAULT '0.00',
  `sconto` decimal(10,2) DEFAULT '0.00',
  `imponibile` decimal(10,2) DEFAULT '0.00',
  `idiva` varchar(10) DEFAULT NULL,
  `imposta` decimal(10,2) DEFAULT '0.00',
  `totale` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`idfattura`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fativa`
--

LOCK TABLES `fativa` WRITE;
/*!40000 ALTER TABLE `fativa` DISABLE KEYS */;
INSERT INTO `fativa` VALUES ('000001','001',700.00,0.00,0.00,700.00,'21',147.00,847.00),('000002','001',10421.50,0.00,0.00,10421.50,'10',1042.15,11463.65),('000003','001',50.00,0.00,0.00,50.00,'10',5.00,55.00);
/*!40000 ALTER TABLE `fativa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fatspesa`
--

DROP TABLE IF EXISTS `fatspesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fatspesa` (
  `idfattura` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `idspesa` varchar(10) DEFAULT NULL,
  `imponibile` decimal(10,2) DEFAULT '0.00',
  `idiva` varchar(10) DEFAULT NULL,
  `imposta` decimal(10,2) DEFAULT '0.00',
  `totale` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`idfattura`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fatspesa`
--

LOCK TABLES `fatspesa` WRITE;
/*!40000 ALTER TABLE `fatspesa` DISABLE KEYS */;
/*!40000 ALTER TABLE `fatspesa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fattura`
--

DROP TABLE IF EXISTS `fattura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fattura` (
  `id` varchar(10) NOT NULL,
  `idcausale` varchar(10) DEFAULT NULL,
  `data` varchar(8) DEFAULT NULL,
  `protocollo` int(11) DEFAULT NULL,
  `numero` varchar(50) DEFAULT NULL,
  `idanag` varchar(10) DEFAULT NULL,
  `idtipoanag` varchar(10) DEFAULT NULL,
  `recapito` text,
  `imponibile` decimal(10,2) DEFAULT '0.00',
  `imposta` decimal(10,2) DEFAULT '0.00',
  `totale` decimal(10,2) DEFAULT '0.00',
  `idmodopag` varchar(10) DEFAULT NULL,
  `idbancacc` varchar(10) DEFAULT NULL,
  `descrizionebanca` varchar(2000) DEFAULT NULL,
  `contoc` varchar(12) DEFAULT NULL,
  `iban` varchar(27) DEFAULT NULL,
  `noteinterne` text,
  `notepiepagina` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fattura`
--

LOCK TABLES `fattura` WRITE;
/*!40000 ALTER TABLE `fattura` DISABLE KEYS */;
INSERT INTO `fattura` VALUES ('000001','01','20120215',1,'F  1/2012','000001','','Via Cantu 86\n23890 Barzago LC',700.00,147.00,847.00,'001',NULL,NULL,NULL,NULL,NULL,NULL),('000002','01','20120319',2,'F  2/2012','000002','','Via Monte Grappa, 21\n23876 Monticello LC',10421.50,1042.15,11463.65,'002',NULL,'Banca popolare di milano - ag Barzago',NULL,'IT77Q0558489260000000000498',NULL,NULL),('000003','01','20120319',3,'F  3/2012','000002','','Via Monte Grappa, 21\n23876 Monticello LC',50.00,5.00,55.00,'002',NULL,'Banca popolare di milano - ag Barzago',NULL,'IT77Q0558489260000000000498',NULL,NULL);
/*!40000 ALTER TABLE `fattura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fogliodiviaggio`
--

DROP TABLE IF EXISTS `fogliodiviaggio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `fogliodiviaggio` (
  `id` varchar(10) NOT NULL,
  `data` varchar(8) DEFAULT NULL,
  `dataritorno` varchar(8) DEFAULT NULL,
  `numero` varchar(10) DEFAULT NULL,
  `idautista1` varchar(10) DEFAULT NULL,
  `autista1` varchar(200) DEFAULT NULL,
  `idautista2` varchar(10) DEFAULT NULL,
  `autista2` varchar(200) DEFAULT NULL,
  `idveicolo` varchar(10) DEFAULT NULL,
  `veicolo` varchar(200) DEFAULT NULL,
  `targa` varchar(200) DEFAULT NULL,
  `idcommittente` varchar(10) DEFAULT NULL,
  `committente` varchar(200) DEFAULT NULL,
  `oraeluogo` varchar(200) DEFAULT NULL,
  `destinazione` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fogliodiviaggio`
--

LOCK TABLES `fogliodiviaggio` WRITE;
/*!40000 ALTER TABLE `fogliodiviaggio` DISABLE KEYS */;
INSERT INTO `fogliodiviaggio` VALUES ('000001','20120215',NULL,'001',NULL,'DURA',NULL,'MURO',NULL,'FIAT IDEA','5214',NULL,'CACCA','das','das');
/*!40000 ALTER TABLE `fogliodiviaggio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `iva`
--

DROP TABLE IF EXISTS `iva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `iva` (
  `id` varchar(10) NOT NULL,
  `iva` varchar(200) DEFAULT NULL,
  `codice` varchar(10) DEFAULT NULL,
  `idtipoiva` varchar(10) DEFAULT NULL,
  `aliquota` int(11) DEFAULT NULL,
  `ispredefinito` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `iva`
--

LOCK TABLES `iva` WRITE;
/*!40000 ALTER TABLE `iva` DISABLE KEYS */;
INSERT INTO `iva` VALUES ('10','IVA 10%',NULL,'00',10,NULL),('21','IVA 21%',NULL,'00',21,1);
/*!40000 ALTER TABLE `iva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `modopag`
--

DROP TABLE IF EXISTS `modopag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `modopag` (
  `id` varchar(10) NOT NULL,
  `modopag` varchar(200) DEFAULT NULL,
  `numrate` int(11) DEFAULT NULL,
  `ispredefinito` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `modopag`
--

LOCK TABLES `modopag` WRITE;
/*!40000 ALTER TABLE `modopag` DISABLE KEYS */;
INSERT INTO `modopag` VALUES ('001','Bonifico bancario 60gg Fm',NULL,NULL),('002','Bonifico bancario 30 giorni fine mese',NULL,NULL);
/*!40000 ALTER TABLE `modopag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nazione`
--

DROP TABLE IF EXISTS `nazione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nazione` (
  `id` varchar(10) NOT NULL,
  `nazione` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nazione`
--

LOCK TABLES `nazione` WRITE;
/*!40000 ALTER TABLE `nazione` DISABLE KEYS */;
INSERT INTO `nazione` VALUES ('AD','Andorra'),('AE','Emirati Arabi Uniti'),('AF','Afghanistan'),('AG','Antigua e Barbuda'),('AI','Anguilla'),('AL','Albania'),('AM','Armenia'),('AN','Antille Olandesi'),('AO','Angol'),('AQ','Antartide'),('AR','Argentina'),('AS','Samoa Americane'),('AT','Austria'),('AU','Australia'),('AW','Aruba'),('AX','Isole Aland'),('AZ','Azerbaigian'),('BA','Bosnia-Erzegovina'),('BB','Barbados'),('BD','Bangladesh'),('BE','Belgio'),('BF','Burkina Faso'),('BG','Bulgaria'),('BH','Bahrain'),('BI','Burundi'),('BJ','Beninv'),('BL','Saint-Barthelemy'),('BM','Bermuda'),('BN','Brunei'),('BO','Bolivia'),('BR','Brasile'),('BS','Bahamas'),('BT','Bhutan'),('BV','Isola Bouvet'),('BW','Botswana'),('BY','Bielorussia'),('BZ','Belize'),('CA','Canada'),('CC','Isole Cocos'),('CD','Repubblica Democratica del Congo ex Zaire'),('CF','Repubblica Centrafricana'),('CG','Repubblica del Congo'),('CH','Svizzera'),('CI','Costa d\'Avorio'),('CK','Isole Cook'),('CL','Cile'),('CM','Camerun'),('CN','Cina Repubblica Popolare Cinese'),('CO','Colombia'),('CR','Costa Rica'),('CU','Cuba'),('CV','Capo Verde'),('CX','Isola Christmas'),('CY','Cipro'),('CZ','Repubblica Ceca'),('DE','Germania'),('DJ','Gibuti'),('DK','Danimarca'),('DM','Dominica'),('DO','Repubblica Dominicana'),('DZ','Algeria'),('EC','Ecuador'),('EE','Estonia'),('EG','Egitto'),('EH','Sahara Occidentale ex Sahara Spagnolo'),('ER','Eritrea'),('ES','Spagna'),('ET','Etiopia'),('FI','Finlandia'),('FJ','Figi'),('FK','Isole Falkland'),('FM','Stati Federati di Micronesia'),('FO','Isole Far Oer'),('FR','Francia'),('GA','Gabon'),('GB','Regno Unito'),('GD','Grenada'),('GE','Georgia'),('GF','Guyana Francese'),('GG','Guernsey'),('GH','Ghana'),('GI','Gibilterra'),('GL','Groenlandia'),('GM','Gambia'),('GN','Guinea'),('GP','Guadalupa'),('GQ','Guinea Equatoriale'),('GR','Grecia'),('GS','Georgia del Sud e isole Sandwich meridionali'),('GT','Guatemala'),('GU','Guam'),('GW','Guinea-Bissau'),('GY','Guyana'),('HK','Hong Kong'),('HM','Isole Heard e McDonald'),('HN','Honduras'),('HR','Croazia'),('HT','Haiti'),('HU','Ungheria'),('ID','Indonesia'),('IE','Irlanda'),('IL','Israele'),('IM','Isola di Man'),('IN','India'),('IO','Territori Britannici dell\'Oceano Indiano comprende Diego Garcia'),('IQ','Iraq'),('IR','Iran'),('IS','Islanda'),('IT','Italia'),('JE','Jersey'),('JM','Giamaica'),('JO','Giordania'),('JP','Giappone'),('KE','Kenya'),('KG','Kirghizistan'),('KH','Cambogia'),('KI','Kiribati'),('KM','Comore'),('KN','Saint Kitts e Nevis'),('KP','Corea del Nord'),('KR','Corea del Sud'),('KW','Kuwait'),('KY','Isole Cayman'),('KZ','Kazakistan'),('LA','Laos'),('LB','Libano'),('LC','Santa Lucia'),('LI','Liechtenstein'),('LK','Sri Lanka'),('LR','Liberia'),('LS','Lesotho'),('LT','Lituania'),('LU','Lussemburgo'),('LV','Lettonia'),('LY','Libia'),('MA','Marocco'),('MC','Monaco'),('MD','Moldavia'),('ME','Montenegro'),('MF','Saint-Martin'),('MG','Madagascar'),('MH','Isole Marshall'),('MK','Macedonia'),('ML','Mali'),('MM','Birmania Myanmar'),('MN','Mongolia'),('MO','Macao'),('MP','Isole Marianne Settentrionali'),('MQ','Martinica'),('MR','Mauritania'),('MS','Montserrat'),('MT','Malta'),('MU','Mauritius'),('MV','Maldive'),('MW','Malawi'),('MX','Messico'),('MY','Malesia'),('MZ','Mozambico'),('NA','Namibia'),('NC','Nuova Caledonia'),('NE','Niger'),('NF','Isola Norfolk'),('NG','Nigeria'),('NI','Nicaragua'),('NL','Olanda Paesi Bassi'),('NO','Norvegia'),('NP','Nepal'),('NR','Nauru'),('NU','Niue'),('NZ','Nuova Zelanda'),('OM','Oman'),('PA','Panama'),('PE','Peru'),('PF','Polinesia Francese comprende l\'Isola Clipperton'),('PG','Papua Nuova Guinea'),('PH','Filippine'),('PK','Pakistan'),('PL','Polonia'),('PM','Saint Pierre e Miquelon'),('PN','Isole Pitcairn'),('PR','Porto Rico'),('PS','Territori Palestinesi Occupati ovvero, Cisgiordania e Striscia di Gaza'),('PT','Portogallo'),('PW','Palau'),('PY','Paraguay'),('QA','Qatar'),('RE','Reunion'),('RO','Romania'),('RS','Serbia'),('RU','Russia'),('RW','Ruanda'),('SA','Arabia Saudita'),('SB','Isole Salomone'),('SC','Seychelles'),('SD','Sudan'),('SE','Svezia'),('SG','Singapore'),('SH','Sant\'Elena'),('SI','Slovenia'),('SJ','Svalbard e Jan Mayen'),('SK','Slovacchia'),('SL','Sierra Leone'),('SM','San Marino'),('SN','Senegal'),('SO','Somalia'),('SR','Suriname'),('ST','Sao Tome'),('SV','El Salvador'),('SY','Siria'),('SZ','Swaziland'),('TC','Isole Turks e Caicos'),('TD','Ciad'),('TF','Territori Francesi del Sud'),('TG','Togo'),('TH','Thailandia'),('TJ','Tagikistan'),('TK','Tokelau'),('TL','Timor Est'),('TM','Turkmenistan'),('TN','Tunisia'),('TO','Tonga'),('TR','Turchia'),('TT','Trinidad e Tobago'),('TV','Tuvalu'),('TW','Repubblica di Cina Taiwan'),('TZ','Tanzania'),('UA','Ucraina'),('UG','Uganda'),('UM','Isole minori esterne degli Stati Uniti'),('US','Stati Uniti d\'America'),('UY','Uruguay'),('UZ','Uzbekistan'),('VA','Citta del Vaticano'),('VC','Saint Vincent e Grenadine'),('VE','Venezuela'),('VG','Isole Vergini Britanniche'),('VI','Isole Vergini Americane'),('VN','Vietnam'),('VU','Vanuatu'),('WF','Wallis e Futuna'),('WS','Samoa ex Samoa Occidentali'),('YE','Yemen'),('YT','Mayotte'),('ZA','Sudafrica'),('ZM','Zambia'),('ZW','Zimbabwe');
/*!40000 ALTER TABLE `nazione` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offdet`
--

DROP TABLE IF EXISTS `offdet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offdet` (
  `idofferta` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `posizione` varchar(100) DEFAULT NULL,
  `isivato` tinyint(1) DEFAULT NULL,
  `ischiuso` tinyint(1) DEFAULT NULL,
  `descri` varchar(100) DEFAULT NULL,
  `destinazione` varchar(100) DEFAULT NULL,
  `noteinizio1` varchar(100) DEFAULT NULL,
  `noteinizio2` varchar(100) DEFAULT NULL,
  `noteinizio3` varchar(100) DEFAULT NULL,
  `noteinizio4` varchar(100) DEFAULT NULL,
  `noteinizio5` varchar(100) DEFAULT NULL,
  `noteinizio6` varchar(100) DEFAULT NULL,
  `noteinizio7` varchar(100) DEFAULT NULL,
  `noteinizio8` varchar(100) DEFAULT NULL,
  `noteinizio9` varchar(100) DEFAULT NULL,
  `noteinizio10` varchar(100) DEFAULT NULL,
  `notefine1` varchar(100) DEFAULT NULL,
  `notefine2` varchar(100) DEFAULT NULL,
  `notefine3` varchar(100) DEFAULT NULL,
  `notefine4` varchar(100) DEFAULT NULL,
  `notefine5` varchar(100) DEFAULT NULL,
  `notefine6` varchar(100) DEFAULT NULL,
  `notefine7` varchar(100) DEFAULT NULL,
  `notefine8` varchar(100) DEFAULT NULL,
  `notefine9` varchar(100) DEFAULT NULL,
  `notefine10` varchar(100) DEFAULT NULL,
  `quantita` decimal(10,2) DEFAULT '0.00',
  `prezzo` decimal(10,2) DEFAULT '0.00',
  `idiva` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idofferta`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offdet`
--

LOCK TABLES `offdet` WRITE;
/*!40000 ALTER TABLE `offdet` DISABLE KEYS */;
INSERT INTO `offdet` VALUES ('000001','001','1',NULL,1,'dahdadasdas+',NULL,'dasdas',NULL,NULL,NULL,'dasdas',NULL,NULL,NULL,NULL,NULL,'das',NULL,'das',NULL,NULL,NULL,NULL,NULL,NULL,NULL,2.00,100.00,'21'),('000001','002','2',NULL,1,'gfdgfd',NULL,'gfdgfd',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,50.00,10.00,'21'),('000002','001','1',1,NULL,'Descrizione e quantita','afs','prima',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'dopo',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,5.00,27.17,'10');
/*!40000 ALTER TABLE `offdet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `offerta`
--

DROP TABLE IF EXISTS `offerta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `offerta` (
  `id` varchar(10) NOT NULL,
  `idcausale` varchar(10) DEFAULT NULL,
  `data` varchar(8) DEFAULT NULL,
  `protocollo` int(11) DEFAULT NULL,
  `numero` varchar(50) DEFAULT NULL,
  `idanag` varchar(10) DEFAULT NULL,
  `recapito` text,
  `isrichiestatelefonica` tinyint(1) DEFAULT NULL,
  `datarichiestatelefonica` varchar(8) DEFAULT NULL,
  `ismail` tinyint(1) DEFAULT NULL,
  `datamail` varchar(8) DEFAULT NULL,
  `protocollomail` varchar(50) DEFAULT NULL,
  `isfax` tinyint(1) DEFAULT NULL,
  `datafax` varchar(8) DEFAULT NULL,
  `protocollofax` varchar(50) DEFAULT NULL,
  `hasdisponibilita` tinyint(1) DEFAULT NULL,
  `hasmassimale` tinyint(1) DEFAULT NULL,
  `noteinterne` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `offerta`
--

LOCK TABLES `offerta` WRITE;
/*!40000 ALTER TABLE `offerta` DISABLE KEYS */;
INSERT INTO `offerta` VALUES ('000001','02','20120215',1,'O  1/2012','000001','Via Cantu 86\n23890 Barzago LC',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),('000002','02','20120319',2,'O  2/2012','000002','Via Monte Grappa, 21\n23876 Monticello LC',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `offerta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `percorso`
--

DROP TABLE IF EXISTS `percorso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `percorso` (
  `id` varchar(50) NOT NULL,
  `path` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `percorso`
--

LOCK TABLES `percorso` WRITE;
/*!40000 ALTER TABLE `percorso` DISABLE KEYS */;
INSERT INTO `percorso` VALUES ('THUNDERBIRD','C:\\Program Files\\Mozilla Thunderbird');
/*!40000 ALTER TABLE `percorso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `postpag`
--

DROP TABLE IF EXISTS `postpag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `postpag` (
  `id` varchar(10) NOT NULL,
  `postpag` varchar(200) DEFAULT NULL,
  `m01` int(11) DEFAULT NULL,
  `m02` int(11) DEFAULT NULL,
  `m03` int(11) DEFAULT NULL,
  `m04` int(11) DEFAULT NULL,
  `m05` int(11) DEFAULT NULL,
  `m06` int(11) DEFAULT NULL,
  `m07` int(11) DEFAULT NULL,
  `m08` int(11) DEFAULT NULL,
  `m09` int(11) DEFAULT NULL,
  `m10` int(11) DEFAULT NULL,
  `m11` int(11) DEFAULT NULL,
  `m12` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `postpag`
--

LOCK TABLES `postpag` WRITE;
/*!40000 ALTER TABLE `postpag` DISABLE KEYS */;
/*!40000 ALTER TABLE `postpag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `provincia`
--

DROP TABLE IF EXISTS `provincia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `provincia` (
  `id` varchar(10) NOT NULL,
  `provincia` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `provincia`
--

LOCK TABLES `provincia` WRITE;
/*!40000 ALTER TABLE `provincia` DISABLE KEYS */;
INSERT INTO `provincia` VALUES ('AG','Agrigento'),('AL','Alessandria'),('AN','Ancona'),('AO','Aosta'),('AP','Ascoli Piceno'),('AQ','L\'Aquila'),('AR','Arezzo'),('AT','Asti'),('AV','Avellino'),('BA','Bari'),('BG','Bergamo'),('BI','Biella'),('BL','Belluno'),('BN','Benevento'),('BO','Bologna'),('BR','Brindisi'),('BS','Brescia'),('BZ','Bolzano'),('CA','Cagliari'),('CB','Campobasso'),('CE','Caserta'),('CH','Chieti'),('CI','Carbonia Iglesias'),('CL','Caltanissetta'),('CN','Cuneo'),('CO','Como'),('CR','Cremona'),('CS','Cosenza'),('CT','Catania'),('CZ','Catanzaro'),('EN','Enna'),('FC','Forli Cesena'),('FE','Ferrara'),('FG','Foggia'),('FI','Firenze'),('FR','Frosinone'),('GE','Genova'),('GO','Gorizia'),('GR','Grosseto'),('IM','Imperia'),('IS','Isernia'),('KR','Crotone'),('LC','Lecco'),('LE','Lecce'),('LI','Livorno'),('LO','Lodi'),('LT','Latina'),('LU','Lucca'),('MB','Monza e della Brianza'),('MC','Macerata'),('ME','Messina'),('MI','Milano'),('MN','Mantova'),('MO','Modena'),('MS','Massa Carrara'),('MT','Matera'),('NA','Napoli'),('NO','Novara'),('NU','Nuoro'),('OG','Ogliastra'),('OR','Oristano'),('OT','Olbia Tempio'),('PA','Palermo'),('PC','Piacenza'),('PD','Padova'),('PE','Pescara'),('PG','Perugia'),('PI','Pisa'),('PN','Pordenone'),('PO','Prato'),('PR','Parma'),('PT','Pistoia'),('PU','Pesaro Urbino'),('PV','Pavia'),('PZ','Potenza'),('RA','Ravenna'),('RC','Reggio Calabria'),('RE','Reggio Emilia'),('RG','Ragusa'),('RI','Rieti'),('RM','Roma'),('RN','Rimini'),('RO','Rovigo'),('SA','Salerno'),('SI','Siena'),('SO','Sondrio'),('SP','La Spezia'),('SR','Siracusa'),('SS','Sassari'),('SV','Savona'),('TA','Taranto'),('TE','Teramo'),('TN','Trento'),('TO','Torino'),('TP','Trapani'),('TR','Terni'),('TS','Trieste'),('TV','Treviso'),('UD','Udine'),('VA','Varese'),('VB','Verbania'),('VC','Vercelli'),('VE','Venezia'),('VI','Vicenza'),('VR','Verona'),('VS','Medio Campidano'),('VT','Viterbo'),('VV','Vibo Valentia');
/*!40000 ALTER TABLE `provincia` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ratapag`
--

DROP TABLE IF EXISTS `ratapag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ratapag` (
  `idmodopag` varchar(10) NOT NULL,
  `id` varchar(10) NOT NULL,
  `idtipopag` varchar(10) DEFAULT NULL,
  `frequenza` int(11) DEFAULT NULL,
  `idtiposcadenza` varchar(10) DEFAULT NULL,
  `giornipiu` int(11) DEFAULT NULL,
  PRIMARY KEY (`idmodopag`,`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ratapag`
--

LOCK TABLES `ratapag` WRITE;
/*!40000 ALTER TABLE `ratapag` DISABLE KEYS */;
INSERT INTO `ratapag` VALUES ('001','001','BO',60,'FM',NULL),('002','001','BO',30,'FM',NULL);
/*!40000 ALTER TABLE `ratapag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `scadenzario`
--

DROP TABLE IF EXISTS `scadenzario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `scadenzario` (
  `id` varchar(200) NOT NULL,
  `idfattura` varchar(10) NOT NULL,
  `idanag` varchar(10) DEFAULT NULL,
  `idtipoanag` varchar(10) DEFAULT NULL,
  `numdoc` varchar(10) DEFAULT NULL,
  `data` varchar(10) DEFAULT NULL,
  `idtipopag` varchar(10) DEFAULT NULL,
  `idtiposcadenzario` varchar(10) DEFAULT NULL,
  `importo` decimal(10,2) DEFAULT '0.00',
  `ispagato` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `scadenzario`
--

LOCK TABLES `scadenzario` WRITE;
/*!40000 ALTER TABLE `scadenzario` DISABLE KEYS */;
INSERT INTO `scadenzario` VALUES ('0000000001','000001','000001','','F  1/2012','20120430','BO','INC',847.00,NULL),('0000000002','000002','000002','','F  2/2012','20120430','BO','INC',11463.65,NULL);
/*!40000 ALTER TABLE `scadenzario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `spesa`
--

DROP TABLE IF EXISTS `spesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `spesa` (
  `id` varchar(10) NOT NULL,
  `spesa` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `spesa`
--

LOCK TABLES `spesa` WRITE;
/*!40000 ALTER TABLE `spesa` DISABLE KEYS */;
/*!40000 ALTER TABLE `spesa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampafatdet`
--

DROP TABLE IF EXISTS `stampafatdet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampafatdet` (
  `id` varchar(10) NOT NULL,
  `posizione` text,
  `descrizione` text,
  `quantita` text,
  `prezzo` text,
  `scontoperc` text,
  `importo` text,
  `iva` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampafatdet`
--

LOCK TABLES `stampafatdet` WRITE;
/*!40000 ALTER TABLE `stampafatdet` DISABLE KEYS */;
INSERT INTO `stampafatdet` VALUES ('0000000001','001','GENNAIO - FEBBRAIO 2012','1,00','10.421,50','','10.421,50','10');
/*!40000 ALTER TABLE `stampafatdet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampafativa`
--

DROP TABLE IF EXISTS `stampafativa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampafativa` (
  `id` varchar(10) NOT NULL,
  `imponibile` varchar(10) NOT NULL,
  `iva` text,
  `descrizioneiva` text,
  `imposta` text,
  PRIMARY KEY (`id`,`imponibile`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampafativa`
--

LOCK TABLES `stampafativa` WRITE;
/*!40000 ALTER TABLE `stampafativa` DISABLE KEYS */;
INSERT INTO `stampafativa` VALUES ('0000000001','10.421,50','10','IVA 10%','1.042,15');
/*!40000 ALTER TABLE `stampafativa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampafatsca`
--

DROP TABLE IF EXISTS `stampafatsca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampafatsca` (
  `id` varchar(10) NOT NULL,
  `data` varchar(10) NOT NULL,
  `totale` text,
  PRIMARY KEY (`id`,`data`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampafatsca`
--

LOCK TABLES `stampafatsca` WRITE;
/*!40000 ALTER TABLE `stampafatsca` DISABLE KEYS */;
INSERT INTO `stampafatsca` VALUES ('0000000001','30/04/2012','11.463,65');
/*!40000 ALTER TABLE `stampafatsca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampafatspesa`
--

DROP TABLE IF EXISTS `stampafatspesa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampafatspesa` (
  `id` varchar(10) NOT NULL,
  `spesa` text,
  `imponibile` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampafatspesa`
--

LOCK TABLES `stampafatspesa` WRITE;
/*!40000 ALTER TABLE `stampafatspesa` DISABLE KEYS */;
/*!40000 ALTER TABLE `stampafatspesa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampafattura`
--

DROP TABLE IF EXISTS `stampafattura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampafattura` (
  `destinatario` text,
  `recapito` text,
  `numero` text,
  `data` text,
  `documento` text,
  `isfiscale` tinyint(1) DEFAULT NULL,
  `codicefiscale` text,
  `isministeriale` tinyint(1) DEFAULT NULL,
  `codiceministeriale` text,
  `partitaiva` text,
  `pagamento` text,
  `banca` text,
  `iban` text,
  `totaleimponibile` text,
  `totaleimposta` text,
  `totalefattura` text,
  `sum_pos` text,
  `sum_neg` text,
  `netto` text,
  `notepiepagina` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampafattura`
--

LOCK TABLES `stampafattura` WRITE;
/*!40000 ALTER TABLE `stampafattura` DISABLE KEYS */;
INSERT INTO `stampafattura` VALUES ('CONSORZIO BRIANTEO PER L\'ISTRUZIONE SCUOLA MEDIA SUPERIORE','Via Monte Grappa, 21\n23876 Monticello LC','F  2/2012','19/03/2012','FATTURA DI VENDITA',0,'85001680132',0,NULL,'01385870132','Bonifico bancario 30 giorni fine mese','','','10.421,50','1.042,15','11.463,65','10.421,50','','10.421,50',NULL);
/*!40000 ALTER TABLE `stampafattura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampafogliodiviaggio`
--

DROP TABLE IF EXISTS `stampafogliodiviaggio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampafogliodiviaggio` (
  `numero` text,
  `data` text,
  `dataritorno` text,
  `autista1` text,
  `autista2` text,
  `veicolo` text,
  `targa` text,
  `committente` text,
  `oraeluogo` text,
  `destinazione` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampafogliodiviaggio`
--

LOCK TABLES `stampafogliodiviaggio` WRITE;
/*!40000 ALTER TABLE `stampafogliodiviaggio` DISABLE KEYS */;
INSERT INTO `stampafogliodiviaggio` VALUES ('001','15/02/2012','NULL','DURA','MURO','FIAT IDEA','5214','CACCA','das','das');
/*!40000 ALTER TABLE `stampafogliodiviaggio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampaoffdet`
--

DROP TABLE IF EXISTS `stampaoffdet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampaoffdet` (
  `id` varchar(10) NOT NULL,
  `corpo` text,
  `prezzo` text,
  `islineaprezzo` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampaoffdet`
--

LOCK TABLES `stampaoffdet` WRITE;
/*!40000 ALTER TABLE `stampaoffdet` DISABLE KEYS */;
INSERT INTO `stampaoffdet` VALUES ('0000000001','Posizione 1',NULL,NULL),('0000000002','prima',NULL,NULL),('0000000003','Descrizione e quantita',' Eur. 149,44 iva inclusa IVA 10%',1),('0000000004','dopo',NULL,NULL);
/*!40000 ALTER TABLE `stampaoffdet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stampaofferta`
--

DROP TABLE IF EXISTS `stampaofferta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stampaofferta` (
  `destinatario` text,
  `recapito` text,
  `data` text,
  `oggetto` text,
  `intestazione` text,
  `isdisponibilita` tinyint(1) DEFAULT NULL,
  `ismassimale` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stampaofferta`
--

LOCK TABLES `stampaofferta` WRITE;
/*!40000 ALTER TABLE `stampaofferta` DISABLE KEYS */;
INSERT INTO `stampaofferta` VALUES ('CONSORZIO BRIANTEO PER L\'ISTRUZIONE SCUOLA MEDIA SUPERIORE','Via Monte Grappa, 21\n23876 Monticello LC','19/03/2012','OFFERTA DI VENDITA O  2/2012','Con riferimento a Vs. cortese richiesta, con la presente Vi sottoponiamo nostro miglior preventivo relativo al seguente servizio.',NULL,NULL);
/*!40000 ALTER TABLE `stampaofferta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipoanag`
--

DROP TABLE IF EXISTS `tipoanag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipoanag` (
  `id` varchar(10) NOT NULL,
  `tipoanag` varchar(200) DEFAULT NULL,
  `idtipocodice` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipoanag`
--

LOCK TABLES `tipoanag` WRITE;
/*!40000 ALTER TABLE `tipoanag` DISABLE KEYS */;
/*!40000 ALTER TABLE `tipoanag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipobanca`
--

DROP TABLE IF EXISTS `tipobanca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipobanca` (
  `id` varchar(10) NOT NULL,
  `tipobanca` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipobanca`
--

LOCK TABLES `tipobanca` WRITE;
/*!40000 ALTER TABLE `tipobanca` DISABLE KEYS */;
INSERT INTO `tipobanca` VALUES ('NS','Nostra banca'),('VS','Vostra banca');
/*!40000 ALTER TABLE `tipobanca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipocausale`
--

DROP TABLE IF EXISTS `tipocausale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipocausale` (
  `id` varchar(10) NOT NULL,
  `tipocausale` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipocausale`
--

LOCK TABLES `tipocausale` WRITE;
/*!40000 ALTER TABLE `tipocausale` DISABLE KEYS */;
INSERT INTO `tipocausale` VALUES ('FAT','Fattura'),('OFF','Offerta');
/*!40000 ALTER TABLE `tipocausale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipocodice`
--

DROP TABLE IF EXISTS `tipocodice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipocodice` (
  `id` varchar(200) NOT NULL,
  `tipocodice` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipocodice`
--

LOCK TABLES `tipocodice` WRITE;
/*!40000 ALTER TABLE `tipocodice` DISABLE KEYS */;
INSERT INTO `tipocodice` VALUES ('ALL','Entrambi'),('FIS','Codice fiscale'),('MIN','Codice ministeriale');
/*!40000 ALTER TABLE `tipocodice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipoiva`
--

DROP TABLE IF EXISTS `tipoiva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipoiva` (
  `id` varchar(10) NOT NULL,
  `tipoiva` varchar(200) DEFAULT NULL,
  `isaliquota` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipoiva`
--

LOCK TABLES `tipoiva` WRITE;
/*!40000 ALTER TABLE `tipoiva` DISABLE KEYS */;
INSERT INTO `tipoiva` VALUES ('00','Imponibile',1),('01','Non imponibile',0),('02','Esente',0),('03','Escluso',0),('04','Fuori campo',0);
/*!40000 ALTER TABLE `tipoiva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tipopag`
--

DROP TABLE IF EXISTS `tipopag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tipopag` (
  `id` varchar(10) NOT NULL,
  `tipopag` varchar(200) DEFAULT NULL,
  `idtipobanca` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipopag`
--

LOCK TABLES `tipopag` WRITE;
/*!40000 ALTER TABLE `tipopag` DISABLE KEYS */;
INSERT INTO `tipopag` VALUES ('AS','Assegno','NS'),('BO','Bonifico','NS'),('RB','Ricevuta Bancaria','VS'),('RD','Rimessa Diretta','NS'),('RI','Rid','NS'),('TR','Tratta','NS');
/*!40000 ALTER TABLE `tipopag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposcadenza`
--

DROP TABLE IF EXISTS `tiposcadenza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tiposcadenza` (
  `id` varchar(10) NOT NULL,
  `tiposcadenza` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposcadenza`
--

LOCK TABLES `tiposcadenza` WRITE;
/*!40000 ALTER TABLE `tiposcadenza` DISABLE KEYS */;
INSERT INTO `tiposcadenza` VALUES ('DF','Data fattura'),('FM','Fine mese');
/*!40000 ALTER TABLE `tiposcadenza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tiposcadenzario`
--

DROP TABLE IF EXISTS `tiposcadenzario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tiposcadenzario` (
  `id` varchar(10) NOT NULL,
  `tiposcadenzario` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tiposcadenzario`
--

LOCK TABLES `tiposcadenzario` WRITE;
/*!40000 ALTER TABLE `tiposcadenzario` DISABLE KEYS */;
INSERT INTO `tiposcadenzario` VALUES ('INC','Incasso'),('PAG','pagamento');
/*!40000 ALTER TABLE `tiposcadenzario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utente`
--

DROP TABLE IF EXISTS `utente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `utente` (
  `id` varchar(10) NOT NULL,
  `utente` varchar(200) DEFAULT NULL,
  `codice` varchar(20) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utente`
--

LOCK TABLES `utente` WRITE;
/*!40000 ALTER TABLE `utente` DISABLE KEYS */;
INSERT INTO `utente` VALUES ('0000','Administrator','Administrator','');
/*!40000 ALTER TABLE `utente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veicolo`
--

DROP TABLE IF EXISTS `veicolo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `veicolo` (
  `id` varchar(10) NOT NULL,
  `veicolo` varchar(200) DEFAULT NULL,
  `targa` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veicolo`
--

LOCK TABLES `veicolo` WRITE;
/*!40000 ALTER TABLE `veicolo` DISABLE KEYS */;
/*!40000 ALTER TABLE `veicolo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `versione`
--

DROP TABLE IF EXISTS `versione`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `versione` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `versione` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `versione`
--

LOCK TABLES `versione` WRITE;
/*!40000 ALTER TABLE `versione` DISABLE KEYS */;
INSERT INTO `versione` VALUES (1,8);
/*!40000 ALTER TABLE `versione` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2012-03-19 23:10:32
