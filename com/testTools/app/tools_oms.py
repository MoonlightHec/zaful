# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/16 0:00 
# @Author : lijun7 
# @File : tools_oms.py
# @desc :
"""
from com.oms.oms_create_order import OmsCreateOrder
from com.oms.oms_create_order_info import OmsOrderInfo


def create_oms_order(user_order_info):
    """
    创建oms订单
    :param user_order_info:
    :return:
    """
    order_info = OmsOrderInfo()
    order_info.customer_id = user_order_info['customer-id']
    order_info.department_id = user_order_info.get('department-id')
    order_info.order_from = user_order_info.get('order-from')
    order_info.settlement_id = user_order_info.get('settlement-id')
    order_info.order_currency = user_order_info.get('order-currency')
    order_info.order_currency_rate = user_order_info.get('order-currency-rate')
    order_info.receiver_email = user_order_info.get('receiver-email')
    order_info.receiver_name = user_order_info.get('receiver-name')
    order_info.receiver_address_1 = user_order_info.get('receiver-address-1')
    order_info.receiver_address_2 = user_order_info.get('receiver-address-2')
    order_info.customer_middle_name = user_order_info.get('customer-middle-name')
    order_info.customer_passport_serial = user_order_info.get('customer-passport-serial')
    order_info.customer_passport = user_order_info.get('customer-passport')
    order_info.customer_passport_issue_date = user_order_info.get('customer-passport-issue-date')
    order_info.receiver_city = user_order_info.get('receiver-city')
    order_info.receiver_province = user_order_info.get('receiver-province')
    order_info.receiver_postcode = user_order_info.get('receiver-postcode')
    order_info.receiver_country_code = user_order_info.get('receiver-country-code')
    order_info.receiver_tel = user_order_info.get('receiver-tel')
    order_info.stock_id = user_order_info.get('stock-id')
    order_info.express_id = user_order_info.get('express-id')
    order_info.express_appoint = user_order_info.get('express-appoint')
    order_info.is_unpacking = user_order_info.get('is-unpacking')
    order_info.registered_fee = user_order_info.get('registered-fee')
    order_info.insurance_fee = user_order_info.get('insurance-fee')
    order_info.shipping_fee = user_order_info.get('shipping-fee')
    order_info.is_invoice = user_order_info.get('is-invoice')
    order_info.remark = user_order_info.get('remark')

    # 产品信息
    products = [
        {"sku": user_order_info["sku0"], "price": user_order_info["price0"], "qty": user_order_info["qty0"], "remark": user_order_info["goods-remark0"]},
    ]
    # 支付信息
    payments = {
        "pay_way": user_order_info["pay-way"],
        "pay_id": user_order_info["pay-id"],
    }
    get_order = OmsCreateOrder(order_info)
    # 创建订单
    return get_order.create_order(products, payments)
