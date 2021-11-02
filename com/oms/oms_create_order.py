# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/13 10:44 
# @Author : lijun7 
# @File : oms_create_order.py
# @desc : oms创建订单
"""
from com.util.get_session import login_session
from com.oms.oms_create_order_info import OmsOrderInfo
from com.util.cursor_util.DbTools import DbTools
from com.util.my_logging import logger


class OmsCreateOrder:
    def __init__(self, order_info):
        self.login = login_session('oms')
        self.data = {
            'customer_id': order_info.customer_id,
            'order_sn': order_info.order_sn,
            'department_id': order_info.department_id,
            'order_from': order_info.order_from,
            'settlement_id': order_info.settlement_id,
            'order_currency': order_info.order_currency,
            'order_currency_rate': order_info.order_currency_rate,
            'receiver_email': order_info.receiver_email,
            'receiver_name': order_info.receiver_name,
            'receiver_address_1': order_info.receiver_address_1,
            'receiver_address_2': order_info.receiver_address_2,
            'customer_middle_name': order_info.customer_middle_name,
            'customer_passport_serial': order_info.customer_passport_serial,
            'customer_passport': order_info.customer_passport,
            'customer_passport_issue_date': order_info.customer_passport_issue_date,
            'receiver_city': order_info.receiver_city,
            'receiver_province': order_info.receiver_province,
            'receiver_postcode': order_info.receiver_postcode,
            'receiver_country_code': order_info.receiver_country_code,
            'receiver_tel': order_info.receiver_tel,
            'stock_id': order_info.stock_id,
            'express_id': order_info.express_id,
            'express_appoint': order_info.express_appoint,
            'is_unpacking': order_info.is_unpacking,
            'registered_fee': order_info.registered_fee,
            'insurance_fee': order_info.insurance_fee,
            'shipping_fee': order_info.shipping_fee,
            'is_invoice': order_info.is_invoice,
            'remark': order_info.remark
        }
        self.account = 0

    def add_products(self, products_info):
        """
        添加产品信息
        :param products_info:
        :return:
        """
        db = DbTools('oms')
        sql = "SELECT * FROM g_oms_goods WHERE goods_sn='%s';"
        # 添加产品信息
        account = 0
        i = 0
        for product in products_info:
            res = db.cursor.execute(sql % product["sku"])
            if res:
                product_info = {
                    f"products[{i}][0]": product["sku"],
                    f"products[{i}][1]": product["price"],
                    f"products[{i}][2]": product["qty"],
                    f"products[{i}][3]": product["remark"]
                }
                self.data.update(product_info)
                # 计算单个商品价格
                account = account + int(product["qty"]) * float(product["price"])
                i += 1
            else:
                logger.info(f"该产品不存在：{product['sku']}")
        # 合计所有费用：商品总价+挂号费+保险费+运费
        self.account = account + float(self.data['registered_fee']) + float(self.data['insurance_fee']) + float(self.data['shipping_fee'])

    def add_payments(self, payments):
        """
        添加支付信息
        :param payments:
        :return:
        """
        # 先款后货订单
        if str(self.data['settlement_id']) == '1':
            payments = {
                "payments[0][0]": payments['pay_way'],
                "payments[0][1]": payments['pay_id'],
                "payments[0][2]": self.account,
            }
            self.data.update(payments)
        # 账期订单
        else:
            logger.info("付款方式不支持")
            pass

    def create_order(self, products_info, payments):
        """
        创建订单
        :param payments: 支付信息
        :param products_info: 产品信息
        :return:
        """
        self.add_products(products_info)
        self.add_payments(payments)

        # 订单暂存区下订单接口
        url = "http://oms.hqygou.com/order/temp/insert"
        res = self.login.session.post(url, data=self.data)
        if res.json()['content'] == '保存成功':
            logger.info(self.data['order_sn'])
            return self.data['order_sn']


if __name__ == '__main__':
    # 注意价格不要有两位小数，python四舍五入不准导致价格不对，订单付款状态会不对
    my_products = [
        {"sku": 148786003, "price": 2.6, "qty": 1, "remark": "产品备注"},
        {"sku": 1428786004, "price": 58.6, "qty": 1, "remark": "产品备注"},
        {"sku": 148786004, "price": 3.6, "qty": 1, "remark": "产品备注"},
    ]
    my_payments = {"pay_way": 9, "pay_id": "20210810134055", "account": 0}
    my_order_info = OmsOrderInfo()
    get_order = OmsCreateOrder(my_order_info)
    get_order.create_order(my_products, my_payments)
