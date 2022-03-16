from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from redis import StrictRedis
from flask_script import Manager
from config import Config

app = Flask(__name__)
# 添加命令行支持，后面还要数据库迁移等功能
manager = Manager(app)

app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy()
db.init_app(app)
# 设置session保存位置: 配置对象里面的属性是类属性
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
# 可以指定session的保存位置，要在app的config中配置
Session(app)
# 开启CSRF保护
CSRFProtect(app)

@app.route("/")
def index():
    # 使用session存储session
    session["name"] = "song"
    return "首页"


if __name__ == '__main__':
    manager.run()
    # app.run(host="0.0.0.0", port=5000)
