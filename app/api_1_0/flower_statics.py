# -*- coding: utf-8 -*-

from bson import json_util
from flask import json
from flask import request
# api 模块添加
from . import api

# Python get Flower Model
from app.api_1_0.api_functions.flowerPackage.get_vsim_hour_day_flower import getFlowers
# sim_package_flower get Model
from api_functions.flowerPackage.get_sim_package_flower import getSimPackageFlowerNextAPI
from api_functions.flowerPackage.get_sim_package_flower import getSimPackageFlowerAPI


@api.route('/get_FlowerQuery/', methods=['POST', 'GET'])
def get_FlowerQuery():
    """
    :return:
    """
    # paramKeyFromRequest = ['querySort','begintime','endtime','mcc','plmn','imsi','agg_group_key','TimezoneOffset']
    Dic_data = request.get_json()
    try:
        querySort = str(Dic_data['querySort'])
        timeList = Dic_data['timeList']
        queryMcc = str(Dic_data['mcc'])
        queryPlmn = str(Dic_data['plmn'])
        queryImsi = str(Dic_data['imsi'])
        aggGroupKey = Dic_data['agg_group_key']
        TimezoneOffset = int(Dic_data['TimezoneOffset'])
    except KeyError as keyerr:
        errInfo = ("前端POST数据异常,KeyError:{}".format(keyerr))
        DicData = []
        DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': DicData}
        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)

    return getFlowers(querySort=querySort,
                      time_list=timeList,
                      mcc=queryMcc,
                      plmn=queryPlmn,
                      imsi=queryImsi,
                      flower_query_key=aggGroupKey,
                      TimezoneOffset=TimezoneOffset)


@api.route('/get_package_flower/', methods=['GET'])
def get_package_flower():
    """
    :return:
    """
    if request.method == 'GET':
        simPackageParam = {
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

        return getSimPackageFlowerAPI(sim_package_param=simPackageParam)

    return False


@api.route('/get_package_flower_next/', methods=['GET', 'POST'])
def get_package_flower_next():
    """
    :return:
    """
    if request.method == 'POST':
        Dic_data = request.get_json()
        try:
            package_date ={
                'country': str(Dic_data['Country']),
                'org': str(Dic_data['Org']),
                'sim_type': str(Dic_data['SimType']),
                'package_type_name': str(Dic_data['PackageTypeName']),
                'next_update_time': str(Dic_data['NextUpdateTime']),
                'ava_status': str(Dic_data['AvaStatus']),
                'business_status': str(Dic_data['BusinessStatus']),
                'package_status': str(Dic_data['PackageStatus']),
                'slot_status': str(Dic_data['SlotStatus']),
                'bam_status': str(Dic_data['BamStatus']),
                'add_group_key': Dic_data['addGroupKey']
            }
            flower_date = {
                'query_type': Dic_data['queryType'],
                'list_time': Dic_data['ListTime'],
                'add_group_key': Dic_data['addGroupKey']
            }

        except KeyError as keyerr:
            errInfo = ("前端POST数据异常,KeyError:{}".format(keyerr))
            DicData = []
            DicResults = {'info': {'err': True, 'errinfo': errInfo}, 'data': DicData}

            return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)

        # errInfo = country+org+sim_type+package_type_name+next_update_time+'status'+ava_status+business_status+\
        #           package_status+slot_status+bam_status
        return getSimPackageFlowerNextAPI(package_data=package_date, flower_data=flower_date)

    return False
