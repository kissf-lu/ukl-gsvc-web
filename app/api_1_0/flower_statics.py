# -*- coding: utf-8 -*-

from bson import json_util
from flask import json
from flask import request
# api 模块添加
from . import api


import time as t
# Python get Flower Model
from app.api_1_0.api_functions.flowerPackage.get_vsim_hour_day_flower import get_flowers
# sim_package_flower get Model
from .api_functions.flowerPackage.get_sim_package_flower import get_sim_package_flower_next_api
from .api_functions.flowerPackage.get_sim_package_flower import get_sim_package_flower_api


@api.route('/get_FlowerQuery/', methods=['POST', 'GET'])
def get_FlowerQuery():
    """
    :return:
    """
    # paramKeyFromRequest = ['querySort','begintime','endtime','mcc','plmn','imsi','agg_group_key','TimezoneOffset']
    dic_data = request.get_json()
    try:
        query_sort = str(dic_data['querySort'])
        time_list = dic_data['timeList']
        query_mcc = str(dic_data['mcc'])
        query_plmn = str(dic_data['plmn'])
        query_imsi = str(dic_data['imsi'])
        agg_group_key = dic_data['agg_group_key']
        time_zone_off_set = int(dic_data['TimezoneOffset'])
    except KeyError as ke:
        errinfo = ("前端POST数据异常,KeyError:{}".format(ke))
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}
        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)

    return get_flowers(query_sort=query_sort,
                       time_list=time_list,
                       mcc=query_mcc,
                       plmn=query_plmn,
                       imsi=query_imsi,
                       flower_query_key=agg_group_key)


@api.route('/get_package_flower/', methods=['GET'])
def get_package_flower():
    """
    :return:
    """
    if request.method == 'GET':
        sim_package_param = {
            'country': request.args.get('Country', 'ae', type=str),
            'orgName': request.args.get('Org', 'gtbu', type=str),
            'simType': request.args.get('SimType', '0', type=str),
            'packageTypeName': request.args.get('PackageTypeName', '', type=str),
            'avaStatus': request.args.get('AvaStatus', '', type=str),
            'businessStatus': request.args.get('BusinessStatus', '', type=str),
            'packageStatus': request.args.get('PackageStatus', '', type=str),
            'slotStatus': request.args.get('SlotStatus', '', type=str),
            'bamStatus': request.args.get('BamStatus', '', type=str)
        }

        return get_sim_package_flower_api(sim_package_param=sim_package_param)

    return False


@api.route('/get_package_flower_next/', methods=['GET', 'POST'])
def get_package_flower_next():
    """
    :return:
    """
    if request.method == 'POST':
        dic_data = request.get_json()
        try:
            package_data = {
                'country': str(dic_data['Country']),
                'org': str(dic_data['Org']),
                'sim_type': str(dic_data['SimType']),
                'package_type_name': str(dic_data['PackageTypeName']),
                'next_update_time': str(dic_data['NextUpdateTime']),
                'ava_status': str(dic_data['AvaStatus']),
                'business_status': str(dic_data['BusinessStatus']),
                'package_status': str(dic_data['PackageStatus']),
                'slot_status': str(dic_data['SlotStatus']),
                'bam_status': str(dic_data['BamStatus']),
                'add_group_key': dic_data['addGroupKey'],
                'dispatch_begin_time': t.strftime('%Y-%m-%d %H:%M:%S', t.gmtime(dic_data['ListTime'][0]['begin'])),
                'dispatch_end_time': t.strftime('%Y-%m-%d %H:%M:%S', t.gmtime(dic_data['ListTime'][-1]['end']))
            }
            flower_data = {
                'query_type': dic_data['queryType'],
                'list_time': dic_data['ListTime'],
                'add_group_key': dic_data['addGroupKey']
            }

        except KeyError as ke:
            errinfo = ("前端POST数据异常,KeyError:{}".format(ke))
            dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': []}

            return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)

        return get_sim_package_flower_next_api(package_data=package_data, flower_data=flower_data)

    return False
