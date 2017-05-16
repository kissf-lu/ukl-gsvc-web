# -*- coding: utf-8 -*-


import json
import time
import pymongo
import pymongo.errors as pymongo_err
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
    struct_formate = time.gmtime(value)
    # 经过localtime转换后变成结构型时间
    # 最后再经过strftime函数转换为字符型正常日期格式。
    try:
        dt = time.strftime(format1, struct_formate)
    except ValueError:
        dt = time.strftime(format2, struct_formate)

    return dt


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


def get_sim_package_static(dic_param):
    """
    
    :param dic_param: 
    :return: 
    """
    errinfo = ''
    sim_package_info_data = []
    country_str = ''
    org_str = ''
    sim_type_str = ''
    package_type_name_str = ''
    ava_status_str = ''
    business_status_str = ''
    package_status_str = ''
    slot_status_str = ''
    bam_status_str = ''
    country = ''
    org = ''
    sim_type = ''
    package_type_name = ''
    ava_status = ''
    business_status = ''
    package_status = ''
    slot_status = ''
    bam_status = ''
    try:
        country = dic_param['country']
        org = dic_param['orgName']
        sim_type = dic_param['simType']
        package_type_name = dic_param['packageTypeName']
        ava_status = dic_param['avaStatus']
        business_status = dic_param['businessStatus']
        package_status = dic_param['packageStatus']
        slot_status = dic_param['slotStatus']
        bam_status = dic_param['bamStatus']
    except KeyError as ke:
        errinfo = ('api simPackageInfo static param keyErr:{}：'.format(ke))
    if errinfo:
        dic_data = []
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': dic_data}
        return dic_results
    else:
        if country:
            country_str = "AND a.`iso2` = '" + country + "'"
        if org:
            if org == 'all':
                org_str = ''
            else:
                org_str = " AND e.`org_name` = '" + org + "' "
        if sim_type:
            sim_type_str = " AND a.`vsim_type` = '" + sim_type + "' "
        if package_type_name:
            package_type_name_str = " AND b.`package_type_name` LIKE  '" + package_type_name + "%' "
        if ava_status:
            ava_status_str = " AND a.`available_status` IN (" + ava_status + ") "
        if business_status:
            business_status_str = " AND a.business_status IN (" + business_status + ") "
        if package_status:
            package_status_str = " AND b.`package_status`  IN (" + package_status + ") "
        if slot_status:
            slot_status_str = " AND a.`slot_status` IN (" + slot_status + ") "
        if bam_status:
            bam_status_str = " AND a.`bam_status` IN (" + bam_status + ") "

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
            "       AND b.`init_flow` IS NOT NULL  " + country_str + org_str + sim_type_str + package_type_name_str +
            ava_status_str + business_status_str + package_status_str + slot_status_str + bam_status_str + " "
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
            "       AND b.`init_flow` IS NOT NULL  " + country_str + org_str + sim_type_str + package_type_name_str +
            ava_status_str + business_status_str + package_status_str + slot_status_str + bam_status_str + " "
            "GROUP BY a.`iso2`,b.`package_type_name`,DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H'), e.`org_name`  "
            ") "
            "ORDER BY Country,NextUpdateTime,PackageName DESC "
        )
        try:
            sim_package_info_data = getJsonData(sys_str=sql_info['src_on_sys']['db'],
                                                data_base=sql_info['src_on_sys']['database'],
                                                query_str=str_query)
        except KeyError as ke:
            errinfo = ("KeyError:{}".format(ke))
        except mysql.connector.Error as err:
            errinfo = ("Something went wrong: {}".format(err))
        if errinfo != '':
            dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
            return dic_results
        else:
            if not sim_package_info_data:
                dic_results = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}
                return dic_results
            else:
                for cs in sim_package_info_data:
                    if type(cs['Percentage']) is decimal.Decimal:
                        cs['Percentage'] = float(cs['Percentage'])
                dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': sim_package_info_data}
                return dic_results


def get_sim_package_flower_api(sim_package_param):
    """
    
    :param sim_package_param: 
    :return: 
    """

    sim_package_info = get_sim_package_static(sim_package_param)

    return json.dumps(sim_package_info, sort_keys=True, indent=4, default=json_util.default)


def mongo_agg_hour(db_str, pip_line, origin_db, append_group_list):
    """
    为查询时间间隔小于等于3天的小时表流量聚合函数
    :param db_str:                 数据库设置参数，key:value类型数据
    :param pip_line:               mongodb pip line 命令参数 
    :param origin_db:              type:list [{},{},...]， 原始数据，默认为上次查询的基础数据
    :param append_group_list:      tyep:list [], 追加计算参数
    :return:                       type:dic, 返回带有附加查询信息的dic类型数据至前端
    """
    agg_data = []
    errinfo = ''
    connection = pymongo.MongoClient(sql_info[db_str]['uri'])
    try:
        agg_data = list(connection.get_database(sql_info[db_str]['db']
                                                ).get_collection(sql_info[db_str]['collection']
                                                                 ).aggregate(pip_line)
                        )
    except KeyError as k_err:
        errinfo = 'erro:' + str(k_err)
    except pymongo_err.OperationFailure:
        errinfo = "DataBase Authentication failed!"
    except pymongo_err.NetworkTimeout:
        errinfo = "DataBase Connection Exceeded SocketTimeoutMS!"
    except pymongo_err.InvalidStringData as isd:
        errinfo = 'err:' + str(isd)
    except:
        errinfo = "Unexpected error"
    connection.close()
    if errinfo:
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
        return dic_results
    else:
        if agg_data:
            for fd in agg_data:
                # {‘_id’:{}}转换成标准json数据
                agg_id_temp = fd.pop('_id')
                fd.update(agg_id_temp)
                # 获得MB 单位流量
                fd['Flower'] = round((fd['Flower'] / 1024 / 1024), 2)
            # 流量合并至套餐表单中
            for pd in origin_db['data']:
                pd_flower_if = False
                for fd in agg_data:
                    if str(pd['imsi']) == fd['imsi']:
                        pd['flower'] = fd['Flower']
                        pd_flower_if = True
                        break
                if not pd_flower_if:
                    pd['flower'] = 0
            # 当percentage_f存在时，前端要求获取oss流量利用率
            if 'percentage_f' in append_group_list:
                for pd in origin_db['data']:
                    pd['percentage_f'] = round((pd['flower'] / (pd['init_flow'] / 1024 / 1024)) * 100, 2)
            if 'dispatch_once_flower' in append_group_list:
                for pd in origin_db['data']:
                    pd['dispatch_once_flower'] = round((pd['flower'] / pd['dispatch_con']), 2)
            dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': origin_db}
            return dic_results
        else:
            dic_results = {'info': {'err': False, 'errinfo': '无查询结果'}, 'data': []}
            return dic_results


def mongo_agg_day(db_str, pip_line_hour, pip_line_day, origin_db, append_group_list):
    """
    为查询时间间隔大于3天的天流量聚合函数
    :param db_str: 
    :param pip_line_hour:           mongodb pip line 命令参数, hour聚合
    :param pip_line_day:            mongodb pip line 命令参数，day聚合
    :param append_group_list:       type:list [], 追加计算参数， 用于选择附加输出信息
    :param origin_db:               type:list [{},{},...]， 原始数据，默认为上次查询的基础数据
    :return: 
    """
    agg_data_hour = []
    agg_data_day = []
    errinfo = ''

    connection_hour = pymongo.MongoClient(sql_info[db_str['hour']]['uri'])
    connection_day = pymongo.MongoClient(sql_info[db_str['day']]['uri'])
    try:
        agg_data_hour = list(connection_hour.get_database(
            sql_info[db_str['hour']]['db']).get_collection(
            sql_info[db_str['hour']]['collection']).aggregate(pip_line_hour)
                             )
        agg_data_day = list(connection_day.get_database(
            sql_info[db_str['day']]['db']).get_collection(
            sql_info[db_str['day']]['collection']).aggregate(pip_line_day)
                            )
    except KeyError as k_err:
        errinfo = 'erro:' + str(k_err)
    except pymongo_err.OperationFailure:
        errinfo = "DataBase Authentication failed!"
    except pymongo_err.NetworkTimeout:
        errinfo = "DataBase Connection Exceeded SocketTimeoutMS!"
    except pymongo_err.InvalidStringData as isd:
        errinfo = 'err:' + str(isd)
    except:
        errinfo = "Unexpected error"
    connection_hour.close()
    connection_day.close()
    if errinfo:
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
        return dic_results
    else:
        if agg_data_day or agg_data_hour:
            try:
                # 天流量整形
                for i in range(len(agg_data_day)):
                    agg_id_temp = agg_data_day[i].pop('_id')  # {‘_id’:{}}释放_id内的数据至外层
                    agg_data_day[i].update(agg_id_temp)
                    agg_data_day[i]['Flower'] = round(((agg_data_day[i]['Flower']) / 1024 / 1024),
                                                      2)  # 流量输出为MB
                # 小时流量整形
                for i in range(len(agg_data_hour)):
                    agg_id_temp = agg_data_hour[i].pop('_id')  # {‘_id’:{}}释放_id内的数据至外层
                    agg_data_hour[i].update(agg_id_temp)
                    agg_data_hour[i]['Flower'] = round(((agg_data_hour[i]['Flower']) / 1024 / 1024),
                                                       2)  # 流量输出为MB
                # 天套餐流量合并至信息表
                for pd in origin_db['data']:
                    pd_flower_if = False
                    for fd in agg_data_day:
                        if str(pd['imsi']) == fd['imsi']:
                            pd['flower'] = fd['Flower']
                            pd_flower_if = True
                            # fd数据为流量日志数据表imsi纬度聚合结果，故每个dic数据imsi无重直，故用break逻辑
                            break
                    # 如果没有匹配到相应的imsi数据，说明该imsi无该次查询流量信息，为0
                    if not pd_flower_if:
                        pd['flower'] = 0
                # origin_db为首次查询套餐信息的基础表，故每个imsi都有，即在imsi纬度，origin_db包含agg_data_hour
                for fd in agg_data_hour:
                    for pd in origin_db['data']:
                        if str(pd['imsi']) == fd['imsi']:
                            # 前端需要精度为2位的小数
                            pd['flower'] = round(pd['flower'] + fd['Flower'], 2)
                            break
                # 计算OSS数据库中的单个imsi流量使用率
                # 当percentage_f存在时，进行计算处理
                if 'percentage_f' in append_group_list:
                    for pd in origin_db['data']:
                        pd['percentage_f'] = round((pd['flower'] / (pd['init_flow'] / 1024 / 1024)) * 100, 2)
                # 当 dispatch_once_flower 存在时，进行单次分卡流量指标统计
                if 'dispatch_once_flower' in append_group_list:
                    for pd in origin_db['data']:
                        pd['dispatch_once_flower'] = round(((pd['flower']) / pd['dispatch_con']), 2)
            # 错误标记-keyerr
            except KeyError as ke:
                errinfo = ('完成流量查询，天流量整形出现错误,KeyError: '.format(ke))
            if errinfo:
                dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
                return dic_results
            else:
                dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': origin_db}
                return dic_results
        else:
            errinfo = '完成流量查询, 无对应套餐流量使用记录！'
            dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': []}
            return dic_results


def get_package_flower(flower_param, package_info):
    """
    
    :param flower_param: 
    :param package_info: 
    :return: 
    """
    agg_data = []
    list_str_imsi = []
    query_type = ''
    list_time = []
    # add_group_key 为前端传入的附加输出选项，用于选择是否计算附加输出信息
    # 目前天流量附加聚合key为 ： percentage_f  为oss流量使用率
    add_group_key = []
    errinfo = ''
    group_id = {'imsi': "$imsi"}
    try:
        query_type = flower_param['query_type']
        list_time = flower_param['list_time']
        add_group_key = flower_param['add_group_key']
    except KeyError as kerr:
        errinfo = '参数设置错误-1：' + str(kerr)
    if errinfo:
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
        return dic_results
    else:
        for pi in package_info['data']:
            list_str_imsi.append(str(pi['imsi']))
        # #----------------------------------hour/day-----------------------------#
        # query type 为 hour / day （GMT0时间）
        #
        #    1、hour 查询时间前端规定为3天(包括)
        #    2、day 查询为超过3天为，day查询分为小时查询及天查询
        if query_type == 'hour':
            if list_time:
                begin_time_unix = int(list_time[0]['begin']) * 1000
                end_time_unix = int(list_time[0]['end']) * 1000
                matchStages = {'createtime': {'$gte': begin_time_unix, '$lt': end_time_unix},
                               'imsi': {'$in': list_str_imsi}
                               }
                pipeline = [
                    {"$match": matchStages
                     },
                    {"$group": {
                        "_id": group_id,
                        'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
                    }
                    }]
                flower_data_hour = mongo_agg_hour(db_str='queryhourFlower',
                                                  pip_line=pipeline,
                                                  origin_db=package_info,
                                                  append_group_list=add_group_key)
                return flower_data_hour
            else:
                errinfo = '小时查询的时间参数为空!'
                dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
                return dic_results
        elif query_type == 'day':
            or_hour_match = []
            day_match = {}
            if list_time:
                # 天查询为三段式查询，[{开头时间}，{中间时间}, {结尾时间}]
                # 为实现起止查询时间小时颗粒度华，{开头时间}和{结尾时间}都为小时纬度查询，{中间时间}为天纬度查询
                for i in range(len(list_time)):
                    # if i !=1 表示不取中间天纬度时间，只取两头小时纬度时间
                    if i != 1:
                        or_hour_match.append({'createtime': {'$gte': int(list_time[i]['begin']) * 1000,
                                                             '$lt': int(list_time[i]['end']) * 1000
                                                             }
                                              })
                    else:
                        day_match = {'createtime': {'$gte': int(list_time[i]['begin']) * 1000,
                                                    '$lt': int(list_time[i]['end']) * 1000
                                                    }
                                     }
                hour_match_stages = {'$or': or_hour_match,
                                     'imsi': {'$in': list_str_imsi}}
                day_match_stages = {'createtime': day_match['createtime'],
                                    'imsi': {'$in': list_str_imsi}}
                pipeline_hour = [
                    {"$match": hour_match_stages
                     },
                    {"$group": {
                        "_id": group_id,
                        'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
                    }
                    }]
                pipeline_day = [
                    {"$match": day_match_stages
                     },
                    {"$group": {
                        "_id": group_id,
                        'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
                    }
                    }]
                db_str = {
                    'hour': 'queryhourFlower',
                    'day': 'querydayFlower'
                }
                flower_data_day = mongo_agg_day(db_str=db_str,
                                                pip_line_hour=pipeline_hour,
                                                pip_line_day=pipeline_day,
                                                origin_db=package_info,
                                                append_group_list=add_group_key)
                return flower_data_day
            else:
                errinfo = '天时间设置列表为空列表！'
                dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
                return dic_results
        else:
            errinfo = '存在不合法的查询类型：hour , day！'
            dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
            return dic_results


def get_package_info(package_set_param):
    """
    
    :param package_set_param: 
    :return: 
    """
    packageInfoData = []
    add_key = []
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
    errinfo = ''
    org_str = ''
    country_str = ''
    sim_type_str = ''
    package_type_name_str = ''
    next_update_time_str = ''
    ava_status_str = ''
    business_status_str = ''
    package_status_str = ''
    slot_status_str = ''
    bam_status_str = ''
    sim_agg_str = ''
    last_update_time_str = ''
    percentage_fs_str = ''
    dispatch_con_str = ''
    dispatch_where_time_set = ''
    dispatch_begin_time = ''
    dispatch_end_time = ''

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
        add_key = package_set_param['add_group_key']
        dispatch_begin_time = package_set_param['dispatch_begin_time']
        dispatch_end_time = package_set_param['dispatch_end_time']
    except KeyError as kerr:
        errinfo = ("Something went wrong as KeyError: {}".format(kerr))
    if errinfo:
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': packageInfoData}

        return dic_results

    else:
        if country:
            country_str = "AND a.`iso2` = '" + country + "'"
        if org:
            if org == 'all':
                org_str = ''
            else:
                org_str = " AND e.`org_name` = '" + org + "' "
        if sim_type:
            sim_type_str = " AND a.`vsim_type` = '" + sim_type + "' "
        if package_type_name:
            package_type_name_str = " AND b.`package_type_name` =  '" + package_type_name + "' "
        if next_update_time:
            next_update_time_str = " AND DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H') = '" + next_update_time + "'"
        if ava_status:
            ava_status_str = " AND a.`available_status` IN (" + ava_status + ") "
        if business_status:
            business_status_str = " AND a.business_status IN (" + business_status + ") "
        if package_status:
            package_status_str = " AND b.`package_status`  IN (" + package_status + ") "
        if slot_status:
            slot_status_str = " AND a.`slot_status` IN (" + slot_status + ") "
        if bam_status:
            bam_status_str = " AND a.`bam_status` IN (" + bam_status + ") "
        if add_key:
            if 'sim_agg' in add_key:
                # 套餐网络集合聚合设置
                sim_agg_str = "p.`name` AS 'sim_agg',  "
            if 'last_update_time' in add_key:
                last_update_time_str = "DATE_FORMAT(b.`last_update_time`,'%Y-%m-%d %H')  AS 'last_update_time', "
            if 'percentage_fs' in add_key:
                # SAAS系统卡流量使用率统计设置
                percentage_fs_str = ("CAST((b.`total_use_flow`/ b.`init_flow`)*100  AS DECIMAL(64,1)) "
                                     "AS 'percentage_fs',  ")
            if ('dispatch_con' in add_key) or ('dispatch_once_flower' in add_key):
                # 分卡次数统计参数设置, 统计分卡次数或单次分卡流量大小时要统计此数据
                dispatch_con_str = "count(d.`imsi`) as 'dispatch_con', "
                dispatch_where_time_set = (" AND '" +
                                           dispatch_begin_time + "'<= d.`create_time`<'" + dispatch_end_time + "' ")
        query_str = (
            "SELECT  "
            "a.`iso2` AS 'country', "
            "a.`imsi` AS 'imsi',  "
            "b.`package_type_name` AS 'package_name',  "
            "b.`init_flow`,  "
            "a.`iccid` AS 'iccid', " + sim_agg_str + last_update_time_str + " "
            ""+percentage_fs_str+dispatch_con_str+" "
            "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'next_update_time' "
            "FROM `t_css_vsim` AS a  "
            "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi`  "
            "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id`  "
            "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id`  "
            "LEFT  JOIN `t_css_plmnset` AS p ON a.`plmnset_id`=p.`id`  "
            "LEFT  JOIN `t_css_user_vsim_log` AS d  ON d.`imsi` = a.`imsi` " 
            "WHERE   b.`package_type_name` IS NOT NULL "
            "        AND b.`init_flow` IS NOT NULL " + org_str + country_str + sim_type_str + package_type_name_str +
            next_update_time_str + ava_status_str + business_status_str + package_status_str + slot_status_str +
            bam_status_str + dispatch_where_time_set+" "
            "GROUP BY a.`iso2`, a.`imsi`, b.`package_type_name`"
        )
        try:
            packageInfoData = getJsonData(sys_str=sql_info['src_on_sys']['db'],
                                          data_base=sql_info['src_on_sys']['database'],
                                          query_str=query_str)
        except KeyError as keyerr:
            errinfo = ("KeyError:{}".format(keyerr))
        except mysql.connector.Error as err:
            errinfo = ("Something went wrong: {}".format(err))
        if errinfo != '':
            dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
            return dic_results
        else:
            if not packageInfoData:
                dic_results = {'info': {'err': False, 'errinfo': "无改套餐对应资源信息！"}, 'data': []}

                return dic_results
            else:
                for cs in packageInfoData:
                    if 'percentage_fs' in cs.keys():
                        if type(cs['percentage_fs']) is decimal.Decimal:
                            cs['percentage_fs'] = float(cs['percentage_fs'])
                dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': packageInfoData}

                return dic_results


def get_sim_package_flower_next_api(package_data, flower_data):
    """
    
    :param package_data: 
    :param flower_data: 
    :return: 
    """
    package_info = get_package_info(package_set_param=package_data)
    if not package_info['data']:
        return json.dumps(package_info, sort_keys=True, indent=4, default=json_util.default)
    else:
        package_flower_data = get_package_flower(flower_param=flower_data, package_info=package_info)

        return json.dumps(package_flower_data, sort_keys=True, indent=4, default=json_util.default)
