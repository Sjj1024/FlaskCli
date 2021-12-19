from flask import Flask, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from redis import StrictRedis

from config import Config

app = Flask(__name__)

app.config.from_object(Config)

# 初始化数据库
db = SQLAlchemy()
db.init_app(app)
# 设置session保存位置
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
Session(app)
CSRFProtect(app)

@app.route("/")
def index():
    session["name"] = "song"
    return "首页"


if __name__ == '__main__':
    app.run()
