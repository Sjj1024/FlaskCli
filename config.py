from redis import StrictRedis


class Config(object):
    """
    项目配置
    """

    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/infomation"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SECRET_KEY = "daasdasetasrysrywerywersdadfasdfasasfasdfasdfasdfasfds"
