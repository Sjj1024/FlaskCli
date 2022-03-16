from flask import session
from flask_script import Manager
import logging
# 添加命令行支持，后面还要数据库迁移等功能
from Info import *

app = creat_app("pro")
manager = Manager(app)


@app.route("/")
def index():
    # 使用session存储session
    session["name"] = "song"
    logging.fatal("fatal")
    logging.error("error")
    logging.warning("warning")
    logging.debug("debug")
    return "首页内容"


if __name__ == '__main__':
    manager.run()
    # app.run(host="0.0.0.0", port=5000)
