# -*- coding: utf-8 -*-

import json
from bson import json_util
from .SqlPack.SQLModel import qureResultAsJson
import mysql.connector
from .SqlPack.SqlLinkInfo import getonSysSrc as Sql

sql_info = Sql


def get_json_data(sys_str, database, query_str):
    """==========================================
    sql查询接口函数
    :param sys_str:
    :param database:
    :param query_str:
    :return:
    =============================================="""
    json_results = qureResultAsJson(sysStr=sys_str, Database=database, query_str=query_str, where=[])
    return json_results


def get_vsim_manul_infor(country, **kwargs):
    """
    手工维护表卡资源信息表查询接口函数
    ========================================================
    :param country: 前端返回必填国家选项，前端设置了此值不能为空逻辑
    :param kwargs:  后台可选参数，如果后续增加返回值，可以随意添加
    :return:        返回制定格式json数据{'info': {}, 'data': {}}
    ========================================================="""
    json_results = []
    query_person = ''
    query_imsi = ''
    query_package_type = ''
    person_where = ''
    imsi_where = ''
    package_type_where = ''
    err_info = ""
    query_country = country
    country_where = ''
    if 'person' in kwargs.keys():
        query_person = kwargs['person']
    if 'imsi' in kwargs.keys():
        query_imsi = kwargs['imsi']
    if 'package_type' in kwargs.keys():
        query_package_type = kwargs['package_type']
    # 逻辑判断
    if (not query_country) and (not query_package_type):
        err_info = '国家和套餐名称不能同时为空！'
    else:
        if query_country or query_package_type:
            if query_country and query_package_type:
                country_where = "`country_iso`= '" + query_country + "' "
                package_type_where = "AND `package_type` LIKE '" + query_package_type + "%' "
            elif query_country and not query_package_type:
                country_where = "`country_iso`= '" + query_country + "' "
            else:
                package_type_where = "`package_type` LIKE '" + query_package_type + "%' "
        if query_person:
            person_where = "AND `person_gsvc`=" + "'" + query_person + "' "
        if query_imsi:
            imsi_where = "AND `imsi` LIKE '" + query_imsi + "%' "

        where = "WHERE  " + country_where + package_type_where + person_where + imsi_where
        query_str = ("SELECT "
                     "`imsi`, "
                     "`country_iso`, "
                     "`country_cn`, "
                     "`person_gsvc`, "
                     "`person_operator`, "
                     "(CASE WHEN `bu_group`='N' THEN 'GTBU' "
                     "WHEN `bu_group`='S' THEN 'S' WHEN `bu_group`='Y' THEN 'Y' END )AS'sys', "
                     "`state`, "
                     "(CASE WHEN `slot_state`=0 THEN '在板' "
                     "WHEN `slot_state`=1 THEN '脱板' WHEN `slot_state`=2 THEN '重复占位' END )AS 'slot_state', "
                     "(CASE WHEN `owner_attr` =0 THEN '否' WHEN `owner_attr` =1 THEN '是' END )AS'owner_attr', "
                     "(CASE WHEN `country_attr` =0 THEN '否' WHEN `country_attr` =1 THEN '是' END )AS'country_attr', "
                     "`vsim_batch_num`, "
                     "`bam_code`, "
                     "`slot_num`, "
                     "`operator`, "
                     "`iccid`, "
                     "`package_type`, "
                     "`charge_noflower`, "
                     "`activated_time`, "
                     "`last_update_time`, "
                     "`next_update_time`, "
                     "`remarks`, "
                     "`phone_num`, "
                     "(CASE WHEN `pay_type`='1' THEN '预付费' WHEN `pay_type`='2' THEN '后付费' END) AS 'pay_type', "
                     "`apn`, "
                     "`shelved_time` "
                     "FROM `vsim_manual_infor` " + where + " "
                     )
        try:
            sys_str = sql_info['getVsimManulInfor']['db']
            database = sql_info['getVsimManulInfor']['database']
            json_results = get_json_data(sys_str=sys_str, database=database, query_str=query_str)
        except KeyError:
            err_info = ("KeyError:{}".format('本地数据库字典配置键值名称有误！'))
        except mysql.connector.Error as err:
            err_info = ("Something went wrong: {}".format(err))
    if err_info != '':
        dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}

        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
    else:
        if not json_results:
            dic_results = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        else:
            dic_results = {'info': {'err': False, 'errinfo': err_info}, 'data': json_results}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)


def qurey_saas_sim(country, imsi, status, business_status, slot_status, bam_status, occupy_status, org,
                   package_status, package_name):
    """
    新架构卡资源查询接口函数，以下参数为sql脚本设置参数
    =====================================================================
    :param country:            imsi卡归属国家参数
    :param imsi:               ismi号码
    :param status:             imsi卡状态参数
    :param business_status:    imsi卡业务状态参数
    :param slot_status:        imsi卡位状态参数
    :param bam_status:         imsi bam状态参数
    :param occupy_status:      imsi卡占用状态参数
    :param org:                imsi卡归属（GTBU, ...）机构参数
    :param package_status:     imsi套餐状态参数
    :param package_name:       imsi套餐名称参数
    :return:                   返回制定格式json数据{'info': {}, 'data': {}}
    =====================================================================
    """
    query_imsi = imsi
    country_where = ''
    imsi_where = ''
    status_where = ''
    business_status_where = ''
    slot_status_where = ''
    bam_status_where = ''
    occupy_status_where = ''
    org_where = ''
    package_status_where = ''
    package_name_where = ''
    json_results = []
    err_info = ""
    if (not country) and (not package_name):
        err_info = '国家和套餐名称不能同时为空！'
    else:
        if country or package_name:
            if country and package_name:
                country_where = "a.`iso2` = '" + country + "' "
                package_name_where = "AND b.`package_type_name` LIKE '" + package_name + "%' "
            elif country and not package_name:
                country_where = "a.`iso2` = '" + country + "' "
            else:
                package_name_where = "b.`package_type_name` LIKE '" + package_name + "%' "
        if query_imsi:
            imsi_where = "AND a.`imsi` LIKE '" + query_imsi + "%' "
        if status:
            status_where = "AND a.`available_status` in (" + status + ") "
        if business_status:
            business_status_where = "AND a.`business_status` in (" + business_status + ") "
        if package_status:
            package_status_where = "AND b.`package_status` in (" + package_status + ") "
        if slot_status:
            slot_status_where = "AND a.`slot_status` in (" + slot_status + ") "
        if bam_status:
            bam_status_where = "AND a.`bam_status` in (" + bam_status + ") "
        if occupy_status:
            occupy_status_where = "AND a.`occupy_status` in (" + occupy_status + ") "
        if org:
            org_where = "AND e.`org_name` = '" + org + "' "

        query_str = ("SELECT "
                     "DISTINCT CAST(a.`imsi` AS CHAR) AS 'imsi', "
                     "a.`iso2`              AS 'country', "
                     "b.`package_type_name`, "
                     "a.`available_status`  AS 'state', "
                     "(CASE WHEN a.`occupy_status`='0' THEN '未占用' "
                     "WHEN a.`occupy_status`='1' THEN '已占用' END"
                     ") AS 'occupy_status', "
                     "(CASE WHEN a.`slot_status`='0' THEN '未拔出' "
                     "WHEN a.`slot_status`='1' THEN '已拔出' END"
                     ") AS 'slot_status', "
                     "(CASE WHEN a.`activate_status`='0' THEN '已激活' WHEN a.`activate_status`='1' THEN '未激活' END"
                     ") AS 'activate_status', "
                     "(CASE WHEN a.`identify_status`='1' THEN '未提交' WHEN a.`identify_status`='2' THEN '待认证' "
                     "WHEN a.`identify_status`='3' THEN '认证通过' WHEN a.`identify_status`='4' THEN '认证失败'  END"
                     ") AS 'identify_status', "
                     "(CASE WHEN a.`business_status`='0' THEN '卡未停用' WHEN a.`business_status`='1' THEN '卡已停用' "
                     "WHEN a.`business_status`='2' THEN '卡预停用' WHEN a.`business_status`='3' THEN '流量不足，停用' "
                     "WHEN a.`business_status`='4' THEN '卡Pending' WHEN a.`business_status`='5' THEN '待测试卡' "
                     "WHEN a.`business_status`='6' THEN '待下架卡' WHEN a.`business_status`='7' THEN '流量封顶停用' END"
                     ") AS 'business_status', "
                     "(CASE WHEN a.`bam_status`='0' THEN 'BAM正常' WHEN a.`bam_status`='1' THEN 'BAM异常' END "
                     ") AS 'bam_status', "
                     "(CASE WHEN b.`package_status`='0' THEN '正常' "
                     "      WHEN b.`package_status`='1' THEN '限速' "
                     "      WHEN b.`package_status`='2' THEN '不可用' "
                     "      WHEN b.`package_status`='3' THEN '套餐过期' END"
                     ") AS 'package_status', "
                     "(CASE WHEN a.`activate_type`='0' THEN '立即激活' ELSE '首次调用激活' END ) AS 'activate_type', "
                     "(CASE WHEN a.`use_locally`='0' THEN '否' WHEN a.`use_locally`='1' THEN '是' END) AS 'use_locally', "
                     "(CASE WHEN a.`vsim_type`='0' THEN '本国卡' WHEN a.`vsim_type`='1' THEN '多国卡' END) AS 'vsim_type', "
                     "CAST(b.`init_flow`/1024/1024 AS UNSIGNED) as 'init_flow', "
                     "CAST(b.`total_use_flow`/1024/1024 AS UNSIGNED) AS 'total_use_flow', "
                     "CAST(b.`leave_flow`/1024/1024 AS UNSIGNED) as 'leave_flow', "
                     "b.`activate_time`, "
                     "b.`last_update_time` AS 'update_time', "
                     "DATE_FORMAT(b.`next_update_time`,'%Y-%m-%d %H:%m:%s') AS 'next_update_time', "
                     "a.`iccid`, "
                     "a.`bam_id` AS 'bam_code', "
                     "CAST(a.`slot_no` AS CHAR)AS 'slot_num', "
                     "e.`org_name`, "
                     "a.`description` AS 'remarks' "
                     "FROM  `t_css_vsim`               AS a "
                     "LEFT  JOIN `t_css_vsim_packages` AS b  ON a.`imsi`=b.`imsi` "
                     "LEFT  JOIN `t_css_group`         AS e  ON a.`group_id`=e.`id` "
                     "WHERE "
                     " " + country_where + package_name_where + imsi_where + status_where + business_status_where +
                     slot_status_where + bam_status_where + occupy_status_where + org_where + package_status_where
                     )
        try:
            str_db = Sql['qureyNVsim']['db']
            database = Sql['qureyNVsim']['database']
            json_results = get_json_data(sys_str=str_db, database=database, query_str=query_str)
        except KeyError as keyerr:
            err_info = ("KeyError:{}".format(keyerr))
        except mysql.connector.Error as err:
            err_info = ("Something went wrong: {}".format(err))
    if err_info != "":
        dic_results = {'info': {'err': True, 'errinfo': err_info}, 'data': []}

        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
    else:
        if not json_results:
            dic_results = {'info': {'err': False, 'errinfo': "No Query Data"}, 'data': []}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)
        else:
            dic_results = {'info': {'err': False, 'errinfo': err_info}, 'data': json_results}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)


def qury_on_sys_src(country, **kwargs):
    """====================================
    查询新架构卡资源状态统计表单API接口
    :param country: country 参数设置接口
    :return:
    ======================================="""
    # ("查询新架构卡资源：---------------------------------------------------")
    query_imsi = ''
    query_status = ''
    query_business_status = ''
    query_slot_status = ''
    query_bam_status = ''
    query_occupy_status = ''
    query_org = ''
    query_package_status = ''
    query_package_name = ''
    if 'imsi' in kwargs.keys():
        query_imsi = kwargs['imsi']
    if 'status' in kwargs.keys():
        query_status = kwargs['status']
    if 'business_status' in kwargs.keys():
        query_business_status = kwargs['business_status']
    if 'slot_status' in kwargs.keys():
        query_slot_status = kwargs['slot_status']
    if 'bam_status' in kwargs.keys():
        query_bam_status = kwargs['bam_status']
    if 'occupy_status' in kwargs.keys():
        query_occupy_status = kwargs['occupy_status']
    if 'org' in kwargs.keys():
        query_org = kwargs['org']
    if 'package_status' in kwargs.keys():
        query_package_status = kwargs['package_status']
    if 'package_type_name' in kwargs.keys():
        query_package_name = kwargs['package_type_name']

    saas_sim_package_record = qurey_saas_sim(country=country, imsi=query_imsi, status=query_status,
                                             business_status=query_business_status, slot_status=query_slot_status,
                                             bam_status=query_bam_status, occupy_status=query_occupy_status,
                                             org=query_org, package_status=query_package_status,
                                             package_name=query_package_name)

    return saas_sim_package_record
