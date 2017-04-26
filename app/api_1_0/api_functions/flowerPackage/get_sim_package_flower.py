# -*- coding: utf-8 -*-


import json
from bson import json_util
import mysql.connector
import decimal
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


def getSimPackageStatic(dic_param):
    """
    
    :param dic_param: 
    :return: 
    """
    errInfo = ''
    countryStr = ''
    orgStr = ''
    simTypeStr = ''
    packageTypeNameStr = ''
    country = ''
    org = ''
    simType = ''
    packageTypeName = ''
    SimPackageInfoData = []
    try:
        country = dic_param['country']
        org = dic_param['orgName']
        simType = dic_param['simType']
        packageTypeName = dic_param['packageTypeName']
    except KeyError:
        errInfo = 'api simPackageInfo static param keyErr!'
    if errInfo:
        dic_data = []
        dic_results = {'info': {'err': True, 'errInfo': errInfo}, 'data': dic_data}
        return dic_results
    else:
        if country:
            countryStr = "AND a.`iso2` = '" + country + "'"
        if org:
            orgStr = " AND e.`org_name` = '" + org + "' "
        if simType:
            simTypeStr = " AND a.`vsim_type` = '" + simType + "' "
        if packageTypeName:
            packageTypeNameStr = " AND b.`package_type_name` LIKE  '" + packageTypeName + "%' "

        str_query = (

            "( "
            "SELECT  "
            "a.`iso2`              AS 'Country',  "
            "CASE WHEN 1 THEN CONCAT('1-合计-',a.`iso2`,'-',e.`org_name` ) END  AS 'PackageName',  "
            "CASE WHEN 1 THEN '' END  AS 'NextUpdateTime',  "
            "COUNT(DISTINCT a.`imsi`) AS 'all_num',  "
            "COUNT(DISTINCT (CASE WHEN ((a.`available_status` = '0')    "
            "                            AND b.`next_update_time` IS NOT NULL   "
            "                            AND b.`next_update_time` > DATE(NOW()) "
            "                            AND b.`package_status`  IN (0,1) "
            "                            AND a.business_status IN (0,4,5) "
            "                            AND (b.service_time_type = 0 "
            "                                  OR (( b.service_time_type = 1 "
            "                                       AND ((b.gmt0_time_end > NOW()  AND NOW() > '00:00:00')  "
            "                                             OR (b.gmt0_time_start < NOW() AND NOW() <= '23:59:59')"
            "                                            )  "
            "                                       AND b.gmt0_time_end < b.gmt0_time_start "
            "                                      )   "
            "                                      OR(b.service_time_type = 1 "
            "                                         AND b.gmt0_time_start < NOW() "
            "                                         AND b.gmt0_time_end > NOW()  "
            "                                         AND   b.gmt0_time_end > b.gmt0_time_start "
            "                                        )"
            "                                  )  "
            "                            ) "
            "                           ) "
            "                      THEN a.`imsi` END)) AS 'ava_num', "
            "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0  "
            "                                       THEN b.`init_flow` "
            "                                       ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage'  "
            "FROM `t_css_vsim` AS a  "
            "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi`  "
            "LEFT  JOIN `t_css_group` AS e          ON a.`group_id`= e.`id`  "
            "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id`  "
            "WHERE  b.`package_type_name` IS NOT NULL "
            "       AND b.`init_flow` IS NOT NULL  " + countryStr + orgStr + simTypeStr + packageTypeNameStr + " "
            "GROUP BY a.`iso2`,e.`org_name`  "
            ") "
            "UNION "
            "( "
            "SELECT  "
            "a.`iso2` AS 'Country',  "
            "b.`package_type_name` AS 'PackageName',  "
            "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'NextUpdateTime', "
            "COUNT(DISTINCT a.`imsi`) AS 'all_num',  "
            "COUNT(DISTINCT (CASE WHEN ((a.`available_status` = '0')    "
            "                            AND b.`next_update_time` IS NOT NULL   "
            "                            AND b.`next_update_time` > DATE(NOW()) "
            "                            AND b.`package_status`  IN (0,1) "
            "                            AND a.business_status IN (0,4,5) "
            "                            AND (b.service_time_type = 0 "
            "                                  OR (( b.service_time_type = 1 "
            "                                       AND ((b.gmt0_time_end > NOW()  AND NOW() > '00:00:00')  "
            "                                             OR (b.gmt0_time_start < NOW() AND NOW() <= '23:59:59')"
            "                                            )  "
            "                                       AND b.gmt0_time_end < b.gmt0_time_start "
            "                                      )   "
            "                                      OR(b.service_time_type = 1 "
            "                                         AND b.gmt0_time_start < NOW() "
            "                                         AND b.gmt0_time_end > NOW()  "
            "                                         AND   b.gmt0_time_end > b.gmt0_time_start "
            "                                        )"
            "                                  )  "
            "                            ) "
            "                           ) "
            "                      THEN a.`imsi` END)) AS 'ava_num', "
            "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 "
            "                                       THEN b.`init_flow` "
            "                                       ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage'  "
            "FROM `t_css_vsim` AS a  "
            "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi`  "
            "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id`  "
            "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id`  "
            "WHERE  b.`package_type_name` IS NOT NULL "
            "       AND b.`init_flow` IS NOT NULL  " + countryStr + orgStr + simTypeStr + packageTypeNameStr + " "
            "GROUP BY a.`iso2`,b.`package_type_name`,DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H'), e.`org_name`  "
            ") "
            "ORDER BY Country,NextUpdateTime,PackageName DESC "
        )
        try:
            SimPackageInfoData = getJsonData(sys_str=sql_info['src_on_sys']['db'],
                                             data_base=sql_info['src_on_sys']['database'],
                                             query_str=str_query)
        except KeyError as keyerr:
            errInfo = ("KeyError:{}".format(keyerr))
        except mysql.connector.Error as err:
            errInfo = ("Something went wrong: {}".format(err))
        if errInfo != '':
            DicResults = {'info': {'err': True, 'errInfo': errInfo}, 'data': []}

            return DicResults
        else:
            if not SimPackageInfoData:
                DicResults = {'info': {'err': False, 'errInfo': "No Query Data"}, 'data': []}
                return DicResults
            else:
                for cs in SimPackageInfoData:
                    if type(cs['Percentage']) is decimal.Decimal:
                        cs['Percentage'] = float(cs['Percentage'])
                DicResults = {'info': {'err': True, 'errInfo': errInfo}, 'data': SimPackageInfoData}
                return DicResults


def getSimPackageFlowerAPI(sim_package_param):
    """
    
    :param sim_package_param: 
    :return: 
    """

    SimPackageInfo = getSimPackageStatic(sim_package_param)

    return json.dumps(SimPackageInfo, sort_keys=True, indent=4, default=json_util.default)
