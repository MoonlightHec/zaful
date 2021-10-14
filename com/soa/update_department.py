# _*_ coding: utf-8 _*_
"""
# @Time : 2021/6/30 15:18 
# @Author : lijun7 
# @File : update_department.py
# @desc : 同步部门表数据
"""
from com.util.http_utils import HttpRequest


def update_user():
    url = 'http://www.obs-pay.com/crontab/department/sync'
    response = HttpRequest.get(url=url)
    print(response.get('preview'))


if __name__ == '__main__':
    update_user()
