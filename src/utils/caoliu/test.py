import base64
import json

import requests


def get_source(key):
    print("获取源地址")
    url = "https://api.github.com/repos/Sjj1024/Sjj1024/contents/src/homes/hotbox.py"
    res = requests.get(url=url, headers={})
    res_json = res.json()
    content = res_json.get("content")
    info_str = base64.b64decode(content).decode("utf-8").replace("hot_urls = ", "")
    json_info = eval(info_str.replace("\n", "").replace(" ", ""))
    hot_homes = json_info.get("data")
    for home in hot_homes:
        if home.get("title") == key:
            return home.get("url")
    return Exception("没有找到源地址")


if __name__ == '__main__':
    get_source("98色花堂1")