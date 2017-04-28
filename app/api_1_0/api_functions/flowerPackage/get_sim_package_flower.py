# -*- coding: utf-8 -*-


import json
import time
import pymongo
from bson import json_util
import mysql.connector
import decimal
# sql json格式查询接口
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
# 获取连接信息
from app.api_1_0.api_functions.SqlPack.SqlLinkInfo import getFlowerQueryFunction as Sql

# 获取新架构卡资源数据库连接信息
sql_info = Sql


def timestamp_datetime(value):
    format1 = '%Y-%m-%d %H:%M:%S'
    format2 = '%Y-%m-%d'
    # value为传入的值为时间戳(整形)，如：1332888820
    structFormate = time.gmtime(value)
    # 经过localtime转换后变成结构型时间
    # 最后再经过strftime函数转换为字符型正常日期格式。
    try:
        dt = time.strftime(format1, structFormate)
    except ValueError:
        dt = time.strftime(format2, structFormate)

    return dt


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
    SimPackageInfoData = []
    countryStr = ''
    orgStr = ''
    simTypeStr = ''
    packageTypeNameStr = ''
    avaStatusStr = ''
    businessStatusStr = ''
    packageStatusStr = ''
    slotStatusStr = ''
    bamStatusStr = ''
    country = ''
    org = ''
    simType = ''
    packageTypeName = ''
    avaStatus = ''
    businessStatus = ''
    packageStatus = ''
    slotStatus = ''
    bamStatus = ''
    try:
        country = dic_param['country']
        org = dic_param['orgName']
        simType = dic_param['simType']
        packageTypeName = dic_param['packageTypeName']
        avaStatus = dic_param['avaStatus']
        businessStatus = dic_param['businessStatus']
        packageStatus = dic_param['packageStatus']
        slotStatus = dic_param['slotStatus']
        bamStatus = dic_param['bamStatus']
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
            if org == 'all':
                orgStr = ''
            else:
                orgStr = " AND e.`org_name` = '" + org + "' "
        if simType:
            simTypeStr = " AND a.`vsim_type` = '" + simType + "' "
        if packageTypeName:
            packageTypeNameStr = " AND b.`package_type_name` LIKE  '" + packageTypeName + "%' "
        if avaStatus:
            avaStatusStr = " AND a.`available_status` IN (" + avaStatus + ") "
        if businessStatus:
            businessStatusStr = " AND a.business_status IN (" + businessStatus + ") "
        if packageStatus:
            packageStatusStr = " AND b.`package_status`  IN (" + packageStatus + ") "
        if slotStatus:
            slotStatusStr = " AND a.`slot_status` IN (" + slotStatus + ") "
        if bamStatus:
            bamStatusStr = " AND a.`bam_status` IN (" + bamStatus + ") "

        str_query = (
            "( "
            "SELECT  "
            "a.`iso2`              AS 'Country',  "
            "CASE WHEN 1 THEN CONCAT('1-合计-',a.`iso2`,'-',e.`org_name` ) END  AS 'PackageName',  "
            "CASE WHEN 1 THEN '' END  AS 'NextUpdateTime',  "
            "CASE WHEN 1 THEN '' END  AS 'LastUpdateTime', "
            "COUNT(DISTINCT a.`imsi`) AS 'all_num',  "
            "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0  "
            "                                       THEN b.`init_flow` "
            "                                       ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage'  "
            "FROM `t_css_vsim` AS a  "
            "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi`  "
            "LEFT  JOIN `t_css_group` AS e          ON a.`group_id`= e.`id`  "
            "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id`  "
            "WHERE  b.`package_type_name` IS NOT NULL "
            "       AND b.`init_flow` IS NOT NULL  " + countryStr + orgStr + simTypeStr + packageTypeNameStr +
            avaStatusStr+businessStatusStr+packageStatusStr+ slotStatusStr + bamStatusStr + " "
            "GROUP BY a.`iso2`,e.`org_name`  "
            ") "
            "UNION "
            "( "
            "SELECT  "
            "a.`iso2` AS 'Country',  "
            "b.`package_type_name` AS 'PackageName',  "
            "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'NextUpdateTime', "
            "DATE_FORMAT(b.`last_update_time`,'%Y-%m-%d %H')  AS 'LastUpdateTime', "
            "COUNT(DISTINCT a.`imsi`) AS 'all_num',  "
            "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 "
            "                                       THEN b.`init_flow` "
            "                                       ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage'  "
            "FROM `t_css_vsim` AS a  "
            "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi`  "
            "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id`  "
            "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id`  "
            "WHERE  b.`package_type_name` IS NOT NULL "
            "       AND b.`init_flow` IS NOT NULL  " + countryStr + orgStr + simTypeStr + packageTypeNameStr +
            avaStatusStr+businessStatusStr+packageStatusStr+ slotStatusStr + bamStatusStr + " "
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


def getPackageFlower(flower_param, package_info):
    """
    
    :param flower_param: 
    :return: 
    """
    list_str_imsi = []
    query_type = ''
    list_time = []
    add_group_key = []
    errInfo = ''
    groupID = {'imsi': "$imsi"}
    try:
        query_type = flower_param['query_type']
        list_time = flower_param['list_time']
        add_group_key = flower_param['add_group_key']
    except KeyError as kerr:
        errInfo = 'erro:' + kerr
    for pi in package_info:
        list_str_imsi.append(''.join(["'", str(pi['ismi']), "'"]))

    if add_group_key:
        for add_key in  add_group_key :
            if add_key == 'time':
                addID = {'time': "$createtime"}
            else:
                continue
            groupID.update(addID)
    if query_type == 'hour':
        if list_time:
            begin_time_unix = int(list_time[0]['begin'])*1000
            end_time_unix = int(list_time[0]['end'])*1000
            matchStages = {'createtime': {'$gte': begin_time_unix, '$lt': end_time_unix},
                           'imsi': {'$in': list_str_imsi}
                           }
            pipeline = [
                {"$match": matchStages
                 },
                {"$group": {
                    "_id": groupID,
                    'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
                }
                }]
            connection = pymongo.MongoClient(sql_info['queryhourFlower']['uri'])
            aggeData = list(connection.get_database(sql_info['queryhourFlower']['db']
                                                    ).get_collection(sql_info['queryhourFlower']['collection']
                                                                     ).aggregate(pipeline)
                            )
            for i in range(len(aggeData)):
                agg_id_temp = aggeData[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
                aggeData[i].update(agg_id_temp)
                aggeData[i]['Flower'] = round(((aggeData[i]['Flower']) / 1024 / 1024), 2)  # 流量输出为MB
                if add_group_key is not None:
                    if ('time' in add_group_key) and ('time' in aggeData[i]):
                        aggeData[i]['time'] = timestamp_datetime(aggeData[i]['time'] / 1000)
            connection.close()
        else:
            errInfo = '小时查询流量有误'

    if errInfo:
        DicResults = {'info': {'err': True, 'errInfo': errInfo}, 'data': []}
        return DicResults




def getPackageInfo(package_set_param, flower_set_param):
    """
    
    :param package_set_param: 
    :return: 
    """
    packageInfoData = []
    country = ''
    org = ''
    sim_type = ''
    package_type_name = ''
    next_update_time = ''
    ava_status = ''
    business_status = ''
    package_status = ''
    slot_status = ''
    bam_status = ''
    errInfo = ''
    countryStr = ''
    simTypeStr = ''
    packageTypeNameStr = ''
    nextUpdateTimeStr = ''
    avaStatusStr = ''
    businessStatusStr = ''
    packageStatusStr = ''
    slotStatusStr = ''
    bamStatusStr = ''
    try:
        country = package_set_param['country']
        org = package_set_param['org']
        sim_type = package_set_param['sim_type']
        package_type_name = package_set_param['package_type_name']
        next_update_time = package_set_param['next_update_time']
        ava_status = package_set_param['ava_status']
        business_status = package_set_param['business_status']
        package_status = package_set_param['package_status']
        slot_status = package_set_param['slot_status']
        bam_status = package_set_param['bam_status']
    except KeyError as kerr:
        errInfo = 'erro:' + kerr
    if country:
        countryStr = "AND a.`iso2` = '" + country + "'"
    if org:
        if org == 'all':
            orgStr = ''
        else:
            orgStr = " AND e.`org_name` = '" + org + "' "
    if sim_type:
        simTypeStr = " AND a.`vsim_type` = '" + sim_type + "' "
    if package_type_name:
        packageTypeNameStr = " AND b.`package_type_name` =  '" + package_type_name + "' "
    if next_update_time:
        nextUpdateTimeStr = " AND DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H') = '" + next_update_time+ "'"
    if ava_status:
        avaStatusStr = " AND a.`available_status` IN (" + ava_status + ") "
    if business_status:
        businessStatusStr = " AND a.business_status IN (" + business_status + ") "
    if package_status:
        packageStatusStr = " AND b.`package_status`  IN (" + package_status + ") "
    if slot_status:
        slotStatusStr = " AND a.`slot_status` IN (" + slot_status + ") "
    if bam_status:
        bamStatusStr = " AND a.`bam_status` IN (" + bam_status + ") "

    query_str = (
        "SELECT  "
        "a.`iso2` AS 'country', "
        "a.`imsi` AS 'imsi',  "
        "b.`package_type_name` AS 'package_name',  "
        "a.`iccid` AS 'iccid' "
        "FROM `t_css_vsim` AS a  "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi`  "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id`  "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id`  "
        "WHERE   b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` IS NOT NULL " + errInfo + countryStr + simTypeStr + packageTypeNameStr +
        nextUpdateTimeStr + avaStatusStr + businessStatusStr + packageStatusStr + slotStatusStr + bamStatusStr
    )
    try:
        packageInfoData = getJsonData(sys_str=sql_info['src_on_sys']['db'],
                                      data_base=sql_info['src_on_sys']['database'],
                                      query_str=query_str)
    except KeyError as keyerr:
        errInfo = ("KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        errInfo = ("Something went wrong: {}".format(err))
    if errInfo != '':
        DicResults = {'info': {'err': True, 'errInfo': errInfo}, 'data': []}

        return DicResults
    else:
        if not packageInfoData:
            DicResults = {'info': {'err': False, 'errInfo': "无改套餐对应资源信息！"}, 'data': []}
            return DicResults
        else:

            package_flower_data = getPackageFlower(flower_param=flower_set_param, package_info=packageInfoData)
            DicResults = {'info': {'err': True, 'errInfo': errInfo}, 'data': packageInfoData}

            return DicResults


def getSimPackageFlowerNextAPI(package_data, flower_data):
    """
    
    :param package_data: 
    :param flower_data: 
    :return: 
    """
    package_info = getPackageInfo(package_set_param=package_data, flower_set_param=flower_data)

    return json.dumps(package_info, sort_keys=True, indent=4, default=json_util.default)
