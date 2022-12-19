import logging
from flask import jsonify, request
from src.moduls.table import table_blu
from src.utils.github.apis import add_caoliu_task_py, add_caoliu_task_yml


@table_blu.route("/addUpdateUser", methods=["POST"])
def add_git_file():
    logging.info("开始创建caoliu自动升级...")
    paylod = request.json
    print(paylod)
    # 先添加一个caoliu.py文件
    user = {
        "username": paylod.get("username"),
        "cookie": paylod.get("cookie"),
        "user_agent": paylod.get("userAgent")
    }
    prefix = "caoliu_"
    user_name = paylod.get("username")
    flag_py, message_py = add_caoliu_task_py(f"{prefix}{user_name}.py", user)
    if flag_py:
        # 添加一个caoliu.yml文件
        flag_yml, message_yml = add_caoliu_task_yml(f"{user_name}.yml", f"{prefix}{user_name}.py")
        if flag_yml:
            return jsonify(code=200, message="success")
        else:
            return jsonify(code=501, message={"message_yml": message_yml})
    else:
        return jsonify(code=501, message={"message_py": message_py})