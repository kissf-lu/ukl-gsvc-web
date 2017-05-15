# -*- coding: utf-8 -*-


import json
from bson import json_util
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
import time
import pymongo
import pymongo.errors as py_mongo_error
import datetime
# 获取连接信息
from app.api_1_0.api_functions.SqlPack.SqlLinkInfo import getFlowerQueryFunction as Sql
# 获取新架构卡资源数据库连接信息
sql_info = Sql


def datetime_timestamp(dt):
    #  dt为字符串标准时间，返回的s为unix时间戳
    #  time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    #  time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28,
    #  tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # �?"2012-03-28 06:53:40"转化为时间戳
    try:
        # 此处为了匹配长天格式时间
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    except ValueError:
        # 此处为了匹配短天格式时间
        s = time.mktime(time.strptime(dt, '%Y-%m-%d'))
    return int(s)


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


def StrTimeTOUnix(dt, format_str):
    """=====================================

    :param dt:
    :param format_str:
    :return:
    ==============================================="""
    s = time.mktime(time.strptime(dt, format_str))

    return s


def unix_2_str_time(value, format_str):
    """============================================

    :param value:
    :param format_str:
    :return:
    "==============================================="""
    # 最后再经过strftime函数转换为字符型正常日期格式。
    dt = time.strftime(format_str, time.localtime(value))
    return dt


def get_gmt0_str_time(str_time, offset):
    """============================
    :param str_time:
    :param offset:
    :return:
    ==============================="""
    try:
        gmt0_date_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')-datetime.timedelta(minutes=offset)
    except ValueError:
        gmt0_date_time = datetime.datetime.strptime(str_time, '%Y-%m-%d') - datetime.timedelta(minutes=offset)

    return str(gmt0_date_time)


def getlistimsi(Data):
    """===========================

    :param Data:
    :return: list_imsi
    ===================================="""
    imsi_data = Data
    list_imsi = []
    if type(imsi_data) is dict:
        for data in imsi_data:
            list_imsi.append(str(data['imsi']))
    elif type(imsi_data) is list:
        for data in imsi_data:
            list_imsi.append(str(data))

    elif type(imsi_data) is str:
        for data in imsi_data.split(','):
            list_imsi.append(data)

    else:
        list_imsi = []

    return list_imsi


def getJosonData(sysStr, Database, query_str):
    """=======================================

    :param sysStr:
    :param Database:
    :param query_str:
    ===========================================
    :return:
    ============================================"""
    jsonResults = qureResultAsJson(sysStr=sysStr,
                                   Database=Database,
                                   query_str=query_str,
                                   where=[])
    return jsonResults


def get_hours_flower(imsi, list_time, mcc, plmn, flower_key):
    """===================================
    :param imsi: type [],
    :param list_time:
    :param mcc: 流量日志表mcc查询条件
    :param plmn: 流量日志表plmn 查询条件
    :param flower_key: mongo group id, 用于添加不同group维度
    =======================================
    :return:
    ======================================="""
    list_imsi = imsi
    # 查询起始和截止时间
    flower_begin_time = list_time[0]['begin']
    flower_end_time = list_time[0]['end']
    query_mcc = mcc
    query_plmn = plmn
    group_item = flower_key
    group_id = {'imsi': "$imsi"}
    if group_item is None:
        keys_null = 'NULL'
    else:
        for keys in group_item:
            if keys == 'plmn':
                add_id = {'plmn': "$plmn"}
            elif keys == 'time':
                add_id = {'time': "$createtime"}
            elif keys == 'mcc':
                add_id = {'mcc': "$mcc"}
            elif keys == 'lac':
                add_id = {'lac': "$lac"}
            else:
                continue
            group_id.update(add_id)

    # Match Stages Set
    # Unix Time Make
    begin_l_unix = int(flower_begin_time)*1000  # (datetime_timestamp(flower_begin_time)) * 1000
    end_l_unix = int(flower_end_time)*1000      # (datetime_timestamp(flower_end_time)) * 1000
    if query_plmn and query_mcc:
            match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi},
                            'mcc': query_mcc,
                            'plmn': query_plmn
                            }
    elif query_mcc and not query_plmn:
            match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi},
                            'mcc': query_mcc
                            }
    elif not query_mcc and query_plmn:
            match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi},
                            'plmn': query_plmn
                            }
    else:
        match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                        'imsi': {'$in': list_imsi}
                        }
    pipeline = [
        {"$match": match_stages
         },
        {"$group": {
            "_id": group_id,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection = pymongo.MongoClient(sql_info['queryhourFlower']['uri'])
    agge_data = list(connection.get_database(sql_info['queryhourFlower']['db']
                                             ).get_collection(sql_info['queryhourFlower']['collection']
                                                              ).aggregate(pipeline)
                     )
    for i in range(len(agge_data)):
        agg_id_temp = agge_data[i].pop('_id')
        agge_data[i].update(agg_id_temp)
        agge_data[i]['Flower'] = round(((agge_data[i]['Flower'])/1024/1024), 2)
        if group_item is not None:
            if ('time' in group_item) and ('time' in agge_data[i]):
                agge_data[i]['time'] = timestamp_datetime(agge_data[i]['time']/1000)
    connection.close()

    return agge_data


def get_days_flower(imsi, begin_time, end_time, mcc, plmn, flower_key):
    """

    :param imsi:
    :param begin_time:
    :param end_time:
    :param mcc:
    :param plmn:
    :param flower_key:
    :return:
    """
    list_imsi = imsi
    # 查询起始和截止时间
    flower_begin_time = begin_time
    flower_end_time = end_time
    query_mcc = mcc
    query_plmn = plmn
    group_item = flower_key
    group_id = {'imsi': "$imsi"}
    if group_item is None:
        keys_null = 'NULL'
    else:
        for keys in group_item:
            if keys == 'plmn':
                add_id = {'plmn': "$plmn"}
            elif keys == 'time':
                add_id = {'time': "$createtime"}
            elif keys == 'mcc':
                add_id = {'mcc': "$mcc"}
            elif keys == 'lac':
                add_id = {'lac': "$lac"}
            else:
                continue

            group_id.update(add_id)

    # Match Stages Set---------------------------------------------------
    # Unix Time Make
    begin_l_unix = int(flower_begin_time)*1000
    end_l_unix = int(flower_end_time)*1000
    if query_plmn and query_mcc:
            match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi},
                            'mcc': query_mcc,
                            'plmn': query_plmn
                            }
    elif query_mcc and not query_plmn:
            match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi},
                            'mcc': query_mcc
                            }
    elif not query_mcc and query_plmn:
            match_stages = {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi},
                            'plmn': query_plmn
                            }
    else:
        match_stages = {'createtime': {'$gte': begin_l_unix, '$lte': end_l_unix},
                        'imsi': {'$in': list_imsi}
                        }
    pipeline = [
        {"$match": match_stages
         },
        {"$group": {
            "_id": group_id,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection = pymongo.MongoClient(sql_info['querydayFlower']['uri'])
    agge_data = list(connection.get_database(sql_info['querydayFlower']['db']
                                             ).get_collection(sql_info['querydayFlower']['collection']
                                                              ).aggregate(pipeline)
                     )
    for i in range(len(agge_data)):
        agg_id_temp = agge_data[i].pop('_id')         # {‘_id’:{}}转换成标准json数据
        agge_data[i].update(agg_id_temp)
        agge_data[i]['Flower'] = round(((agge_data[i]['Flower'])/1024/1024), 2)  # 流量输出为MB
        if group_item is not None:
            if ('time' in group_item) and ('time' in agge_data[i]):
                agge_data[i]['time'] = timestamp_datetime(agge_data[i]['time']/1000)
    connection.close()

    return agge_data


def get_days_flower_thr_time(imsi, time_list, mcc, plmn, flower_key):
    """
    
    :param imsi: 
    :param time_list: 
    :param mcc: 
    :param plmn: 
    :param flower_key: 
    :return: 
    """
    list_imsi = imsi
    list_time = time_list
    query_mcc = mcc
    query_plmn = plmn
    group_item = flower_key
    group_id = {'imsi': "$imsi"}
    or_hour_match = []
    day_match = {}
    return_data = []
    if list_time:
        for i in range(len(list_time)):
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
                         'imsi': {'$in': list_imsi}}
    day_match_stages = {'createtime': day_match['createtime'],
                        'imsi': {'$in': list_imsi}}
    if group_item is None:
        pass
    else:
        for keys in group_item:
            if keys == 'plmn':
                add_id = {'plmn': "$plmn"}
            elif keys == 'time':
                add_id = {'time': "$createtime"}
            elif keys == 'mcc':
                add_id = {'mcc': "$mcc"}
            elif keys == 'lac':
                add_id = {'lac': "$lac"}
            else:
                continue

            group_id.update(add_id)

    if query_plmn:
        hour_match_stages.update({
            'plmn': query_plmn
        })
        day_match_stages.update({
            'plmn': query_plmn
        })

    if query_mcc:
        hour_match_stages.update({
            'mcc': query_mcc
        })
        day_match_stages.update({
            'mcc': query_mcc
        })
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
    connection_hour = pymongo.MongoClient(sql_info['queryhourFlower']['uri'])
    agge_data_hour = list(connection_hour.get_database(sql_info['queryhourFlower']['db']
                                                       ).get_collection(sql_info['queryhourFlower']['collection']
                                                                        ).aggregate(pipeline_hour)
                          )
    connection_hour.close()
    connection_day = pymongo.MongoClient(sql_info['querydayFlower']['uri'])
    agge_data_day = list(connection_day.get_database(sql_info['querydayFlower']['db']
                                                     ).get_collection(sql_info['querydayFlower']['collection']
                                                                      ).aggregate(pipeline_day)
                         )
    connection_day.close()

    if agge_data_day:
        for i in range(len(agge_data_day)):
            agg_id_temp = agge_data_day[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
            agge_data_day[i].update(agg_id_temp)
            agge_data_day[i]['Flower'] = round(((agge_data_day[i]['Flower']) / 1024 / 1024), 2)  # 流量输出为MB
            if group_item is not None:
                if ('time' in group_item) and ('time' in agge_data_day[i]):
                    agge_data_day[i]['time'] = timestamp_datetime(agge_data_day[i]['time'] / 1000)

    if agge_data_hour:
        for i in range(len(agge_data_hour)):
            agg_id_temp = agge_data_hour[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
            agge_data_hour[i].update(agg_id_temp)
            agge_data_hour[i]['Flower'] = round(((agge_data_hour[i]['Flower']) / 1024 / 1024), 2)  # 流量输出为MB
            if group_item is not None:
                if ('time' in group_item) and ('time' in agge_data_hour[i]):
                    # 小时表的显示时间重新设置为日
                    agge_data_hour[i]['time'] = time.strftime('%Y-%m-%d', time.gmtime(agge_data_hour[i]['time'] / 1000))

    if not group_item:
        if agge_data_day and agge_data_hour:
            return_data.extend(agge_data_day)
            # pop_lis = []
            for rd in return_data:
                temp_pop_di = None
                for i in range(len(agge_data_hour)):
                    if rd['imsi'] == agge_data_hour[i]['imsi']:
                        rd['Flower'] = round(agge_data_hour[i]['Flower'] + rd['Flower'], 2)
                        temp_pop_di = i
                        break
                if temp_pop_di is not None:
                    agge_data_hour.pop(temp_pop_di)
            if agge_data_hour:
                return_data.extend(agge_data_hour)

        elif agge_data_day and not agge_data_hour:
            return_data.extend(agge_data_day)
        elif agge_data_hour and not agge_data_day:
            return_data.extend(agge_data_hour)
        else:
            return_data = []
    else:
        if agge_data_day:
            # 完成流量合并操作
            return_data.extend(agge_data_day)
        if agge_data_hour:
            # 完成流量合并操作
            return_data.extend(agge_data_hour)

    return return_data


def get_flowers(query_sort, time_list, mcc, plmn, imsi, flower_query_key):
    """=====================================================================
    gsvc mongodb 流量查询接口函数。完成小时/月维度imsi流量查询，返回查询数据

    ========================================================================
    :param query_sort: hour/day 类型的查询，小时或天；
    :param time_list: 查询时间设置列表[]
    :param mcc: 设置查询mcc
    :param plmn: 设置查询plmn
    :param imsi: type: sting , 设置查询imsi,
    :param flower_query_key: 流量查询的附加聚合键值
    =========================================================================
    :return: 返回带有err，data信息 dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': dic_data}
    =============================================================================================================="""
    query_sort = query_sort
    list_time = time_list
    query_mcc = str(mcc)
    query_plmn = str(plmn)
    query_imsi = getlistimsi(imsi)
    query_flower_key = flower_query_key
    errinfo = ''
    dic_data = []
    if (not query_sort) or (not query_imsi) or (not list_time):
        dic_results = {'info': {'err': True, 'errinfo': '存在空类型参数'}, 'data': []}
        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
    else:
        if query_sort == 'hours':
            try:
                dic_data = get_hours_flower(imsi=query_imsi, list_time=list_time, mcc=query_mcc,
                                            plmn=query_plmn, flower_key=query_flower_key)
            except ValueError:
                errinfo = "input Date Time ValueError"
            except py_mongo_error.OperationFailure:
                errinfo = "DataBase Authentication failed!"
            except py_mongo_error.NetworkTimeout:
                errinfo = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errinfo = "Unexpected error"
            if errinfo:
                dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': dic_data}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            else:
                if dic_data:
                    dic_results = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数'}, 'data': dic_data}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
                else:
                    dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': dic_data}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        else:
            try:
                if len(time_list) == 1:
                    dic_data = get_days_flower(imsi=query_imsi, begin_time=time_list[0]['begin'],
                                               end_time=time_list[0]['end'], mcc=query_mcc,
                                               plmn=query_plmn, flower_key=query_flower_key)
                else:
                    dic_data = get_days_flower_thr_time(imsi=query_imsi, time_list=time_list, mcc=query_mcc,
                                                        plmn=query_plmn, flower_key=query_flower_key)

            except ValueError:
                errinfo = "天维度的短时间日期有问题！"
            except py_mongo_error.OperationFailure:
                errinfo = "DataBase Authentication failed!"
            except py_mongo_error.NetworkTimeout:
                errinfo = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errinfo = "Unexpected error"
            if errinfo:
                dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': dic_data}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            else:
                if dic_data:
                    dic_results = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数'}, 'data': dic_data}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
                else:
                    dic_results = {'info': {'err': False, 'errinfo': errinfo}, 'data': dic_data}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
