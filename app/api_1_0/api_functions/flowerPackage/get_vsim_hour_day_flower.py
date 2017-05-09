# -*- coding: utf-8 -*-


import json
from bson import json_util
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
import time
import pymongo
import pymongo.errors as pyMonogErr
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
    structFormate = time.gmtime(value)
    # 经过localtime转换后变成结构型时间
    # 最后再经过strftime函数转换为字符型正常日期格式。
    try:
        dt = time.strftime(format1, structFormate)
    except ValueError:
        dt = time.strftime(format2, structFormate)

    return dt


def StrTimeTOUnix(dt, format_str):
    """=====================================

    :param dt:
    :param format_str:
    :return:
    ==============================================="""
    s = time.mktime(time.strptime(dt, format_str))

    return s


def UnixTOStrTime(value, format_str):
    """============================================

    :param value:
    :param format_str:
    :return:
    "==============================================="""
    # 最后再经过strftime函数转换为字符型正常日期格式。
    dt = time.strftime(format_str, time.localtime(value))
    return dt


def getGMT0StrTime(str_time, offset):
    """=======================================
    :param str_time:
    :param offset:
    :return:
    ==========================================="""
    try:
        GMT0dateTime = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')-datetime.timedelta(minutes=offset)
    except ValueError:
        GMT0dateTime = datetime.datetime.strptime(str_time, '%Y-%m-%d') - datetime.timedelta(minutes=offset)

    return str(GMT0dateTime)


def getlistimsi(Data):
    """===========================

    :param Data:
    :return: list_imsi
    ===================================="""
    imsiData = Data
    list_imsi = []
    if type(imsiData) is dict:
        for data in imsiData:
            list_imsi.append(str(data['imsi']))
    elif type(imsiData) is list:
        for data in imsiData:
            list_imsi.append(str(data))

    elif type(imsiData) is str:
        for data in imsiData.split(','):
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


def getHoursFlower(imsi, list_time, Mcc, Plmn, FlowerKey):
    """===================================
    :param imsi: type [],
    :param list_time:
    :param Mcc: 流量日志表mcc查询条件
    :param Plmn: 流量日志表plmn 查询条件
    :param FlowerKey: mongo group id, 用于添加不同group维度
    =======================================
    :return:
    ======================================="""
    list_imsi = imsi
    returnData = []
    # 查询起始和截止时间
    flowerBegintime = list_time[0]['begin']
    flowerEndtime = list_time[0]['end']
    queryMcc = Mcc
    queryPlmn = Plmn
    groupItem = FlowerKey
    groupID = {'imsi': "$imsi"}
    if groupItem is None:
        keysNULL = 'NULL'
    else:
        for keys in groupItem:
            if keys == 'plmn':
                addID = {'plmn': "$plmn"}
            elif keys == 'time':
                addID = {'time': "$createtime"}
            elif keys == 'mcc':
                addID = {'mcc': "$mcc"}
            elif keys == 'lac':
                addID = {'lac': "$lac"}
            else:
                continue
            groupID.update(addID)

    # Match Stages Set
    # Unix Time Make
    beginLUnix = int(flowerBegintime)*1000  # (datetime_timestamp(flowerBegintime)) * 1000
    endLUnix = int(flowerEndtime)*1000      # (datetime_timestamp(flowerEndtime)) * 1000
    matchStages = {}
    if queryPlmn and queryMcc:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc,
                           'plmn': queryPlmn
                           }
    elif queryMcc and not queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc
                           }
    elif not queryMcc and queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'plmn': queryPlmn
                           }
    else:
        matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                       'imsi': {'$in': list_imsi}
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
        agg_id_temp = aggeData[i].pop('_id')                  # {‘_id’:{}}转换成标准json数据
        aggeData[i].update(agg_id_temp)
        aggeData[i]['Flower'] = round(((aggeData[i]['Flower'])/1024/1024), 2)  # 流量输出为MB
        if groupItem is not None:
            if ('time' in groupItem) and ('time' in aggeData[i]):
                aggeData[i]['time'] = timestamp_datetime(aggeData[i]['time']/1000)
    connection.close()

    return aggeData


def getDaysFlower(imsi, Begintime, Endtime, Mcc, Plmn, FlowerKey):
    """

    :param imsi:
    :param Begintime:
    :param Endtime:
    :param Mcc:
    :param Plmn:
    :param FlowerKey:
    :return:
    """
    list_imsi = imsi
    returnData = []
    # 查询起始和截止时间
    flowerBegintime = Begintime
    flowerEndtime = Endtime
    queryMcc = Mcc
    queryPlmn = Plmn
    groupItem = FlowerKey
    groupID = {'imsi': "$imsi"}
    if groupItem is None:
        keysNULL = 'NULL'
    else:
        for keys in groupItem:
            if keys == 'plmn':
                addID = {'plmn': "$plmn"}
            elif keys == 'time':
                addID = {'time': "$createtime"}
            elif keys == 'mcc':
                addID = {'mcc': "$mcc"}
            elif keys == 'lac':
                addID = {'lac': "$lac"}
            else:
                continue

            groupID.update(addID)

    # Match Stages Set---------------------------------------------------
    # Unix Time Make
    beginLUnix = int(flowerBegintime)*1000   # (datetime_timestamp(flowerBegintime)) * 1000
    endLUnix = int(flowerEndtime)*1000       # (datetime_timestamp(flowerEndtime)) * 1000
    if queryPlmn and queryMcc:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc,
                           'plmn': queryPlmn
                           }
    elif queryMcc and not queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'mcc': queryMcc
                           }
    elif not queryMcc and queryPlmn:
            matchStages = {'createtime': {'$gte': beginLUnix, '$lt': endLUnix},
                           'imsi': {'$in': list_imsi},
                           'plmn': queryPlmn
                           }
    else:
        matchStages = {'createtime': {'$gte': beginLUnix, '$lte': endLUnix},
                       'imsi': {'$in': list_imsi}
                       }
    pipeline = [
        {"$match": matchStages
         },
        {"$group": {
            "_id": groupID,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection = pymongo.MongoClient(sql_info['querydayFlower']['uri'])
    aggeData = list(connection.get_database(sql_info['querydayFlower']['db']
                                            ).get_collection(sql_info['querydayFlower']['collection']
                                                             ).aggregate(pipeline)
                    )
    for i in range(len(aggeData)):
        agg_id_temp = aggeData[i].pop('_id')         # {‘_id’:{}}转换成标准json数据
        aggeData[i].update(agg_id_temp)
        aggeData[i]['Flower'] = round(((aggeData[i]['Flower'])/1024/1024), 2)  # 流量输出为MB
        if groupItem is not None:
            if ('time' in groupItem) and ('time' in aggeData[i]):
                aggeData[i]['time'] = timestamp_datetime(aggeData[i]['time']/1000)
    connection.close()

    return aggeData


def getDaysFlowerThrTime(imsi, time_list, mcc, plmn, flower_key):
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
    queryMcc = mcc
    queryPlmn = plmn
    groupItem = flower_key
    groupID = {'imsi': "$imsi"}
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
    if groupItem is None:
        pass
    else:
        for keys in groupItem:
            if keys == 'plmn':
                addID = {'plmn': "$plmn"}
            elif keys == 'time':
                addID = {'time': "$createtime"}
            elif keys == 'mcc':
                addID = {'mcc': "$mcc"}
            elif keys == 'lac':
                addID = {'lac': "$lac"}
            else:
                continue

            groupID.update(addID)

    if queryPlmn:
        hour_match_stages.update({
            'plmn': queryPlmn
        })
        day_match_stages.update({
            'plmn': queryPlmn
        })

    if queryMcc:
        hour_match_stages.update({
            'mcc': queryMcc
        })
        day_match_stages.update({
            'mcc': queryMcc
        })
    pipeline_hour = [
        {"$match": hour_match_stages
         },
        {"$group": {
            "_id": groupID,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    pipeline_day = [
        {"$match": day_match_stages
         },
        {"$group": {
            "_id": groupID,
            'Flower': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection_hour = pymongo.MongoClient(sql_info['queryhourFlower']['uri'])
    aggeData_hour = list(connection_hour.get_database(sql_info['queryhourFlower']['db']
                                                      ).get_collection(sql_info['queryhourFlower']['collection']
                                                                       ).aggregate(pipeline_hour)
                         )
    connection_hour.close()
    connection_day = pymongo.MongoClient(sql_info['querydayFlower']['uri'])
    aggeData_day = list(connection_day.get_database(sql_info['querydayFlower']['db']
                                                    ).get_collection(sql_info['querydayFlower']['collection']
                                                                     ).aggregate(pipeline_day)
                        )
    connection_day.close()

    if aggeData_day:
        for i in range(len(aggeData_day)):
            agg_id_temp = aggeData_day[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
            aggeData_day[i].update(agg_id_temp)
            aggeData_day[i]['Flower'] = round(((aggeData_day[i]['Flower']) / 1024 / 1024), 2)  # 流量输出为MB
            if groupItem is not None:
                if ('time' in groupItem) and ('time' in aggeData_day[i]):
                    aggeData_day[i]['time'] = timestamp_datetime(aggeData_day[i]['time'] / 1000)

    if aggeData_hour:
        for i in range(len(aggeData_hour)):
            agg_id_temp = aggeData_hour[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
            aggeData_hour[i].update(agg_id_temp)
            aggeData_hour[i]['Flower'] = round(((aggeData_hour[i]['Flower']) / 1024 / 1024), 2)  # 流量输出为MB
            if groupItem is not None:
                if ('time' in groupItem) and ('time' in aggeData_hour[i]):
                    # 小时表的显示时间重新设置为日
                    aggeData_hour[i]['time'] = time.strftime('%Y-%m-%d', time.gmtime(aggeData_hour[i]['time'] / 1000))

    if not groupItem:
        if aggeData_day and aggeData_hour:
            return_data.extend(aggeData_day)
            # pop_lis = []
            for rd in return_data:
                temp_pop_di = None
                for i in range(len(aggeData_hour)):
                    if rd['imsi'] == aggeData_hour[i]['imsi']:
                        rd['Flower'] = aggeData_hour[i]['Flower'] + rd['Flower']
                        temp_pop_di = i
                        break
                if temp_pop_di is not None:
                    aggeData_hour.pop(temp_pop_di)
            if aggeData_hour:
                return_data.extend(aggeData_hour)

        elif aggeData_day and not aggeData_hour:
            return_data.extend(aggeData_day)
        elif aggeData_hour and not aggeData_day:
            return_data.extend(aggeData_hour)
        else:
            return_data = []
    else:
        if aggeData_day:
            # 完成流量合并操作
            return_data.extend(aggeData_day)
        if aggeData_hour:
            # 完成流量合并操作
            return_data.extend(aggeData_hour)

    return return_data


def getFlowers(querySort, time_list, mcc, plmn, imsi, flower_query_key, time_zone_offset):
    """=====================================================================
    gsvc mongodb 流量查询接口函数。完成小时/月维度imsi流量查询，返回查询数据

    ========================================================================
    :param querySort: hour/day 类型的查询，小时或天；
    :param time_list: 查询时间设置列表[]
    :param mcc: 设置查询mcc
    :param plmn: 设置查询plmn
    :param imsi: type: sting , 设置查询imsi,
    :param flower_query_key: 流量查询的附加聚合键值
    :param time_zone_offset: 时区，相对GMT0时间
    =========================================================================
    :return: 返回带有err，data信息 DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': DicData}
    =============================================================================================================="""
    querysort = querySort
    list_time = time_list
    queryMcc = str(mcc)
    queryPlmn = str(plmn)
    queryImsi = getlistimsi(imsi)
    queryFlowerKey = flower_query_key
    errInfo = ''
    DicData = []
    if (not querysort) or (not queryImsi) or (not list_time):
        DicResults = {'info': {'err': True, 'errinfo': '存在空类型参数'}, 'data': []}
        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
    else:
        if querysort == 'hours':
            try:
                DicData = getHoursFlower(imsi=queryImsi,
                                         list_time=list_time,
                                         Mcc=queryMcc,
                                         Plmn=queryPlmn,
                                         FlowerKey=queryFlowerKey)
            except ValueError:
                errInfo = "input Date Time ValueError"
            except pyMonogErr.OperationFailure:
                errInfo = "DataBase Authentication failed!"
            except pyMonogErr.NetworkTimeout:
                errInfo = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errInfo = "Unexpected error"
            if errInfo:
                DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': DicData}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
            else:
                if DicData:
                    DicResults = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数'}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
                else:
                    DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
        else:
            try:
                if len(time_list) == 1:
                    DicData = getDaysFlower(imsi=queryImsi,
                                            Begintime=time_list[0]['begin'],
                                            Endtime=time_list[0]['end'],
                                            Mcc=queryMcc,
                                            Plmn=queryPlmn,
                                            FlowerKey=queryFlowerKey)
                else:
                    DicData = getDaysFlowerThrTime(imsi=queryImsi,
                                                   time_list=time_list,
                                                   mcc=queryMcc,
                                                   plmn=queryPlmn,
                                                   flower_key=queryFlowerKey)

            except ValueError:
                errInfo = "天维度的短时间日期有问题！"                     # 'Database Error!'
            except pyMonogErr.OperationFailure:
                errInfo = "DataBase Authentication failed!"
            except pyMonogErr.NetworkTimeout:
                errInfo = "DataBase Connection Exceeded SocketTimeoutMS!"
            except:
                errInfo = "Unexpected error"
            if errInfo:
                DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': DicData}
                return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
            else:
                if DicData:
                    DicResults = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数'}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
                else:
                    DicResults = {'info': {'err': False, 'errinfo': errInfo}, 'data': DicData}
                    return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)
