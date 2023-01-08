import logging
from flask import jsonify
from src.moduls.dashboard import dashbord_blu
from src.utils.caoliu.tools import get_all_caoliu_home


@dashbord_blu.route("/homes", methods=["GET", "POST"])
def get_homes():
    logging.info("获取所有的回家地址")
    homes = []
    # 获取所有的草榴地址
    caoliu = get_all_caoliu_home()
    homes.append({
        "key": "1024地址",
        "homes": caoliu
    })
    return jsonify(code=200, message="success", data=homes)

# @categorys_blu.route("/query", methods=["GET", "POST"])
# def query():
#     logging.info("查找文章分类")
#     user_list = Categorys.query.all()
#     print(user_list)
#     result = [u.to_json() for u in user_list]
#     return jsonify(result), 200
#
# @categorys_blu.route("/query_sql", methods=["GET", "POST"])
# def query_sql():
#     logging.info("查找文章分类")
#     res = db.session.execute("select * from categorys").fetchall()
#     emp_json_list = [dict(zip(item.keys(), item)) for item in res]
#     print(emp_json_list)
#     return jsonify(emp_json_list), 200
