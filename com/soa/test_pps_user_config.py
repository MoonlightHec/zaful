# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/7 16:45 
# @Author : mhec 
# @File : pps_user_config.py
# @desc : 用户配置中心
"""
import json

import pytest

from com.soa.resource.pay_params import user_config_datas
from com.util.cursor_util import db
from com.util.http_utils import HttpRequest
from com.util.sort_yaml import ordered_yaml_load


class AssertFun:
    def __init__(self, res, assert_data):
        self.res = res
        self.assert_data = assert_data
        self.cursor = db.get_connect('PAY').cursor()

    def assert_select(self, method):
        actual = None
        res_body = json.loads(self.res.get('response')['body'])
        res_data = res_body['data']
        if res_data:
            actual = res_data['configKey']
        expect = self.assert_data['config_key']
        if actual == expect:
            print("{}用例执行通过".format(method))
        else:
            print("{}用例执行失败".format(method))
        print('actual:【{}】----expect:【{}】\n'.format(actual, expect))

    def assert_delete(self, method):
        expect = self.assert_data['message']
        actual = self.res.get('response')['header']['message']
        print('接口返回:【{}】\n'.format(self.res.get('preview')))
        if expect == actual:
            print("{}用例执行通过".format(method))
        else:
            print("{}用例执行失败".format(method))
        print('actual:【{}】----expect:【{}】\n'.format(actual, expect))

    def assert_add(self, method):
        self.assert_delete(method)

    def assert_update(self, method):
        self.assert_delete(method)

    def assert_select_list(self, method):
        if self.res.get('response')['header']['message']:
            print("请求参数错误！")
        else:
            print(self.res.get('response'))
            res_body = json.loads(self.res.get('response')['body'])
            print('接口返回:【{}】\n'.format(json.dumps(res_body, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)))


@pytest.mark.parametrize('case_datas', user_config_datas['config_case'])
def test_user_config(case_datas):
    """
    用户配置
    :return:
    """
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    case_list = case_datas['cases']
    for case_data in case_list:
        # 获取测试用例yaml文件数据
        header = {
            "service": "com.globalegrow.spi.mpay.inter.PayUserConfigService",
            "method": case_data['method'],
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        }
        body = {
            "header": header,
            "body": case_data['body']
        }
        # 获取接口请求结果
        res = HttpRequest.post(url=url, headers=headers, body=body)

        assert_fun = AssertFun(res, case_data['assert'])
        function = getattr(assert_fun, case_data['assert_method'])
        function(case_data['method'])


def user_config(method):
    url = 'http://10.40.2.62:2087/gateway/'
    headers = {"Content-Type": "application/json"}

    datas = ordered_yaml_load(r'./resource/pps_user_config_cases')
    case_datas = datas['config_case'][method]['cases']
    for case_data in case_datas:
        # 获取测试用例yaml文件数据
        header = {
            "service": "com.globalegrow.spi.mpay.inter.PayUserConfigService",
            "method": case_data['method'],
            "domain": "",
            "version": "1.0.0",
            "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
        }
        body = {
            "header": header,
            "body": case_data['body']
        }
        print(u'请求参数\n{}'.format(json.dumps(body, sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)))
        # 获取接口请求结果
        res = HttpRequest.post(url=url, headers=headers, body=body)
        try:
            assert_fun = AssertFun(res, case_data['assert'])
            switcher = {
                '0': assert_fun.assert_select,
                '1': assert_fun.assert_delete,
                '2': assert_fun.assert_add,
                '3': assert_fun.assert_update,
                '4': assert_fun.assert_select_list
            }
            # 执行断言方法
            switcher.get(str(method))(case_data['method'])
        except KeyError:
            pass


if __name__ == '__main__':
    # pytest.main(['-s', 'test_pps_user_config.py'])
    user_config(2)
