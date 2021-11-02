# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/18 16:54 
# @Author : lijun7 
# @File : soa_create_order_info.py
# @desc :
"""
import datetime
import time


class SoaOrderInfo:
    def __init__(self):
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        order_sn = 'U{}{}'.format(''.join(today[2:10].split('-')), int(time.time()))
        self.order_sn = order_sn
        self.price = 0
        self.currency_code = "USA"
        self.country_name = "美国"
        self.site_code = "ZF"
