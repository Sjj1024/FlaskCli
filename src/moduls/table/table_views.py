import logging
from flask import jsonify, request
from src.models import CaoliuUsers
from src.moduls.table import table_blu
from src.utils.caoliu.tools import get_userinfo_by_cookie, check_name_avliable, regist_caoliu
from src import db

@table_blu.route("/list", methods=["GET", "POST"])
def table_list():
    logging.info("开始获取列表内容")
    try:
        paginate = CaoliuUsers.query.order_by(-CaoliuUsers.id).paginate(1, 10)
        result = [u.to_json() for u in paginate.items]
        return jsonify(code=200, message="success", data={"total": paginate.total, "items": result})
    except Exception as e:
        return jsonify(code=430, message=f"获取失败:{e}")


@table_blu.route("/addUser", methods=["POST"])
def add_user():
    logging.info("开始添加用户")
    param_dict = request.json
    print(param_dict)
    username = param_dict.get("username")
    password = param_dict.get("password")
    email = param_dict.get("email")
    invcode = param_dict.get("invcode")
    cookie = param_dict.get("cookie")
    userAgent = param_dict.get("userAgent")
    desc = param_dict.get("desc")
    caoliu_info = CaoliuUsers()
    if invcode:
        print("注册逻辑")
        res = regist_caoliu(username, invcode, email)
        if res:
            try:
                caoliu_info.user_name = username
                caoliu_info.password = password
                caoliu_info.grade = "新手上路"
                caoliu_info.email = email
                caoliu_info.weiwang = 1
                caoliu_info.article_number = 0
                caoliu_info.contribute = 0
                caoliu_info.desc = desc
                caoliu_info.money = 0
                caoliu_info.cookie = cookie
                caoliu_info.user_agent = userAgent
                caoliu_info.able_invate = False
                caoliu_info.lease = False
                caoliu_info.authentication = ""
                caoliu_info.contribute_link = ""
                db.session.add(caoliu_info)
                db.session.commit()
            except Exception as e:
                print(e)
                return jsonify(code=205, message=f"注册异常:{e}")
            return jsonify(code=200, message="success")
        else:
            return jsonify(code=205, message="注册异常")
    elif cookie:
        print("cookie逻辑")
        user_info = get_userinfo_by_cookie(param_dict.get("cookie"), param_dict.get("userAgent"))
        caoliu_info.user_name = user_info.get("user_name")
        caoliu_info.user_id = user_info.get("user_id")
        caoliu_info.grade = user_info.get("dengji")
        caoliu_info.email = user_info.get("email")
        caoliu_info.weiwang = user_info.get("weiwang")
        caoliu_info.article_number = user_info.get("fatie")
        caoliu_info.contribute = user_info.get("gongxian")
        caoliu_info.desc = desc
        caoliu_info.money = user_info.get("money")
        caoliu_info.cookie = cookie
        caoliu_info.user_agent = userAgent
        caoliu_info.able_invate = False
        caoliu_info.lease = False
        caoliu_info.authentication = ""
        caoliu_info.contribute_link = user_info.get("gongxian_link")
        try:
            db.session.add(caoliu_info)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=205, message=f"注册异常:{e}")
        return jsonify(code=200, message="success")
    else:
        print("没有邀请码也没有cookie，逻辑错误")
        return jsonify(code=205, message="没有邀请码也没有cookie")


@table_blu.route("/delUser", methods=["DELETE"])
def del_user():
    logging.info("开始删除用户")
    # {'username': '1111111', 'password': '1024xiaoshen@gmail.com', 'email': '1024xiaoshen@gmail.com', 'invcode': '11111', 'token': '111111'}
    param_dict = request.json
    print(param_dict)
    return jsonify(code=200, message="success")


@table_blu.route("/queryUser", methods=["POST"])
def query_user_by_cookie():
    print("通过cookie查询用户信息")
    param_dict = request.json
    cookie = param_dict.get("cookie")
    userAgent = param_dict.get("userAgent")
    if "winduser" not in cookie:
        return jsonify(code=511, message="fail", data={"user_name": 'cookie不正确', "grader": "0"})
    user_info = get_userinfo_by_cookie(cookie, userAgent)
    if user_info:
        return jsonify(code=200, message="success", data=user_info)
    else:
        return jsonify(code=511, message="fail", data=user_info)


@table_blu.route("/queryUsername", methods=["POST"])
def query_username_available():
    print("通过cookie查询用户信息")
    param_dict = request.json
    username = param_dict.get("username")
    password = param_dict.get("password")
    email = param_dict.get("email")
    invcode = param_dict.get("invcode")
    cookie = param_dict.get("cookie")
    userAgent = param_dict.get("userAgent")
    desc = param_dict.get("desc")
    good, info = check_name_avliable(username)
    if good:
        return jsonify(code=200, message={"flag": good, "info": info})
    else:
        return jsonify(code=203, message={"flag": good, "info": info})

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
