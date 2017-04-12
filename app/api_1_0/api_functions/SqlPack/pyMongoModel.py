# -*- coding: utf-8 -*-
'''
Created on 2016年6月28日

@author: lujian

Python pymongo 数据库参数声明区域
'''

oss_system_mongodbquery = 'mongodb://mongoquery:FnVWVDvnWeuinx7@52.74.132.61:55075/oss_system?authMechanism=SCRAM-SHA-1'
gsvcdbAdmin = 'mongodb://dbAdmin:dbAdminacc@52.42.214.40:27017/gsvcdb?authMechanism=SCRAM-SHA-1'

gsvcdb = 'gsvcdb'
oss_systemDB = 'oss_system'

oss_systemBaseCollection ='t_terminal_flow_upload'

gsvcdbCollections = ['hourChargeFlower', 'dayChargeFlower', 'VsimFlowerOf140']

sql_info = {
    'getCountryProbDic':{'queryFlower':{'uri': gsvcdbAdmin, 'db': gsvcdb, 'collection': gsvcdbCollections[0]}},
    'getFlower':{'queryhourFlower':{'uri': gsvcdbAdmin, 'db': gsvcdb, 'collection': gsvcdbCollections[0]},
                 'querydayFlower':{'uri': gsvcdbAdmin, 'db': gsvcdb, 'collection': gsvcdbCollections[1]}},
    'get140Flower':{'query140Flower':{'uri': gsvcdbAdmin, 'db': gsvcdb, 'collection': gsvcdbCollections[2]}}
}


#(--------------------------------------errConnectionsinfo---------------------)
PyMog = {'MongoClient':["GTBU","S"],
         'Database':["ucl_oss_performancelog","N_oss_perflog"],
         'Sheet':["t_term_vsim_estfail","t_term_vsim_estsucc"]}


MongoClient = {"GTBU":"pymongo.MongoClient('52.76.228.13',57111)",
               "S":"pymongo.MongoClient('202.82.79.129',10076)",
               "N_bss":"pymongo.MongoClient('mongodb://mongoquery:FnVWVDvnWeuinx7@52.74.132.61:55065/bss?authMechanism=SCRAM-SHA-1')",
               "N_oss_perflog":"pymongo.MongoClient('mongodb://mongoquery:FnVWVDvnWeuinx7@52.74.132.61:55075/oss_perflog?authMechanism=SCRAM-SHA-1')",
               }
Database = {"ucl_oss_performancelog": "ucl_oss_performancelog", "N_oss_perflog": "oss_perflog"}
Sheet = {"t_term_vsim_estfail": "t_term_vsim_estfail",
         "t_term_vsim_estsucc": "t_term_vsim_estsucc",
         "FlowDetailedRecord": "FlowDetailedRecord",
         }
