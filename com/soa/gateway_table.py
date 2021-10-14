# _*_ coding: utf-8 _*_
"""
# @Time : 2021/7/19 15:21 
# @Author : lijun7 
# @File : gateway_table.py
# @desc : 64表查订单数据
"""
from flask import json

from com.util.http_utils import HttpRequest


def get_after_risk(order):
    """
    oms推送事后风控信息到支付
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}
    data = {
        "header": {
            "service": "com.globalegrow.spi.pay.inter.PayGatewayService",
            "method": "queryOrderPayGateway",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": {
            "siteCode": "ZF",
            "platform": 1,
            "pipelineCode": "ZF",
            "parentOrderSn": order.get('order_sn'),
            "userId": order.get('user_id')
        }
    }
    output = HttpRequest.post(url=url, headers=headers, body=data)
    res_body = output.get('response')['body'].replace('\\', '')
    try:
        gateway = json.loads(res_body).get('data')['payGateways']

    except TypeError:
        gateway = []
    print(len(gateway))
    print(res_body)


if __name__ == '__main__':
    order_list = [
        {"order_sn": "UU1808202046130061", "user_id": 3405038},
        {"order_sn": "U1706081108222408", "user_id": 0},
        {"order_sn": "U1711241335499892", "user_id": 0}
    ]
    for order in order_list:
        get_after_risk(order)
