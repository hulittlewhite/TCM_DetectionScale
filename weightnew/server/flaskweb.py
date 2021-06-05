#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from flask import request, Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
# r'/*' 是通配符，让本服务器所有的URL 都允许跨域请求
CORS(app, resources=r'/*')


@app.route('/', methods=["POST"])
def post_data():
    pass


# 访问的URL：http://127.0.0.1:5000/
@app.route('/', methods=["GET", "POST"])  # GET 和 POST 都可以
def get_data():
    # 假设有如下 URL
    # http://10.8.54.48:5000/index?name=john&age=20
    print(request)
    res = gettest1()
    res = {"category_count": res[0], "total_amount": res[1], "total": res[2]}
    res = jsonify(res)
    return res


# 访问的URL：http://127.0.0.1:5000/
@app.route('/getproducts', methods=["GET", "POST"])  # GET 和 POST 都可以
def get_product():
    print(request)
    res = get_product_info()
    res = jsonify(res)
    return res


# 访问的URL：http://127.0.0.1:5000/getname?name=john&age=20
@app.route('/getname', methods=["GET"])
def get_name_info():
    print(request)
    name = request.args.get("name")  # 如果有参数
    age = request.args.get("age")
    res = "your name is: %s, your age is: %s" % (name, age)
    res = jsonify(res)
    return res


mylist2 = [2, 7.5, 3.65, 3.5]


def get_product_info():
    global mylist2
    products = list()
    products.append({"name": "艾叶", "products_count": mylist2[0], "unit_price": mylist2[1]})
    products.append({"name": "白矾", "products_count": mylist2[2], "unit_price": mylist2[3]})
    mylist2[0] += 1
    mylist2[2] += 1
    return products


mylist1 = [1, 2, 3]


def gettest1():
    global mylist1
    mylist1 = list(map(lambda x: x + 1, mylist1))
    return mylist1


def gettest2(data):
    return data * 2


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
