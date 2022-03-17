from . import index_blu
from ... import redis_store


@index_blu.route("/")
def index():
    # 使用session存储session
    print(redis_store)
    redis_store.set("name", "song")
    return "首页内容"