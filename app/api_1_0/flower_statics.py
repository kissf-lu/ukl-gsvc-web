# -*- coding: utf-8 -*-

from bson import json_util
from flask import json
from flask import request

# Python get Flower Model
from app.api_1_0.api_functions.flowerPackage.get_vsim_hour_day_flower import getFlowers
from . import api


@api.route('/get_FlowerQuery/', methods=['POST', 'GET'])
def get_FlowerQuery():
    """
    :return:
    """
    # paramKeyFromRequest = ['querySort','begintime','endtime','mcc','plmn','imsi','agg_group_key','TimezoneOffset']
    Dic_data = request.get_json()
    try:
        querySort = str(Dic_data['querySort'])
        begintime = str(Dic_data['begintime'])
        endtime = str(Dic_data['endtime'])
        queryMcc = str(Dic_data['mcc'])
        queryPlmn = str(Dic_data['plmn'])
        queryImsi = str(Dic_data['imsi'])
        aggGroupKey = Dic_data['agg_group_key']
        TimezoneOffset = int(Dic_data['TimezoneOffset'])
    except KeyError:
        errinfo = '前端POST数据异常!'
        DicData = []
        DicResults = {'info': {'err': True, 'errinfo': errinfo}, 'data': DicData}
        return json.dumps(DicResults, sort_keys=True, indent=4, default=json_util.default)

    return getFlowers(querySort=querySort,
                      begintime=begintime,
                      endtime=endtime,
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
        country = request.args.get('Country', 'ae', type=str)
        orgName = request.args.get('Org', 'gtbu', type=str)
        vsimType = request.args.get('SimType', '0', type=str)
        packageTypeName = request.args.get('PackageTypeName', '', type=str)

        errinfo = '前端后端API测试： get args ->' + country + '-' + orgName + '-' + vsimType + '-' + packageTypeName
        dic_data = []
        dic_results = {'info': {'err': True, 'errinfo': errinfo}, 'data': dic_data}

        return json.dumps(dic_results, sort_keys=True, indent=4, default=json_util.default)

    return False
