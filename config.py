import logging

from redis import StrictRedis


class Config(object):
    """
    项目配置
    """
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    # 数据库配置
    USERNAME = "postgres"
    PASSWORD = "123456"
    DATA_IP = "192.168.191.144"
    DATA_PORT = 5432
    DATABASE_NAME = "sunmanage"
    # SQLALCHEMY_DATABASE_URI = "mysql://root:123456@localhost:3306/infomation"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{USERNAME}:{PASSWORD}@{DATA_IP}:{DATA_PORT}/{DATABASE_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_HOST = "192.168.191.144"
    REDIS_PORT = 6379
    # Session配置
    SESSION_TYPE = "redis"
    # 指定session保存的位置
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_KEY_PREFIX = "Session"
    SESSION_USE_SIGNER = True
    SESSION_PERMANENT = False
    PERMANENT_SESSION_LIFETIME = 86400 * 2
    SECRET_KEY = "rIucD1qEuL3/iLaV5+6MbMjzHjlhvJBwgvtZi/A2tCmVoLmGTLCQYQ=="

    # 163邮箱服务器地址
    MAIL_HOST = 'smtp.163.com'
    # 163用户名
    MAIL_USER = 'sjjhub@163.com'
    # 密码(部分邮箱为授权码)
    MAIL_PASS = '521xiaoshen'

    # Github配置
    GIT_API_URL = "https://api.github.com"
    GIT_URL = "https://github.com"
    GIT_USERNAME = "Sjj1024"
    GIT_REPOS = "Sjj1024"
    GIT_TOKEN = "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"


class DevelopMentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    DEBUG = True


config = {
    "dev": DevelopMentConfig,
    "pro": ProductionConfig,
    "test": TestingConfig
}


# 数据库表创建
"""
DROP TABLE IF EXISTS "public"."users";
CREATE TABLE "public"."users" (
  "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  "user_name" varchar(255) COLLATE "pg_catalog"."default",
  "password" varchar(255) COLLATE "pg_catalog"."default",
  "nick_name" varchar(255) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "phone" varchar(255) COLLATE "pg_catalog"."default",
  "gender" varchar(255) COLLATE "pg_catalog"."default",
  "signature" varchar(255) COLLATE "pg_catalog"."default",
  "head_img" varchar(255) COLLATE "pg_catalog"."default",
  "creat_time" date,
  "role_id" int4
);

CREATE TABLE "public"."users" (
  "id" int4 NOT NULL DEFAULT nextval('users_id_seq'::regclass),
  "user_name" varchar(255) COLLATE "pg_catalog"."default",
  "password" varchar(255) COLLATE "pg_catalog"."default",
  "nick_name" varchar(255) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "phone" varchar(255) COLLATE "pg_catalog"."default",
  "gender" varchar(255) COLLATE "pg_catalog"."default",
  "signature" varchar(255) COLLATE "pg_catalog"."default",
  "head_img" varchar(255) COLLATE "pg_catalog"."default",
  "creat_time" date,
  "role_id" int4 DEFAULT 0,
  "money" int4 DEFAULT 0,
  "cookie" varchar(255) COLLATE "pg_catalog"."default",
  "user_agent" varchar(255) COLLATE "pg_catalog"."default",
  "contribute" int4 DEFAULT 0,
  "weiwang" int4 DEFAULT 0,
  "current_moey" int4 DEFAULT 0,
  "regular_moey" int4 DEFAULT 0,
  "able_invate" bool DEFAULT false,
  "lease" bool DEFAULT false,
  "article_number" int4 DEFAULT 0
);
"""