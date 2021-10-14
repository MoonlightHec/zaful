# _*_ coding: utf-8 _*_
"""
# @Time : 2021/9/9 11:25 
# @Author : lijun7 
# @File : pay_awx.py
# @desc :
"""

import requests
from flask import json


class AWX_Test:
    def __init__(self):
        self.allDomains = {
            'apiDomain': 'https://api-demo.airwallex.com',
            'fileDomain': 'https://files-demo.airwallex.com',
            'paDomain': 'https://pci-api-demo.airwallex.com',
            'isDomain': 'https://pci-api-demo.airwallex.com'
        }
        self.client = {
            'clientId': '4OuJUnXeQuGF9jZuEhl8-Q',
            'apiKey': 'df2bc288be96410ef540d16290f00d67761d342af8f9774845d26c5428c72644e99e44ad86f89e32d7ad60b01a622ed1',
        }
        self.headers = {
            "Authorization": "Bearer {}".format(self.login()),
            "Content-Type": "application/json",
        }

    def login(self):
        url = '{}/api/v1/authentication/login?api_key={}&client_id={}'.format(self.allDomains['paDomain'], self.client['apiKey'], self.client['clientId'])
        headers = {
            'Content-Type': 'application/json',
            'x-client-id': self.client['clientId'],
            'x-api-key': self.client['apiKey']
        }
        res = requests.post(url=url, headers=headers)
        token = res.json().get('token')
        # print("login token:\n{}".format(token))
        return token

    def get_payment(self, transaction_id):
        """
        查询支付记录
        :param transaction_id:
        :return:
        """
        url = '{}/api/v1/pa/payment_intents/{}'.format(self.allDomains['paDomain'], transaction_id)
        headers = self.headers
        res = requests.get(url, headers=headers)
        self.preview(res)

    def get_refunds(self, payment_intent_id):
        """
        查询awx退款记录
        :param payment_intent_id:
        :return:
        """
        url = '{}/api/v1/pa/refunds'.format(self.allDomains['paDomain'])
        params = {
            "payment_intent_id": payment_intent_id
        }
        res = requests.get(url, headers=self.headers, params=params)
        if res.status_code == 200:
            return res

    def preview(self, response):
        try:
            print(json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))
        except AttributeError:
            print(json.dumps(response, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False))

    def run_refunds(self, payment_intent_id='', result='SUCCEEDED', awx_refund_sn=None):
        """
        模拟第三方发送退款通知
        :param payment_intent_id:
        :param result:退款结果
        :param awx_refund_sn: 退款id
        :return:
        """
        items = self.get_refunds(payment_intent_id).json()['items']
        if awx_refund_sn:
            for item in items:
                if item['metadata']['refundSn'] == awx_refund_sn:
                    refunds_obj = item
        else:
            refunds_obj = items[0]
        self.preview(refunds_obj)
        refunds_obj['status'] = result
        data = {
            "accountId": "acct_xJ_pXQ3pOiOiGCkcSP0c7Q",
            "createdAt": "2021-08-18T00:54:49+0000",
            "data": {
                "object": refunds_obj
            },
            "id": "evt_hkdmnwcv6g1iq8mc8ik_694bm8",
            "name": "refund.succeeded",
            "version": "2020-04-30",
            "account_id": "acct_xJ_pXQ3pOiOiGCkcSP0c7Q",
            "created_at": "2021-08-18T00:54:49+0000"
        }
        if result == 'FAILED':
            data['name'] = 'refund.failed'

        url = 'http://10.40.2.52:8182/awx/notify'
        res = requests.post(url, headers=self.headers, json=data)
        if res.status_code == 200:
            print('接收退款通知成功')


if __name__ == '__main__':
    intent_id = 'int_hkdmlcbfqg36aecw3cl'
    awx_pay_sn = 'U2110102021599653'
    refund_sn = 'B210923013287182905DVI'
    awx_cc = AWX_Test()
    # awx_cc.get_payment(intent_id)
    print(awx_cc.preview(awx_cc.get_refunds(intent_id)))
    # result='FAILED',result='SUCCEEDED'
    awx_cc.run_refunds(payment_intent_id=intent_id, result='SUCCEEDED')
