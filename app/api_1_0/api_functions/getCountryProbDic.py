# -*- coding: utf-8 -*-


import json
from bson import json_util
from bson.code import Code
from .SqlPack.SQLModel import qureResultAsJson
import time
import pymongo
import pymongo.errors as mongodb_error
import mysql.connector
import datetime
# 获取连接信息
from .SqlPack.pyMongoModel import (sql_info, MongoClient, Database, Sheet)
# Mongo_Model
from .SqlPack.Mongo_Model import (msmongo, pygroup)
from .SqlPack.SqlLinkInfo import getCountryProbDic
# 获取新架构卡资源数据库连接信息
Sql = getCountryProbDic['getSrc']


def datetime_timestamp(dt):
    # dt为字符串
    # 中间过程，一般都�?要将字符串转化为时间数组
    time.strptime(dt, '%Y-%m-%d %H:%M:%S')
    # �?"2012-03-28 06:53:40"转化为时间戳
    s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
    return int(s)


def get_gmt0_str_time(str_time, off_set):
    """

    :param str_time:
    :param off_set:
    :return:
    """
    gmt0_date_time = datetime.datetime.strptime(str_time, '%Y-%m-%d %H:%M:%S')-datetime.timedelta(minutes=off_set)

    return str(gmt0_date_time)


def get_list_imsi(dic_data):
    """

    :param dic_data:
    :return: list dic imsi
    """
    list_imsi = []
    for i in range(len(dic_data)):
        list_imsi.append(str(dic_data[i]['imsi']))

    return list_imsi


def get_json_data(sys_str, database, query_str):
    """

    :param sys_str:
    :param database:
    :param query_str:
    :return:
    """
    json_results = qureResultAsJson(sysStr=sys_str, Database=database, query_str=query_str, where=[])

    return json_results


def assemble_err_info(query_data, err_data):
    """

    :param query_data:
    :param err_data:
    :return:
    """
    assemble_err_info_base_data = query_data
    assemble_err_info_err_data = err_data
    for i in range(len(assemble_err_info_base_data)):
        str_err = ''
        find_imsi = False
        for j in range(len(assemble_err_info_err_data)):
            if str(assemble_err_info_base_data[i]['imsi']) == str(assemble_err_info_err_data[j]['vsimImsi']):
                str_err = str_err + '(' + str(int(assemble_err_info_err_data[j]['errType'])) + "," + \
                          str(int(assemble_err_info_err_data[j]['errCode'])) + ' :' + str(
                    int(assemble_err_info_err_data[j]['count'])) + ')'
                find_imsi = True
        if not find_imsi:
            str_err = 'NULL'
        err = {'err': str_err}
        assemble_err_info_base_data[i].update(err)

    return assemble_err_info_base_data


def get_err(query_data, begin_time, end_time):
    """

    :param query_data:
    :param begin_time:
    :param end_time:
    :return:
    """
    get_err_base_data = query_data
    imsi = []                        # 存储问题imsi
    for dic in get_err_base_data:
        imsi.append(str(dic['imsi']))
    condition = {"vsimImsi": {"$in": imsi},
                 # "errType":8,
                 # "mcc":'602',
                 # "errCode":{"$in" : [7,]},
                 "errorTime": {"$gte": (int(begin_time) * 1000),
                               "$lte": (int(end_time) * 1000)}
                 }
    ms_mongo = msmongo(MongoClient=MongoClient["N_oss_perflog"], Database=Database["N_oss_perflog"],
                       Sheet=Sheet["t_term_vsim_estfail"])
    key = {"vsimImsi": 1, "errType": 1, "errCode": 1}
    initial = {"count": 0}
    reducer = Code("""function(obj, prev){prev.count ++}""")
    lis_mongo_tab = ["vsimImsi", "errType", "errCode", "count"]
    mongo_err = pygroup(ms_mongo, "t_term_vsim_estfail", key, condition, initial, reducer, lis_mongo_tab)
    return_err_data = assemble_err_info(query_data=get_err_base_data, err_data=mongo_err)

    return return_err_data


def get_country_flower(dic_data, begin_time, end_time, flower_threshold):
    """

    :param dic_data:
    :param begin_time:
    :param end_time:
    :param flower_threshold:
    :return:
    """

    query_data = dic_data
    return_data = []
    # 获取list imsi
    list_imsi = get_list_imsi(query_data)
    # 查询起始和截止时间
    flower_begin_time = begin_time
    flower_end_time = end_time
    flower_having_set = flower_threshold
    begin_l_unix = int(flower_begin_time) * 1000
    end_l_unix = int(flower_end_time) * 1000
    pipeline = [{"$match": {'createtime': {'$gte': begin_l_unix, '$lt': end_l_unix},
                            'imsi': {'$in': list_imsi}
                            }
                 },
                {"$group": {"_id": {'imsi': "$imsi"},
                            "Flower": {'$sum':  {'$add': ["$userFlower", "$sysFlower"]}
                                       }
                            }
                 }
                ]
    connection = pymongo.MongoClient(sql_info['getCountryProbDic']['queryFlower']['uri'])
    agg_data = list(connection.get_database(sql_info['getCountryProbDic']['queryFlower']['db']
                                            ).get_collection(sql_info['getCountryProbDic']['queryFlower']['collection']
                                                             ).aggregate(pipeline))
    for i in range(len(agg_data)):
        agg_id_temp = agg_data[i].pop('_id')
        agg_data[i].update(agg_id_temp)
        agg_data[i]['Flower'] = round(((agg_data[i]['Flower'])/1024/1024), 2)
    connection.close()
    pip_imsi = []
    for i in range(len(query_data)):
        if_zero_flower = True
        for j in range(len(agg_data)):
            if str((agg_data[j]['imsi'])) == str(query_data[i]['imsi']):
                if_zero_flower = False
                if agg_data[j]['Flower'] <= int(flower_having_set):
                    query_data[i].update({'Flower': agg_data[j]['Flower']})
                else:
                    pip_imsi.append(int(query_data[i]['imsi']))
        if if_zero_flower:
            query_data[i].update({'Flower': 0})
    for dic in query_data:
        if int(dic['imsi']) not in pip_imsi:
            return_data.append(dic)

    return return_data


def get_imsi_flower(dic_data, begin_time, end_time):
    """

    :param dic_data:
    :param begin_time:
    :param end_time:
    :return:
    """

    query_data = dic_data
    # 获取list imsi
    list_imsi = get_list_imsi(query_data)
    # 查询起始和截止时间
    flower_begin_time = begin_time
    flower_end_time = end_time
    begin_l_unix = int(flower_begin_time) * 1000
    end_l_unix = int(flower_end_time) * 1000
    pipeline = [
        {"$match": {'createtime': {'$gte': begin_l_unix, '$lte': end_l_unix},
                    'imsi': {'$in': list_imsi}
                    }
         },
        {"$group": {
            "_id": {'imsi': "$imsi"},
            'Flower': {'$sum':  {'$add': ["$userFlower", "$sysFlower"]}}
        }
        }]
    connection = pymongo.MongoClient(sql_info['getCountryProbDic']['queryFlower']['uri'])
    agg_data = list(connection.get_database(sql_info['getCountryProbDic']['queryFlower']['db']
                                            ).get_collection(sql_info['getCountryProbDic']['queryFlower']['collection']
                                                             ).aggregate(pipeline))

    for i in range(len(agg_data)):
        agg_id_temp = agg_data[i].pop('_id')  # {‘_id’:{}}转换成标准json数据
        agg_data[i].update(agg_id_temp)
        agg_data[i]['Flower'] = round(((agg_data[i]['Flower'])/1024/1024), 2)
    # 更新流量记录
    for i in range(len(query_data)):
        if_zero_flower = True
        for j in range(len(agg_data)):
            if str((agg_data[j]['imsi'])) == str(query_data[i]['imsi']):
                if_zero_flower = False
                query_data[i].update({'Flower': agg_data[j]['Flower']})
        if if_zero_flower:
            query_data[i].update({'Flower': 0})
    connection.close()

    return query_data


def get_country_dispatch_and_vsim_info(country, query_plmn, begin_time, endtime, dispatch_threshold):
    """

    :param country:
    :param query_plmn:
    :param begin_time:
    :param endtime:
    :param dispatch_threshold:
    :return:
    """
    query_country = country
    str_plmn = query_plmn
    query_begin_time = begin_time
    query_end_time = endtime
    str_dispatch_threshold = dispatch_threshold
    if str_plmn == '':
        query_plmn_str = ''
    else:
        query_plmn_str = ' '+'AND a.`plmn` IN (' + str_plmn + ') '
    if query_country == '':
        query_country_str = ''
    else:
        query_country_str = "" + "AND a.`iso2`= '" + query_country + "' "
    query_str_vsim = (
        "SELECT "
        "a.`iso2` AS 'country', "
        "(CAST(a.`imsi` AS CHAR)) AS 'imsi', "
        "a.`iccid`, "
        "b.`package_type_name`, "
        "DATE_FORMAT(b.`next_update_time`, '%Y-%m-%d %H:%i:%s') AS 'next_update_time', "
        "p.`name` AS 'sim_agg', "
        "a.`bam_id` as 'bam', "
        "COUNT(c.`imsi`)AS 'imsi_con', "
        "COUNT(DISTINCT c.`imei`)AS 'imei_con' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` b "
        "	ON a.`imsi`=b.`imsi`  "
        "LEFT  JOIN `t_css_user_vsim_log` AS c "
        "        ON c.`imsi`=a.`imsi` "
        "LEFT  JOIN `t_css_plmnset` AS p "
        "        ON a.`plmnset_id`=p.`id`"
        "WHERE  "
        "     a.`bam_status`='0' "
        "     AND a.`slot_status`='0' " + query_country_str + " " + query_plmn_str + ""
        "     AND a.`available_status`='0' "
        "     AND c.`create_time`>= " + "'" + query_begin_time + "'"
        "     AND c.`create_time`< " + "'" + query_end_time + "'"
        "GROUP BY a.`iso2`, "
        "a.`imsi`, "
        "a.`iccid`, "
        "b.`package_type_name`, "
        "b.`next_update_time` "
        "HAVING COUNT(c.`imsi`)> " + "'" + str(str_dispatch_threshold) + "'"
    )
    dic_results = get_json_data(sys_str=Sql['db'], database=Sql['database'], query_str=query_str_vsim)

    return dic_results


def get_imsi_dispatch_and_vsim_info(imsi, begin_time, endtime):
    """============================================

    :param imsi:
    :param begin_time:
    :param endtime:
    :return:
    =================================================="""
    strimsi = imsi
    query_begin_time = begin_time
    query_end_time = endtime
    query_str_vsim = (
        "SELECT "
        "a.`iso2` AS 'country', "
        "(CAST(a.`imsi` AS CHAR)) AS 'imsi', "
        "a.`iccid`, "
        "b.`package_type_name`, "
        "b.`next_update_time`, "
        "a.`bam_id` AS 'bam', "
        "COUNT(c.`imsi`)AS 'imsi_con', "
        "COUNT(DISTINCT c.`imei`)AS 'imei_con' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` b "
        "	ON a.`imsi`=b.`imsi`  "
        "LEFT  JOIN `t_css_user_vsim_log` AS c "
        "        ON c.`imsi`=a.`imsi` "
        "WHERE  "
        "     a.`imsi` IN (" + strimsi + ")"
        "     AND a.`bam_status`='0' "
        "     AND a.`slot_status`='0' "
        "     AND a.`available_status`='0' "
        "     AND c.`create_time`>= " + "'" + query_begin_time + "'"
        "     AND c.`create_time`< " + "'" + query_end_time + "'"
        "GROUP BY a.`iso2`, "
        "a.`imsi`, "
        "a.`iccid`, "
        "b.`package_type_name`, "
        "b.`next_update_time` "
    )
    dic_results = get_json_data(sys_str=Sql['db'], database=Sql['database'], query_str=query_str_vsim)

    return dic_results


def get_prob_fisrt_dic(query_sort, query_pram, query_plmn, begin_time, end_time, dispatch_begin_time,
                       dispatch_end_time, timezone_off_set, dispatch_threshold, flower_threshold):
    """
    
    :param query_sort: 
    :param query_pram: 
    :param query_plmn: 
    :param begin_time: 
    :param end_time: 
    :param dispatch_begin_time: 
    :param dispatch_end_time: 
    :param timezone_off_set: 
    :param dispatch_threshold: 
    :param flower_threshold: 
    :return: 
    """
    query_sort = query_sort
    query_pram = query_pram
    query_plmn = query_plmn
    query_begin_time = begin_time
    query_end_time = end_time
    query_dispatch_begin_t = dispatch_begin_time
    query_dispatch_end_t = dispatch_end_time
    quey_dispatch_threshold = dispatch_threshold
    query_flower_threshold = flower_threshold
    err_info = ''
    dic_data = []
    get_err_dic_data = []
    if (query_sort == '') or (query_begin_time == '') or\
            (query_end_time == '') or (quey_dispatch_threshold == '') or \
            (query_flower_threshold == '') or (query_dispatch_begin_t == '') or (query_dispatch_end_t == ''):
        dic_results = {'info': {'err': True, 'errinfo': '存在空类型参数'}, 'data': []}

        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
    else:
        if query_sort == 'country':
            try:
                dic_data = get_country_dispatch_and_vsim_info(country=query_pram, query_plmn=query_plmn,
                                                              begin_time=query_dispatch_begin_t,
                                                              endtime=query_dispatch_end_t,
                                                              dispatch_threshold=quey_dispatch_threshold)
            except ValueError:
                err_info = "NDatabase input Date Time ValueError"
            except mysql.connector.Error as err:
                err_info = ("Something went wrong: {}".format(err))
            if err_info != '':
                dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': dic_data}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            elif not dic_data:
                dic_results = {'info': {'err': True, 'errinfo': '无分卡记录查询结果，请重新设置查询参数'}, 'data': dic_data}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            else:
                try:
                    get_flower_dic_data = get_country_flower(dic_data=dic_data, begin_time=query_begin_time,
                                                             end_time=query_end_time,
                                                             flower_threshold=query_flower_threshold)
                    get_err_dic_data = get_err(query_data=get_flower_dic_data, begin_time=query_begin_time,
                                               end_time=query_end_time)
                except mongodb_error.OperationFailure:
                    err_info = "MongoDataBase Authentication failed!"
                except mongodb_error.NetworkTimeout:
                    err_info = "MongoDataBase Connection Exceeded SocketTimeoutMS!"
                except:
                    err_info = "MongoDataBase Unexpected error"
                if err_info != '':
                    dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
                else:
                    dic_results = {'info': {'err': False, 'errinfo': err_info}, 'data': get_err_dic_data}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        else:
            try:
                dic_data = get_imsi_dispatch_and_vsim_info(imsi=query_pram, begin_time=query_dispatch_begin_t,
                                                           endtime=query_dispatch_end_t)
            except ValueError:
                err_info = "NDatabase input Date Time ValueError"  # 'Database Error!'
            except mysql.connector.Error as err:
                err_info = ("Something went wrong: {}".format(err))
            except:
                err_info = "NDatabase Unexpected error"
            if err_info != '':
                dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': dic_data}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)

            elif not dic_data:
                dic_results = {'info': {'err': True, 'errinfo': '无查询结果，请重新设置查询参数！'}, 'data': dic_data}
                return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
            else:
                try:
                    get_flower_dic_data = get_imsi_flower(dic_data=dic_data, begin_time=query_begin_time,
                                                          end_time=query_end_time)

                    get_err_dic_data = get_err(query_data=get_flower_dic_data, begin_time=query_begin_time,
                                               end_time=query_end_time)
                except mongodb_error.OperationFailure:
                    err_info = "MongoDataBase Authentication failed!"
                except mongodb_error.NetworkTimeout:
                    err_info = "MongoDataBase Connection Exceeded SocketTimeoutMS!"
                except:
                    err_info = "MongoDataBase Unexpected error"
                if err_info != '':
                    dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
                else:
                    dic_results = {'info': {'err': False, 'errinfo': err_info}, 'data': get_err_dic_data}
                    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
