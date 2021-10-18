# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/15 17:21 
# @Author : lijun7 
# @File : order_all_process.py
# @desc :
"""
import requests

from com.get_session import login_session
from com.util.cursor_util.DbTools import DbTools


class OrderAllProcess:
    def __init__(self, order_sn):
        self.order_sn = order_sn

    def get_picking_sn(self):
        """
        获得配货单号
        :return:
        """
        oms_db = DbTools('OMS')
        new_order_sql = "SELECT order_number_new FROM oms.o_oms_order_picking_info WHERE order_sn='%s'"
        new_order_res = oms_db.execute_sql(new_order_sql, self.order_sn)
        del oms_db
        try:
            picking_sn = new_order_res[0][0]
            return picking_sn
        except IndexError:
            return '未找到配货单，可能oms未配货'

    def wms_get_picking_order(self):
        """
        wms接收配货单
        :return:
        """
        wms_db = DbTools('WMS')
        try:
            order_number_new = self.get_picking_sn()
            # 查找配货单id
            id_sql = "SELECT id FROM prepare_goods WHERE  prepare_goods_no='%s'"
            id_res = wms_db.execute_sql(id_sql, order_number_new)
            picking_id = id_res[0][0]
            del wms_db
            # 执行接收配货单脚本
            if picking_id:
                url = "http://wms.hqygou.com/daemon/picking_order_queue/autoCreatePackage/{}".format(str(picking_id)[-1:])
                return requests.get(url).text
        except IndexError:
            return 'oms未同步配货单'

    def deal_question(self):
        """
        处理订单问题
        :return:
        """
        oms_db = DbTools('OMS')
        # 处理地址异常问题，否则要在wos处理
        address_sql = "UPDATE o_oms_order_question SET order_question_status=3 WHERE order_sn='%s' AND order_question_type_id=2;"
        oms_db.execute_sql(address_sql, self.order_sn)

        # 处理其他问题
        other_sql = "SELECT order_question_id FROM oms.o_oms_order_question  WHERE order_sn='%s';"
        question_ids = oms_db.execute_sql(other_sql, self.order_sn)
        # 问题无需处理操作请求接口
        url = "http://oms.hqygou.com/order/process/process"
        login = login_session('oms')
        for question_id in question_ids:
            data = {
                "order_question_id": question_id[0],
                "order_question_process_id": 3,
                "not_send_email": 1
            }
            login.session.post(url, data=data).json()
        # 检查问题是否都处理了
        check_sql = "SELECT order_question_id FROM oms.o_oms_order_question WHERE order_sn='%s' AND order_question_status!=3;"
        if oms_db.execute_sql(check_sql, self.order_sn):
            return "有问题处理失败，请手动处理"
        return '处理成功！'

    def oms_piking_order(self, stock_id, express_id):
        """
        oms订单配货
        :return:
        """
        # 获取配货订单信息
        oms_session = login_session('oms')
        order_data_url = "http://oms.hqygou.com/order/picking/getorderjsondata"
        order_data = {
            "order_sn": self.order_sn,
            "stock_id": stock_id
        }
        goods_data = oms_session.session.post(order_data_url, order_data).json()['data']['goods']

        # 发起配货请求
        # 获取请求参数
        picking_data = {
            "is_temp": 0,
            "is_remote": 0,
            "is_from_picking": 1,
            "stock_id": stock_id,
            "express_id": express_id,
            "order_sn": self.order_sn,
            "goods_weight": 0,
            "express_list": "加拿大专线(FZ)",
            "overweight": 0,
            "first_declare_total": 0,
            "last_declare_total": None
        }
        goods_weight = 0
        for goods in goods_data:
            picking_goods_data = {
                f"goods[{goods['goods_sn']}][goods_sn]": goods['goods_sn'],
                f"package_length_{goods['goods_sn']}": goods['package_length'],
                f"package_width_{goods['goods_sn']}": goods['package_width'],
                f"package_height_{goods['goods_sn']}": goods['package_height'],
                f"goods_weight_{goods['goods_sn']}": goods['goods_weight'],
                f"goods[148786003][picking_quantity]": goods['goods_quantity'],
            }
            goods_weight += float(goods['goods_weight'])
            picking_data.update(picking_goods_data)
        picking_data.update({"goods_weight": goods_weight})
        # 请求配货
        picking_url = "http://oms.hqygou.com/order/picking/save"
        return oms_session.session.post(picking_url, picking_data).json()


if __name__ == '__main__':
    # process = OrderAllProcess('Z2012222036285905')
    process = OrderAllProcess('U2110181634521325')
    print(process.oms_piking_order().json())
