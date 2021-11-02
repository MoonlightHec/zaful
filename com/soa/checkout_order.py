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


class CheckoutOrder:
    """
    数据没法同步到oms，废弃
    """

    def __init__(self, country_name):
        self.country_name = country_name

    def checkout_order(self):
        """
        网站造单，生成收银台页面
        :return:
        """
        headers = {"Content-Type": "application/json"}

        # 环境
        env = {"desc": "旧测试环境", "url": "http://10.40.2.62:2087/gateway/", "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"}
        # env = {"desc":"新测试环境","url":"http://soa-gateway.gw-ec.com/gateway","tokenId":"9988830f2e3c20e61948653d0697bbff"}

        with open('./resource/checkout_order.json', 'r', encoding='utf8') as order_stream:
            body = json.load(order_stream)

        # 生成订单号
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        order_sn = 'U{}{}'.format(''.join(today[2:10].split('-')), int(time.time()))

        # 获取收货国家信息
        with open('./resource/address_book.json', 'r', encoding='utf-8') as fd:
            address = json.load(fd)[self.country_name]

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
        price = 80
        currency_code = 'EUR'
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
        data = {
            "header": {
                "service": "com.globalegrow.spi.pay.inter.PayService",
                "method": "checkout",
                "domain": "",
                "version": "1.0.0",
                "tokenId": env['tokenId']
            },
            "body": body
        }

        response = requests.post(url=env['url'], headers=headers, json=data)
        res_body = response.json()['body']
        if res_body:
            json_body = json.loads(res_body)
            print('order_sn:%s' % order_sn)
            print('token:%s' % json_body['data']['token'])
            print('收银台链接:%s' % json_body['data']['redirectUrl'])

        else:
            print(json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


if __name__ == '__main__':
    cko_order = CheckoutOrder("美国accept")
    cko_order.checkout_order()
