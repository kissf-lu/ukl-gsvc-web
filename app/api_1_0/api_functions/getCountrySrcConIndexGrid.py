# -*- coding: utf-8 -*-

import json
from bson import json_util
from .SqlPack.SQLModel import qureResultAsJson
import decimal
import mysql.connector


def getJosonData(sysStr, Database, query_str):
    """

    :param sysStr:
    :param Database:
    :param query_str:
    :return:
    """
    json_results = qureResultAsJson(sysStr=sysStr, Database=Database, query_str=query_str, where=[])

    return json_results


def mergeDataFunc(sourData, mergeData, mergekey, mergeindex):
    """

    :param sourData:
    :param mergeData:
    :param mergekey:
    :param mergeindex:
    :return:
    """
    havemeragenum = []
    for i in range(len(sourData)):
        pre_merge_data = {}
        for j in range(len(mergeData)):
            ifmerge = True
            if j in havemeragenum:
                continue
            for key in mergekey:
                if (key in sourData[i].keys()) and (key in mergeData[j].keys()):
                    if sourData[i][key] == mergeData[j][key]:
                        continue
                    else:
                        ifmerge = False
                        break

            if ifmerge:
                havemeragenum.extend([j])  # 核实相同后记录核实行
                for key in mergeindex:
                    if key in mergeData[j].keys():
                        pre_merge_data.update({key: mergeData[j][key]})
                break

        if pre_merge_data != {}:
            sourData[i].update(pre_merge_data)
    return sourData


def qureyNcountrySrcCon(sys_str, database, country, org_name, vsim_type):
    """
    
    :param sys_str: 
    :param database: 
    :param country: 
    :param org_name: 
    :param vsim_type: 
    :return: 
    """

    query_country = country
    query_org_name = org_name
    vsim_type = vsim_type
    country_set = ''
    org_name_set = ''
    vsim_typ_set = ''
    err_info = ''
    qurey_result = []
    if query_country:
        country_set = "AND a.`iso2` = '" + query_country + "' "
    if query_org_name:
        if query_org_name == 'all':
            org_name_set = " "
        else:
            org_name_set = "AND e.`org_name` = '" + query_org_name + "' "
    if vsim_type:
        vsim_typ_set = "AND a.`vsim_type` = '" + vsim_type + "' "
    query_str = (
        "(SELECT "
        "a.`iso2`              AS 'Country', "
        "CASE WHEN 1 THEN concat('1-合计-',a.`iso2`,'-',e.`org_name` ) END  AS 'PackageName', "
        "CASE WHEN 1 THEN '' END  AS 'NextUpdateTime', "
        "CASE WHEN e.`org_name` is null THEN '总计' else e.`org_name` END  AS 'ORG', "
        "COUNT(DISTINCT a.`imsi`) AS 'all_num', "
        "COUNT(DISTINCT (CASE WHEN a.`activate_status` = 1 THEN a.`imsi` END)) AS 'unact_num', "
        "COUNT(DISTINCT (CASE WHEN a.`available_status` != 0  "
        "                          AND a.`business_status` NOT IN (3) "
        "                          AND a.`activate_status` = 0 "
        "                          THEN a.`imsi` END)) AS 'stop_num',"
        "COUNT(DISTINCT (CASE WHEN a.`business_status`= 3 "
        "                          AND b.`next_update_time` > NOW() "
        "                          AND a.`activate_status` = 0 "
        "                     THEN a.`imsi` END)) AS 'flow_unenought_num', "
        "COUNT(DISTINCT (CASE WHEN ((a.`available_status` = '0') "
        "                AND b.`next_update_time` IS NOT NULL "
        "                AND b.`next_update_time` > NOW() "
        "                AND ((b.`last_update_time` is not null and b.`last_update_time`< NOW()) "
        "                      OR b.`last_update_time` IS NULL "
        "                         ) "
        "                AND b.`package_status` IN (0,1) "
        "                AND a.business_status IN (0,4,5) "
        "                AND (b.service_time_type = 0  "
        "                     OR (( b.service_time_type = 1 AND ((b.gmt0_time_end > NOW() AND NOW() > '00:00:00') "
        "                           OR (b.gmt0_time_start < NOW() AND NOW() <= '23:59:59')) "
        "                               AND b.gmt0_time_end < b.gmt0_time_start )  "
        "                     OR(b.service_time_type = 1 AND b.gmt0_time_start < NOW()AND b.gmt0_time_end > NOW() "
        "                        AND   b.gmt0_time_end > b.gmt0_time_start )) "
        "                     ) "
        "                 ) "
        "                THEN a.`imsi` END)) AS 'ava_num', "
        "CASE WHEN 1 THEN '' END AS 'WarningFlow', "
        "CAST(SUM(CASE WHEN `activate_status` = 0 "
        "              THEN b.`init_flow` "
        "              ELSE 0 END )/1024/1024/1024 AS DECIMAL(64,1))AS 'TotalFlower', "
        "CAST(SUM(b.`total_use_flow`)/1024/1024/1024 AS DECIMAL(64,1)) AS 'UsedFlower', "
        "CAST(SUM(b.`leave_flow`)/1024/1024/1024 AS DECIMAL(64,1))    AS 'LeftFlower', "
        "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 "
        "                                       THEN b.`init_flow` "
        "                                       ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi` "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id` "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id` "
        "WHERE   a.`bam_status` = '0' "
        "        AND a.`slot_status` = '0'  " + country_set + org_name_set + vsim_typ_set + " "
        "        AND b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` is not null "
        "GROUP BY a.`iso2`,e.`org_name` "
        ") "
        "union "
        "( "
        "SELECT "
        "a.`iso2`              AS 'Country', "
        "b.`package_type_name` AS 'PackageName', "
        "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H')  AS 'NextUpdateTime', "
        "e.`org_name`          AS 'ORG', "
        "COUNT(DISTINCT a.`imsi`) AS 'all_num', "
        "COUNT(DISTINCT (CASE WHEN a.`activate_status` = 1 THEN a.`imsi` END)) AS 'unact_num', "
        "COUNT(DISTINCT (CASE WHEN ((a.`available_status` !=0 AND a.`business_status` NOT IN (3) "
        "                            ) "
        "                           OR"
        "                          (a.`available_status` =0 "
        "                              AND (( "
        "                                   b.`package_status` NOT IN (0,1)  "
        "                                    )OR( "
        "                                   b.`package_status` IN (0,1)   "
        "                                   AND b.service_time_type = 1  "
        "                                       AND ((b.`gmt0_time_start`< b.`gmt0_time_end` "
        "	                                         AND ((b.`gmt0_time_end`< NOW() AND NOW() <='23:59:59') "
        "                                                 OR ('00:00:00'<= NOW() AND NOW() < b.`gmt0_time_start`)) "
        "	                                         )OR( "
        "	                                         b.`gmt0_time_start`>b.`gmt0_time_end` "
        "	                                         AND (b.`gmt0_time_end`< NOW() AND NOW()<=b.`gmt0_time_start`) "
        "	                                         ) "
        "	                                    ) "
        "	                                ) "
        "	                            ) "
        "	                     ) "
        "	                    ) "
        "	                    AND a.`activate_status` = '0' "
        "                     THEN a.`imsi` END)) AS 'stop_num',"
        "COUNT(DISTINCT (CASE WHEN a.`business_status`= 3 "
        "                          AND b.`next_update_time` > NOW() "
        "                          AND a.`activate_status` = 0 "
        "                     THEN a.`imsi` END)) AS 'flow_unenought_num', "
        "COUNT(DISTINCT (CASE WHEN ((a.`available_status` = '0') "
        "                     AND b.`next_update_time` IS NOT NULL "
        "                     AND b.`next_update_time` > NOW() "
        "                     AND ((b.`last_update_time` is not null and b.`last_update_time`< NOW()) "
        "                           OR b.`last_update_time` IS NULL "
        "                          ) "
        "                     AND b.`package_status` IN (0,1) "
        "                     AND a.business_status IN (0,4,5) "
        "                     AND (b.service_time_type = 0  "
        "                          OR (( b.service_time_type = 1 AND ((b.gmt0_time_end > NOW() AND NOW() > '00:00:00') "
        "                          OR (b.gmt0_time_start < NOW() AND NOW() <= '23:59:59')) "
        "                                                              AND b.gmt0_time_end < b.gmt0_time_start )  "
        "                          OR(b.service_time_type = 1 AND b.gmt0_time_start < NOW()AND b.gmt0_time_end > NOW() "
        "                                                     AND   b.gmt0_time_end > b.gmt0_time_start )) "
        "                             )"
        "                          )"
        "                THEN a.`imsi` END)) AS 'ava_num', "
        "CAST(c.`warning_flow`/1024/1024 AS UNSIGNED) AS 'warning_flow', "
        "CAST(SUM(CASE WHEN `activate_status` = 0 "
        "              THEN b.`init_flow` "
        "              ELSE 0 END )/1024/1024/1024 AS DECIMAL(64,1))AS 'TotalFlower', "
        "CAST(SUM(b.`total_use_flow`)/1024/1024/1024 AS DECIMAL(64,1)) AS 'UsedFlower', "
        "CAST(SUM(b.`leave_flow`)/1024/1024/1024 AS DECIMAL(64,1))    AS 'LeftFlower', "
        "CAST((SUM(b.`total_use_flow`)/SUM(CASE WHEN `activate_status` = 0 "
        "                                       THEN b.`init_flow` "
        "                                        ELSE 0 END ))*100  AS DECIMAL(64,1)) AS 'Percentage' "
        "FROM `t_css_vsim` AS a "
        "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`= b.`imsi` "
        "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`= e.`id` "
        "LEFT  JOIN `t_css_package_type`  AS c  ON c.`id` = b.`package_type_id` "
        "WHERE   a.`bam_status` = '0' "
        "        AND a.`slot_status` = '0'  " + country_set + org_name_set + vsim_typ_set + " "
        "        AND b.`package_type_name` IS NOT NULL "
        "        AND b.`init_flow` is not null "
        "GROUP BY a.`iso2`,b.`package_type_name`,DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H'), e.`org_name` "
        ") "
        "ORDER BY `Country`, `PackageName`, `ORG` "
    )
    try:
        qurey_result = getJosonData(sys_str, database, query_str)

    except KeyError as keyerr:
        err_info = ("KeyError:{}".format(keyerr))
    except mysql.connector.Error as err:
        err_info = ("Something went wrong: {}".format(err))
    if err_info != '':
        dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}
        return dic_results
    else:
        if not qurey_result:
            dic_results = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}
            return dic_results
        else:
            for cs in qurey_result:
                if type(cs['TotalFlower']) is decimal.Decimal:
                    cs['TotalFlower'] = float(cs['TotalFlower'])
                if type(cs['UsedFlower']) is decimal.Decimal:
                    cs['UsedFlower'] = float(cs['UsedFlower'])
                if type(cs['LeftFlower']) is decimal.Decimal:
                    cs['LeftFlower'] = float(cs['LeftFlower'])
                if type(cs['Percentage']) is decimal.Decimal:
                    cs['Percentage'] = float(cs['Percentage'])

            dic_results = {'info': {'err': False, 'errinfo': err_info}, 'data': qurey_result}

            return dic_results


def qury_country_src_con(country, org_name, vsim_type):
    """
    
    :param country: 
    :param org_name: 
    :param vsim_type: 
    :return: 
    """

    # ("统计新架构卡资源：---------------------------------------------------")
    N_countrySrcCon = qureyNcountrySrcCon('config_N',
                                          'glocalme_css',
                                          country,
                                          org_name,
                                          vsim_type)

    return json.dumps(N_countrySrcCon, sort_keys=True, indent=4, default=json_util.default)
