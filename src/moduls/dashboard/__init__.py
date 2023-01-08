from flask import Blueprint

# 创建蓝图，并设置蓝图前缀
dashbord_blu = Blueprint("dashbord", __name__, url_prefix='/api1/dashboard')

from . import dashbord_view