# -*- coding: utf-8 -*-


import json
from bson import json_util
# sql json格式查询接口
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
# 获取连接信息
from app.api_1_0.api_functions.SqlPack.SqlLinkInfo import getFlowerQueryFunction as Sql

# 获取新架构卡资源数据库连接信息
sql_info = Sql


def getJsonData(sys_str, data_base, query_str):
    """
    
    :param sys_str: 
    :param data_base: 
    :param query_str: 
    :return: 
    """
    jsonResults = qureResultAsJson(sysStr=sys_str,
                                   Database=data_base,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def getSimPackageFlowerAPI(sim_package_param):
    """
    
    :param sim_package_param: 
    :return: 
    """
