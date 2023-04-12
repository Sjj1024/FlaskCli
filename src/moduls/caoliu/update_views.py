import copy
import datetime
import logging
from flask import jsonify, request
from src.moduls.caoliu import table_blu
from src.utils.caoliu.tools import get_userinfo_by_cookie, login_get_cookie
from src.utils.github.apis import add_caoliu_task_file, del_caoliu_task_file, dispatches_workflow_run, get_repo_action, \
    get_file_sha
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
        check_user[
            "check_link"] = f"{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows/Check{user_name}.yml"
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


@table_blu.route("/saveUserInfo", methods=["POST"])
def save_userinfo():
    logging.info("开始保存用户信息...")
    user_data = request.json
    update_user_list = CaoliuUsers.query.filter_by(user_name=user_data.get("user_name"))
    update_user_list.update(user_data)
    db.session.commit()
    return jsonify(code=200, message="success")


@table_blu.route("/updateUserInfo", methods=["POST"])
def get_new_userinfo():
    logging.info("开始更新用户信息...")
    paylod = request.json
    username = paylod.get("user_name")
    password = paylod.get("password")
    email = paylod.get("email")
    cookie = paylod.get("cookie")
    user_agent = paylod.get("user_agent")
    important = paylod.get("important")
    original = paylod.get("original")
    if cookie:
        user_info = get_userinfo_by_cookie(cookie, user_agent, email)
        update_user_list = CaoliuUsers.query.filter_by(cookie=cookie)
        if isinstance(user_info, str):
            # 说明Cookie失效
            return jsonify(code=207, message=user_info)
    elif password:
        cookie, user_agent = login_get_cookie(username, password)
        if not cookie:
            return jsonify(code=212, message="登陆失败，可能是登陆次数过多导致的")
        user_info = get_userinfo_by_cookie(cookie, user_agent, email)
        update_user_list = CaoliuUsers.query.filter_by(user_name=username)
    else:
        return jsonify(code=211, message="没有cookie和用户名密码")
    if update_user_list and user_info:
        user_caoliu = update_user_list.all()[0].to_json()
        user_caoliu["user_name"] = user_info.get("user_name")
        user_caoliu["article_number"] = user_info.get("fatie")
        user_caoliu["cookie"] = cookie
        user_caoliu["contribute"] = user_info.get("gongxian")
        user_caoliu["contribute_link"] = user_info.get("gongxian_link")
        user_caoliu["grade"] = user_info.get("dengji")
        user_caoliu["important"] = 5 if "永久禁言" in user_info["desc"] else important
        user_caoliu["money"] = user_info.get("money")
        user_caoliu["current_money"] = user_info.get("current_money")
        user_caoliu["regular_money"] = user_info.get("regular_money")
        user_caoliu["user_id"] = user_info.get("user_id")
        user_caoliu["weiwang"] = user_info.get("weiwang")
        user_caoliu["desc"] = user_info.get("desc") if "永久禁言" in user_info["desc"] else user_caoliu[
                                                                                                "desc"] + user_info.get(
            "desc")
        user_caoliu["able_invate"] = user_info.get("able_invate")
        user_caoliu["authentication"] = user_info.get("authentication")
        user_caoliu["regist_time"] = user_info.get("regist_time")
        user_caoliu["update_time"] = str(datetime.datetime.now())
    else:
        return jsonify(code=207, message="没有查找到该用户或获取该用户详细信息出错，可能是Cookie无效")
    # 如果工作流存储为空，则获取工作流详情
    if not user_caoliu.get("task_file_sha") and username:
        task_workflow = get_repo_action(username, "Commit")
        if task_workflow:
            task_link = f'{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/{task_workflow.get("path").replace(".github/", "")}'
            task_file_sha = get_file_sha(task_workflow.get("path"))
            task_status = "已开启"
            user_caoliu["task_link"] = task_link
            user_caoliu["task_file_sha"] = task_file_sha
            user_caoliu["task_status"] = task_status
        else:
            task_status = "未开启"
            user_caoliu["task_status"] = task_status
    # 如果工作流存储为空，则获取工作流详情
    if not user_caoliu.get("check_file_sha") and username:
        check_workflow = get_repo_action(username, "Check")
        if check_workflow:
            check_link = f'{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/{check_workflow.get("path").replace(".github/", "")}'
            check_file_sha = get_file_sha(check_workflow.get("path"))
            check_status = "已开启"
            user_caoliu["check_link"] = check_link
            user_caoliu["check_file_sha"] = check_file_sha
            user_caoliu["check_status"] = check_status
        else:
            check_status = "未开启"
            user_caoliu["check_status"] = check_status
    # 判断是不是被禁言了，然后删除升级的工作流，并且降级到5级
    if "禁止發言" in user_info.get("desc") and paylod.get("task_file_sha"):
        user = {
            "username": username,
            "yml_sha": paylod.get("task_file_sha"),
            "prefix": "caoliu_"
        }
        del_caoliu_task_file(f".github/workflows/{username}.yml", user)
    try:
        if not original or isinstance(original, int):
            user_caoliu["original"] = copy.deepcopy(user_caoliu)
        update_user_list.update(user_caoliu)
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify(code=212, message="更新数据库操作失败", data=e)
    return jsonify(code=200, message="success", data=user_caoliu)


@table_blu.route("/addUpdateUser", methods=["POST"])
def add_git_file():
    logging.info("开始创建caoliu自动升级...")
    paylod = request.json
    # 先添加一个caoliu.py文件
    cookie = paylod.get("cookie")
    user_agent = paylod.get("userAgent")
    user_name = paylod.get("username")
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
        update_user[
            "task_link"] = f"{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows/{user_name}.yml"
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
