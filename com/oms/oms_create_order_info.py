# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/12 18:21 
# @Author : lijun7 
# @File : oms_create_order_info.py
# @desc :
"""
import datetime
import time


class OmsOrderInfo:
    def __init__(self):
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        order_sn = 'U{}{}'.format(''.join(today[2:10].split('-')), int(time.time()))
        self.customer_id = 775
        self.order_sn = order_sn
        self.department_id = 42
        self.order_from = 45
        self.settlement_id = 1
        self.order_currency = 'USD'
        self.order_currency_rate = 1.0000000000
        self.receiver_email = 'lijun7@globalegrow.com'
        self.receiver_name = '李军7'
        self.receiver_address_1 = 'address_1'
        self.receiver_address_2 = 'address_2'
        self.customer_middle_name = None
        self.customer_passport_serial = None
        self.customer_passport = None
        self.customer_passport_issue_date = None
        self.receiver_city = 'ADELSHOFEN'
        self.receiver_province = 'Alaska'
        self.receiver_postcode = '55555'
        self.receiver_country_code = 'DE'
        self.receiver_tel = '545775444'
        self.stock_id = 1
        self.express_id = 17
        self.express_appoint = 0
        self.is_unpacking = 1
        self.registered_fee = 0.5
        self.insurance_fee = 0.1
        self.shipping_fee = 1.5
        self.is_invoice = 0
        self.remark = None



