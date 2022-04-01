import logging

from flask import request, make_response

from Info import redis_store, constants
from Info.moduls.register import passport_blu
from Info.utils.captcha.captcha import captcha
from Info.utils.common_util import send_email


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
    response.headers["ImageName"] = name
    return response


@passport_blu.route("/send_email", methods=["POST"])
def check_send_email():
    """
    1.获取图片验证码和发送对象邮箱地址
    2.校验图片验证码并发送邮件
    :return:
    """
    logging.info("发送邮箱验证码")
    param_dict = request.json
    img_name = param_dict.get("img_name")
    img_code = param_dict.get("img_code")
    email = param_dict.get("send_email")
    redis_img_code = redis_store.get(img_name)
    if redis_img_code and redis_img_code == img_code:
        send_email("欢迎注册", "恭喜您注册成功", email)
        return "注册成功"
    else:
        return "注册失败"