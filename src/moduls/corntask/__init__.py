from flask import Blueprint

# 创建蓝图，并设置蓝图前缀
task_blu = Blueprint("taskblue", __name__, url_prefix='/api1/task')

from . import task_views
