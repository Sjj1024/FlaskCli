from flask import Blueprint

# 创建蓝图，并设置蓝图前缀
pay_blu = Blueprint("payblue", __name__, url_prefix='/api1/pay')

from . import pay_info