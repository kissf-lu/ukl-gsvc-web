# -*- coding: utf-8 -*-


import os
import sys
import datetime
import time
#import xlrd
#import xlwt
import  xdrlib
#import mysql.connector

import pymongo
import json
from bson.son import SON
from bson.code import Code

#import smtplib
#from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

#-------------------------------------------------------------------mongo-Code------------------------------------------------------------------------------

class msmongo:
    """对查询mongo的封装操作
    """
    def __init__(self,MongoClient,Database,Sheet):
        self.MongoClient = MongoClient
        self.Database= Database
        self.Sheet = Sheet
        
        
    def __GetConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """

        db=self.MongoClient+"."+self.Database+"."+self.Sheet
        if not db:
            raise(NameError,"没有设置数据库信息")
        conn = eval(db)
        if not conn:
            raise(NameError,"连接数据库失败")
        else:
            return db
        
    def db_find(self,where,select,order):
        #查询函数\
        db = self.__GetConnect()
        find_order = db+"."+"find(where,select)"+"."+"sort("+"\""+order["order_by"]+"\""+","+"pymongo"+"."+order["sort_type"]+")"
        #print(find_order)
        cursor = eval(find_order)
        return cursor
    
    def db_group(self,key,condition,initial,reducer):
        db = self.__GetConnect()
        gp = db+"."+"group(key,condition,initial,reducer)" #+"."+"sort("+"\""+order["order_by"]+"\""+","+"pymongo"+"."+order["sort_type"]+")"
        results = eval(gp)
        return results
        
    def qurey_out(self,cursor,lis_tab,sheet):
        tab="con"
        #print(sheet)
        err_Code = []
        for i in range(len(lis_tab)):
            tab=tab+"\t"+lis_tab[i]
        #print(tab)
        con=1
        for document in cursor:
            
            out_doc=str(con)
            #print(document)
            for i in range(len(lis_tab)):
                if lis_tab[i] == "errorTime" :
                    out_doc=out_doc+"\t"+str(timestamp_datetime(document[lis_tab[i]]))
                    #err_Code.append(str(timestamp_datetime(document[lis_tab[i]])))
                else:
                    out_doc=out_doc+"\t"+str(document[lis_tab[i]])
                    #err_Code.append(str(document[lis_tab[i]]))

            #print(out_doc)
            
            con=con+1
            err_Code.append(document)
        return err_Code

def timestamp_datetime(value):
    format = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间戳(整形)，如：1332888820
    value = time.localtime(value)
    ## 经过localtime转换后变成
    ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # 最后再经过strftime函数转换为正常日期格式。
    dt = time.strftime(format, value)
    return dt

def datetime_timestamp(dt):
     #dt为字符串
     #中间过程，一般都需要将字符串转化为时间数组
     time.strptime(dt, '%Y-%m-%d %H:%M:%S')
     ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
     #将"2012-03-28 06:53:40"转化为时间戳
     s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
     return int(s)
    
def pyfind(msMog,sheet,select,where,order,lis_tab):
    cur = msMog.db_find(where,select,order)
    msMog.qurey_out(cur,lis_tab,sheet)

def pygroup(msMog,sheet,key,condition,initial,reducer,lis_tab):
    cur = msMog.db_group(key,condition,initial,reducer)
    return msMog.qurey_out(cur,lis_tab,sheet)

#-------------------------------------------------------------------mongo-Code-End-----------------------------------------------------------------------------

