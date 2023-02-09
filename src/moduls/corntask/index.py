# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.triggers.cron import CronTrigger
# # 5位的cron是从分钟开始计算,最后一位不能使用?需要使用*代替,times与delFiles是需要调用的函数名
# sched = BackgroundScheduler()
#
#
# def delFiles(dir_path, beforeDay="30"):
#     """
#     :param dir_path: 文件路径
#     :param beforeDay: 需要删除的天数
#     :return:
#     """
#     print(f"定时任务执行了{dir_path} : {beforeDay}")
#
#
# # 开始添加定时任务
# # sched.add_job(times, CronTrigger.from_crontab('*/5 * * * *'))
# # args用于函数中进行传值,可以随机命名,只需要在后面传递参数即可
# sched.add_job(delFiles, CronTrigger.from_crontab('*/1 * * * *'), args=("dir_path", "30"))
# # 定时更新caoliu用户信息: 每12小时
# # sched.add_job(update_caoliu_info, CronTrigger.from_crontab('0 */12 * * *'))
# # sched.add_job(update_caoliu_info, CronTrigger.from_crontab('0 */5 * * *'))
# # sched.add_job(re_git_pull_run, CronTrigger.from_crontab('0 */10 * * *'))
# # 因为定时任务sched.start是阻塞的，所以可以放到一个线程里面执行
# # t = Thread(target=sched.start)
# # t.start()
# # 如果想使用阻塞的形式，就可以直接sched.start()运行
# print(" * 注入 定时任务 模块 corntask 成功")
# sched.start()
