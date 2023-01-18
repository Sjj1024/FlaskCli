import logging

import requests
from flask import jsonify, request
from sqlalchemy import or_
from src.models import CaoliuUsers
from src.moduls.table import table_blu
from src.utils.caoliu.tools import get_userinfo_by_cookie, check_name_avliable, regist_caoliu, login_get_cookie, \
    get_invcode_list, pay_some_invcode, get_article_list, get_commit_list, get_ref_commit_list
from src import db


@table_blu.route("/list", methods=["GET", "POST"])
def table_list():
    logging.info("开始获取列表内容")
    try:
        param_dict = request.json
        # print(param_dict)
        page_num = param_dict.get("pageNum")
        pageSize = param_dict.get("pageSize")
        username = param_dict.get("username")
        weiwang = param_dict.get("weiwang")
        level = param_dict.get("level")
        status = param_dict.get("status")
        yaoqing = param_dict.get("yaoqing")
        if status == "已被删除":
            query = CaoliuUsers.query.filter(CaoliuUsers.isDeleted == True)
        elif len(status) == 1:
            query = CaoliuUsers.query.filter(CaoliuUsers.important == int(status))
        else:
            query = CaoliuUsers.query.filter(or_(CaoliuUsers.isDeleted.is_(None), CaoliuUsers.isDeleted == False))
        if username:
            query = query.filter(CaoliuUsers.user_name == username)
        if weiwang:
            query = query.filter(CaoliuUsers.weiwang >= weiwang)
        if level:
            query = query.filter(CaoliuUsers.grade == level)
        if "禁言" in status:
            query = query.filter(CaoliuUsers.desc.like(f'%{status}%'))
        if "正常" in status:
            query = query.filter(~CaoliuUsers.desc.contains('禁言'))
        if yaoqing == "可以购买":
            query = query.filter(CaoliuUsers.able_invate == yaoqing)
        elif yaoqing == "不可以":
            query = query.filter(~CaoliuUsers.able_invate.contains('可以购买'))
        query = query.order_by(CaoliuUsers.important)
        paginate = query.order_by(-CaoliuUsers.id).paginate(page_num, pageSize)
        result = [u.to_json() for u in paginate.items]
        # print(result)
        return jsonify(code=200, message="success", data={"total": paginate.total, "items": result})
    except Exception as e:
        print(f"查询异常： {e}")
        return jsonify(code=430, message=f"获取失败:{e}")


def get_caoliu_user(username="", password="", cookie="", user_agent="", desc=""):
    if password:
        cookie, user_agent = login_get_cookie(username, password)
    if len(user_agent) < 10:
        return user_agent
    user_info = get_userinfo_by_cookie(cookie, user_agent)
    if isinstance(user_info, str):
        return user_info
    caoliu_info = CaoliuUsers()
    caoliu_info.user_name = user_info.get("user_name")
    caoliu_info.password = password
    caoliu_info.user_id = user_info.get("user_id")
    caoliu_info.grade = user_info.get("dengji")
    caoliu_info.email = user_info.get("email")
    caoliu_info.weiwang = user_info.get("weiwang")
    caoliu_info.article_number = user_info.get("fatie")
    caoliu_info.contribute = user_info.get("gongxian")
    caoliu_info.desc = desc + user_info.get("desc")
    caoliu_info.money = user_info.get("money")
    caoliu_info.regist_time = user_info.get("regist_time")
    caoliu_info.cookie = cookie
    caoliu_info.user_agent = user_agent
    caoliu_info.able_invate = user_info.get("able_invate")
    caoliu_info.lease = False
    caoliu_info.authentication = user_info.get("authentication")
    caoliu_info.contribute_link = user_info.get("gongxian_link")
    caoliu_info.task_status = "未开启"
    caoliu_info.check_status = "未开启"
    return caoliu_info


@table_blu.route("/tempAddUser", methods=["POST"])
def temp_add_user():
    logging.info("开始暂存用户信息...")
    param_dict = request.json
    print(param_dict)
    username = param_dict.get("username", None)
    password = param_dict.get("password", None)
    email = param_dict.get("email", None)
    cookie = param_dict.get("cookie", None)
    userAgent = param_dict.get("userAgent", None)
    important = param_dict.get("important", None)
    desc = param_dict.get("desc", None)
    caoliu_info = CaoliuUsers()
    caoliu_info.user_name = username
    caoliu_info.password = password
    caoliu_info.email = email
    caoliu_info.cookie = cookie
    caoliu_info.user_agent = userAgent
    caoliu_info.important = important
    caoliu_info.desc = desc
    caoliu_info.task_status = "未开启"
    caoliu_info.check_status = "未开启"
    caoliu_info.weiwang = 0
    caoliu_info.contribute = 0
    caoliu_info.grade = "暂存用户待更新"
    caoliu_info.able_invate = "false"
    try:
        db.session.add(caoliu_info)
        db.session.commit()
        print(f"添加用户成功！")
    except Exception as e:
        print(e)
        return jsonify(code=205, message=f"添加登陆异常:{e}")
    return jsonify(code=200, message="success")


@table_blu.route("/addUser", methods=["POST"])
def add_user():
    logging.info("开始添加用户")
    param_dict = request.json
    print(param_dict)
    username = param_dict.get("username", None)
    password = param_dict.get("password", None)
    email = param_dict.get("email", None)
    invcode = param_dict.get("invcode", None)
    cookie = param_dict.get("cookie", None)
    userAgent = param_dict.get("userAgent", None)
    important = param_dict.get("important", None)
    desc = param_dict.get("desc", None)
    if invcode:
        print("注册逻辑")
        res = regist_caoliu(username, password, invcode, email)
        if res:
            caoliu_info = get_caoliu_user(username, password, desc=desc)
            if isinstance(caoliu_info, str):
                return jsonify(code=205, message=f"注册异常:{caoliu_info}")
        else:
            return jsonify(code=205, message="注册异常")
    elif cookie:
        print("cookie逻辑")
        caoliu_info = get_caoliu_user(cookie=cookie, user_agent=userAgent, desc=desc)
        if isinstance(caoliu_info, str):
            return jsonify(code=205, message=f"Cookie逻辑:{caoliu_info}")
    elif password:
        print("开始登陆逻辑")
        caoliu_info = get_caoliu_user(username, password, desc=desc)
        if isinstance(caoliu_info, str):
            return jsonify(code=205, message=f"登陆逻辑异常:{caoliu_info}")
        if not caoliu_info:
            return jsonify(code=214, message="用户密码错误，请更换密码后再试")
    else:
        print("没有邀请码也没有cookie，逻辑错误")
        return jsonify(code=205, message="没有邀请码也没有cookie")
    try:
        caoliu_info.important = important
        caoliu_info.original = caoliu_info.to_dict()
        caoliu_info.desc = desc
        db.session.add(caoliu_info)
        db.session.commit()
        print(f"添加用户成功！")
    except Exception as e:
        print(e)
        return jsonify(code=205, message=f"添加登陆用户异常:{e}")
    return jsonify(code=200, message="success")


@table_blu.route("/delUser", methods=["DELETE"])
def del_user():
    logging.info("开始删除用户")
    param_dict = request.json
    logging.info(f"开始删除用户: {param_dict}")
    # 如果有action任务，把任务删除
    if param_dict.get("task_file_sha"):
        requests.delete("http://localhost:5000/api1/table/delUpdateUser", json=param_dict)
    if param_dict.get("check_file_sha"):
        requests.delete("http://localhost:5000/api1/table/delCheckUser", json=param_dict)
    CaoliuUsers.query.filter_by(id=param_dict.get("id")).update({"isDeleted": True})
    db.session.commit()
    return jsonify(code=200, message="success")


@table_blu.route("/getUserById", methods=["POST"])
def get_user_by_id():
    logging.info("开始查询用户详细信息")
    param_dict = request.json
    logging.info(f"开始查询用户: {param_dict}")
    user = CaoliuUsers.query.get(param_dict.get("id"))
    if user:
        user_info = user.to_json()
        return jsonify(code=200, message="success", data=user_info)
    else:
        return jsonify(code=210, message="未查找到用户信息")


@table_blu.route("/getInvcodeList", methods=["POST"])
def get_user_invcode_list():
    logging.info("开始查找邀请码列表")
    user_id = request.json.get('id')
    pageNum = request.json.get('pageNum')
    user = CaoliuUsers.query.get(user_id)
    if user:
        user_info = user.to_json()
        invcodes = get_invcode_list(user_info.get("cookie"), user_info.get("user_agent"), pageNum)
        if isinstance(invcodes, str):
            return jsonify(code=210, message=invcodes)
        return jsonify(code=200, message="success", data=invcodes)
    else:
        return jsonify(code=210, message="未查找到用户信息")


@table_blu.route("/getArticleList", methods=["POST"])
def get_user_article_list():
    logging.info("开始获取用户文章列表")
    user_id = request.json.get('id')
    pageNum = request.json.get('pageNum')
    user = CaoliuUsers.query.get(user_id)
    if user:
        user_info = user.to_json()
        articles = get_article_list(user_info.get("cookie"), user_info.get("user_agent"), pageNum)
        if isinstance(articles, str):
            return jsonify(code=210, message=articles)
        return jsonify(code=200, message="success", data=articles)
    else:
        return jsonify(code=210, message="未查找到用户信息")


@table_blu.route("/getCommitList", methods=["POST"])
def get_user_commit_list():
    logging.info("开始获取用户评论列表")
    user_id = request.json.get('id')
    pageNum = request.json.get('pageNum')
    user = CaoliuUsers.query.get(user_id)
    if user:
        user_info = user.to_json()
        articles = get_commit_list(user_info.get("cookie"), user_info.get("user_agent"), pageNum)
        if isinstance(articles, str):
            return jsonify(code=210, message=articles)
        return jsonify(code=200, message="success", data=articles)
    else:
        return jsonify(code=210, message="未查找到用户信息")


@table_blu.route("/getRefCommitList", methods=["POST"])
def get_user_ref_commit_list():
    logging.info("开始获取用户点评列表")
    user_id = request.json.get('id')
    pageNum = request.json.get('pageNum')
    user = CaoliuUsers.query.get(user_id)
    if user:
        user_info = user.to_json()
        articles = get_ref_commit_list(user_info.get("cookie"), user_info.get("user_agent"), pageNum)
        if isinstance(articles, str):
            return jsonify(code=210, message=articles)
        return jsonify(code=200, message="success", data=articles)
    else:
        return jsonify(code=210, message="未查找到用户信息")


@table_blu.route("/payInvcode", methods=["POST"])
def pay_some_invcode_list():
    logging.info("开始购买邀请码invnum")
    user_id = request.json.get('id')
    invnum = request.json.get('invnum')
    user = CaoliuUsers.query.get(user_id)
    if user:
        user_info = user.to_json()
        invcodes = pay_some_invcode(user_info.get("cookie"), user_info.get("user_agent"), invnum)
        if invcodes:
            return jsonify(code=200, message="success", data=invcodes)
        else:
            return jsonify(code=211, message="操作失败", data=invcodes)
    else:
        return jsonify(code=210, message="未查找到用户信息")


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
