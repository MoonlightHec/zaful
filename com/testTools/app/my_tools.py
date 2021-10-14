# _*_ coding: utf-8 _*_
"""
# @Time : 2021/10/14 17:03 
# @Author : lijun7 
# @File : my_tools.py
# @desc :
"""
import urllib

from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/mytools/oms/create_order", methods=["GET", "POST"])
def create_order():
    print("header {}".format(request.headers))
    print("args ", request.args)
    print("form {}".format(request.form.to_dict()))
    user_order_info = {}
    for k, v in request.form.to_dict().items():
        user_order_info.update({k: v})
        print(f"self.{k}={v}")
    return jsonify(user_order_info)


if __name__ == "__main__":
    app.config["JSON_AS_ASCII"] = False
    app.run(host="127.0.0.1", port=8080)
