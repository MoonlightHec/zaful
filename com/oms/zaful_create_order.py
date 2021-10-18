# _*_ coding: utf-8 _*_
"""
# @Time : 2021/7/13 17:33 
# @Author : lijun7 
# @File : zaful_create_order.py
# @desc :
"""
import hashlib

import requests

# 禁用安全警告信息；requests忽略ssl证书后，控制台不再输出警告信息
from com.oms.WebminObj import WebminObj
from com.util.cursor_util.DbTools import DbTools
from com.util.http_utils import HttpRequest

requests.packages.urllib3.disable_warnings()


def push_mq(order_sn, joint=False):
    """
    2.前端网站推送订单到MQ
    :param order_sn: 订单号
    :param joint: 是否是联合订单
    :return:
    """
    if joint:
        # 联合订单
        url = 'http://www.pc-zaful-master-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/warehouse/OrderToOmsApi.php?order_sn=%s' % order_sn
        print('联合订单')
    else:
        # 普通订单
        url = 'http://www.pc-zaful-master-php5.fpm.egomsl.com/eload_admin/crontab/xcmq/order_to_oms_api.php?order_sn=%s' % order_sn
        print('普通订单')
    response = HttpRequest.get(url)
    print(response)


def audit_payment(order_sn):
    """
    4.审核付款单
    :param order_sn:订单号
    :return:
    """
    db_tools = DbTools('OMS')
    connect = db_tools.connect
    cursor = db_tools.cursor
    sql = "UPDATE f_oms_payment_info SET matched_status=1 WHERE order_sn=\'%s\';"
    cursor.execute(sql % order_sn)
    connect.commit()
    del db_tools


def webmin_job(*args):
    """
    5.匹配订单
    :param webmin_name: 脚本名称
    :param order_sn: 订单编号
    :return:
    """
    web_script = WebminObj('oms')
    web_script.run_script(*args)


def md5(string):
    m = hashlib.md5()
    m.update(string.encode("utf8"))
    print("加密前：【{}】,加密后：【{}】".format(string, m.hexdigest()))
    return m.hexdigest()


def joint_order_2oms(order_sn, step=0):
    """
    联合订单推送到oms
    :param order_sn:
    :param step:
    :return:
    """
    md5(order_sn)
    if step == 0:
        # 网站推送订单
        push_mq(order_sn, joint=True)
    elif step == 1:
        # oms导入脚本
        web_soaOrder_received = WebminObj('oms', 'soa_mq_oms_received')
        web_soaOrder_received.run_script()
    elif step == 2:
        # 投递脚本
        web_soaOrder_intoMq = WebminObj('oms', 'soa_order_into_mq')
        web_soaOrder_intoMq.run_script(order_sn, md5(order_sn)[:2])
    elif step == 3:
        # 消费脚本
        web_soaOrder_into_oms = WebminObj('oms', 'get_soa_mq_into_oms')
        web_soaOrder_into_oms.run_script()
    else:
        return


if __name__ == '__main__':
    oms_order_sn = 'U2110151634282684'
    # 网站MQ推送订单到oms
    # push_mq(oms_order_sn, joint=False)

    # oms接收订单
    webmin_job('同步soa订单', oms_order_sn)
    # 审核付款单
    # audit_payment(oms_order_sn)
    """
    # 匹配订单
    # match_payment_info 正常订单
    # match_payment_info_nopay cod订单
    """
    # webmin_job('匹配订单', oms_order_sn)

    # 联合订单推送到oms
    # joint_order_2oms(oms_order_sn, step=1)
