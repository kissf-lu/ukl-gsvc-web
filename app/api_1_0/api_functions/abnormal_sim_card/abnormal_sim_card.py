# -*- coding: utf-8 -*-


# sql json格式查询接口
from app.api_1_0.api_functions.SqlPack.SQLModel import qureResultAsJson
# sql information of connect to mysql
from app.api_1_0.api_functions.SqlPack.SqlLinkInfo import getonSysSrc as sqlLink
# redis model
import redis as r

mysql_link = {
    'css': sqlLink['qureyNVsim']
}


def get_json_data(sys_str, data_base, query_str):
    """
    qureResultAsJson 自带链接断开操作
    :param sys_str: 
    :param data_base: 
    :param query_str: 
    :return: 
    """
    json_results = qureResultAsJson(sysStr=sys_str, Database=data_base, query_str=query_str, where=[])
    return json_results


def redis_connect_ping():
    """
    
    :return: if ping ok True else False
    """
    redis_con = r.StrictRedis(host='localhost', port=6379, db=0, password='redis#gsvc')

    if redis_con.ping():
        li = redis_con.client_list()
        print('connect ok!')
        try:
            for conn in li:
                print('kill connect: ', conn['addr'])
            redis_con.client_kill(conn['addr'])
        except KeyError as ke:
            print('There is something error as KeyError:{}'.format(ke))


        return True
    else:
        return False


if __name__ == '__main__':

    if redis_connect_ping():
        print('out!')
