# _*_ coding: utf-8 _*_
"""
# @Time : 2021/5/24 16:01 
# @Author : mhec 
# @File : risk_part_table.py
# @desc : 风控分表测试
"""
from com.util.cursor_util import db


def empty_data(table=None):
    """
    清空新表数据，默认全部三个表清空
    :param table: 清空指定表数据
    :return:
    """
    connect = db.get_connect('PAY')
    cursor = connect.cursor()
    switcher = (
        'pay_info_detail_',
        'pay_risk_event_',
        'pay_after_info_detail_'
    )
    for table_name in switcher:
        if table:
            table_name = table + '_'
        for index in range(0, 65):
            table_num = table_name + str(index)
            sql = "DELETE FROM %s;"
            cursor.execute(sql % table_num)
            connect.commit()
        if table:
            print("删除成功")
            break
    cursor.close()
    connect.close()


def sum_datas(table=None):
    """
    计算数量差异
    :return:
    """
    connect = db.get_connect('PAY')
    cursor = connect.cursor()
    switcher = (
        'pay_info_detail_',
        'pay_risk_event_',
        'pay_after_info_detail_'
    )
    num_new = {}
    for table_name in switcher:
        # 计算新表总数据
        if table:
            table_name = table + '_'
        key_name_new = table_name + 'new'
        num_new[key_name_new] = 0
        for index in range(0, 65):
            table_num = table_name + str(index)
            sql = "SELECT COUNT(*) FROM %s;"
            cursor.execute(sql % table_num)
            amount = cursor.fetchall()[0][0]

            # 新表重复数据
            repeat = 0
            repeat_sql = "SELECT COUNT(*) AS c,t.unique_id FROM %s t GROUP BY unique_id HAVING c>1"
            cursor.execute(repeat_sql % table_num)
            if cursor.fetchall():
                repeat = cursor.rowcount
            if amount != 0:
                print('%s:总数量【%s】，重复的unique_id数量【%s】' % (table_num, amount, repeat))
            num_new[key_name_new] += amount

        # 计算旧表总数据
        key_name_old = table_name + 'old'
        sql = "SELECT COUNT(*) FROM %s;"
        cursor.execute(sql % table_name[:-1])
        amount = cursor.fetchall()[0][0]
        num_new[key_name_old] = amount
        if table:
            break
    print(num_new)
    cursor.close()
    connect.close()


def run_task():
    """
    历史数据任务执行完后，对比数据差异
    :return:
    """
    connect = db.get_connect('PAY')
    cursor = connect.cursor()

    no = '31'
    switcher = (
        'pay_info_detail_' + no,
        'pay_risk_event_' + no,
        'pay_after_info_detail_' + no
    )
    for table_name in switcher:
        # new_sql = "SELECT * FROM %s WHERE user_email='##cGJ85o+mZRleIVd7pzx5T97CvLPMTGnE2ereCvNnMnI=';"
        new_sql = "SELECT * FROM %s where pay_sn='P2108130132871633088W6' ;"
        cursor.execute(new_sql % table_name)
        # 获取所有表字段
        col_name_list = [field[0] for field in cursor.description]
        if cursor.rowcount:
            new_datas = cursor.fetchall()
            print("------------------新表%s，共查出【%s】条数据:-------------------" % (table_name, cursor.rowcount))
            for new_data in new_datas:
                old_sql = 'SELECT * FROM %s WHERE id = \'%s\' '
                cursor.execute(old_sql % (table_name[:-3], new_data[1]))
                old_data = cursor.fetchall()
                for j, dif_new in enumerate(new_data):
                    dif_old = old_data[0][j - 1]
                    if dif_new != dif_old:
                        print("数据有差异%s【旧表：%s,新表:%s】" % (col_name_list[j], dif_old, dif_new))
                print('\n')

    cursor.close()
    connect.close()


def get_data(pay_sn=None):
    """
    新下单数据，对比三个表数据差异
    :param pay_sn:
    :return:
    """
    connect = db.get_connect('PAY')
    cursor = connect.cursor()
    switcher = (
        'pay_info_detail_',
        'pay_risk_event_',
        'pay_after_info_detail_'
    )
    for table_name in switcher:
        # 查旧表数据
        old_sql = "SELECT * FROM %s WHERE pay_sn = '%s';"
        cursor.execute(old_sql % (table_name[:-1], pay_sn))
        if cursor.rowcount:
            old_datas = cursor.fetchall()
            print("\n旧表%s，共查处【%s】条数据:" % (table_name[:-1], cursor.rowcount))
            for old_data in old_datas:
                print(old_data)

        # 查新表数据
        for index in range(0, 65):
            table_num = table_name + str(index)
            sql = "SELECT * FROM %s WHERE pay_sn = '%s';"
            cursor.execute(sql % (table_num, pay_sn))
            # 获取所有表字段
            col_name_list = [field[0] for field in cursor.description]
            if cursor.rowcount:
                new_datas = cursor.fetchall()
                print("新表%s，共查处【%s】条数据:" % (table_num, cursor.rowcount))
                for i, new_data in enumerate(new_datas):
                    print(new_data)
                    for j, dif_new in enumerate(new_data):
                        dif_old = old_datas[i][j - 1]
                        if dif_new != dif_old:
                            if j != 0:
                                print("数据有差异%s【旧表：%s,新表:%s】" % (col_name_list[j], dif_old, dif_new))
    cursor.close()
    connect.close()


if __name__ == '__main__':
    # 新数据差异
    get_data(pay_sn='P210817013489103850X7Z')
    # 清空数据
    # empty_data('pay_risk_event')
    # 历史数据差异
    # run_task()
    # 历史数据数量
    # sum_datas('pay_risk_event')
