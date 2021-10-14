# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/17 14:49 
# @Author : lijun7 
# @File : checkout_order.py
# @desc : 生成收银台页面
"""
import datetime
import time

import requests
from flask import json

from com.util.cursor_util.DbTools import DbTools


def deal_string(*args):
    return ' '.join(args).replace(' ', '+')


def save_order_info(body):
    with open('../oms/resource/zf_order_info.json', 'r', encoding='utf-8') as read_order:
        origin_order_info = json.load(read_order)
    order_addressI_info = body['orderInfos'][0]['orderAddressInfo']
    origin_order_info['order_number'] = body['orderInfos'][0]['orderSn']
    # origin_order_info['customers'] = deal_string(order_addressI_info['firstName'], order_addressI_info['lastName'])
    origin_order_info['customers'] = deal_string(order_addressI_info['firstName'], order_addressI_info['lastName']).encode("utf-8").decode("utf-8")
    origin_order_info['city'] = deal_string(order_addressI_info['city'])
    origin_order_info['state'] = deal_string(order_addressI_info['state'])
    origin_order_info['yuan_goods_amount'] = body['orderInfos'][0]['orderGoodsInfos'][0]['price']
    origin_order_info['goods_amount'] = body['orderInfos'][0]['orderGoodsInfos'][0]['price']
    origin_order_info['order_currency'] = body['orderInfos'][0]['currencyCode']
    origin_order_info['order_rate'] = body['orderInfos'][0]['currencyRate']
    origin_order_info['order_create_time'] = body['orderInfos'][0]['createTime']
    origin_order_info['country'] = order_addressI_info['countryCode']
    origin_order_info['address1'] = order_addressI_info['addressLine1']
    origin_order_info['address2'] = order_addressI_info['addressLine2']
    origin_order_info['zip_code'] = order_addressI_info['postalCode']
    origin_order_info['tel'] = order_addressI_info['telephone']
    print(body['orderInfos'][0]['createTime'])
    origin_order_info['order_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(body['orderInfos'][0]['createTime']))
    origin_order_info['total_price'] = body['orderInfos'][0]['orderAmount']
    with open('../oms/resource/zf_order_info2.json', 'w', encoding='utf-8') as write_order:
        json.dump(origin_order_info, write_order)


def checkout_order(country_name='美国'):
    """
    网站造单，生成收银台页面
    :param country_name: 收货国家名称
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    with open('./resource/checkout_order.json', 'r', encoding='utf8') as order_stream:
        body = json.load(order_stream)

    # 生成订单号
    today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    order_sn = 'U{}{}'.format(''.join(today[2:10].split('-')), int(time.time()))

    # 获取收货国家信息
    with open('./resource/address_book.json', 'r', encoding='utf-8') as fd:
        address = json.load(fd)[country_name]

    body['orderInfos'][0]['orderSn'] = order_sn
    body['orderInfos'][0]['orderAddressInfo']['firstName'] = address['firstName']
    body['orderInfos'][0]['orderAddressInfo']['lastName'] = address['lastName']
    body['orderInfos'][0]['orderAddressInfo']['countryCode'] = address['countryCode']
    body['orderInfos'][0]['orderAddressInfo']['countryName'] = address['countryName']
    body['orderInfos'][0]['orderAddressInfo']['state'] = address['state']
    body['orderInfos'][0]['orderAddressInfo']['addressLine1'] = 'addressLine1'
    body['orderInfos'][0]['orderAddressInfo']['addressLine2'] = 'addressLine2'
    body['orderInfos'][0]['orderAddressInfo']['city'] = 'ADELSHOFEN'
    body['orderInfos'][0]['createTime'] = int(time.time())
    body['parentOrderSn'] = order_sn
    # 需要改价格的订单
    price = 81.59
    currency_code = 'USD'
    body['orderInfos'][0]['orderAmount'] = price
    body['orderInfos'][0]['orderGoodsInfos'][0]['price'] = round(price - 0.01, 2)
    body['payAmount'] = price
    body['orderInfos'][0]['currencyCode'] = currency_code
    # 获取汇率
    db = DbTools('PAY')
    sql = "SELECT currency_rate FROM pay_currency_rate WHERE site_code='ZF' AND currency_code ='%s';"
    cursor = db.cursor
    cursor.execute(sql % currency_code)
    if cursor.rowcount:
        currency_rate = cursor.fetchone()[0]
    del db
    body['orderInfos'][0]['currencyRate'] = str(currency_rate)
    save_order_info(body)
    data = {
        "header": {
            "service": "com.globalegrow.spi.pay.inter.PayService",
            "method": "checkout",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": body
    }

    response = requests.post(url=url, headers=headers, json=data)
    res_body = response.json()['body']
    if res_body:
        json_body = json.loads(res_body)
        print('order_sn:%s' % order_sn)
        print('token:%s' % json_body['data']['token'])
        print('收银台链接:%s' % json_body['data']['redirectUrl'])
        # save_order_info(body)

    else:
        print(json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


if __name__ == '__main__':
    checkout_order("美国accept")
