# -*- coding: utf-8 -*-


'''
Created on 2016年6月28日

@author: lujian

Python Sql类模块声明区域
'''
import mysql.connector
import datetime
#from GlobalParams import Sql_Dic


class msSql(object):
    '''
    msSql define calss of sql connection objects:
    (sysSql:connect to sys str type,Database:qurey database name str type)
    '''
    def __init__(self, sysSql, Database):
        '''
        Constructor
        class parameters define
        '''
        self.sysSql = sysSql #连接系统数据库字符名称，进行客户端登录验证
        self.Database = Database#连接系统数据库子数据库名称，定向某一指定数据库
    def _Get_sysDBDic(self):
        """
        定义数据的连接字典
        """
        Sql_Dic = {
           'config_amzami': { 'user': 'cc_user',              # 新加坡商用环境数据库(主数据库)-远程连接
                              'password': 'AmzRedGsvcRootAcc',
                              'host': '52.74.132.61',
                              'port': 55162,
                              'database': 'gsvcdatabase'
                              },
           'config_amzlocal': {'user': 'root',                 # 美国测试环境开发库-本地root连接
                               'password': 'AmzRedGsvcRootAcc',
                               'host': 'localhost',
                               'port': 3306,
                               'database': 'gsvcdatabase',
                               # 'raise_on_warnings': False,
                               # 'use_pure': False,
                               },
           'config_Devlocal' : {                               # 本地pc开发库-本地连接
                                'user': 'root',
                                'password': 'gsvc123456',
                                'host': 'localhost',
                                'port': 3306,
                                'database': 'devdatabase',
                                #'raise_on_warnings': False,
                                #'use_pure': False,
                                },
           'config_DevAmz': {'user': 'cc_user',                   # 美国测试环境开发库-远程连接
                             'password': 'AmzRedGsvcAdminAcc',
                             'host': '52.42.214.40',
                             'port': 3306,
                             'database': 'devdatabase',
                             # 'raise_on_warnings': False,
                             # 'use_pure': False,
                             },
           'config_UMS': {'user': 'cc_user',
                           'password': 'AmzRedGsvcRootAcc',
                           'host': '52.74.132.61',
                           'port': 55162,
                           'database': 'login_history',
                           # 'raise_on_warnings': False,
                           # 'use_pure': False,
                           },
           'config_N' : {
                          'user': 'itquery',
                          'password': 'btf2nuGNXUV9Xbebtf2nuGNXUV9Xbe',
                          'host': '52.74.132.61',
                          'port': 55151,
                          'database': 'glocalme_css',
                          #'raise_on_warnings': False,
                          #'use_pure': False,
                          },
           'config_S' : {
                          'user': 'Queryonly',
                          'password': 'Queryonly!=',
                          'host': '202.82.79.130',
                          'port': 10023,
                          'database': 'ucloudplatform',
                          #'raise_on_warnings': False,
                          #'use_pure': False,
                          },
           'config_Y': {
                         'user': 'itquery',
                         'password': 'btf2nuGNXUV9Xbebtf2nuGNXUV9Xbe',
                         'host': '52.28.234.221',
                         'port': 55151,
                         'database': 'ucloudplatform',
                         'raise_on_warnings': False,
                          # 'use_pure': False,
                         },
        }
        try:
            if self.sysSql in Sql_Dic.keys():
                return Sql_Dic[self.sysSql]
        except KeyError as keyerr:
            print("暂时没有：",self.sysSql,"errDiscrip:\n",keyerr)

    def get_connec(self):
        """
        """
        sysdb = self._Get_sysDBDic()#获取全局变量，更新鉴权连接系统数据库
        sysdb.update({'database' : self.Database})#更新子数据库设置
        #print(sysdb)
        conn = mysql.connector.connect(**sysdb)
        #ping通数据库，防止长时间断开连接
        conn.ping(True)
        connectReturn =  conn
        return connectReturn

#sql_qure 完成结果查询

def get_DataBaseConn(sysSql,Database):
    """

    :param sysSql:
    :param Database:
    :return: database connection course
    """
    db = msSql(sysSql,Database).get_connec()
    return db
def sql_qure(db,query_str,where):
    """
    本部分重点完成sql库的cursor获取，返回所有查询结果cursor.fetchall()
    sql_qure(db：connect to db link,
    select_name: output key as talbe name ,
    query_str：qurey str pass to sql cursor.execute,
    where:conditions set for sql qurey)
    """

    find = query_str
    cursor = db.cursor()
    if where ==[]:
        #print (find)
        cursor.execute(find)
    else:
        cursor.execute(find,where) #where条件设置
    fetch_result = cursor.fetchall()#sql会按照slelect顺序输出[(fiel1,fiel2, fiel,,,),(,,,),(,,,)]
    cursor.close()
    return fetch_result
def Sql_Dicqure(db,query_str,where):
    """
    本部分重点完成sql库的cursor获取，返回所有查询结果cursor.fetchall()
    sql_qure(db：connect to db link,
    select_name: output key as talbe name ,
    query_str：qurey str pass to sql cursor.execute,
    where:conditions set for sql qurey)
    """

    find = query_str
    cursor = db.cursor(dictionary=True, buffered=True)
    if where ==[]:
        #print (find)
        cursor.execute(find)
    else:
        cursor.execute(find,where) #where条件设置
    fetch_result = cursor.fetchall()#sql会按照slelect顺序输出[(fiel1,fiel2, fiel,,,),(,,,),(,,,)]
    cursor.close()
    db.close()
    return fetch_result
def updateSQLData(sysStr,Database,updateStr,value):

    cnx = msSql(sysStr,Database).get_connec()
    cnx.ping(True)
    cursor = cnx.cursor()
    cursor.execute(updateStr,value)
    cnx.commit()
    cursor.close()
    cnx.close()

def qureResultAsJson(sysStr,Database,query_str,where):
    """
    db：connect to db link,
    select_name: output key as talbe name ,
    query_str：qurey str pass to sql cursor.execute,
    where:conditions set for sql qurey

    完成数据库查询sql_qure返回结果的Json格式输出，方便存储数据
    """
    db = msSql(sysStr,Database).get_connec()
    sql_result = Sql_Dicqure(db, query_str, where)
    if sql_result == []:
        return sql_result
    else:
        for i in range(len(sql_result)):
            for keys in sql_result[i]:
                if type(sql_result[i][keys]) is datetime.datetime:
                    sql_result[i][keys] = str(sql_result[i][keys])

        return sql_result
