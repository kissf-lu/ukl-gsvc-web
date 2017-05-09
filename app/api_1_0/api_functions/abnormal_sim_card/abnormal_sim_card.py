# -*- coding: utf-8 -*-


# sql json格式查询接口
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
# sql information of connect to mysql
from app.api_1_0.api_functions.SqlPack.SqlLinkInfo import getonSysSrc as sqlLink

mysql_link = {
    'css': sqlLink['qureyNVsim']
}


def getJsonData(sys_str, data_base, query_str):
    """
    qureResultAsJson 自带链接断开操作
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

