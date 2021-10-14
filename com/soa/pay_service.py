# _*_ coding: utf-8 _*_
"""
# @Time : 2021/9/14 16:40 
# @Author : lijun7 
# @File : refund_withdrawal.py
# @desc : SOA对外部系统提供的gateway服务
# 已实现的功能：
退款
提现
"""
import random

import requests
from flask import json

from com.util.cursor_util.DbTools import DbTools


def get_case_datas(pay_gateway_id=31, pay_sn=None):
    """
    获取订单信息
    :param pay_sn:
    :param pay_gateway_id: 订单所在gateway分表序号
    :param pay_id: 数据主键id
    :return:
    """
    sql = 'SELECT id,parent_order_sn,pay_status,pay_sn,pay_account,site_code,currency_code,pay_amount,channel_code,' \
          'currency_code,currency_rate,pay_currency_amount,user_id FROM pay_gateway_%s WHERE pay_sn ="%s";' % (pay_gateway_id, pay_sn)
    db = DbTools('PAY')
    cursor = db.cursor
    cursor.execute(sql)
    del db
    for row in cursor.fetchall():
        case_data = {
            'des': row[5],
            'order_sn': row[1],
            'pay_sn': row[3],
            'siteCode': row[5],
            'amount': float(row[7]),
            'account': row[4],
            'currency_amount': float(row[11]),
            'message': None,
            'success': None,
            'currency_code': row[9],
            'currency_rate': float(row[10]),
            'channel': row[8],
            'user_id': row[12]
        }
    return case_data


class PayService:
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}
        self.url = 'http://10.40.2.62:2087/gateway/'
        self.data_header = {
            "service": "com.globalegrow.spi.pay.inter.RefundService",
            "method": "refund",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        }
        self.data = {
            "header": self.data_header,
            "body": None
        }

    def pay_run(self, service, method, body):
        self.data['header']['service'] = service
        self.data['header']['method'] = method
        self.data['body'] = body
        res = requests.post(url=self.url, headers=self.headers, json=self.data)
        return res

    def refunds(self, refund_type=0, pay_sn=None, refunds_amount=None):
        """
        oms请求支付退款接口
        :param refund_type: # 0原路退 1电子钱包
        :param pay_sn: # 退款支付号
        :param refunds_amount: # 退款金额，默认全部退
        :return:
        """
        case_data = get_case_datas(pay_sn=pay_sn)
        if refunds_amount:
            case_data['currency_amount'] = refunds_amount
            case_data['amount'] = refunds_amount / case_data['currency_rate']
        body = {
            "orderSn": case_data['order_sn'],
            "refundAccountId": 2359975,
            "refundDtos": [{
                "amount": case_data['amount'],
                "channelCode": case_data['channel'],
                "currencyAmount": case_data['currency_amount'],
                "currencyCode": case_data['currency_code'],
                "currencyRate": case_data['currency_rate'],
                "omsTxId": case_data['pay_sn'],
                "paySn": case_data['pay_sn']
            }],
            "refundType": refund_type,  # 0原路退 1电子钱包
            "remark": "一级原因:客户原因退款,二级原因:忘记使用折扣码",
            "siteCode": case_data['siteCode'],
            "sourceId": 'TKSQ2018070422' + str(random.randint(100000, 999999)),
            "userEmail": "lijun7@globalegrow.com",
            "userId": case_data['user_id']
        }
        res = self.pay_run(service='com.globalegrow.spi.pay.inter.RefundService', method='refund', body=body)
        print(json.dumps(res.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))

    def withdrawal(self, pay_sn=None, amount=None):
        """
        提现接口
        :param pay_sn: 订单号
        :param amount: 提现金额，默认全部提现
        :return:
        """
        case_data = get_case_datas(pay_sn=pay_sn)
        if amount:
            case_data['amount'] = amount
        body = {
            "userId": case_data['user_id'],
            "siteCode": case_data['siteCode'],
            "withdrawalInfoList": [
                {
                    "paySn": case_data['pay_sn'],
                    "channelCode": case_data['channel'],
                    "withdrawalAmount": case_data['amount'],
                    "sourceId": 'TKSQ2018070422' + str(random.randint(100000, 999999)),
                    "withdrawalAccountId": str(random.randint(100000000000, 999999999999)),
                    "withdrawalCurrencyAmount": case_data['currency_amount'],
                    "withdrawalCurrencyCode": case_data['currency_code'],
                    "withdrawalCurrencyRate": case_data['currency_rate']
                }
            ]
        }
        res = self.pay_run(service='com.globalegrow.spi.pay.inter.RefundService', method='withdrawal', body=body)
        print(self.data)
        print(json.dumps(res.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))


if __name__ == '__main__':
    pay = PayService()
    pay.refunds(pay_sn='P210922013287173008EAB', refunds_amount=20)
