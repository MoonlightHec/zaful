# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/12 9:38 
# @Author : mhec 
# @File : Reuters.py
# @desc : 汇率XE Reuters
"""
import requests
from flask import json


def get_reuters():
    url = 'https://www.reuters.com/companies/api/getFetchQuotes/false'
    currency = ['AUD', 'CAD']
    for cur in currency:
        url = url + ',' + 'USD' + cur
    print(url)
    headers = {"Content-Type": "application/json"}

    res = requests.get(url=url, headers=headers).json()
    rates = res['market_data']['currencypairs']
    count = len(res['market_data']['currencypairs'])
    currency_list = []
    for rate in rates:
        last = rate['last']
        symbol = rate['symbol']
        currency = {
            'last': last,
            'symbol': symbol
        }
        currency_list.append(currency)
    result = {'currency': currency_list}
    result_json = json.dumps(result, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
    print('获取到%s条汇率数据' % count)
    print('market_data{}'.format(result_json))
    with open(r'./resource/reuters.json', 'w') as stream:
        stream.write(json.dumps(res, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


def get_xe():
    """
    主页：https://www.xe.com/
    :return:
    """
    url = 'https://www.xe.com/api/protected/midmarket-converter/'
    headers = {
        "Content-Type": "application/json",
        "authorization": "Basic bG9kZXN0YXI6ODlJb2puVGVyUXlYcFVUQUJLcUljcFViQU4zUnZvUTQ="
    }
    res = requests.get(url=url, headers=headers).json()
    with open('./resource/xe_rate.json', 'w') as stream:
        stream.write(json.dumps(res, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))
    currency_list = ['HKD', 'ZAR']
    for currency in currency_list:
        print('%s:%s' % (currency, res['rates'][currency]))


if __name__ == '__main__':
    get_xe()
