# -*- coding: utf-8 -*-


"""======================================================
本模块为批量修改数据库信息接口函数，设计mysql,mongo等数据库:
==========================================================
1、手工维护表批量更新、导入、删除资源API接口，以下为对应的三个接口函数：
dele_manule_vsim_src，insert_manule_vsim_src，update_manule_vsim_src
2、新卡测试接口：

===================================================================
@author: lujian
============================================================================"""
# import mysql.connector
import json
from bson import json_util
from .updateSqlPack.insertoneColModle import (insertModel, insertFetchSRCModel)
from .updateSqlPack.updateOneColModle import updateModel
from .updateSqlPack.deleteModel import deleteModel
from .SqlPack.SqlLinkInfo import DataApiFuncSqlLink as Sql

SqlInfo = Sql


def confirm_excel_template_reg(excel_col_name, reg_col_name):
    """===================================
    本函数为内部调用函数，确认批量模板是否正确。
    :param excel_col_name:
    :param reg_col_name:
    :return:
    ======================================"""
    col_base = reg_col_name
    col_confirm = excel_col_name
    confirm_rs = True

    if (col_base != []) and (col_confirm != []):
        if len(col_base) != len(col_confirm):
            confirm_rs = False
        else:
            for i in range(len(col_base)):
                try:
                    if col_base[i] != col_confirm[i]:
                        confirm_rs = False
                except IndexError:
                    confirm_rs = False
    else:
        confirm_rs = False

    return confirm_rs


def get_dict_excel_data(array_data, key_database, key_mirr_database):
    """==========================================================
    本函数将前端传入的array_data数据和对应的key_database
    :param array_data: 待处理前端数据
    :param key_database: 与数据库的列表相同，用于替换前端中文标头值
    :param key_mirr_database: 与前端表头相同的中文列表
    =============================================================
    :return:
    =================================================================="""
    dic_data = []
    key_dic = key_database
    key_mirr = key_mirr_database
    err_info = ''
    if (type(array_data) is list) and (len(array_data) >= 2):
        for i in range(len(array_data)):
            temp_dic = {}
            if i == 0:
                excel_clo_name = array_data[0]
                # 根据excelCloName和key_mirr判断模板是否正确
                if_confirm = confirm_excel_template_reg(excel_col_name=excel_clo_name, reg_col_name=key_mirr)
                if not if_confirm:
                    err_info = "模板非法！核实模板是否正确！"
                    return_dict_data = {'err': True, 'errinfo': err_info, 'data': []}

                    return return_dict_data
            else:
                for j in range(len(key_dic)):
                    try:
                        temp_dic.update({key_dic[j]: array_data[i][j]})
                    except IndexError:
                        err_info = 'Index Error'
                dic_data.append(temp_dic)

    else:
        err_info = '导入数据不合法！请核实模板数据。'
    if err_info:
        return_dict_data = {'err': True, 'errinfo': err_info, 'data': []}
    else:
        return_dict_data = {'err': False, 'errinfo': err_info, 'data': dic_data}

    return return_dict_data


def get_dict_excel_data_next(array_data, key_database, key_mirr_database):
    """==========================================================
    本函数将前端传入的array_data数据和对应的key_database
    :param array_data: 待处理前端数据
    :param key_database: 与数据库的列表相同，用于替换前端中文标头值
    :param key_mirr_database: 与前端表头相同的中文列表
    =============================================================
    :return:
    =================================================================="""
    dic_data = []
    key_dic = key_database
    key_mirr = key_mirr_database
    err_info = ''
    if (type(array_data) is list) and (len(array_data) >= 2):
        for i in range(len(array_data)):
            temp_dic = {}
            if i == 0:
                excel_clo_name = array_data[0]
                # 根据excelCloName和key_mirr判断模板是否正确
                if_confirm = confirm_excel_template_reg(excel_col_name=excel_clo_name, reg_col_name=key_mirr)
                if not if_confirm:
                    err_info = "模板非法！核实模板是否正确！"
                    return_dict_data = {'err': True, 'errinfo': err_info, 'data': []}

                    return return_dict_data
            else:
                for j in range(len(key_dic)):
                    try:
                        temp_dic.update({key_dic[j]: array_data[i][j]})
                    except IndexError:
                        err_info = 'Index Error'
                dic_data.append(temp_dic)

    else:
        err_info = '导入数据不合法！请核实模板数据。'
    if err_info:
        return_dict_data = {'err': True, 'errinfo': err_info, 'data': []}
    else:
        return_dict_data = {'err': False, 'errinfo': err_info, 'data': dic_data}

    return return_dict_data


def dele_manul_vsim_src(array_data):
    """=============================
    数据删除API函数
    :param array_data:
    :return:
    ================================"""
    data_from_js = array_data
    delete_database_item = [u'imsi']
    delete_data_mirr = [u'imsi']
    dic_data = get_dict_excel_data(array_data=data_from_js, key_database=delete_database_item,
                                   key_mirr_database=delete_data_mirr)
    if dic_data['err']:
        return_json_data = {'err': True, 'errinfo': dic_data['errinfo']}
        return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
    else:
        state_result = deleteModel(SqlInfo=SqlInfo['DeleManuleVsimSrc'], arrayDicData=dic_data['data'],
                                   delete_key='imsi')
        if state_result != '':
            return_json_data = {'err': True, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
        else:
            return_json_data = {'err': False, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)


def insert_manul_vsim_src(array_data):
    """============================
    数据插入API函数
    :param array_data:
    :return:
    ==============================="""
    # state_result = ''
    data_from_js = array_data
    # 此key用于替换insertDataMirr中对应的key，用于后续进行数据库插入key
    insert_database_item = [
        u'imsi',
        u'person_gsvc',
        u'country_cn',
        u'operator',
        u'charge_noflower',
        u'operator_info',
        u'pay_mode',
        u'call_mode',
        u'remarks',
        u'person_operator',
        u'expiring_time',
        u'vsim_batch_num',
        u'owner_attr',
        u'country_attr'
    ]
    # 此key为核实前端表格表头是否符合实际模板要求：列数相同、顺序相同
    insert_data_mirr = [
        u'imsi',
        u'负责人',
        u'国家',
        u'运营商',
        u'超套餐限速/费用',
        u'运营商网站的注册信息',
        u'套餐办理方式',
        u'查询方式',
        u'备注',
        u'运营接口人',
        u'下架日期',
        u'卡批次',
        u'是否代理商卡 0否，1是代理商卡',
        u'卡的国家属性 0本国卡，1是多国卡'
    ]
    dic_data = get_dict_excel_data(array_data=data_from_js, key_database=insert_database_item,
                                   key_mirr_database=insert_data_mirr)
    if dic_data['err']:
        return_json_data = {'err': True, 'errinfo': dic_data['errinfo']}
        return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
    else:
        state_result = insertFetchSRCModel(sql_info=SqlInfo['InsertManuleVsimSrc'],
                                           dic_data=dic_data['data'],
                                           key_dic={'insert': 'imsi',
                                                    'merge': 'imsi'})
        if state_result != '':
            return_json_data = {'err': True, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
        else:
            return_json_data = {'err': False, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)


def update_manule_vsim_src(array_data):
    """==================================
    数据更新API函数
    :param array_data:
    ======================================
    :return:
    ======================================"""
    # state_result = ''
    data_from_js = array_data
    # ("此key用于替换insertDataMirr中对应的key，用于后续进行数据库插入key")
    update_database_item = [
        u'imsi',
        u'person_gsvc',
        u'country_cn',
        u'operator',
        u'charge_noflower',
        u'operator_info',
        u'pay_mode',
        u'call_mode',
        u'remarks',
        u'person_operator',
        u'expiring_time',
        u'vsim_batch_num',
        u'owner_attr',
        u'country_attr'
    ]
    # ("此key为核实前端表格表头是否符合实际模板要求：列数相同、顺序相同")
    update_data_mirr = [
        u'imsi',
        u'负责人',
        u'国家',
        u'运营商',
        u'超套餐限速/费用',
        u'运营商网站的注册信息',
        u'套餐办理方式',
        u'查询方式',
        u'备注',
        u'运营接口人',
        u'下架日期',
        u'卡批次',
        u'是否代理商卡 0否，1是代理商卡',
        u'卡的国家属性 0本国卡，1是多国卡'
    ]
    dic_data = get_dict_excel_data(array_data=data_from_js, key_database=update_database_item,
                                   key_mirr_database=update_data_mirr)

    if dic_data['err']:
        return_json_data = {'err': True, 'errinfo': dic_data['errinfo']}
        return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
    else:
        state_result = updateModel(sql_info=SqlInfo['updateManuleVsimSrc'],
                                   dic_data=dic_data['data'],
                                   update_key='imsi')
        if state_result:
            return_json_data = {'err': True, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
        else:
            return_json_data = {'err': False, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)


def delete_new_vsim_test_info(array_data):
    """=============================
    数据删除API函数
    :param array_data:
    :return:
    ================================"""
    data_from_js = array_data
    delete_database_item = [u'id_newvsimtest']
    delete_data_mirr = [u'id_newvsimtest']
    dic_data = get_dict_excel_data(array_data=data_from_js, key_database=delete_database_item,
                                   key_mirr_database=delete_data_mirr)
    if dic_data['err']:
        return_json_data = {'err': True, 'errinfo': dic_data['errinfo']}
        return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
    else:
        state_result = deleteModel(SqlInfo=SqlInfo['NewVsimTestInfo']['Delete'],
                                   arrayDicData=dic_data['data'],
                                   delete_key='id_newvsimtest')
        if state_result != '':
            return_json_data = {'err': True, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
        else:
            return_json_data = {'err': False, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)


def insert_new_vsim_test_info(array_data):
    """============================
    数据插入API函数
    :param array_data:
    :return:
    ==============================="""
    # state_result = ''
    data_from_js = array_data
    # 此key用于替换insertDataMirr中对应的key，用于后续进行数据库插入key
    insert_database_item = [
        u'person_supplier',
        u'person_test',
        u'card_info',
        u'vsim_type',
        u'country_cn',
        u'country_iso',
        u'operator',
        u'plmn',
        u'rat',
        u'config_change',
        u'imsi',
        u'user_code',
        u'imei',
        u'device_type',
        u'success_time',
        u'change_time',
        u'register_operator',
        u'eplmn',
        u'register_rat',
        u'lac',
        u'cellid',
        u'service_usability',
        u'stability_onehour',
        u'agree_mbr',
        u'agree_consistency',
        u'fail_reason',
        u'remark'
    ]
    # 此key为核实前端表格表头是否符合实际模板要求：列数相同、顺序相同
    insert_data_mirr = [
        u"卡提供人",
        u"测试人",
        u"测试卡信息",
        u"卡类型(0本国, 1多国)",
        u"国家",
        u"简称",
        u"运营商",
        u"plmn",
        u"网络制式(GSM-4，WCDM-8，LTE-16，GSM/WCDMA-12,WCDMA/LTE-24,GSM/WCDMA/LTE-28)",
        u"配置更改",
        u"imsi",
        u"账户",
        u"imei",
        u"设备类型",
        u"调卡成功时间",
        u"换卡时间",
        u"注册运营商",
        u"eplmn",
        u"注册网络",
        u"lac",
        u"cellid",
        u"测试是否通过(0 否, 1是)",
        u"小时稳定性(0 否, 1是)",
        u"协商速率",
        u"协商速率一致性(0 否, 1是)",
        u"失败原因",
        u"备注"
    ]
    dic_data = get_dict_excel_data(array_data=data_from_js, key_database=insert_database_item,
                                   key_mirr_database=insert_data_mirr)
    if dic_data['err']:
        return_json_data = {'err': True, 'errinfo': dic_data['errinfo']}
        return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
    else:
        state_result = insertModel(sql_info=SqlInfo['NewVsimTestInfo']['Insert'],
                                   dic_data=dic_data['data'],
                                   insert_key='id_newvsimtest')
        if state_result != '':
            return_json_data = {'err': True, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
        else:
            return_json_data = {'err': False, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)


def update_new_vsim_test_info(array_data):
    """============================
    数据插入API函数
    :param array_data:
    :return:
    ==============================="""
    # state_result = ''
    data_from_js = array_data
    # 此key用于替换insertDataMirr中对应的key，用于后续进行数据库插入key
    insert_database_item = [
        u'id_newvsimtest',
        u'person_supplier',
        u'person_test',
        u'card_info',
        u'vsim_type',
        u'country_cn',
        u'country_iso',
        u'operator',
        u'plmn',
        u'rat',
        u'config_change',
        u'imsi',
        u'user_code',
        u'imei',
        u'device_type',
        u'success_time',
        u'change_time',
        u'register_operator',
        u'eplmn',
        u'register_rat',
        u'lac',
        u'cellid',
        u'service_usability',
        u'stability_onehour',
        u'agree_mbr',
        u'agree_consistency',
        u'fail_reason',
        u'remark'
    ]
    # 此key为核实前端表格表头是否符合实际模板要求：列数相同、顺序相同
    insert_data_mirr = [
        u"测试id",
        u"卡提供人",
        u"测试人",
        u"测试卡信息",
        u"卡类型(0本国, 1多国)",
        u"国家",
        u"简称",
        u"运营商",
        u"plmn",
        u"网络制式(GSM-4，WCDM-8，LTE-16，GSM/WCDMA-12,WCDMA/LTE-24,GSM/WCDMA/LTE-28)",
        u"配置更改",
        u"imsi",
        u"账户",
        u"imei",
        u"设备类型",
        u"调卡成功时间",
        u"换卡时间",
        u"注册运营商",
        u"eplmn",
        u"注册网络",
        u"lac",
        u"cellid",
        u"测试是否通过(0 否, 1是)",
        u"小时稳定性(0 否, 1是)",
        u"协商速率",
        u"协商速率一致性(0 否, 1是)",
        u"失败原因",
        u"备注"
    ]
    dic_data = get_dict_excel_data(array_data=data_from_js, key_database=insert_database_item,
                                   key_mirr_database=insert_data_mirr)
    if dic_data['err']:
        return_json_data = {'err': True, 'errinfo': dic_data['errinfo']}
        return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
    else:
        state_result = updateModel(sql_info=SqlInfo['NewVsimTestInfo']['Update'],
                                   dic_data=dic_data['data'],
                                   update_key='id_newvsimtest')
        if state_result != '':
            return_json_data = {'err': True, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
        else:
            return_json_data = {'err': False, 'errinfo': state_result}
            return json.dumps(return_json_data, sort_keys=True, indent=4, default=json_util.default)
