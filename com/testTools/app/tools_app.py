# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/14 17:03 
# @Author : lijun7 
# @File : tools_app.py
# @desc :
"""

from flask import Flask, request, jsonify

from com.oms.WebminObj import WebminObj
from com.oms.order_all_process import OrderAllProcess
from com.testTools.app.tools_oms import create_user_order

app = Flask(__name__)


@app.route("/myTools/oms/create_order", methods=["GET", "POST"])
def get_order_info():
    """
    oms创建订单
    :return:
    """
    print("header {}".format(request.headers))
    print("args ", request.args)
    print("form {}".format(request.form.to_dict()))
    # 将获取到的表单数据转化为dict
    user_order_info = request.form.to_dict()
    order_sn = create_user_order(user_order_info)
    if order_sn:
        return jsonify(f"订单编号：{order_sn}")
    return "创建失败"
    # return render_template('index.html',data=user_order_info)


@app.route("/myTools/oms/webmin", methods=["GET", "POST"])
def run_webmin():
    """
    webmin脚本
    :return:
    """
    script_info = request.form.to_dict()
    print("form {}".format(script_info))
    webmin_params = []
    for value in script_info.values():
        if value:
            webmin_params.append(value)

    web_script = WebminObj(app_name='oms')
    return web_script.run_script(*webmin_params)


@app.route("/myTools/oms/allProcess/dealQuestion", methods=["GET", "POST"])
def order_process_deal_question():
    """
    处理订单问题
    :return:
    """
    order_sn_web = request.form.to_dict()
    print("form {}".format(order_sn_web))
    order_sn = order_sn_web['order-sn']
    process = OrderAllProcess(order_sn)
    return process.deal_question()


@app.route("/myTools/oms/allProcess/createPickingOrder", methods=["GET", "POST"])
def order_process_picking_order():
    """
    生成配货单
    :return:
    """
    picking_info = request.form.to_dict()
    print("form {}".format(picking_info))
    order_sn = picking_info['order-sn']
    stock_id = picking_info['stock-id']
    express_id = picking_info['express-id']
    process = OrderAllProcess(order_sn)
    return process.oms_piking_order(stock_id, express_id)


@app.route("/myTools/oms/allProcess/postPickingInfo", methods=["GET", "POST"])
def order_process_post_picking():
    """
    同步配货单
    :return:
    """
    order_sn_web = request.form.to_dict()
    print("form {}".format(order_sn_web))
    order_sn = order_sn_web['order-sn']
    process = OrderAllProcess(order_sn)
    picking_sn = process.get_picking_sn()
    web_script = WebminObj(app_name='oms')
    return web_script.run_script('同步配货单到WMS', picking_sn)


@app.route("/myTools/oms/allProcess/getPickingInfo", methods=["GET", "POST"])
def order_process_get_picking():
    """
    wms接收配货单生成包裹
    :return:
    """
    order_sn_web = request.form.to_dict()
    print("form {}".format(order_sn_web))
    order_sn = order_sn_web['order-sn']
    process = OrderAllProcess(order_sn)
    return process.wms_get_picking_order()


if __name__ == "__main__":
    app.config["JSON_AS_ASCII"] = False
    app.run(host="127.0.0.1", port=8080)
