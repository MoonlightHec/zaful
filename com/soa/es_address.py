# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/3 11:12 
# @Author : River 
# @File : es_address.py
# @desc : ES灰名单
"""
import json

import requests


def delete_or_select():
    """
    es灰名单地址数据增删查
    :return:
    """
    url_par = ('_new', '')
    url_type = 'GET'
    blacklist_id = '1000112438'
    url = 'http://10.40.2.46:9200/pay_risk_fulladress_list_index%s/fulladress_list_type%s/pay_blacklist_%s'
    headers = {"Content-Type": "application/json", "Authorization": "Basic c29hOnNvYTY2NjY2Ng=="}
    for num in url_par:
        request_url = url % (num, num, blacklist_id)
        # 查询es数据
        if 'GET' == url_type:
            response = requests.get(request_url).json()
        # 删除es数据
        elif 'DELETE' == url_type:
            response = requests.delete(request_url).json()
        # 往es添加数据
        elif 'PUT' == url_type:
            write_data = {"cause_type": 3, "fulladdress": "pt braga vizela 11111115 massachusetts avenue", "lock_status": 1,
                          "match_level_default_type": 0, "match_numbers": 100, "match_ratio": 0.75}
            response = requests.put(request_url, headers=headers, json=write_data).json()
        # json格式输出 sort_keys:是否按照a-z排序；indent：缩进格数；separators：设置分隔符
        output = json.dumps(response, sort_keys=False, indent=4, separators=(',', ':'))
        print('request-%s: %s' % (url_type, request_url))
        print('blacklist_id:%s' % blacklist_id)
        print('response:')
        print(output)


delete_or_select()
