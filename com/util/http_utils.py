# _*_ coding: utf-8 _*_
"""
# @Time : 2021/2/4 14:55 
# @Author : River 
# @File : HttpRequest.py
# @desc :
"""
import json
from json import JSONDecodeError

import requests

from com.util.my_logging import logger


class HttpRequest:
    @staticmethod
    def get(url, headers=None, params=None):
        """
        :param url: 请求地址
        :param headers: 请求头
        :param params: 请求参数
        :return:
        """
        response = requests.get(url, headers=headers, params=params)
        try:
            preview = json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
            output = {'request': url, 'response': response.json(), 'preview': preview}
        except JSONDecodeError:
            output = response.text
        return output

    @staticmethod
    def post(url, headers=None, cookies=None, body=None, verify=False):
        """
        :param verify:
        :param url: 请求地址
        :param headers: 请求头
        :param cookies:
        :param body: 请求body
        :return:
        """
        headers_type = headers.get("Content-Type")
        if headers_type == "application/json":
            response = requests.post(url, headers=headers, cookies=cookies, json=body, verify=verify)
        elif headers_type == "application/x-www-form-urlencoded":
            response = requests.post(url, headers=headers, cookies=cookies, data=body, verify=verify)
        else:
            print("请求参数格式不支持")
            return
        try:
            """
            处理接口返回数据
            返回格式为json
            sort_keys=False：按字母排序
            indent=4:格式化缩进
            separators = (',', ':') ','逗号左右空格，':'冒号左右空格
            ensure_ascii：unicode转中文
            """
            preview = json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
            output = {'request': url, 'body': body, 'response': response.json(), 'preview': preview}
            return output
        except JSONDecodeError:
            return {'request': url, 'response': response}

    @staticmethod
    def file(url, headers=None, cookies=None, img=None):
        with open(img['path'] + img['name'], 'rb') as stream:
            body = {
                'file': (img['name'], stream, img['type'])
            }
            response = requests.post(url=url, headers=headers, cookies=cookies, files=body)
        preview = json.dumps(response.json(), sort_keys=False, indent=4, separators=(',', ':'), ensure_ascii=False)
        output = {'request': url, 'body': body, 'response': response.json(), 'preview': preview}
        logger.info(output.get('response'))
        return output
