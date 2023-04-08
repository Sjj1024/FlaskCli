from src.models import *
from src.moduls.corntask import task_blu
from flask import jsonify, request
from src import db
from src.utils.task_config.task_control import *


@task_blu.route("/updateCaoliu", methods=["GET", "POST"])
def update_caoliu_info():
    print(f"定时更新coaliu用户信息")
    all_caoliu = CaoliuUsers.query.all()
    for cao in all_caoliu:
        cao_info = cao.to_json()
        grade = cao_info.get("grade")
        # user_name = cao_info.get("user_name")
        if grade == "禁止發言":
            print(f"禁止发言用户：{cao_info}")
            continue
        try:
            res = requests.post("http://localhost:5000/api1/table/updateUserInfo", json=cao_info)
            print(f"{cao_info.get('user_name')}更新结果：{res.json()}")
            if res.json().get("code") != 200:
                raise Exception(f"更新用户信息异常:{res.json()}")
        except Exception as e:
            print(f"{cao_info.get('user_name')}更新结果：{e}")
    print(f"所有数据已经更新完毕！！！")
    return jsonify(code=200, message="正常")


@task_blu.route("/addCaoliuCommit", methods=["GET", "POST"])
def add_caoliu_commit_local():
    print(f"添加1024的定时评论任务")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    corn_tab = param_dict.get("corn", None) or "05 */3 * * *"
    try:
        update_user_list = CaoliuUsers.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if user_name in update_user["task_file_sha"]:
            return jsonify(code=205, message="任务已存在", data=f"任务已存在")
        task_id = add_caoliu_commit_task(user_name, cookie, user_agent, corn_tab)
        update_user["task_file_sha"] = task_id
        update_user["task_status"] = "已开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/runCaoliuCommit", methods=["GET", "POST"])
def run_caoliu_commit_local():
    print(f"添加1024的定时评论任务")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    try:
        run_caoliu_commit_task(user_name, cookie, user_agent)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/addTangCommit", methods=["GET", "POST"])
def add_tang_commit_local():
    print(f"添加98的定时评论任务")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    corn_tab = param_dict.get("corn", None) or "05 */3 * * *"
    try:
        update_user_list = Tang98Users.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if update_user["task_file_sha"] and user_name in update_user["task_file_sha"]:
            return jsonify(code=205, message="任务已存在", data=f"任务已存在")
        task_id = add_tang_commit_task(user_name, cookie, user_agent, corn_tab)
        update_user["task_file_sha"] = task_id
        update_user["task_status"] = "已开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/delCaoliuCommit", methods=["DELETE"])
def del_caoliu_commit():
    print(f"删除1024自动评论任务: ")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    try:
        update_user_list = CaoliuUsers.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if not update_user["task_file_sha"]:
            return jsonify(code=205, message="error", data=f"任务不存在")
        del_caoliu_commit_article(user_name)
        update_user["task_file_sha"] = ""
        update_user["task_status"] = "未开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/delTangCommit", methods=["DELETE"])
def del_tang_commit():
    print(f"删除98自动评论任务: ")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    try:
        update_user_list = Tang98Users.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if not update_user["task_file_sha"]:
            return jsonify(code=205, message="error", data=f"任务不存在")
        del_tang_commit_article(user_name)
        update_user["task_file_sha"] = ""
        update_user["task_status"] = "未开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/addCaoliuSign", methods=["GET", "POST"])
def add_caoliu_sign():
    param_dict = request.json
    print(f"添加1024签到任务: {param_dict}")
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    article_link = param_dict.get("link", None)
    corn_tab = param_dict.get("corn", None) or "50 17 * * *"
    commit_str = param_dict.get("commit", None) or "今日签到"
    try:
        if not article_link:
            return jsonify(code=207, message="请输入需要签到的文章链接")
        update_user_list = CaoliuUsers.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if update_user["sign_task_id"]:
            return jsonify(code=205, message="error", data=f"任务已存在")
        task_id = add_caoliu_sign_article(user_name, cookie, user_agent, article_link, commit_str, corn_tab)
        update_user["sign_task_id"] = task_id
        update_user["sign_task_status"] = "已开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/addTangSign", methods=["GET", "POST"])
def add_tangtang_sign():
    param_dict = request.json
    print(f"添加98签到任务: {param_dict}")
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    corn_tab = param_dict.get("corn", None) or "50 17 * * *"
    try:
        update_user_list = Tang98Users.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if update_user["sign_task_id"]:
            return jsonify(code=205, message="error", data=f"任务已存在")
        task_id = add_tang_sign_article(user_name, cookie, user_agent, corn_tab)
        update_user["sign_task_id"] = task_id
        update_user["sign_task_status"] = "已开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/runTangSign", methods=["GET", "POST"])
def run_tangtang_sign():
    param_dict = request.json
    print(f"运行98签到任务: {param_dict}")
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    try:
        run_tang_sign_article(user_name, cookie, user_agent)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/runTangCommit", methods=["GET", "POST"])
def run_tangtang_commit():
    param_dict = request.json
    print(f"运行98评论任务: {param_dict}")
    user_name = param_dict.get("user_name")
    cookie = param_dict.get("cookie")
    user_agent = param_dict.get("user_agent")
    try:
        run_tang_commit_article(user_name, cookie, user_agent)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/delCaoliuSign", methods=["DELETE"])
def del_caoliu_sign():
    print(f"删除1024签到任务: ")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    try:
        update_user_list = CaoliuUsers.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if not update_user["sign_task_id"]:
            return jsonify(code=205, message="error", data=f"任务不存在")
        del_caoliu_sign_article(user_name)
        update_user["sign_task_id"] = ""
        update_user["sign_task_status"] = "未开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")


@task_blu.route("/delTangSign", methods=["DELETE"])
def del_tang_sign():
    print(f"删除98签到任务: ")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    try:
        update_user_list = Tang98Users.query.filter_by(user_name=user_name)
        if update_user_list:
            update_user = update_user_list.all()[0].to_json()
        else:
            return jsonify(code=207, message="没有查找到该用户")
        if not update_user["sign_task_id"]:
            return jsonify(code=205, message="error", data=f"任务不存在")
        del_tangtang_sign_article(user_name)
        update_user["sign_task_id"] = ""
        update_user["sign_task_status"] = "未开启"
        try:
            update_user_list.update(update_user)
            db.session.commit()
        except Exception as e:
            print(e)
            return jsonify(code=212, message="更新数据库操作失败", data=e)
        return jsonify(code=200, message="success")
    except Exception as e:
        return jsonify(code=205, message="error", data=f"出错消息: {e}")
