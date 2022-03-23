import logging

from flask import request

from Info.moduls.register import passport_blu


@passport_blu.route("/", methods=["POST"])
def regist():
    logging.info("开始注册")
    # 1. 获取参数
    param_dict = request.json
    mobile = param_dict.get("mobile")
    smscode = param_dict.get("smscode")
    password = param_dict.get("password")
    return "sss"

