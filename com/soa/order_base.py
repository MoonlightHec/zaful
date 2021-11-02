# _*_ coding: utf-8 _*_
"""
# @Time : 2021/1/26 16:59 
# @Author : lijun7
# @File : order_base.py
# @desc : 查询订单信息
"""

# 链接数据库
from com.util.cursor_util.DbTools import DbTools


def get_pay_info(sql_par):
    """
    根据字段名查询订单数据
    :param sql_par:
    :return:
    """
    db = DbTools('PAY')
    cursor = db.cursor
    print(
        "id    parent_trade_sn        trade_sn               parent_order_sn      pay_sn            site_code pay_status channel_code transaction_id\t")
    # 获取sql查询语句及where条件
    pay_sn_list = []
    order_sn_list = []
    for index in range(1, 65):
        table_num = 'pay_gateway_' + str(index)
        sql = "SELECT id,parent_trade_sn,trade_sn,parent_order_sn,pay_sn,site_code,pay_status,channel_code,transaction_id FROM %s WHERE %s = '%s';"
        cursor.execute(sql % (table_num, sql_par['field'], sql_par['value']))
        if cursor.rowcount:
            for row in cursor.fetchall():
                print("%s %s %s %s %s      %s   %s   %s   %s\t" % row)
                # print(row)
                pay_sn_list.append(row[4])
                order_sn_list.append(row[3])
            print("支付状态pay_status(0-未支付 1-处理中 2-已支付 3-退款中 4-退款成功 5退款失败 6支付失败 7部分退款)")
            print("所在表：%s" % table_num)
            print('共查找出', cursor.rowcount, '条数据')
    del db
    return pay_sn_list, order_sn_list


if __name__ == '__main__':
    # 常用字段：parent_order_sn,paySn,transaction_id
    get_pay_info(sql_par={
        'field': 'parent_order_sn',
        'value': 'L2111020224199179'
    })
