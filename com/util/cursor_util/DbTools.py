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
from com.util.my_logging import logger


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

    def execute_sql(self, mysql, *args):
        self.cursor.execute(mysql % args)
        result = self.cursor.fetchall()
        self.connect.commit()
        logger.info("execute_sql影响数据：{}".format(self.cursor.rowcount))
        return result


if __name__ == '__main__':
    logger.info("yyyyyyyyyyyyyyyy")
