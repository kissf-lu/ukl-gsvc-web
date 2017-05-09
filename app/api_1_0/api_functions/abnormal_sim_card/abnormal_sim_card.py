# -*- coding: utf-8 -*-


# sql json格式查询接口
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
# sql information of connect to mysql
from app.api_1_0.api_functions.SqlPack.SqlLinkInfo import getonSysSrc as sqlLink

mysql_link = {
    'css': sqlLink['qureyNVsim']
}
