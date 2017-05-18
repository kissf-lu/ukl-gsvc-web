# -*- coding: utf-8 -*-


import json
from bson import json_util
import mysql.connector
from .SqlPack.SQLModel import qureResultAsJson
from .SqlPack.SqlLinkInfo import DataApiFuncSqlLink as Sql

Sql_Info = Sql['NewVsimTestInfo']['query']


def get_json_data(sys_str, database, query_str):
    """==========================================
    sql查询接口函数，sql-connector插件接口
    :param sys_str:     type:str  查询数据库系统，对应相应数据库连接
    :param database:    type:str  查询数据库系统子数据库，为对应数据库名称
    :param query_str:   type:str  sql查询脚本字符串，推送之数据库引擎进行查询
    :return:            type:list[{},{},...]  返回列表字典
    =============================================="""
    json_results = qureResultAsJson(sysStr=sys_str, Database=database, query_str=query_str, where=[])
    return json_results


def get_new_vsim_info(person, country, test_vsim_info):
    """
    sql 查询接口函数，查询测试卡信息表sql
    :param person:
    :param country:
    :param test_vsim_info:
    :return:
    """
    json_results = []
    query_person = person
    query_country = country
    query_test_vsim_info = test_vsim_info
    param = {'person_test': query_person, 'country_iso': query_country, 'card_info': query_test_vsim_info}
    err_info = ""
    where_set = ""
    for key, value in param.items():
        i = 0
        if value:
            if i == 0:
                if key != 'card_info':
                    where_set = where_set+"WHERE `"+key+"`"+"='"+value+"' "
                else:
                    where_set = where_set+"WHERE `card_info` LIKE " + "'%" + query_test_vsim_info + "%' "
            else:
                if key != 'card_info':
                    where_set = where_set+' AND `'+key+'`'+"='"+value+"' "
                else:
                    where_set = where_set + " AND `card_info` LIKE " + "'%" + query_test_vsim_info + "%' "
            i += 1
    try:
        query_str = (
            "SELECT  "
            "`id_newvsimtest` AS 'id_newvsimtest', "
            "`person_supplier`, "
            "`person_test`, "
            "`card_info`, "
            "(case when `vsim_type`=0 then '本国卡' else '多国卡' end) as 'vsim_type', "
            "`country_cn`, "
            "`country_iso`, "
            "`operator`, "
            "`plmn`, "
            "(CASE WHEN `rat`='4' THEN 'GSM' "
            "      WHEN `rat`='8' THEN 'WCDM' "
            "      WHEN `rat`='16' THEN 'LTE' "
            "      WHEN `rat`='12' THEN 'GSM/WCDMA' "
            "      WHEN `rat`='24' THEN 'WCDMA/LTE' "
            "      WHEN `rat`='28' THEN 'GSM/WCDMA/LTE' "
            " END) AS 'rat', "
            "`config_change`, "
            "`imsi`, "
            "`user_code`, "
            "`imei`, "
            "`device_type`, "
            "`success_time`, "
            "`change_time`, "
            "`register_operator`, "
            "`eplmn` as 'eplmn', "
            "(CASE WHEN `register_rat`='4' THEN 'GSM' "
            "      WHEN `register_rat`='8' THEN 'WCDM' "
            "      WHEN `register_rat`='16' THEN 'LTE' "
            "      WHEN `register_rat`='12' THEN 'GSM/WCDMA' "
            "      WHEN `register_rat`='24' THEN 'WCDMA/LTE' "
            "      WHEN `register_rat`='28' THEN 'GSM/WCDMA/LTE' "
            " END) AS 'register_rat', "
            "`lac`, "
            "`cellid`, "
            "(case when `service_usability` = 0 then '否' else '是' end) as 'service_usability', "
            "(CASE WHEN `stability_onehour` = 0 THEN '否' ELSE '是' END) AS 'stability_onehour', "
            "`agree_mbr`, "
            "(CASE WHEN `agree_consistency`= 0 then '否' else '是' end) as 'agree_consistency', "
            "`fail_reason`, "
            "`remark` as 'remark' "
            "FROM `vsim_test_info` as i "
            " "+where_set
        )
        # print query_str
        db = Sql_Info['db']
        database = Sql_Info['database']
        json_results = get_json_data(sys_str=db, database=database, query_str=query_str)
    except KeyError as keyerr:
        err_info = ("KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        err_info = ("Something went wrong: {}".format(err))
    if err_info:
        dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}

        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)

    else:
        if not json_results:
            dic_results = {'info': {'err': True, 'errinfo': "No Query Data"}, 'data': []}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        else:
            dic_results = {'info': {'err': False, 'errinfo': err_info}, 'data': json_results}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)


def get_new_vsim_test_info(person, country, test_vsim_info):
    """==============================================================
    测试卡信息表查询接口，完成指定person country 
    :param person:          type:str  测试人姓名
    :param country:         type:str  测试国家
    :param test_vsim_info:  type:str  测试卡信息
    :return:                type:dic  {'info': {'err': boolean, 'errinfo': str}, 'data': list}
    
    ==========================================================================================="""

    new_vsim_test_info = get_new_vsim_info(person, country, test_vsim_info)

    return new_vsim_test_info
