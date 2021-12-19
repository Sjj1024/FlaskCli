class Config(object):
    """
    项目配置
    """

    DEBUG = True
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/infomation"
    SQLALCHEMY_TRACK_MODIFICATIONS = False