from flask import Blueprint

# 创建蓝图，并设置蓝图前缀
passport_blu = Blueprint("register", __name__, url_prefix='/api1/user')

from . import regist_views
