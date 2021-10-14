# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/12 9:32 
# @Author : lijun7 
# @File : get_session.py
# @desc : 获取应用session
"""
import re

import requests


class login_session:
    def __init__(self, app_name, user_name="lijun7", password="lijun789"):
        self.token = None
        self.session = requests.session()
        url = 'http://user.hqygou.com/login/index/checklogin'
        data = {
            "from": "",
            "dosubmit": "",
            "username": user_name,
            "password": password
        }
        res = self.session.post(url=url, data=data)
        try:
            assert "用户管理中心" in res.text
        except AssertionError:
            print("用户中心登录失败\n" + res.text)
            return
        switcher = {
            "plm": self.get_plm_session,
            "oms": self.get_oms_session,
            "wos": self.get_wos_session
        }
        switcher.get(app_name.lower())()

    def get_plm_session(self):
        """
        plm只需要用户中心session
        :return:
        """
        return self.session

    def get_oms_session(self):
        """
        oms需要系统内部session
        :return:
        """
        # 获取系统session
        self.session.get('http://user.hqygou.com/login/index/sso/?struli=aHR0cDovL29tcy5ocXlnb3UuY29tfGh0dHA6Ly9vbXMuaHF5Z291LmNvbQ==&from=OMS')

        # 验证登录信息是否有效
        check_res = self.session.post("http://oms.hqygou.com/index/index/getpageinfo", data={"module": "order", "controller": "current", "action": "search"})
        try:
            assert "userName not set" not in check_res.text
        except AssertionError:
            print("系统登录失败\n" + check_res.text)
            return
        print("系统登录成功")
        return self.session

    def get_wos_session(self):
        """
        wos需要系统内部session和token
        :return:
        """
        # 获取系统session和token
        res = self.session.get(
            'http://user.hqygou.com/login/index/sso?struli=aHR0cDovL3dvcy5ocXlnb3UuY29tL3YxL2xvZ2luL2luZGV4P2NsaWVudD1odHRwcyUzQSUyRiUyRndvcy5ocXlnb3UuY29tJTJGJTIzJTJGaG9tZSUyRml'
            'uZGV4fGh0dHA6Ly93b3MuaHF5Z291LmNvbS92MS9sb2dpbi9pbmRleD9jbGllbnQ9aHR0cHMlM0ElMkYlMkZ3b3MuaHF5Z291LmNvbSUyRiUyMyUyRmhvbWUlMkZpbmRleA%3D%3D&from=WOS_TEST')
        self.token = re.findall(r'token=(.*)', res.url)[0]

        # 验证登录信息是否有效
        check_res = self.session.get('https://wos.hqygou.com/v1/menus/index', headers={"Authorization": "Bearer {}".format(self.token)})
        data_length = len(check_res.json()['data'])
        try:
            assert data_length != 0
        except AssertionError:
            print("系统登录失败\n" + check_res.text)
            return
        return self.session, self.token


if __name__ == '__main__':
    ls = login_session(app_name='oms', user_name='yaojie', password='123456')
