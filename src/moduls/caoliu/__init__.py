from flask import Blueprint

# 创建蓝图，并设置蓝图前缀
table_blu = Blueprint("tableblue", __name__, url_prefix='/api1/caoliu')

from . import table_views
from . import update_views
