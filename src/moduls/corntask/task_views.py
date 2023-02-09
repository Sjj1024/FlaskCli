import requests
from src.models import CaoliuUsers
from src.moduls.corntask import task_blu
from flask import jsonify, request
from src.utils.caoliu.task_control import *


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
def add_caoliu_commit():
    print(f"添加1024的定时评论任务")
    param_dict = request.json
    user_name = param_dict.get("user_name")
    add_caoliu_commit_task(user_name, "cookie", "user_agent", "*/1 * * * *")
    return jsonify(code=200, message="success")
