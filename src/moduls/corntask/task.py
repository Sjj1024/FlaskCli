import time
from src.utils.common_util import send_weixin
import requests


# 删除存放30天的文件
def delFiles(dir_path, beforeDay="30"):
    """
    :param dir_path: 文件路径
    :param beforeDay: 需要删除的天数
    :return:
    """
    print(f"定时任务执行了{dir_path} : {beforeDay}")


def times():
    print(time.strftime("定时任务执行了: %Y-%m-%d-%H_%M_%S", time.localtime()))
    if time.localtime().tm_hour == 11 and time.localtime().tm_min == 10:
        send_weixin("该订饭了", "今天吃什么呢？还是大米先生？")


def update_caoliu_info():
    res = requests.get("http://localhost:5000/api1/task/updateCaoliu")
    print(res)
    send_weixin("更新所有1024用户信息结果", res)