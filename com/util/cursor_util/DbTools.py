# _*_ coding: utf-8 _*_
"""
# @Time : 2021/8/27 9:10 
# @Author : lijun7 
# @File : DbTools.py
# @desc :
"""
import os

import pymysql

from com.util import sort_yaml


class DbTools:
    def __init__(self, name):
        path = r'/db_hqyg_config.yaml'
        # 获取当前文件db.py绝对路径
        db_path = os.path.dirname(os.path.abspath(__file__))
        datas = sort_yaml.ordered_yaml_load(db_path + path)

        db_config = datas[name.upper()]
        self.connect = pymysql.connect(**db_config)
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.cursor.close()
        self.connect.close()

    def execute_sql(self, sql, *args):
        self.cursor.execute(sql % args)
        res = self.cursor.fetchall()
        self.connect.commit()
        return res


if __name__ == '__main__':
    db = DbTools('oms')
    sql = "SELECT * FROM oms.s_oms_send_email WHERE order_sn ='%s';"
    res = db.cursor.execute(sql % ('U2110102021599653',))
    print(res)
    res2 = db.execute_sql(sql % ('U2110102021599653',))
    print(res2)
    del db
