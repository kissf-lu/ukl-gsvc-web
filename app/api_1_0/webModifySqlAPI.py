# -*- coding: utf-8 -*-
"""
    webModifySqlAPI
    ~~~~~~~~~~~~~~
    为web应用与后台数据库操作（插入，更新，删除操作）的接口
    api_functions 中的DataApiFunc.py为其接口函数汇聚点，所有全局变量设置都在此；所有后台函数调用都在此设置
    Implementation helpers for the JSON support in Flask.

    :copyright: (c) 2015 by Armin kissf lu.
    :license: ukl, see LICENSE for more details.
"""

from . import api
from flask import json
from flask import request
from bson import json_util
# DataApiFunc 为数据库更新、插入、删除数据等操作函数
from .api_functions.DataApiFunc import (dele_manul_vsim_src,
                                        insert_manul_vsim_src,
                                        update_manule_vsim_src,
                                        delete_new_vsim_test_info,
                                        insert_new_vsim_test_info,
                                        update_new_vsim_test_info
                                        )


@api.route('/delet_manulVsim/', methods=['POST'])
def delet_manulVsim():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return dele_manul_vsim_src(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/insert_manulVsim/', methods=['POST'])
def insert_manulVsim():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return insert_manul_vsim_src(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/update_manulVsim/', methods=['POST'])
def update_manulVsim():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return update_manule_vsim_src(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/delet_newvsimtest_info_table/', methods=['POST'])
def delet_newvsimtest_info_table():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return delete_new_vsim_test_info(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/insert_newvsimtest_info_table/', methods=['POST'])
def insert_newvsimtest_info_table():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return insert_new_vsim_test_info(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)


@api.route('/update_newvsimtest_info_table/', methods=['POST'])
def update_newvsimtest_info_table():
    """

    :return:
    """
    if request.method == 'POST':
        arrayData = request.get_array(field_name='file')

        return update_new_vsim_test_info(array_data=arrayData)

    else:
        returnJsonData = {'err': True, 'errinfo': '操作违法！', 'data': []}

        return json.dumps(returnJsonData, sort_keys=True, indent=4, default=json_util.default)
