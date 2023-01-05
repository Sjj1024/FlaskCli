from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from threading import Thread
import time

from src.utils.common_util import send_weixin


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


dir_path = r'E:\桌面\民宿'
# 5位的cron是从分钟开始计算,最后一位不能使用?需要使用*代替,times与delFiles是需要调用的函数名
sched = BackgroundScheduler()
sched.add_job(times, CronTrigger.from_crontab('*/5 * * * *'))
# 删除30天前的文件
# args用于函数中进行传值,可以随机命名,只需要在后面传递参数即可
sched.add_job(delFiles, CronTrigger.from_crontab('*/5 * * * *'), args=(dir_path, "30"))
# 因为定时任务sched.start是阻塞的，所以可以放到一个线程里面执行
t = Thread(target=sched.start)
t.start()
# 如果想使用阻塞的形式，就可以直接sched.start()运行
print(" * 注入 定时任务 模块 corntask 成功")
# sched.start()
