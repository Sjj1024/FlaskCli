import os

from flask import Flask
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from redis import StrictRedis
from config import config


def creat_app(con:str):
    # 将业务代码抽离出来
    app = Flask(__name__)
    # 可以通过设置环境变量配置不同的环境
    config_env = os.environ.get("config")
    if config_env is not None:
        con = config_env
    app.config.from_object(config[con])
    # 初始化数据库
    db = SQLAlchemy()
    db.init_app(app)
    # 设置session保存位置: 配置对象里面的属性是类属性
    redis_store = StrictRedis(host=config[con].REDIS_HOST, port=config[con].REDIS_PORT)
    # 可以指定session的保存位置，要在app的config中配置
    Session(app)
    # 开启CSRF保护
    CSRFProtect(app)
    return app
