from flask import jsonify
from src import db, config_obj
from src.models import CaoliuUsers
from src.moduls.corntask import task_blu
from src.utils.caoliu.tools import get_userinfo_by_cookie, login_get_cookie
from src.utils.github.apis import get_repo_action, get_file_sha


@task_blu.route("/updateCaoliu", methods=["GET", "POST"])
def update_caoliu_info():
    print(f"定时更新coaliu用户信息")
    all_caoliu = CaoliuUsers.query.all()
    for cao in all_caoliu:
        try:
            # 判断是否有cookie
            cao_info = cao.to_json()
            username = cao_info.get("user_name")
            cookie = cao_info.get("cookie")
            password = cao_info.get("password")
            user_agent = cao_info.get("user_agent")
            if cookie:
                user_info = get_userinfo_by_cookie(cookie, user_agent)
            elif password:
                cookie, user_agent = login_get_cookie(username, password)
                if not cookie:
                    print(f"{username} : 登陆失败，可能是登陆次数过多导致的")
                user_info = get_userinfo_by_cookie(cookie, user_agent)
            else:
                return jsonify(code=211, message="没有cookie和用户名密码")
            update_user_list = CaoliuUsers.query.filter_by(user_name=username)
            user_caoliu = {}
            if update_user_list and user_info:
                user_caoliu = update_user_list.all()[0].to_json()
                user_caoliu["article_number"] = user_info.get("fatie")
                user_caoliu["cookie"] = cookie
                user_caoliu["contribute"] = user_info.get("gongxian")
                user_caoliu["contribute_link"] = user_info.get("gongxian_link")
                user_caoliu["grade"] = user_info.get("dengji")
                user_caoliu["money"] = user_info.get("money")
                user_caoliu["user_id"] = user_info.get("user_id")
                user_caoliu["weiwang"] = user_info.get("weiwang")
            else:
                print(f"{username} : 没有查找到该用户或获取该用户详细信息出错，可能是Cookie无效")
            # 如果工作流存储为空，则获取工作流详情
            if not user_caoliu.get("task_file_sha", None):
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
            if not user_caoliu.get("check_file_sha"):
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
            update_user_list.update(user_caoliu)
            db.session.commit()
        except Exception as e:
            print(e)
    return jsonify(code=200, message="正常")
