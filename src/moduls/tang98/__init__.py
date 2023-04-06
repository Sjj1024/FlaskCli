from flask import Blueprint

# 创建蓝图，并设置蓝图前缀
tang98_blu = Blueprint("tangtang", __name__, url_prefix='/api1/tang98')

from . import table_views
from . import update_views
