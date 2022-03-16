from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis

from config import config

# 将业务代码抽离出来
app = Flask(__name__)
app.config.from_object(config["pro"])

# 初始化数据库
db = SQLAlchemy()
db.init_app(app)
# 设置session保存位置: 配置对象里面的属性是类属性
redis_store = StrictRedis(host=config["pro"].REDIS_HOST, port=config["pro"].REDIS_PORT)
# 可以指定session的保存位置，要在app的config中配置
Session(app)
# 开启CSRF保护
CSRFProtect(app)
