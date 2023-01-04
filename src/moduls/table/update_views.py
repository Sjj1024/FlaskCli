import logging
from flask import jsonify, request
from src.moduls.table import table_blu
from src.utils.caoliu.tools import get_userinfo_by_cookie, login_get_cookie
from src.utils.github.apis import add_caoliu_task_file, del_caoliu_task_file, dispatches_workflow_run
from src.models import CaoliuUpdate, CaoliuUsers
from src import db, config_obj


@table_blu.route("/addCheckUser", methods=["POST"])
def add_check_file():
    logging.info("开始创建caoliu账号监控...")
    paylod = request.json
    cookie = paylod.get("cookie")
    user_agent = paylod.get("userAgent")
    user_info = get_userinfo_by_cookie(cookie, user_agent)
    user_name = user_info.get("user_name")
    check_user_list = CaoliuUsers.query.filter_by(user_name=user_name)
    if check_user_list:
        check_user = check_user_list.all()[0].to_json()
    else:
        return jsonify(code=207, message="没有查找到该用户")
    user = {
        "username": user_name,
        "password": paylod.get("password"),
        "new_password": paylod.get("new_password"),
        "cookie": cookie,
        "user_agent": user_agent,
        "prefix": "caoliu_"
    }
    flag_yml, message_yml = add_caoliu_task_file(f".github/workflows/Check{user_name}.yml", user, file_type="check")
    if flag_yml:
        check_user["check_link"] = f"{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows/Check{user_name}.yml"
        check_user["check_file_sha"] = message_yml
        check_user["check_status"] = "已开启"
        try:
            check_user_list.update(check_user)
            db.session.commit()
        except Exception as e:
            print(e)
        return jsonify(code=200, message="success")
    else:
        return jsonify(code=501, message={"message_yml": message_yml})


@table_blu.route("/newUserInfo", methods=["POST"])
def get_new_userinfo():
    logging.info("开始获取新的用户信息...")
    paylod = request.json
    username = paylod.get("user_name")
    password = paylod.get("password")
    cookie = paylod.get("cookie")
    user_agent = paylod.get("userAgent")
    if cookie:
        user_info = get_userinfo_by_cookie(cookie, user_agent)
    elif password:
        cookie, user_agent = login_get_cookie(username, password)
        if not cookie:
            return jsonify(code=212, message="登陆失败，可能是登陆次数过多导致的")
        user_info = get_userinfo_by_cookie(cookie, user_agent)
    else:
        return jsonify(code=211, message="没有cookie和用户名密码")
    update_user_list = CaoliuUsers.query.filter_by(user_name=username)
    if update_user_list:
        update_user = {
            "article_number": user_info.get("fatie"),
            "authentication": "",
            "cookie": cookie,
            "contribute": user_info.get("gongxian"),
            "grade": user_info.get("dengji"),
            "money": user_info.get("money"),
            "user_id": user_info.get("user_id"),
            "weiwang": user_info.get("weiwang")
        }
    else:
        return jsonify(code=207, message="没有查找到该用户")
    try:
        update_user_list.update(update_user)
        db.session.commit()
    except Exception as e:
        print(e)
    return jsonify(code=200, message="success")


@table_blu.route("/addUpdateUser", methods=["POST"])
def add_git_file():
    logging.info("开始创建caoliu自动升级...")
    paylod = request.json
    # 先添加一个caoliu.py文件
    cookie = paylod.get("cookie")
    user_agent = paylod.get("userAgent")
    user_info = get_userinfo_by_cookie(cookie, user_agent)
    user_name = user_info.get("user_name")
    update_user_list = CaoliuUsers.query.filter_by(user_name=user_name)
    if update_user_list:
        update_user = update_user_list.all()[0].to_json()
    else:
        return jsonify(code=207, message="没有查找到该用户")
    user = {
        "username": user_name,
        "password": paylod.get("password"),
        "new_password": paylod.get("new_password"),
        "cookie": cookie,
        "user_agent": user_agent,
        "prefix": "caoliu_"
    }
    flag_yml, message_yml = add_caoliu_task_file(f".github/workflows/{user_name}.yml", user, "task")
    if flag_yml:
        update_user["task_link"] = f"{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows/{user_name}.yml"
        update_user["task_file_sha"] = message_yml
        update_user["task_status"] = "已开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
        return jsonify(code=200, message="success")
    else:
        return jsonify(code=501, message={"message_yml": message_yml})


@table_blu.route("/dispatchesRun", methods=["POST"])
def dispatch_work_run():
    logging.info("触发一个工作流运行...")
    paylod = request.json
    user_name = paylod.get("username")
    res = dispatches_workflow_run(user_name)
    if res:
        return jsonify(code=200, message="success")


@table_blu.route("/delUpdateUser", methods=["DELETE"])
def del_git_file():
    logging.info("删除caoliu自动升级...")
    paylod = request.json
    caoliu_user: CaoliuUsers = CaoliuUsers.query.get(paylod.get("id"))
    user = {
        "username": caoliu_user.user_name,
        "yml_sha": caoliu_user.task_file_sha,
        "prefix": "caoliu_"
    }
    if not caoliu_user.task_file_sha:
        return jsonify(code=501, message="缺少文件sha值")
    flag_yml, message_yml = del_caoliu_task_file(f".github/workflows/{user.get('username')}.yml", user)
    if flag_yml:
        try:
            CaoliuUsers.query.filter_by(user_name=caoliu_user.user_name).update(
                {"task_link": "", "task_file_sha": "", "task_status": "未开启"})
            db.session.commit()
            return jsonify(code=200, message="success")
        except Exception as e:
            print(e)
            return jsonify(code=501, message=f"删除用户信息失败...{e}")
    else:
        return jsonify(code=501, message={"message_yml": message_yml})


@table_blu.route("/delCheckUser", methods=["DELETE"])
def del_check_file():
    logging.info("删除caoliu账号监控...")
    paylod = request.json
    caoliu_user: CaoliuUsers = CaoliuUsers.query.get(paylod.get("id"))
    user = {
        "username": caoliu_user.user_name,
        "yml_sha": caoliu_user.check_file_sha,
        "prefix": "caoliu_"
    }
    flag_yml, message_yml = del_caoliu_task_file(f".github/workflows/Check{user.get('username')}.yml", user)
    if flag_yml:
        try:
            CaoliuUsers.query.filter_by(user_name=caoliu_user.user_name).update(
                {"check_link": "", "check_file_sha": "", "check_status": "未开启"})
            db.session.commit()
            return jsonify(code=200, message="success")
        except Exception as e:
            print(e)
            return jsonify(code=501, message=f"删除用户信息失败...{e}")
    else:
        return jsonify(code=501, message={"message_yml": message_yml})


@table_blu.route("/updateList", methods=["GET", "POST"])
def table_update_list():
    logging.info("开始获取升级任务列表")
    try:
        paginate = CaoliuUpdate.query.order_by(-CaoliuUpdate.id).paginate(1, 10)
        result = [u.to_json() for u in paginate.items]
        return jsonify(code=200, message="success", data={"total": paginate.total, "items": result})
    except Exception as e:
        return jsonify(code=430, message=f"获取失败:{e}")
