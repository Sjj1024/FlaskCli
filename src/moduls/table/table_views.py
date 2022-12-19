import logging

from flask import jsonify, request

from src.moduls.table import table_blu
from src.utils.github.apis import add_caoliu_task_py


@table_blu.route("/list", methods=["GET", "POST"])
def table_list():
    logging.info("开始获取列表内容")
    try:
        table_data = []
        for i in range(1, 15):
            table_data.append(
                {"id": i, "username": f"woshibiaoti{i}", "grade": f"新手上路{i}", "weiwang": f"song{i}", "gongxian": "2022-12-11",
                 "money": 300 + i, "publick": "12/12/22", "mazi": "yqsdfasdfasdfsdf",
                 "email": "1024sssssxiaoshen@gmail.com"})
        total = len(table_data) * 50
        return jsonify(code=200, message="success", data={"total": total, "items": table_data})
    except Exception as e:
        return jsonify(code=430, message=f"获取失败:{e}")


@table_blu.route("/addUser", methods=["POST"])
def add_user():
    logging.info("开始添加用户")
    param_dict = request.json
    user_name = param_dict.get("username")
    password = param_dict.get("password")
    return jsonify(code=200, message="success")

@table_blu.route("/queryUser", methods=["POST"])
def query_user_by_cookie():
    print("通过cookie查询用户信息")
    param_dict = request.json
    cookie = param_dict.get("cookie")
    UserAgent = param_dict.get("UserAgent")
    return jsonify(code=200, message="success")
# @table_blu.route("/login", methods=["POST"])
# def login():
#     logging.info("开始登陆")
#     # 1. 获取参数
#     param_dict = request.json
#     user_name = param_dict.get("username")
#     password = param_dict.get("password")
#     try:
#         user = User.query.filter(User.user_name == user_name).first()
#     except Exception as e:
#         logging.error(f"查询数据库错误{e}")
#         return jsonify(code=430, message=f"查询失败:{e}")
#     if not user:
#         return jsonify(code=430, message="用户不存在")
#     if not user.check_password(password):
#         return jsonify(code=430, message="密码错误")
#     session["user_id"] = user.id
#     session["user_name"] = user.user_name
#     # 获取用户id，传入生成token的方法，并接收返回的token
#     token = create_token(user.id)
#     return jsonify(code=200, message="登陆成功", data={"token": token})
#
#
# @table_blu.route("/list", methods=["GET"])
# def info():
#     user_info = {"name": "1024小神", "avatar": "https://img-blog.csdnimg.cn/53781995003f4706a2c50884c620c7ef.png"}
#     return jsonify(code=200, message="success", data=user_info)
#
#
# @table_blu.route("/logout", methods=["GET", "POST"])
# def logout():
#     # user_info = {"name": "1024小神", "avatar": "https://img-blog.csdnimg.cn/53781995003f4706a2c50884c620c7ef.png"}
#     return jsonify(code=200, message="success")
#
#
# @table_blu.route("/imgcode")
# def creat_imgcode():
#     logging.info("生成图片验证码")
#     name, code, img = captcha.generate_captcha()
#     logging.info(f"名称：{name}，code:{code}， img:{img}")
#     redis_store.set(name, code, constants.IMAGE_CODE_REDIS_EXPIRES)
#     response = make_response(img)
#     response.headers["Content-Type"] = "image/jpg"
#     response.headers["ImageName"] = name
#     return response
#
#
# @table_blu.route("/send_email", methods=["POST"])
# def check_send_email():
#     """
#     1.获取图片验证码和发送对象邮箱地址
#     2.校验图片验证码并发送邮件
#     :return:
#     """
#     logging.info("发送邮箱验证码")
#     param_dict = request.json
#     img_name = param_dict.get("img_name")
#     img_code = param_dict.get("img_code")
#     email = param_dict.get("send_email")
#     # redis_img_code = redis_store.get(img_name)
#     # if redis_img_code and redis_img_code == img_code:
#     if img_code:
#         send_email("欢迎注册", "恭喜您注册成功", email)
#         return jsonify(code=200, message="注册成功")
#     else:
#         return jsonify(code=410, message="注册失败")
