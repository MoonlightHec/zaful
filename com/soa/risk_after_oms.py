# _*_ coding: utf-8 _*_
"""
# @Time : 2021/3/15 10:01 
# @Author : River 
# @File : risk_after_oms.py
# @desc : oms推送事后风控结果
"""
from com.util.http_utils import HttpRequest


def get_after_risk(pay_sn):
    """
    oms推送事后风控信息到支付
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}
    data = {
        "header": {
            "service": "com.globalegrow.risk.api.core.RiskCoreService",
            "method": "afterRiskProcessor",
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        },
        "body": {
            "paySn": pay_sn, "omsId": ""
        }
    }
    response = HttpRequest.post(url=url, headers=headers, body=data)
    print(response.get('preview'))


if __name__ == '__main__':
    for i in range(0,1):
        get_after_risk('P211028013287162412PVC')
