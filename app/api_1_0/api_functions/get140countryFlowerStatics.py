# -*- coding: utf-8 -*-

# import sys
import json
from bson import json_util
import mysql.connector
from .SqlPack.SQLModel import qureResultAsJson
import time
import datetime
import pymongo
import pymongo.errors as mongodb_error
# from SqlPack.pyMongoModel import (sql_info)
from .SqlPack.SqlLinkInfo import get140countryFlowerStatics as SqlInfo

sql_info = SqlInfo

imsiInfo_sysStr = sql_info['140src']['db']
imsiInfo_Database = sql_info['140src']['database']


def get_json_data(sys_str, data_base, query_str):
    """

    :param sys_str:
    :param data_base:
    :param query_str:
    :return:
    """
    json_results = qureResultAsJson(sysStr=sys_str, Database=data_base, query_str=query_str, where=[])

    return json_results


def timestamp_datetime(value):
    format_str = '%Y-%m-%d %H:%M:%S'
    # value为传入的值为时间�?(整形)，如�?1332888820
    value = time.localtime(value)
    # # 经过localtime转换后变�?
    # # time.struct_time
    # (tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=0)
    # �?后再经过strftime函数转换为正常日期格式�??
    dt = time.strftime(format_str, value)
    return dt


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都�?要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    # time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28,
    # tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
    # �?"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def get_gmt0_str_time(str_time, off_set):
    """

    :param str_time:
    :param off_set:
    :return:
    """
    try:
        gmt0_date_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')-datetime.timedelta(minutes=off_set)
    except ValueError:
        gmt0_date_time = datetime.datetime.strptime(str_time, '%Y-%m-%d') - datetime.timedelta(minutes=off_set)

    return str(gmt0_date_time)


def get_list_imsi(data_imsi):
    """
    本函数为获取符型list函数
    :param data_imsi:dic,list,string数据转换为字符型list
    :return: list_imsi
    """
    imsi_data = data_imsi
    list_imsi = []
    if type(imsi_data) is dict:
        for data in imsi_data:
            list_imsi.append(str(data['imsi']))

    elif type(imsi_data) is list:

        for data in imsi_data:
            if type(data) is dict:
                list_imsi.append(str(data['imsi']))
            if type(data) is str:
                list_imsi.append(str(data))

    elif type(imsi_data) is str:
        for data in imsi_data.split(','):
            list_imsi.append(data)

    else:
        list_imsi = []

    return list_imsi


def get_all_flower(begin_l_unix, end_l_unix, list_imsi):
    """

    :param begin_l_unix:
    :param end_l_unix:
    :param list_imsi:
    :return:
    """
    if not list_imsi:
        return []
    else:
        group_id = {'imsi': "$imsi"}
        match_stages = {'createtime': {'$gte': begin_l_unix, '$lte': end_l_unix}, 'imsi': {'$in': list_imsi}}
        pipeline = [
            {"$match": match_stages
             },
            {"$group": {
                "_id": group_id,
                'all': {'$sum': {'$add': ["$userFlower", "$sysFlower"]}}
            }
            }]
        connection = pymongo.MongoClient(sql_info['get140Flower']['uri'])
        agg_data = list(
            connection.get_database(
                sql_info['get140Flower']['db']
            ).get_collection(
                sql_info['get140Flower']['collection']
            ).aggregate(pipeline)
        )
        for i in range(len(agg_data)):
            agg_id_temp = agg_data[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
            agg_data[i].update(agg_id_temp)
            # 流量输出为MB
            agg_data[i]['all'] = round(((agg_data[i]['all']) / 1024 / 1024), 2)
        connection.close()

        return agg_data


def get_us_flower(begin_l_unix, end_l_unix, list_imsi):
    """

    :param begin_l_unix:
    :param end_l_unix:
    :param list_imsi:
    :return:
    """
    if not list_imsi:
        return []
    else:
        group_id = {'imsi': "$imsi"}
        match_stages = {
            'createtime': {'$gte': begin_l_unix, '$lte': end_l_unix},
            'imsi': {'$in': list_imsi},
            'mcc': {"$in": ['311', '310']},
            # 剔除关岛、塞班岛流量
            'lac': {"$nin": ['0', '10', '60', '208']}
        }
        pipeline = [
            {
                "$match": match_stages
             },
            {
                "$group": {
                    "_id": group_id,
                    'internalflower': {
                        '$sum': {
                            '$add': ["$userFlower", "$sysFlower"]
                        }
                    }
                }
            }
        ]
        connection = pymongo.MongoClient(sql_info['get140Flower']['uri'])
        agg_data = list(connection.get_database(sql_info['get140Flower']['db']
                                                ).get_collection(
            sql_info['get140Flower']['collection']
            ).aggregate(pipeline))
        for i in range(len(agg_data)):
            agg_id_temp = agg_data[i].pop('_id')                      # {‘_id’:{}}转换成标准json数据
            agg_data[i].update(agg_id_temp)
            # 流量输出为MB
            agg_data[i]['internalflower'] = round(((agg_data[i]['internalflower']) / 1024 / 1024), 2)

        connection.close()

        return agg_data


def get_not_us_flower(begin_l_unix, end_l_unix, list_imsi):
    """
    非美国流量获取模块，暂时未使用
    :param begin_l_unix:
    :param end_l_unix:
    :param list_imsi:
    :return:
    """
    if not list_imsi:
        return []
    else:
        group_id = {'imsi': "$imsi"}
        match_stages = {
            'createtime': {
                '$gte': begin_l_unix, '$lte': end_l_unix
            },
            'imsi': {
                '$in': list_imsi
            },
            # or 1-为美国关岛塞班岛流量（不计入美国）； 2-为非美国本土流量
            "$or": [
                {
                    'mcc': {
                        "$in": ['311', '310']
                    },
                    'lac': {
                        "$in": ['0', '10', '60', '208']
                    }
                },
                {
                    'mcc': {
                        "$nin": ['311', '310']
                    }
                 }
            ]
        }
        pipeline = [
            {
                "$match": match_stages
             },
            {
                "$group": {
                    "_id": group_id,
                    'externalflower': {
                        '$sum': {
                            '$add': ["$userFlower", "$sysFlower"]
                        }
                    }
                }
            }
        ]
        connection = pymongo.MongoClient(sql_info['get140Flower']['uri'])
        agg_data = list(connection.get_database(sql_info['get140Flower']['db']).get_collection(
            sql_info['get140Flower']['collection']).aggregate(pipeline))
        for i in range(len(agg_data)):
            agg_id_temp = agg_data[i].pop('_id')                            # {‘_id’:{}}转换成标准json数据
            agg_data[i].update(agg_id_temp)
            # 流量输出为MB
            agg_data[i]['externalflower'] = round(((agg_data[i]['externalflower']) / 1024 / 1024), 2)

        connection.close()

        return agg_data


def get_140country_flower(start_date, stop_date, data):
    """
    本函数用于获取140国卡流量统计接口
    :param start_date: string type datetime from web. Set mongodb begin unix time
    :param stop_date: string type datetime from web. Set mongodb end unix time
    :param data: 为140国卡资源信息表，为最后整合返回数据，后续统计完每张imsi流量记录后更新记录至该data
    :return: 返回最后的统计数据，类型为list dic[{}],{},...]
    """
    """
    begin_l_unix and end_l_unix is unix timestamp from 1970, is long int types.
    """
    begin_l_unix = int(start_date)*1000          # (datetime_timestamp(start_date)) * 1000
    end_l_unix = int(stop_date)*1000             # (datetime_timestamp(stop_date)) * 1000
    imsi_data = data
    list_imsi = get_list_imsi(imsi_data)
    # query total flower and us flower from mongodb
    all_flower = get_all_flower(begin_l_unix=begin_l_unix, end_l_unix=end_l_unix, list_imsi=list_imsi)
    us_flower = get_us_flower(begin_l_unix=begin_l_unix, end_l_unix=end_l_unix, list_imsi=list_imsi)
    for imsi_info in imsi_data:
        for af in all_flower:
            if af['imsi'] == imsi_info['imsi']:
                imsi_info.update({'all': af['all']})
    for imsi_info in imsi_data:
        for us in us_flower:
            if us['imsi'] == imsi_info['imsi']:
                imsi_info.update({'internalflower': us['internalflower']})
    for imsi_info in imsi_data:
        if 'all' in imsi_info.keys():
            if imsi_info['all'] != 0:
                if 'internalflower' in imsi_info.keys():
                    imsi_info.update({'externalflower': (imsi_info['all'] - imsi_info['internalflower']),
                                     'percentage': round(
                                         ((imsi_info['all'] - imsi_info['internalflower'])/imsi_info['all']) * 100, 2)
                                      })
                else:
                    imsi_info.update({'externalflower': imsi_info['all'],
                                     'percentage': round(((imsi_info['all']) / imsi_info['all']) * 100, 2)})

    return imsi_data


def get_140country_src():
    """
    本函数获取系统中140国卡的imsi、org、state、groupname信息
    :return:
    """

    query_str = ("SELECT  "
                 "DISTINCT (CAST(a.`imsi` AS CHAR)) AS 'imsi',  "
                 "e.`org_name` AS 'org',  "
                 "a.`available_status` AS 'state',  "
                 "(case when a.`occupy_status` = 0 then '未占用' else '已占用' end) AS 'occupy_status', "
                 "GROUP_CONCAT(DISTINCT b.`package_type_name` "
                 "ORDER BY b.`package_type_name` SEPARATOR ';') AS 'package_type', "
                 "c.`name` AS 'groupname'  "
                 "FROM  `t_css_vsim` AS a  "
                 "LEFT  JOIN `t_css_vsim_packages` as b  "
                 "	ON a.`imsi`=b.`imsi`  "
                 "LEFT JOIN `t_css_plmnset` AS c  "
                 "	ON a.`plmnset_id`=c.`id`  "
                 "LEFT JOIN `t_css_operator` AS d  "
                 "	ON a.`operator_id`=d.`id`  "
                 "LEFT JOIN `t_css_group` AS e  "
                 "	ON a.`group_id`=e.`id`  "
                 "WHERE   a.`iso2`='us'  "
                 "	AND b.`package_type_name` LIKE '%140国%'  "
                 "GROUP BY (CAST(a.`imsi` AS CHAR)) "
                 )
    imsi_info = get_json_data(sys_str=imsiInfo_sysStr, data_base=imsiInfo_Database, query_str=query_str)
    # print query_str
    return imsi_info


def qury_140country_flower_statics(begin_time, end_time, time_zone_off_set):
    """

    :param begin_time:
    :param end_time:
    :param time_zone_off_set:
    :return:
    """
    begin_date = begin_time
    end_date = end_time
    # queryTimezoneOffset = int(time_zone_off_set)
    # queryGMTOBeginTime = get_gmt0_str_time(str_time=begin_date,off_set=queryTimezoneOffset)
    # queryGMTOEndTime = get_gmt0_str_time(str_time=end_date,off_set=queryTimezoneOffset)
    info_140country = []
    flower_data = []
    err_info_src = ''
    err_info_flower = ''
    if (not begin_date) or (not end_date):
        dic_results = {'info': {'err': True, 'errinfo': '时间参数异常！'}, 'data': []}
        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
    else:
        try:
            info_140country = get_140country_src()
        except mysql.connector.Error as err:
            err_info_src = "Something went wrong: {}".format(err)
        except:
            err_info_src = "Unexpected error"
        if err_info_src:
            dic_results = {'info': {'err': True, 'errinfo': err_info_src}, 'data': []}
            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        elif not info_140country:
            err_info_src = '系统无套餐名包含140国卡的信息！'
            dic_results = {'info': {'err': True, 'errinfo': err_info_src}, 'data': []}
            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        else:
            try:
                flower_data = get_140country_flower(start_date=begin_date,  stop_date=end_date,
                                                    data=info_140country)
            except ValueError:
                err_info_flower = "input Date Time ValueError"
            except mongodb_error.OperationFailure:
                err_info_flower = "DataBase Authentication failed!"
            except mongodb_error.NetworkTimeout:
                err_info_flower = "DataBase Connection Exceeded SocketTimeoutMS!"
            #except:
            #    err_info_flower = "Unexpected error"

            if err_info_flower:
                dic_results = {'info': {'err': True, 'errinfo': err_info_flower}, 'data': []}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            elif not flower_data:
                err_info_flower = '无指定时间范围内140国卡流量使用记录！'
                dic_results = {'info': {'err': True, 'errinfo': err_info_flower}, 'data': []}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            else:
                returnData = flower_data
                dic_results = {'info': {'err': False, 'errinfo': ''}, 'data': returnData}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
