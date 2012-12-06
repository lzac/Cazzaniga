# -*- coding: utf-8 -*-

import pro_10101_nazione as p10101                      
import pro_10102_provincia as p10102                    
import pro_10104_iva as p10104                         
import pro_10105_modopag as p10105                      
import pro_10109_tipopag as p10109                      
import pro_10111_postpag as p10111                      
import pro_10300_bancacc as p10300                      
import pro_10502_cliente as p10502                                    
import pro_10400_fattura as p10400                      
import pro_10129_spesa as p10129                        
import pro_10216_causale_fat as p10216   
import pro_10217_causale_off as p10217                              
import pro_30020_scainc as p30020                          
import pro_30021_scapag as p30021 
import pro_10120_tipoanagrafica as p10120
import pro_230_autista as p230
import pro_231_veicolo as p231
import pro_232_fogliodiviaggio as p232
import pro_10450_offerta as p10450
import pro_10460_prezzoviaggio as p10460
import pro_250_moduloassenza as p250
import pro_251_tipoassenza as p251

moduli = {
          'p10101' : p10101,
          'p10102' : p10102,
          'p10104' : p10104,
          'p10105' : p10105,
          'p10109' : p10109,
          'p10111' : p10111,
          'p10129' : p10129,
          'p10300' : p10300,
          'p10502' : p10502,
          'p10216' : p10216,
          'p10217' : p10217,
          'p10400' : p10400,
          'p30020' : p30020,
          'p30021' : p30021,
          'p10120': p10120,
          'p230':p230,
          'p231':p231,
          'p232':p232,
          'p10450':p10450,
          'p10460':p10460,
          'p250' : p250,
          'p251' : p251
        }