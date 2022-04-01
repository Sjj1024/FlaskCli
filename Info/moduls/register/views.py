import logging

from flask import request, make_response

from Info import redis_store, constants
from Info.moduls.register import passport_blu
from Info.utils.captcha.captcha import captcha


@passport_blu.route("/", methods=["POST"])
def regist():
    logging.info("开始注册")
    # 1. 获取参数
    param_dict = request.json
    mobile = param_dict.get("mobile")
    smscode = param_dict.get("smscode")
    password = param_dict.get("password")
    return "sss"


@passport_blu.route("/imgcode")
def creat_imgcode():
    logging.info("生成图片验证码")
    name, code, img = captcha.generate_captcha()
    logging.info(f"名称：{name}，code:{code}， img:{img}")
    redis_store.set(name, code, constants.IMAGE_CODE_REDIS_EXPIRES)
    response = make_response(img)
    response.headers["Content-Type"] = "image/jpg"
    return response
