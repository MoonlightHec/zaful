# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/18 18:44 
# @Author : lijun7 
# @File : soa_create_order.py
# @desc :
"""
import datetime
import os
import time

import pika
import requests
from flask import json

from com.soa.soa_create_order_info import SoaOrderInfo
from com.util.cursor_util.DbTools import DbTools

# 获取当前文件绝对路径
from com.util.my_logging import logger

db_path = os.path.dirname(os.path.abspath(__file__))


def get_address(country_name):
    # 获取收货国家地址信息
    with open(f'{db_path}/resource/address_book.json', 'r', encoding='utf-8') as fd:
        # 获取当前文件db.py绝对路径
        return json.load(fd)[country_name]


def get_currency_rate(currency_code):
    # 获取汇率
    db = DbTools('PAY')
    sql = "SELECT currency_rate FROM pay_currency_rate WHERE site_code='ZF' AND currency_code ='%s';"
    cursor = db.cursor
    cursor.execute(sql % currency_code)
    if cursor.rowcount:
        return str(cursor.fetchone()[0])
    del db


def deal_string(*args):
    """
    推送MQ数据字符串处理
    :param args:
    :return:
    """
    return ' '.join(args).replace(' ', '+')


class SoaCreateOrder:
    def __init__(self, order_info):
        self.price = order_info.price
        self.currency_code = order_info.currency_code
        self.currency_rate = get_currency_rate(order_info.currency_code)
        self.address_book = get_address(order_info.country_name)
        self.site_code = order_info.site_code
        self.create_time = int(time.time())
        # 生成订单号
        today = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        self.order_sn = 'U{}{}'.format(''.join(today[2:10].split('-')), int(time.time()))
        self.body = {
            "appVersion": None,
            "billingAddressInfo": None,
            "cancelUrl": "http://cart.pc-zaful-master-php5.fpm.egomsl.com/shopping-cart.html",
            "checkoutOrderTag": None,
            "checkoutType": "0",
            "cooperationType": None,
            "dropShipping": None,
            "isPromotionGoods": "false",
            "lang": "en",
            "notifyUrl": "http://www.pc-zaful-master-php5.fpm.egomsl.com/co-pay-ac-notify.html",
            "orderInfos": [
                {
                    "activityDeductAmount": "0.0",
                    "contrabands": None,
                    "couponDeductAmount": "0.0",
                    "createTime": self.create_time,
                    "currencyCode": self.currency_code,
                    "currencyRate": self.currency_rate,
                    "expireTime": None,
                    "exponent": "2",
                    "handlingFee": None,
                    "hasUseCoupon": "0",
                    "insuranceFee": "0.01",
                    "integralDeductAmount": "0.0",
                    "logisticCouponDeductAmount": None,
                    "logisticsGroupName": "Standard Shipping",
                    "logisticsLevel": "1",
                    "logisticsMethod": "Standard Shipping",
                    "orderAddressInfo": {
                        "addressLine1": "addressLine1",
                        "addressLine2": "addressLine2",
                        "city": "city",
                        "countryCode": self.address_book["countryCode"],
                        "countryName": self.address_book["countryName"],
                        "email": "lijunn7@globalegrow.com",
                        "firstName": self.address_book["firstName"],
                        "lastName": self.address_book["lastName"],
                        "postalCode": "77777",
                        "state": self.address_book["state"],
                        "telephone": "15255557845"
                    },
                    "orderAmount": str(self.price),
                    "orderCurrencyAmount": None,
                    "orderGoodsInfos": [
                        {
                            "catName": " Zipper Embossing Argyle Satchel",
                            "catalogue": "Accessories > Bags > Zipper Embossing Argyle Satchel",
                            "categoryId": "33",
                            "categoryName": "Accessories",
                            "goodsExponent": None,
                            "goodsSn": "148786003",
                            "operationType": None,
                            "price": str(round(self.price - 0.01, 2)),
                            "qty": "1",
                            "shopCode": None,
                            "title": "Zipper Embossing Argyle Satchel - Deep Blue"
                        }
                    ],
                    "orderSn": self.order_sn,
                    "orderType": "0",
                    "shippingFee": "0.0",
                    "taxesAmount": "0.0",
                    "trackingFee": "0.0",
                    "userEmail": "lijun7@globalegrow.com",
                    "userId": "188265"
                }
            ],
            "parentOrderSn": self.order_sn,
            "payAmount": str(self.price),
            "payCurrencyAmount": None,
            "payExtendsInfoDto": None,
            "pipelineCode": self.site_code,
            "platform": "1",
            "prepayInfo": None,
            "returnUrl": "http://www.pc-zaful-master-php5.fpm.egomsl.com/co-pay-ac-payok.html",
            "roundType": None,
            "siteCode": self.site_code,
            "swellOrderAmount": None,
            "tokenCreateTime": None,
            "userInfo": {
                "couponNo": "",
                "createTime": self.create_time,
                "dayOfBirth": None,
                "gender": None,
                "growthScore": None,
                "hasGuessCheckout": "1",
                "hasShippedRecords": "0",
                "isNewUser": "0",
                "monthOfBirth": None,
                "registerWay": "1",
                "userEmail": "lijun7@globalegrow.com",
                "userId": "188265",
                "userIp": "10.8.34.246",
                "userLevel": None,
                "yearOfBirth": None
            },
            "userInfoCollection": {
                "reorderItems": "true",
                "shopperAccountModifiedDate": "1629077389",
                "shopperAccountShippingAddressFirstUseDate": "1629077389",
                "shoppingAccountPasswordChangeDate": "1610963371"
            }
        }

    def create_order(self):
        """
        创建订单
        :return:
        """
        url = 'http://10.40.2.62:2087/gateway/'
        headers = {"Content-Type": "application/json"}
        data = {
            "header": {
                "service": "com.globalegrow.spi.pay.inter.PayService",
                "method": "checkout",
                "domain": "",
                "version": "1.0.0",
                "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
            },
            "body": self.body
        }
        response = requests.post(url=url, headers=headers, json=data)
        res_body = response.json()['body']
        if res_body:
            json_body = json.loads(res_body)
            # 订单创建成功，保存订单信息
            self.save_order_info()
            order_success = {
                "order_sn": self.order_sn,
                "收银台链接": json_body['data']['redirectUrl']
            }
            logger.info(f"下单成功：{order_success}")
            logger.info(self.body)
            return json_body['data']['redirectUrl']
        else:
            return json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)

    def save_order_info(self):
        """
        保存订单信息，用于后期推送至oms
        :return:
        """
        origin_order_info = {
            "order_number": self.order_sn,
            "order_id": "49746",
            "pay_ip": "10.8.34.226",
            "payment_status": "1",
            "user_id": "188265",
            "user_email": "lijun7@globalegrow.com",
            "customers": deal_string(self.address_book["firstName"], self.address_book['lastName']),
            "city": "city",
            "state": deal_string(self.address_book["state"]),
            "barangay": "",
            "invoice": "0",
            "remark": "",
            "tax_id": "",
            "taxes_amount": "0.00",
            "point_money": 0,
            "yuan_goods_amount": self.price - 0.01,
            "goods_amount": self.price - 0.01,
            "promotion_code_youhuilv": "",
            "promotion_code": None,
            "used_point": 0,
            "giveIntegral": self.price,
            "order_currency": self.currency_code,
            "order_rate": self.currency_rate,
            "order_create_time": self.create_time,
            "order_from": "45",
            "wj_linkid": "0",
            "order_site": self.site_code,
            "amount_info": f"Items+Sub-total+:{self.price - 0.01}+{self.currency_code}+-+saving:0+{self.currency_code}++++Insurance+0.01+{self.currency_code}+++Shipping+Costs+:"
                           f"0+++tracking_number_price:+0.01=Grand+Total:{self.price}+{self.currency_code}",
            "country": self.address_book["countryCode"],
            "customer_email": "lijun7@globalegrow.com",
            "address1": "address1",
            "address2": "address2",
            "zip_code": "77777",
            "tel": "15255557845",
            "tracking_number_price": 0.01,
            "payment": "",
            "insure_fee": "0.01",
            "handling_fee": "0.00",
            "express": "1",
            "total_post": 0,
            "preferential": 0,
            "order_date": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.create_time)),
            "total_price": self.price,
            "order_product_array": [
                {
                    "rec_id": "68567",
                    "is_lucky_bag": "0",
                    "is_free_shipping": "1",
                    "shipping_price": "21.76",
                    "product_code": "148786003",
                    "quantity": "1",
                    "product_sale_price": self.price - 0.01,
                    "goods_pay_price": "0.00",
                    "product_post_price": "0",
                    "product_remark": "Color: DEEP BLUE ",
                    "goods_type": "0",
                    "cat_id": "33",
                    "delivery_level": "2",
                    "goods_main_type": 0,
                    "is_drainage": "0",
                    "final_shipping_date": "2021-10-12",
                    "discount_price": self.price - 0.01
                }
            ],
            "omsOrderGoodsDeducts": [
                {
                    "goodsSn": "148786003",
                    "growthVal": 0,
                    "qty": "1",
                    "useDeductIntegral": 0,
                    "giveIntegral": self.price
                }
            ],
            "user_info": "YTo3Njp7czo3OiJ1c2VyX2lkIjtzOjY6IjE4ODI2NSI7czo5OiJmaXJzdG5hbWUiO047czo4OiJsYXN0bmFtZSI7TjtzOjg6Im5pY2tuYW1lIjtzOjY6ImxpanVuNyI7czo1OiJlbWFpbCI7czoyMjoibGlqdW43QGdsb2JhbGVncm93LmNvbSI7czozOiJzZXgiO3M6MToiMCI7czoxMDoiYWRkcmVzc19pZCI7czo0OiI5OTgzIjtzOjg6InJlZ190aW1lIjtzOjEwOiIxNjEwOTYzMzcxIjtzOjg6InJlZ19mcm9tIjtzOjE6IjEiO3M6MTI6Im1ha2Vtb25leV9pZCI7czowOiIiO3M6MTA6Imxhc3RfbG9naW4iO3M6MTA6IjE2MzI4OTYxNDEiO3M6OToibGFzdF90aW1lIjtzOjE5OiIwMDAwLTAwLTAwIDAwOjAwOjAwIjtzOjc6Imxhc3RfaXAiO3M6MTE6IjEwLjguMzQuMjI2IjtzOjY6InJlZ19pcCI7czoxMDoiMTAuMzUuMS41NCI7czoxNToibGFzdF9vcmRlcl90aW1lIjtzOjEwOiIxNjMyOTkyNDk5IjtzOjExOiJ2aXNpdF9jb3VudCI7czozOiIxMTYiO3M6OToidXNlcl9yYW5rIjtzOjE6IjAiO3M6NToicGhvbmUiO047czoxMjoiaXNfdmFsaWRhdGVkIjtzOjE6IjEiO3M6MTQ6InZhbGlkYXRlZF90aW1lIjtzOjEwOiIxNjEwOTYzODM2IjtzOjg6ImlzX3Vuc3ViIjtzOjE6IjAiO3M6MTQ6ImlzX25lZWRfY2hrbnVtIjtzOjE6IjEiO3M6ODoiY29tX3JhdGUiO3M6NDoiMC4wNSI7czo5OiJ1c2VyX3R5cGUiO3M6MToiMCI7czoxMjoiaW50cm9kdWN0aW9uIjtOO3M6MTQ6InBheXBhbF9hY2NvdW50IjtOO3M6OToid2pfbGlua2lkIjtzOjE6IjAiO3M6NjoiaXNfZGFvIjtzOjE6IjAiO3M6MTE6ImF2YWlkX3BvaW50IjtzOjQ6IjE4MTciO3M6MTg6ImlzX2Rpbmd5dWVfc3VjY2VzcyI7czoxOiIxIjtzOjEyOiJkaW5neXVlX3RpbWUiO3M6MTk6IjAwMDAtMDAtMDAgMDA6MDA6MDAiO3M6MTI6ImRpbmd5dWVfZnJvbSI7czowOiIiO3M6MTA6ImRpbmd5dWVfaXAiO3M6MDoiIjtzOjk6InNlbmRfbWFpbCI7czoxOiIwIjtzOjE4OiJpc19zeW5jX3RvX21haWxzeXMiO3M6MToiMCI7czoxMToiaXNfZmFjZWJvb2siO3M6MToiMCI7czoyNToicmVzZXRfcGFzc3dvcmRfdmVyaWZ5Y29kZSI7czo0MzoiNTk5YjJhYTAzNTNhZmY2NDFmZDMzODNmYWQzMWU4MjdfMTYxMjQ5MTM4MyI7czoxMjoicGF5X3Bhc3N3b3JkIjtzOjA6IiI7czoyOToicmVzZXRfcGF5X3Bhc3N3b3JkX3ZlcmlmeWNvZGUiO3M6MDoiIjtzOjI1OiJyZXNldF9wYXlfcGFzc3dvcmRfZXhwaXJlIjtzOjEwOiIxNjEyNDkyMjk5IjtzOjIzOiJ3YWxsZXRfZWZmZWN0aXZlX2Ftb3VudCI7czo0OiIwLjAwIjtzOjIxOiJ3YWxsZXRfaW52YWxpZF9hbW91bnQiO3M6NDoiMC4wMCI7czo1OiJmYnVpZCI7czoxOiIwIjtzOjg6Imdvb2dsZUlkIjtzOjA6IiI7czo2OiJmYnVpbGQiO3M6MToiMCI7czo2OiJhdmF0YXIiO3M6Mjk6ImltYWdlcy9kb21laW1nL3VzZXJoZWFkZXIucG5nIjtzOjE3OiJmYWNlYm9va191c2VyX3NyYyI7czoxOiIwIjtzOjg6ImJpcnRoZGF5IjtOO3M6NToidG9rZW4iO3M6MDoiIjtzOjk6ImFwaV90b2tlbiI7czozMjoiNDBiNTdkMmY4MTBmNWEzYjI3MjVhNmViMzUxMGIyYjIiO3M6MTc6InRva2VuX3Zpc2l0X3RpbWVzIjtzOjE6IjAiO3M6NDoibGFuZyI7czoyOiJlbiI7czoxMjoiYWZmaWxpYXRlX2lkIjtzOjE6IjAiO3M6MTM6InVzZXJfZ3JvdXBfaWQiO3M6MToiMCI7czoxNToiaXNfdG9fY29tbXVuaXR5IjtzOjE6IjAiO3M6MTM6InVzZXJfdmlwX3R5cGUiO3M6MToiMCI7czo1OiJnYWlucyI7czo0OiIwLjAwIjtzOjE2OiJncm93X3VwZGF0ZV90aW1lIjtzOjE6IjAiO3M6MTU6Imxhc3RfcG9pbnRfdGltZSI7czoxMDoiMTYzMjg5NjE0MSI7czoyNzoiZWZmZWN0aXZlX2xldmVsX3VwZGF0ZV90aW1lIjtzOjE6IjAiO3M6MTc6ImFwaV90b2tlbl9leHBpcmVzIjtzOjEwOiIxNjQwNjc4OTE3IjtzOjY6ImFmX3VpZCI7czowOiIiO3M6NToiYWRfaWQiO3M6MDoiIjtzOjE5OiJpc19wZXJmZWN0X2ludGVncmFsIjtzOjE6IjAiO3M6MTM6InBvcHVwX2V4cGlyZXMiO3M6MTA6IjE2NDgxNzc4NjEiO3M6ODoiaXNfcm9ib3QiO3M6MToiMCI7czo2OiJpc19kZWwiO3M6MToiMCI7czo4OiJpc19ndWVzdCI7czoxOiIwIjtzOjIyOiJpc19ndWVzdF9yZWdpc3Rlcl9mcm9tIjtzOjE6IjAiO3M6MTE6InBpcGVsaW5lX2lkIjtzOjE6IjEiO3M6MTI6ImlzX3Bob25lX3JlZyI7czoxOiIwIjtzOjE4OiJpc191cGRhdGVfYmlydGhkYXkiO3M6MToiMCI7czo1OiJ2a3VpZCI7czowOiIiO3M6MTA6ImlzX3ZrX3VzZXIiO3M6MToiMCI7czo4OiJhcHBsZV9pZCI7czowOiIiO3M6MTM6ImlzX2FwcGxlX3VzZXIiO3M6MToiMCI7fQ==",
            "drop_shipping_order_number": "",
            "express_code": "",
            "order_warehouse": "ZQ01",
            "is_urgent": 1,
            "used_wallet": 1,
            "order_class": "0",
            "coupon_sign": 0
        }
        with open(f"{db_path}/resource/soa_order_info.json", 'w', encoding='utf-8') as write_order:
            json.dump(origin_order_info, write_order)


def push_to_oms(payment):
    """
    推送订单信息到oms
    :return:
    """
    with open(f"{db_path}/resource/soa_order_info.json", 'r', encoding='utf-8') as read_order:
        message = json.load(read_order)
        message['payment'] = payment
        message = json.dumps(message)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='10.40.6.89',
            port=5672,
            credentials=pika.PlainCredentials('oms_test', 'oms_test')
        )
    )
    # 创建一个 AMQP 信道（Channel）,建造一个大邮箱，隶属于这家邮局的邮箱
    channel = connection.channel()
    # 声明消息队列firstTester，消息将在这个队列传递，如不存在，则创建
    channel.queue_declare(queue='orderInfo_OMS')
    # 向队列插入数值 routing_key的队列名为firstTester，body 就是放入的消息内容，exchange指定消息在哪个队列传递，这里是空的exchange但仍然能够发送消息到队列中，因为我们使用的是我们定义的空字符串“”exchange（默认的exchange）
    channel.basic_publish(exchange='', routing_key='orderInfo_OMS', body=message)
    # 关闭连接
    connection.close()


if __name__ == '__main__':
    order_info = SoaOrderInfo()
    order_info.country_name = "德国"
    order_info.currency_code = "EUR"
    order_info.price = 50
    order_info.site_code = "ZF"
    get_soa_order = SoaCreateOrder(order_info)
    print(get_soa_order.create_order())
