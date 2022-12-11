import logging

from flask import request, make_response, jsonify, session

from Info import redis_store, constants, db
from Info.models import User
from Info.moduls.user import passport_blu
from Info.utils.captcha.captcha import captcha
from Info.utils.common_util import send_email, create_token


@passport_blu.route("/regist", methods=["POST"])
def regist():
    logging.info("开始注册")
    # 1. 获取参数
    param_dict = request.json
    user_name = param_dict.get("user_name")
    mobile = param_dict.get("mobile")
    email = param_dict.get("email")
    password = param_dict.get("password")
    user = User()
    user.user_name = user_name
    user.phone = mobile
    user.password = password
    user.email = email
    user.role_id = 1
    db.session.add(user)
    try:
        db.session.commit()
        return jsonify(code=200, message="注册成功")
    except Exception as e:
        return jsonify(code=430, message=f"注册失败:{e}")


@passport_blu.route("/login", methods=["POST"])
def login():
    logging.info("开始登陆")
    # 1. 获取参数
    param_dict = request.json
    user_name = param_dict.get("username")
    password = param_dict.get("password")
    try:
        user = User.query.filter(User.user_name == user_name).first()
    except Exception as e:
        logging.error(f"查询数据库错误{e}")
        return jsonify(code=430, message=f"查询失败:{e}")
    if not user:
        return jsonify(code=430, message="用户不存在")
    if not user.check_password(password):
        return jsonify(code=430, message="密码错误")
    session["user_id"] = user.id
    session["user_name"] = user.user_name
    # 获取用户id，传入生成token的方法，并接收返回的token
    token = create_token(user.id)
    return jsonify(code=200, message="登陆成功", data={"token": token})


@passport_blu.route("/info", methods=["GET"])
def info():
    user_info = {"name": "1024小神", "avatar": "https://img-blog.csdnimg.cn/53781995003f4706a2c50884c620c7ef.png"}
    return jsonify(code=200, message="success", data=user_info)


@passport_blu.route("/logout", methods=["GET", "POST"])
def logout():
    # user_info = {"name": "1024小神", "avatar": "https://img-blog.csdnimg.cn/53781995003f4706a2c50884c620c7ef.png"}
    return jsonify(code=200, message="success")


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
    # redis_img_code = redis_store.get(img_name)
    # if redis_img_code and redis_img_code == img_code:
    if img_code:
        send_email("欢迎注册", "恭喜您注册成功", email)
        return jsonify(code=200, message="注册成功")
    else:
        return jsonify(code=410, message="注册失败")
