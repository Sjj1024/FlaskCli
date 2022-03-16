from . import index_blu


@index_blu.route("/")
def index():
    # 使用session存储session
    return "首页内容"