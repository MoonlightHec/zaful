# coding=utf-8
from flask import Flask, request, jsonify
import urllib

app = Flask(__name__)


@app.route("/get/sum", methods=["GET", "POST"])
def get_sum():
    data = request.get_data()
    print("header {}".format(request.headers))
    print("data = ", data)

    text = data.decode("utf-8")
    sp = text.split("&")
    print("text = {}".format(text))

    print(urllib.parse.unquote(text, encoding="utf-8"))

    i = 0
    kv = {}
    for s in sp:
        print("{} s = {}".format(i, s))
        pp = s.split("=")
        if (len(pp) == 2):
            value = pp[1]
            kv[pp[0]] = value
            print(urllib.parse.unquote(value, encoding="utf-8"))

    print("kv {}".format(kv))
    info = {}
    info['name'] = "中文"
    info["age"] = 8928
    return jsonify(info)


if __name__ == "__main__":
    app.config["JSON_AS_ASCII"] = False
    app.run(host="127.0.0.1", port=8080)