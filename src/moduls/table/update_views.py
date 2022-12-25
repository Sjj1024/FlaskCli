import logging
from flask import jsonify, request
from src.moduls.table import table_blu
from src.utils.caoliu.tools import get_userinfo_by_cookie, login_get_cookie
from src.utils.github.apis import add_caoliu_task_file, del_caoliu_task_file, dispatches_workflow_run
from src.models import CaoliuUpdate
from src import db, config_obj


@table_blu.route("/addUpdateUser", methods=["POST"])
def add_git_file():
    logging.info("开始创建caoliu自动升级...")
    paylod = request.json
    # 先添加一个caoliu.py文件
    cookie = paylod.get("cookie")
    user_agent = paylod.get("userAgent")
    # 有密码存在就走登陆逻辑
    if paylod.get("password"):
        cookie, user_agent = login_get_cookie(paylod.get("username"), paylod.get("password"))
    user_info = get_userinfo_by_cookie(cookie, user_agent)
    user_name = user_info.get("user_name")
    update_user = CaoliuUpdate()
    update_user.user_name = user_info.get("user_name")
    update_user.cookie = cookie
    update_user.user_agent = user_agent
    update_user.task_status = 0
    update_user.desc = paylod.get("desc")
    update_user.able_invate = False
    update_user.lease = False
    update_user.grade = user_info.get("dengji")
    update_user.user_id = user_info.get("user_id")
    update_user.article_num = user_info.get("fatie")
    update_user.weiwang = user_info.get("weiwang")
    update_user.money = user_info.get("money")
    update_user.contribute = user_info.get("gongxian")
    update_user.email = user_info.get("email")
    user = {
        "username": paylod.get("username"),
        "password": paylod.get("password"),
        "cookie": cookie,
        "user_agent": user_agent,
        "prefix": "caoliu_"
    }
    flag_yml, message_yml = add_caoliu_task_file(f".github/workflows/{user_name}.yml", user)
    if flag_yml:
        update_user.task_link = f"{config_obj.GIT_URL}/{config_obj.GIT_USERNAME}/{config_obj.GIT_REPOS}/actions/workflows/{user_name}.yml"
        update_user.yml_file_sha = message_yml
        try:
            db.session.add(update_user)
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
    caoliu_user: CaoliuUpdate = CaoliuUpdate.query.get(paylod.get("id"))
    # 先添加一个caoliu.py文件
    user = {
        "username": caoliu_user.user_name,
        "py_sha": caoliu_user.py_file_sha,
        "yml_sha": caoliu_user.yml_file_sha,
        "prefix": "caoliu_"
    }
    flag_yml, message_yml = del_caoliu_task_file(f".github/workflows/{user.get('username')}.yml", user)
    if flag_yml:
        try:
            db.session.delete(caoliu_user)
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
