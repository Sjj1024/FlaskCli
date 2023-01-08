import requests
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
        cao_info = cao.to_json()
        try:
            res = requests.post("http://localhost:5000/api1/table/updateUserInfo", json=cao_info)
            print(f"{cao_info.get('user_name')}更新结果：{res.json()}")
            if res.json().get("code") != 200:
                raise Exception(f"更新用户信息异常:{res.json()}")
        except Exception as e:
            print(f"{cao_info.get('user_name')}更新结果：{e}")
    print(f"所有数据已经更新完毕！！！")
    return jsonify(code=200, message="正常")
