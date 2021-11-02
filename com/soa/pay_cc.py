# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/21 17:26 
# @Author : lijun7 
# @File : pay_cc.py
# @desc :
"""
import requests
from flask import json

from com.util.my_logging import logger


class Pay_CC:
    def __init__(self):
        self.url = 'https://sandbox-pg.pacypay.com/'

    def get_pay_info(self, pay_sn):
        """
        获取支付请求信息
        :param pay_sn:
        :return:
        """
        url = '{}/query/transaction'.format(self.url)
        params = {
            "merchantNo": "2246",
            "tradeTimeStart": "2021-10-11 00:00:00",
            "tradeTimeEnd": "2022-10-11 00:00:00",
            "sign": "b45dc50226e63ff0b0b14979fc0bdfe8f03ed012ae55ece7ba3d029ecb700b46"
        }
        all_data = requests.get(url, params).json()["trans"]
        for data in all_data:
            if data['transactionId'] == pay_sn:
                print(json.dumps(data, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


if __name__ == '__main__':
    pay_cc = Pay_CC()
    pay_cc.get_pay_info('P211022013287171803NJE')
