# -*- coding: utf-8 -*-

from flask import request
from . import api
from .api_functions.get140countryFlowerStatics import qury_140country_flower_statics


@api.route('/get_140countryFlowerStatics/', methods=['POST'])
def get_140country_flower_statics():
    """
    本API140国卡统计页面统计数据接口
    :return:
    """
    if request.method == 'POST':
        dic_data = request.get_json()
        begin_time = str(dic_data['beginTime'])
        end_time = str(dic_data['endTime'])
        time_zone_off_set = str(dic_data['TimezoneOffset'])

        return qury_140country_flower_statics(begin_time=begin_time, end_time=end_time,
                                              time_zone_off_set=time_zone_off_set)

    return False
