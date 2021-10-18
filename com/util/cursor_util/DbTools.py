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

    def execute_sql(self, mysql, *args):
        self.cursor.execute(mysql % args)
        result = self.cursor.fetchall()
        self.connect.commit()
        print("execute_sql影响数据：{}".format(self.cursor.rowcount))
        return result


if __name__ == '__main__':
    db = DbTools('wms')
    sql = "UPDATE prepare_goods set `status`=4 WHERE prepare_goods_no = '%s';"
    sns = ['Test28644001122155168639911', 'Test41444385812012168639311', 'Test58883404204506168638131', 'Test38679606414920168637901', 'Test96336041436144168637541',
           'Test93105501069950168636111', 'Test20528087644320168635811', 'Test18030197405691168635781', 'Test18013970354452168635341', 'Test18636171569769168635131',
           'Test21020799593317168635121', 'Test74129687684849168635111', 'Test67223087752245168635061', 'Test59702663902899168634911', 'Test74210799754860168634671',
           'Test13434894083093168633261', 'Test24586875535643168633051', 'Test33487041550071168630291', 'Test10596342634474168629131', 'Test95211927796162168628032',
           'Test33845664780576168623722', 'Test69679572355913168623382', 'Test93542063739771168622232', 'Test46348900483967168620262', 'Test40495298673854168620242',
           'Test56250614886118168619462', 'Test30082956150921168618792', 'Test16574999371120168618732', 'Test67281587343419168617812', 'Test63583913384008168617002',
           'Test90719591352831168616232', 'Test15970866569466168614102', 'Test57148424524293168613322', 'Test36148205340362168613282', 'Test70412329185282168612812',
           'Test44709473335150168612792', 'Test73560727595163168612732', 'Test19655623439450168612722', 'Test42539507386811168612672']
    sns2 = ['S4556687277040182185257', 'S1744727334729138065646']
    for sn in sns2:
        db.execute_sql(sql, sn)
    del db
