# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/19 16:27 
# @Author : lijun7 
# @File : tools_soa.py
# @desc :
"""
from com.soa.soa_create_order import SoaCreateOrder, push_to_oms
from com.soa.soa_create_order_info import SoaOrderInfo


def create_soa_order(user_order_info):
    """
    创建soa订单
    :param user_order_info:
    :return:
    """
    order_info = SoaOrderInfo()
    order_info.price = float(user_order_info['price'])
    order_info.currency_code = user_order_info['currency-code']
    order_info.country_name = user_order_info['country-name']
    order_info.site_code = user_order_info['site-code']

    # 创建订单
    get_soa_order = SoaCreateOrder(order_info)
    return get_soa_order.create_order()


if __name__ == '__main__':
    order_infos = {
        "country-name": "美国",
        "currency-code": "USD",
        "price": 50,
        "site-code": "ZF"
    }
    # create_soa_order(order_infos)
    push_to_oms("AWX_CC")
