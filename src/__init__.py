import logging
import os
import pkgutil
import re
import sys
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, Blueprint
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

from config import config, Config

# 给变量加注释，让其可以自动提示
redis_store = None  # type: StrictRedis
db: SQLAlchemy = None

# 全局配置类
config_obj: Config = None


# 下面这种也是一样的，变量提示，后面引入之后也可以自动获取提示
# redis_store: StrictRedis = None


def setup_log(log_level):
    # 没有日志文件夹就自动创建
    path = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(path):
        os.mkdir(path)
    # 设置日志的记录等级
    logging.basicConfig(level=log_level)  # 调试debug级
    # 文件名，以日期作为文件名
    log_file_name = path + os.sep + 'logger'
    # 下面的日志处理二选一：RotatingFileHandler TimedRotatingFileHandler
    # 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
    # file_log_handler = RotatingFileHandler(log_file_str, maxBytes=1024, backupCount=3)
    # 间隔5(S)创建新的日志文件
    file_log_handler = TimedRotatingFileHandler(log_file_name, when='S', interval=60, backupCount=3)
    # 设置日志文件后缀
    file_log_handler.suffix = '%Y-%m-%d-%H-%M.log'
    file_log_handler.extMatch = re.compile(r'^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}.log')
    # 创建日志记录的格式 日志等级 输入日志信息的文件名 行数 日志信息
    formatter = logging.Formatter('%(asctime)s [%(module)s] %(levelname)s [%(lineno)d] %(message)s')
    # 为刚创建的日志记录器设置日志记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flask app使用的）添加日志记录器
    logging.getLogger().addHandler(file_log_handler)


def search_blueprint(app: Flask):
    """
    扫描蓝图，并自动注入app中
    """
    app_dict = {}
    pkg_list = pkgutil.walk_packages(__path__, __name__ + ".")
    for _, module_name, ispkg in pkg_list:
        __import__(module_name)
        module = sys.modules[module_name]
        module_attrs = dir(module)
        for name in module_attrs:
            var_obj = getattr(module, name)
            if isinstance(var_obj, Blueprint):
                if app_dict.get(name) is None:
                    app_dict[name] = var_obj
                    app.register_blueprint(var_obj)
                    print(" * 注入 %s 模块 %s 成功" % (Blueprint.__name__, var_obj.__str__()))


def get_platform():
    import platform
    sys_platform = platform.platform().lower()
    if "windows" in sys_platform:
        return "windows"
    else:
        return "macos"


def import_corn_task():
    import src.moduls.corntask.index


def check_host():
    global config_obj
    host_list = [config_obj.REDIS_HOST, config_obj.DATA_IP, config_obj.GIT_API_URL, config_obj.GIT_URL]
    ping_str = "ping -n 1" if get_platform() == "windows" else "ping -c1"
    for host in host_list:
        host = host.replace("https://", "www.") if host.startswith("https") else host
        f = os.popen(f"{ping_str} {host}", "r")
        if "100% 丢失" in f.read():
            print(f" * 地址异常:{host}")


def creat_app(con: str):
    # 将业务代码抽离出来
    # 可以访问到静态资源是因为flaksk会自动生成静态文件路由，__name__就表示当前模块，所以会将静态文件也加载进去
    app = Flask(__name__)
    # 可以通过设置环境变量配置不同的环境
    config_env = os.environ.get("config")
    if config_env is not None:
        con = config_env
    app.config.from_object(config[con])
    # 设施配置类
    global config_obj
    config_obj = config[con]()
    # 初始化数据库
    global db
    db = SQLAlchemy()
    db.init_app(app)
    # 日志等级配置
    setup_log(config[con].LOG_LEVEL)
    # 设置session保存位置: 配置对象里面的属性是类属性
    global redis_store
    redis_store = StrictRedis(host=config[con].REDIS_HOST, port=config[con].REDIS_PORT, decode_responses=True)
    # 可以指定session的保存位置，要在app的config中配置
    Session(app)
    # 开启CSRF保护
    # TODO 开启保护
    # CSRFProtect(app)
    # 注册蓝图,放到这里就不会出现导入redis_store出错的问题:什么时候使用，什么时候导入
    search_blueprint(app)
    # 检查网络配置
    # check_host()
    # 注入定时任务
    import_corn_task()
    return app
