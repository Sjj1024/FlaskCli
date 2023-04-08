import datetime
import json
import random
import re
import time
import sys
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText


class AutoCommit:
    def __init__(self, name, cookie="", user_agent=""):
        self.cant_title = []
        self.cant_tid = []
        self.posted_article = {}
        self.source_url = ""
        self.user_name = name
        self.post_url = self.source_url + "/post.php?"
        self.get_source_url()
        self.grader = ""
        self.weiwang = 0
        self.commit_dist_num = 9
        self.cl_cookie = cookie
        self.user_agent = user_agent
        self.titles_href = []

    def get_soup(self, page_url):
        # 获取单张我的评论页面中的所有评论过的文章id和标题
        time.sleep(1)
        header = {
            "user-agent": self.user_agent,
            "cookie": self.cl_cookie,
            "referer": self.source_url + "/index.php"
        }
        try:
            res = requests.get(page_url, headers=header, timeout=10)
            html = res.content.decode()
        except Exception as e:
            print(f"有错误{e},开始重试新的请求......")
            source_url = self.get_source_url()
            new_url = page_url.replace(self.source_url, source_url)
            res = requests.get(new_url, headers=header, timeout=10)
            html = res.content.decode()
            self.source_url = source_url
        soup = BeautifulSoup(html, "lxml")
        if "登 錄" in soup.decode():
            print(f"{self.user_name}Cookie失效............")
            self.send_email(f"{self.user_name}Cookie失效", f"{soup.decode()}")
            return soup
        return soup

    def get_source_url(self):
        if self.source_url:
            return self.source_url
        url = "https://get.xunfs.com/app/listapp.php"
        data = {"a": "get18", "system": "ios"}
        res = requests.post(url=url, data=data)
        res_json = json.loads(res.content.decode("utf-8"))
        # 打印出地址信息和更新时间
        home_url = [res_json["url1"], res_json["url2"], res_json["url3"], res_json["update"]]
        for i in home_url:
            url = "https://" + i
            try:
                res = requests.get(url, timeout=10)
                if res.status_code == 200:
                    print(f"获取到的地址是:{url}")
                self.source_url = url
                return url
            except:
                continue

    def get_simple_info(self):
        print("获取简短信息.....")
        source_url = self.get_source_url()
        url = source_url + "/profile.php"
        soup = self.get_soup(url)
        liangbu_renzheng = "已設置 停用" in soup.select("#main")[0].get_text()
        if soup:
            # 获取简单信息
            user_name = re.search(r'用戶名: (.*?)[（|<]', soup.decode()).group(1)
            user_id = re.search(r'uid=(.*?)">[查看資料|查看個人資料]', soup.decode()).group(1)
            self.grader = re.search(r'頭銜: (.*?)<', soup.decode()).group(1)
            fatie = re.search(r'發帖: (.*?)<', soup.decode()).group(1)
            self.weiwang = re.search(r'威望: (.*?)點<', soup.decode()).group(1)
            money = re.search(r'金錢: (.*?) USD<', soup.decode()).group(1)
            gongxian = re.search(r'貢獻: (.*?) 點<', soup.decode()).group(1)
            if "註冊時間" in soup.decode():
                regist_time = re.search(r'註冊時間: (.*?)<', soup.decode()).group(1)
            else:
                regist_time = re.search(r'註冊: (.*?)<', soup.decode()).group(1)
            authentication = "已设置" if liangbu_renzheng else "未設置"
            user_info = {
                "user_name": user_name,
                "user_id": user_id,
                "dengji": self.grader,
                "jifen": "",
                "fatie": fatie,
                "weiwang": self.weiwang,
                "money": money,
                "gongxian": gongxian,
                "gongxian_link": "",
                "regist_time": regist_time,
                "email": "",
                "desc": "",
                "able_invate": "",
                "authentication": authentication
            }
            if self.grader == "禁止發言":
                print(f"获取到禁止發言用户-----{self.user_name}")
                self.send_email(f"{self.user_name}禁止发言了", f"{user_info}: {soup.decode()}")
            print(f"获取的用户信息:{user_info}")
            return user_info

    def get_userinfo(self):
        print("get_userinfo_bycookie-----")
        # 获取下一页的链接, 有就返回，没有就返回false
        source_url = self.get_source_url()
        url = source_url + "/profile.php"
        soup = self.get_soup(url)
        if soup:
            gread_span = soup.select("#main > div.t > caoliu > tr > td:nth-child(3) > a")  # 如果没有找到，返回None
            email_span = soup.select("#main > div.t > caoliu > tr > td:nth-child(2) > a")  # 如果没有找到，返回None
            info_url = f"{source_url}/{gread_span[0].get('href')}"
            email_url = f"{source_url}/{email_span[0].get('href')}"
            print(f"您的用户名是：, 您的等级是：{info_url}")
            info_soup = self.get_soup(info_url)
            email_soup = self.get_soup(email_url)
            if info_soup and email_soup:
                email = re.search(r"E-MAIL\n(.*?)com",
                                  email_soup.select("#main > form")[0].get_text()).group(1) + "com"
                all_info = info_soup.select("#main > div:nth-child(3)")[0].select("caoliu")[0].get_text()
                user_name = re.search(r'用戶名(.*?) \(', all_info).group(1)
                user_id = re.search(r'\(數字ID:(.*?)\)', all_info).group(1)
                dengji = re.search(r'會員頭銜(.*?)\n', all_info).group(1)
                jifen = re.search(r'綜合積分(.*?)\n', all_info).group(1)
                fatie = re.search(r'發帖(.*?)\n', all_info).group(1)
                weiwang = re.search(r'威望(.*?) 點\n', all_info).group(1)
                money = re.search(r'金錢(.*?) USD\n', all_info).group(1)
                gongxian = re.search(r'貢獻(.*?) 點\n', all_info).group(1)
                gongxian_link = re.search(r'隨機生成\)(.*?)\n', all_info).group(1)
                regist_time = re.search(r'註冊時間(.*?)\n', all_info).group(1)
                self.userinfo = {
                    "user_name": user_name,
                    "user_id": user_id,
                    "dengji": dengji,
                    "jifen": jifen,
                    "fatie": fatie,
                    "weiwang": weiwang,
                    "money": money,
                    "gongxian": gongxian,
                    "gongxian_link": gongxian_link,
                    "regist_time": regist_time,
                    "email": email
                }
                return self.userinfo
            else:
                return {}
        else:
            return {}

    def get_commited_article_count(self, link):
        print("获取打卡签到的文章统计....")

    # 获取已评论文章列表
    def get_commiteds(self):
        print("获取已评论文章")
        article_dict = {}
        # 获取下一页的链接, 有就返回，没有就返回false
        url = self.source_url + "/personal.php?action=post"
        soup = self.get_soup(url)
        last_num = soup.find(id="last")  # 如果没有找到，返回None
        if last_num:
            print("说明有不止一页评论内容")
            last_num = soup.find(id="last").get("href")
            all_page = last_num.split("page=")[1]
            all_num = int(all_page) + 1
            # 如果评论过的文章大与2页，就按两页算
            if all_num > 2:
                all_num = 2
            for i in range(1, all_num):
                page_url = self.source_url + f"/personal.php?action=post&page={i}"
                print(f"正在抽取第{i}页中的评论数据")
                soup = self.get_soup(page_url)
                # 通过soup获得已经评论过的文章id和标题
                article_list = soup.select(".a2")
                article_title = [i.get_text() for i in article_list]
                article_id = [i.get("href") for i in article_list]
                tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
                article_dict.update(dict(zip(tid_list, article_title)))
        else:
            print("说明只有一页评论内容")
            article_list = soup.select(".a2")
            article_title = [i.get_text() for i in article_list]
            article_id = [i.get("href") for i in article_list]
            tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
            article_dict.update(dict(zip(tid_list, article_title)))
        print(f"获取到评论过的文章个数是：{len(article_dict)}----------------->")
        return article_dict

    # 获取发布的文章
    def get_posted_tids(self):
        print("获取发布的文章")
        article_dict = {}
        # 获取下一页的链接, 有就返回，没有就返回false
        url = self.source_url + "/personal.php"
        soup = self.get_soup(url)
        last_num = soup.find(id="last")  # 如果没有找到，返回None
        if last_num:
            print("说明有不止一页评论内容")
            last_num = soup.find(id="last").get("href")
            all_page = last_num.split("page=")[1]
            all_num = int(all_page) + 1
            # 如果评论过的文章大与2页，就按两页算
            if all_num > 2:
                all_num = 2
            for i in range(1, all_num):
                page_url = self.source_url + f"/personal.php?action=post&page={i}"
                print(f"正在抽取第{i}页中的评论数据")
                soup = self.get_soup(page_url)
                # 通过soup获得已经评论过的文章id和标题
                article_list = soup.select(".a2")
                article_title = [i.get_text() for i in article_list]
                article_id = [i.get("href") for i in article_list]
                tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
                article_dict.update(dict(zip(tid_list, article_title)))
        else:
            print("说明只有一页评论内容")
            article_list = soup.select(".a2")
            article_title = [i.get_text() for i in article_list]
            article_id = [i.get("href") for i in article_list]
            tid_list = [i.split("tid=")[1].split("&")[0] for i in article_id]
            article_dict.update(dict(zip(tid_list, article_title)))
        print(f"获取已发布的文章个数是：{len(article_dict)}----------------->")
        return article_dict

    # 获取账号等级
    def get_grade(self):
        print("获取用户名和账号等级")
        # 获取下一页的链接, 有就返回，没有就返回false
        url = self.source_url + "/index.php"
        soup = self.get_soup(url)
        if "請輸入用戶名" in soup.decode():
            print(f"没有获取到用户名等信息:{soup.decode()}")
            self.send_email(f"{self.user_name} :评论异常,Cookie失效", soup.decode())
        gread_span = soup.select("body")[0].get_text()  # 如果没有找到，返回None
        self.user_name = re.search(r'\t(.*?) 退出', gread_span).group(1)
        self.grader = soup.select("tr.tr3")[0].select("span.s3")[0].get_text()
        self.weiwang = re.search(r'威望: (.*?) 點', gread_span).group(1)
        self.jinqian = re.search(r'金錢: (.*?) USD', gread_span).group(1)
        self.gongxian = re.search(r'貢獻: (.*?) 點', gread_span).group(1)
        print(f"您的用户名：{self.user_name}, 等级：{self.grader}, 威望：{self.weiwang}，貢獻：{self.gongxian}")
        if int(self.weiwang) >= 100:
            print("开始产邀请码了")
        return self.grader

    def get_one_title(self, link):
        url = link
        print(f"开始获取{url}文章title tid fid")
        soup = self.get_soup(url)
        time.sleep(5)
        title = soup.select("h4.f16")[0].get_text()
        tid = re.search(r'tid=(.*?)&', soup.decode()).group(1)
        fid = re.search(r'var fid = (.*?);', soup.decode()).group(1)
        return title, tid, fid

    # 获取技术交流版块前两页文章列表
    def get_titles(self):
        print("获取技术交流区前三页的文章链接，并提取tid和标题")
        jishu_article_dict = {}
        for i in range(1, 3):
            # 获取下一页的链接, 有就返回，没有就返回false
            url = self.source_url + f"/thread0806.php?fid=7&search=&page={i}"
            print(f"开始获取{url}页文章链接")
            soup = self.get_soup(url)
            time.sleep(5)
            titles = soup.select("td.tal h3 a") or soup.select("div.t_one a")
            titles_href = [x.get("href") for x in titles]
            self.titles_href = self.titles_href + titles_href
            titles_text = [x.get_text() for x in titles]
            # 提取出文章的tid
            if i == 1:  # 如果获取到的是第一页的链接，则剔除前8个链接，因为那是社区公告
                titles_href = [x.get("href") for x in titles][10:]
                titles_text = [x.get_text() for x in titles][10:]
            tid_list = []
            for x in titles_href:
                if "html" in x:
                    tid_list.append(x.split("/")[-1].split(".")[0])
                elif "tid" in x:
                    tid_list.append(x.split("=")[1])
            # 判断如果获取到的tidlist长度和titles_text长度一样，就压缩成字典，保存到列表中
            if len(tid_list) == len(titles_text):
                jishu_article_dict.update(dict(zip(tid_list, titles_text)))
            else:
                print("获取到的文章列表长度不一致")
                return
        # 所有页面文章链接获取到之后，将链接打印出来
        print(f"获取到技术区文章个数是：{len(jishu_article_dict)}----------------->")
        if len(jishu_article_dict):
            print(f"有文章列表，所以可以发送评论")
        else:
            print(f"没有获取到文章...无法发送评论")
        return jishu_article_dict

    # 筛选出没有评论过的文章链接
    def filters_titles(self, posted_article, jishu_article):
        print("筛选出没有评论过的文章链接")
        posted_article_keys = set(posted_article.keys())
        jishu_article_keys = set(jishu_article.keys())
        commited_tid = posted_article_keys & jishu_article_keys
        filtered_tid = jishu_article_keys.difference(posted_article_keys)
        filtered_article_link = {}
        for i in filtered_tid:
            filtered_article_link[i] = jishu_article[i]
        print(f"过滤中发现已经评论过的文章个数是：{len(commited_tid)}----------------->")
        print(f"获取到过滤后没有评论过的文章个数是：{len(filtered_article_link)}----------------->")
        # 对文章随机排序
        dict_key_ls = list(filtered_article_link.keys())
        random.shuffle(dict_key_ls)
        new_dict = {}
        for key in dict_key_ls:
            new_dict[key] = filtered_article_link.get(key)
        return new_dict

    def random_sleep_second(self, min_second=5, max_second=30):
        sleep_time = random.randint(min_second * 60, max_second * 60)
        print("当前时间是", datetime.datetime.now())
        print(f"开始随机睡眠{sleep_time} 秒，也就是 {sleep_time / 60} 分钟......")
        time.sleep(sleep_time)

    def weiwang_big_100(self):
        if int(self.weiwang) >= 100:
            print("大于100了")
            return True
        else:
            return False

    def get_article_commit_random(self, tid):
        print(f"获取一篇文章的评论，随机抽取其中一个给自己用")
        for href in self.titles_href:
            if tid in href:
                source_href = f"{self.source_url}/{href}"
                article_soup = self.get_soup(source_href)
                commit_list = article_soup.select("div.do_not_catch") or article_soup.select("div.tpc_cont")
                commit_str_list = [commit.get_text().strip() for commit in commit_list[1:]]
                self.dont_commit_str = ["1024", "感谢分享"]
                commit_fillter_str = [commit for commit in commit_str_list if commit not in self.dont_commit_str]
                return random.choice(commit_fillter_str)
        return ""

    def send_commit_jishu(self, tid, title, commit, random_sleep=False):
        print(f"{self.user_name} 技术区回复内容: {title} : {commit}")
        if self.weiwang_big_100():
            return
        post_url = self.source_url + "/post.php?"
        gbk_title = f"Re:{title}".encode()
        gbk_commit = commit.encode()
        commit_data = {
            "atc_money": 0,
            "atc_rvrc": 0,
            "atc_usesign": 1,
            "atc_convert": 1,
            "atc_autourl": 1,
            "atc_title": gbk_title,
            "atc_content": gbk_commit,
            "step": 2,
            "action": "reply",
            "fid": 7,
            "tid": tid,
            "atc_attachment": "none",
            "pid": None,
            "article": None,
            "verify": "verify", }
        zuiai_header = {
            "user-agent": self.user_agent,
            "cookie": self.cl_cookie,
            "content-type": "application/x-www-form-urlencoded"
        }
        rel_url = post_url
        # 随机睡眠几分钟
        if random_sleep:
            self.random_sleep_second()
        response = requests.post(rel_url, headers=zuiai_header, data=commit_data, timeout=10)
        res_html = response.content.decode()
        success = "發貼完畢點擊進入主題列表"
        guashui = "灌水預防機制已經打開，在1024秒內不能發貼"
        every_10 = "用戶組權限：你所屬的用戶組每日最多能發 10 篇帖子"
        if success in res_html or guashui in res_html or every_10 in res_html:
            print(f"{self.user_name}回复帖子{tid}:{title} : {commit} 成功------------->")
            self.posted_article.update({tid: title})
            return True
        else:
            print(f"{self.user_name}回复帖子{tid}:{title}失败------------->{res_html}")
            if "被管理員禁言" in res_html:
                return res_html
            return False

    # 开始发起评论
    def send_commit(self, tid, title, commit, sleep=True):
        print(f"开始发起评论: {title} : {commit}")
        if self.weiwang_big_100():
            return "威望大于100了"
        post_url = self.source_url + "/post.php?"
        gbk_title = f"Re:{title}".encode()
        gbk_commit = commit.encode()
        commit_data = {
            "atc_money": 0,
            "atc_rvrc": 0,
            "atc_usesign": 1,
            "atc_convert": 1,
            "atc_autourl": 1,
            "atc_title": gbk_title,
            "atc_content": gbk_commit,
            "step": 2,
            "action": "reply",
            "fid": 7,
            "tid": tid,
            "atc_attachment": "none",
            "pid": None,
            "article": None,
            "verify": "verify", }
        zuiai_header = {
            "user-agent": self.user_agent,
            "cookie": self.cl_cookie,
            "content-type": "application/x-www-form-urlencoded"
        }
        # 随机睡眠几分钟
        if sleep:
            self.random_sleep_second()
        response = requests.post(post_url, headers=zuiai_header, data=commit_data, timeout=10)
        res_html = response.content.decode()
        success = "發貼完畢點擊進入主題列表"
        guashui = "灌水預防機制已經打開，在1024秒內不能發貼"
        every_10 = "用戶組權限：你所屬的用戶組每日最多能發 10 篇帖子"
        if success in res_html or guashui in res_html or every_10 in res_html:
            print(f"{self.user_name}回复帖子{tid}:{title} : {commit} 成功------------->")
            self.posted_article.update({tid: title})
            return True
        else:
            print(f"{self.user_name}回复帖子{tid}:{title}失败------------->{res_html}")
            if "被管理員禁言" in res_html:
                return res_html
            return res_html

    def send_email(self, title, msg, email="648133599@qq.com"):
        content = str(msg)
        # 163邮箱服务器地址
        mail_host = "smtp.163.com"
        # 163用户名
        mail_user = "lanxingsjj@163.com"
        # 密码(部分邮箱为授权码)
        mail_pass = "QULRMYHTUVMHYVGM"
        # 邮件发送方邮箱地址
        sender = "lanxingsjj@163.com"
        # 邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
        receivers = [email]
        # 设置email信息
        # 邮件内容设置
        message = MIMEText(content, 'plain', 'utf-8')
        # 邮件主题
        message['Subject'] = title
        # 发送方信息
        message['From'] = sender
        # 接受方信息
        message['To'] = receivers[0]
        # 登录并发送邮件
        try:
            # 在阿里云上就要改为下面这种，本地和服务器都友好：
            smtpObj = smtplib.SMTP_SSL(mail_host, 465)
            # 登录到服务器
            smtpObj.login(mail_user, mail_pass)
            # 发送
            smtpObj.sendmail(sender, receivers, message.as_string())
            # 退出
            smtpObj.quit()
            print('send email success')
        except smtplib.SMTPException as e:
            print('send email error', e)  # 打印错误

    # 执行主程序
    def run(self, sleep=True):
        print("评论程序开始运行")
        self.grader = self.get_grade()
        self.posted_article = self.get_commiteds()
        self.posted_article.update(self.get_posted_tids())
        jishu_article = self.get_titles()
        filtered_link = self.filters_titles(self.posted_article, jishu_article)
        for tid, title in filtered_link.items():
            # 过滤掉禁止无关回复的文章
            if tid in self.cant_tid or any([True for t in self.cant_title if t in title]):
                print(f"遇到了不可以回复的文章{title} : {tid}")
                continue
            if self.grader == "新手上路":
                commit = "1024"  # 回复帖子的内容
                commit_list = ["我支持你", "了解一下", "发帖辛苦", "我喜欢这个", "点赞支持", "感谢分享", "你很棒",
                               "我很喜欢", "感谢你的发帖", "还有更骚的", "你很厉害", "这个也不错", "有点意思",
                               "不知道真假", "我想试试", "有没有看过的", "不错不错"]
                commit = random.choice(commit_list)
            else:
                commit_list = ["我支持你", "了解一下", "发帖辛苦", "我喜欢这个", "点赞支持", "感谢分享", "你很棒",
                               "我很喜欢", "感谢你的发帖", "还有更骚的", "你很厉害", "这个也不错", "有点意思",
                               "不知道真假", "有没有看过的", "不错不错", "这个不错", "感谢分享"]
                commit = random.choice(commit_list)
            # 从要评论的文章的评论列表随机获取一个评论内容
            commit_str = self.get_article_commit_random(tid) or commit
            print(f"{self.user_name} 的评论的内容是：{commit_str}")
            try:
                res = self.send_commit(tid, title, commit_str, sleep)
                if res is True:
                    return
                elif res == "威望大于100了":
                    self.send_email(f"{self.user_name}评论异常", res)
                    return
                else:
                    self.send_email(f"{self.user_name}评论异常", res)
                    return
            except Exception as e:
                print(e)
                self.send_email(f"{self.user_name}评论异常", e)


def get_my_ip():
    res = requests.get('http://myip.ipip.net', timeout=5).text
    print(res)


def check_white_day(min, max):
    print("判断是不是白天....")
    print("当前时间是", datetime.datetime.now())
    current_hour = datetime.datetime.now().hour
    if min <= current_hour <= max:
        print(f"{current_hour} 点是白天")
        return True
    else:
        print(f"{current_hour} 点是晚上，黑夜啊")
        return False


def sign_one_article(user_name, cookie, user_agent, link, commit="今日签到"):
    # 定时签到的任务
    print(f"{user_name}只评论一个文章，定时签到任务: {user_name}")
    # 判断是不是白天，是的话再评论，否则退出
    if not check_white_day(17, 22):
        print(f"是黑夜，所以不参与发表评论，直接退出.......")
        return
    commiter = AutoCommit(user_name, cookie, user_agent)
    # 获取简单个人信息
    commiter.get_simple_info()
    # 获取已经签到了多少次
    # commiter.get_commiteds()
    # https://cl.6273x.xyz/read.php?tid=5522451&toread=0&page=307#97203157
    # t_link = "https://cl.6273x.xyz/htm_data/2302/7/5522451.html"
    t_link = link
    title, tid, fid = commiter.get_one_title(t_link)
    commiter.send_commit_jishu(tid, title, commit, random_sleep=True)


def one_commit(user_name="", cookie="", user_agent="", sleep=True):
    # 定时评论的函数
    print("当前时间是", datetime.datetime.now())
    # 判断是不是白天，是的话再评论，否则退出
    if not check_white_day(8, 15) and sleep:
        print(f"是黑夜，所以不参与发表评论，直接退出.......")
        return
    if user_name and cookie and user_agent:
        print("传入的User可用")
    else:
        print("正在运行的脚本名称: '{}'".format(sys.argv[0]))
        print("脚本的参数数量: '{}'".format(len(sys.argv)))
        print("脚本的参数: '{}'".format(str(sys.argv)))
        user_name = sys.argv[1]
        cookie = sys.argv[2]
        user_agent = sys.argv[3]
    commiter = AutoCommit(user_name, cookie, user_agent)
    # 配置不可以回复的文章
    commiter.cant_tid = ['5448754', "5448978", "5424564"]
    commiter.cant_title = ["禁止无关回复", "乱入直接禁言", "禁言", "无关", "禁止", "乱入"]
    commiter.run(sleep)


if __name__ == '__main__':
    user_name = "kissking"
    cookie = 'ismob=1; PHPSESSID=mcu4gb74ard3iapm36iuqlt0as; 227c9_ck_info=%2F%09; 227c9_groupid=8; 227c9_winduser=AgNdDAdrB1ZTVVBXAAFdBwNcAVRTDVAGBFYMVlBTBVEBCANQBQRt; 227c9_lastvisit=0%091676022418%09%2Findex.php%3F'
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    link = "https://cl.6273x.xyz/htm_data/2302/7/5522451.html"
    # sign_one_article(user_name, cookie, user_agent, link)
    one_commit(user_name, cookie, user_agent)
