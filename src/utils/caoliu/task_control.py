import datetime
import random
import time
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
# 配置持久化
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from tzlocal import get_localzone
from src import config_obj

# 存储位置
SCHEDULER_JOBSTORES = {'default': SQLAlchemyJobStore(url=config_obj.SQLALCHEMY_DATABASE_URI)}
executors = {
    'default': ThreadPoolExecutor(20)
}
# job默认配置
job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 600000  # 600秒的任务超时容错
}
scheduler = BackgroundScheduler()
scheduler.configure(jobstores=SCHEDULER_JOBSTORES, job_defaults=job_defaults, timezone=get_localzone(), executors=executors)


def add_task():
    print("注入定时任务")


def add_caoliu_commit_task(user_name, cookie, user_agent, corn):
    print(f"添加1024评论任务: {user_name}")
    scheduler.add_job(delFiles, CronTrigger.from_crontab('*/1 * * * *'), args=(user_name, "30"), id=user_name)


def del_task(task_id):
    print("删除定时任务")


def update_task(task_id):
    print("删除定时任务")


def get_all_task():
    print("获取所有定时任务")


def delFiles(dir_path, beforeDay="30"):
    """
    :param dir_path: 文件路径
    :param beforeDay: 需要删除的天数
    :return:
    """
    sleep_time = random.randint(2 * 60, 5 * 60)
    print(f"开始随机睡眠{sleep_time} 秒，也就是 {sleep_time / 60} 分钟......")
    time.sleep(sleep_time)
    print(f"定时任务执行了{dir_path} : {datetime.datetime.now()}")


scheduler.start()
