#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import decimal
from bson import json_util
import mysql.connector
from .SqlPack.SQLModel import qureResultAsJson

old_sys_str = 'config_S'
ucloudplatform_db = 'ucloudplatform'
saas_sys_str = 'config_N'
glocalme_css_db = 'glocalme_css'
amzami_sys_str = 'config_amzami'
amzami_gsvc_db = 'gsvcdatabase'


def get_json_data(sys_str, database, query_str):
    """

    :param sys_str:
    :param database:
    :param query_str:
    :return:
    """
    json_results = qureResultAsJson(sysStr=sys_str, Database=database, query_str=query_str, where=[])
    return json_results


def get_saas_vsim_country_static(country):
    """

    :param country:
    :return:
    """
    query_country = country

    if query_country == "":
        where = ""
    else:
        where = "AND `iso2`=" + "'" + query_country + "' "

    query_str_vsim = ("SELECT "
                      "a.`iso2` AS 'country', "
                      "COUNT(1) AS 'all_num', "
                      "COUNT(CASE WHEN (a.`available_status`=0 "
                      "                 AND b.`package_status`<>2 "
                      "                 AND a.`business_status`IN('0','4','5') "
                      "                 AND c.`pool_id` IS NOT NULL "
                      "                 AND a.`expire_time`>=NOW() "
                      "                 AND b.`expire_time`>=NOW()) "
                      "           THEN '0' "
                      "      END) AS 'available_num', "
                      "   COUNT(CASE WHEN a.`available_status`=0 "
                      "               AND b.`package_status`<>2 "
                      "               AND a.`business_status`IN('0','4','5') "
                      "               AND c.`pool_id` IS NOT NULL "
                      "               AND a.`expire_time`>=NOW() "
                      "               AND b.`expire_time`>=NOW() "
                      "               AND a.`occupy_status`=0 "
                      "               THEN '1' "
                      "         END) AS 'unoccupy_num' "
                      "FROM `t_css_vsim`AS a "
                      "LEFT  JOIN `t_css_vsim_packages` b "
                      "      ON a.`imsi`=b.`imsi` "
                      "LEFT JOIN `t_css_v_pool_map` AS c "
                      "       ON c.`vsim_id`=a.`id` "
                      "WHERE "
                      "   (b.`package_type_name` NOT  REGEXP '.*[0-9]国.*') " + where + " "
                      "   AND a.`bam_status`=0 "
                      "   AND a.`slot_status`=0 "
                      "   AND a.`vsim_type` = 0 "
                      "   AND a.`dr`=0   "
                      "GROUP BY a.`iso2` "
                      "ORDER BY COUNT(DISTINCT a.`imsi`) DESC ")
    json_results_sass_sim = get_json_data(sys_str=saas_sys_str, database=glocalme_css_db, query_str=query_str_vsim)

    return json_results_sass_sim


def get_vsim_package_flow_status(country):
    """

    :return:
    """
    query_country = country
    if query_country == "":
        where = ""
    else:
        where = "AND `iso2`=" + "'" + query_country + "' "

    query_str_flow = (
        "SELECT "
        "a.`iso2`              AS 'Country', "
        "b.`package_type_name` AS 'PackageName', "
        "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'NextUpdateTime', "
        "e.`org_name`          AS 'ORG', "
        "CAST((SUM(b.`total_use_flow`)/SUM(CASE "
        "                                  WHEN `activate_status` = 0 "
        "                                  THEN b.`init_flow` ELSE 0 END ))*100  "
        "AS DECIMAL(64,1)) AS 'Percentage' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi` "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id` "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id` "
        "WHERE   a.`bam_status` = '0' "
        "        AND a.`slot_status` = '0'  "
        "        " + where + " "
        "        AND b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` IS NOT NULL "
        "        AND e.`org_name` = 'GTBU' "
        "GROUP BY a.`iso2`,b.`package_type_name`,DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H'), e.`org_name` "
    )

    vsim_package_flow_status = get_json_data(sys_str=saas_sys_str, database=glocalme_css_db, query_str=query_str_flow)

    return vsim_package_flow_status


def get_vsim_country_static(country, **kwargs):
    """
    为主页gsvc HOME popchart图形接口
    :param country: 按国家进行数据统计
    :param kwargs: 后续根据需求变化增加变量
    :return:
    """
    query_country = country
    err_info = ''
    vsim_flower_static = []
    try:
        vsim_flower_static = get_vsim_package_flow_status(query_country)
    except KeyError as keyerr:
        err_info = ("when query max_user raise KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        err_info = ("Something went wrong when query max_user: {}".format(err))
    if err_info:
        dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}
    else:
        if not vsim_flower_static:
            dic_results = {'info': {'err': False, 'errinfo': "No Data"}, 'data': []}

        else:
            for fs in vsim_flower_static:
                if type(fs['Percentage']) is decimal.Decimal:
                    fs['Percentage'] = float(fs['Percentage'])

            dic_results = {'info': {'err': False, 'errinfo': ''}, 'data': vsim_flower_static}
    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)


def get_muti_line_on_shelf_ava_card(country):
    """
    本函数用于获取新架构在架卡状态统计数据：在架卡数、可用卡数
    :param country:
    :return:
    """
    query_country = country
    # (当前国家总计卡数、可用卡数数据获取------------------------------GTBU-----------------------------------------)
    query_saas_on_shelf_and_ava_card = (
        "SELECT "
        "a.`iso2` AS 'country', "
        "COUNT(1) AS 'on_shelf_num', "
        "COUNT(CASE WHEN (a.`available_status`=0 "
        "                 AND b.`package_status`<>2 "
        "                 AND a.`business_status`IN('0','4','5') "
        "                 AND c.`pool_id` IS NOT NULL "
        "                 AND a.`expire_time`>=NOW() "
        "                 AND b.`expire_time`>=NOW()) "
        "           THEN '0' "
        "      END) AS 'ava_num' "
        "FROM `t_css_vsim`AS a "
        "LEFT  JOIN `t_css_vsim_packages` b "
        "      ON a.`imsi`=b.`imsi` "
        "LEFT JOIN `t_css_v_pool_map` AS c "
        "      ON c.`vsim_id`=a.`id` "
        "WHERE "
        "   (b.`package_type_name` NOT  REGEXP '.*[0-9]国.*')"
        "   AND a.`iso2`=" + "'" + query_country + "' "
        "   AND a.`bam_status`=0 "
        "   AND a.`slot_status`=0 "
        "   AND a.`vsim_type` = 0 "
        "   AND a.`dr`=0   "
        "GROUP BY a.`iso2` "
    )
    json_results_on_shelf_and_ava_card = get_json_data(sys_str=saas_sys_str, database=glocalme_css_db,
                                                       query_str=query_saas_on_shelf_and_ava_card)
    return json_results_on_shelf_and_ava_card


def get_muti_line_old_on_shelf_and_ava_card(country):
    """
    本函数用于获取老系统在架卡状态统计数据：在架卡数、可用卡数
    :param country:
    :return:
    """
    query_country = country
    # (当前国家总计卡数、可用卡数数据获取------------------------------S-----------------------------------------)
    query_old_onshelf_and_ava_card = (
        "SELECT  "
        "a.`country_code2`AS 'country', "
        "COUNT(1) AS 'on_shelf_num', "
        "COUNT(CASE WHEN  "
        " a.`state`='00000' OR a.`state`='10000' THEN 1 END )AS 'ava_num' "
        "FROM `t_resvsim` AS a "
        "LEFT JOIN `t_resvsimpackagetype`AS c ON c.`itemid`=a.`packagetype` "
        "LEFT JOIN `t_resvsimowner`AS e ON e.`sourceid`=a.`imsi` "
        "LEFT JOIN `t_resoperator` AS r ON r.`code`=a.`sid` "
        "LEFT JOIN `t_usmguser_parent`   AS f    ON f.`uid`=e.`ownerid`  "
        "WHERE a.`state` LIKE '_0__0' "  # 在板卡条件
        "AND e.`sourceid` IS NULL  "  # 是否代理商卡判断，NULL非代理商卡
        "AND (c.`name` NOT  REGEXP '.*[0-9]国.*') "
        "AND a.`country_code2`=" + "'" + query_country + "'"
        "GROUP BY a.`country_code2` "
    )

    on_shelf_and_ava_card = get_json_data(sys_str=old_sys_str, database=ucloudplatform_db,
                                          query_str=query_old_onshelf_and_ava_card)

    return on_shelf_and_ava_card


def get_muti_line_max_user(country, begintime, endtime, bu_type_set, time_dim_set):
    """

    :param country:
    :param begintime:
    :param endtime:
    :param bu_type_set:
    :param time_dim_set:
    :return:
    """
    query_country = country
    query_begin_time = begintime
    query_end_time = endtime
    bu_type_set = bu_type_set
    time_dim_set = time_dim_set
    query_str__max_user = (
        "SELECT b.country,"
        "       DATE_FORMAT(b.sampletime, " + time_dim_set + ") AS sampletime , "
        "       MAX(b.onlinemax) AS onlinemax "
        "FROM ( "
        "SELECT a.`country`, a.`createtime` AS sampletime, CAST(SUM(a.`onlinemax`) AS UNSIGNED) AS onlinemax "
        "FROM `gsvcdatabase`.`max_onlingusr_hour` AS a "
        "WHERE a.`country`= " + "'" + query_country + "' "
        "      AND a.`createtime`>= " + "'" + query_begin_time + "' " +
        "AND a.`createtime`<" + "'" + query_end_time + "' "
        "   " + bu_type_set +
        "GROUP BY a.`country`, a.`createtime` ) AS b "
        "GROUP BY b.country ,DATE_FORMAT(b.sampletime, " + time_dim_set + ")"
    )

    json_results_max_user = get_json_data(sys_str=amzami_sys_str, database=amzami_gsvc_db,
                                          query_str=query_str__max_user)

    return json_results_max_user


def get_index_html_muti_line_data(country, begintime, endtime, **kwargs):
    """
    :本部分用于获取绘制主页国家峰值曲线图数据。获取国家峰值用户、在板卡数、可用卡数统计数据
    :param country:
    :param begintime:
    :param endtime:
    :param kwargs:
    :return:
    """
    # (maxonline 曲线数据获取)
    bu = ''
    bu_type_set = " "  # bu类型设置
    time_dim_set = "'%Y-%m-%d'"  # 时间维度设置
    max_user = []
    vsim_con = []
    err_info = ''
    if 'butype' in kwargs.keys():
        butype = kwargs['butype']
        bu = kwargs['butype']
        if butype:
            if butype == 'GTBU':
                butype = '2'
                bu_type_set = bu_type_set + " AND a.`butype`= " + butype + " "

    if 'timedim' in kwargs.keys():
        timedim = kwargs['timedim']
        if timedim != "":
            if timedim == 'month':
                time_dim_set = "'%Y-%m'"
    try:
        max_user = get_muti_line_max_user(country=country, begintime=begintime, endtime=endtime,
                                          bu_type_set=bu_type_set, time_dim_set=time_dim_set)
    except KeyError as keyerr:
        err_info = ("when query max_user raise KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        err_info = ("Something went wrong when query max_user: {}".format(err))
    if err_info:
        dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}
    else:
        if not max_user:
            dic_results = {'info': {'err': False, 'errinfo': "No max_user Data"}, 'data': []}

        else:
            try:
                if bu == 'ALL':
                    vsim_con = get_muti_line_on_shelf_ava_card(country=country)
                else:
                    vsim_con = get_muti_line_on_shelf_ava_card(country=country)
            except KeyError as keyerr:
                err_info = ("when query vsim_con raise KeyError:{}".format(keyerr))
            except mysql.connector.Error as err:
                err_info = ("Something went wrong when query vsim_con: {}".format(err))
            if err_info:
                dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}
            else:
                dic_results = {'info': {'err': False, 'errinfo': ''},
                               'data': {'max_user': max_user, 'sim_con': vsim_con}}

    return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
