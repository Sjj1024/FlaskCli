import logging
from flask import jsonify
from . import index_blu


@index_blu.route("/")
def index():
    logging.info("访问首页")
    # 使用session存储session
    return "首页内容"


@index_blu.route("/user")
def query_user():
    # 返回所有用户保存到list中
    user_list = ["1"]
    return jsonify(user_list), 200


@index_blu.route("/adduser")
def add_user():
    # 测试数据库
    return "添加成功"
