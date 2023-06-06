import base64
import datetime
import json
import os
import random
import re
import smtplib
import sys
import time
from email.mime.text import MIMEText
from urllib import parse
import requests
from bs4 import BeautifulSoup


class TangTang(object):
    def __init__(self):
        self.residue_score = 10
        self.last_score = 1
        self.id_list = []
        self.commit_strs = []
        self.score_strs = []
        self.name = ""
        self.cookie = ""
        self.user_name = ""
        self.user_money = ""
        self.ji_fei = ""
        self.user_agent = ""
        self.source_url = self.get_source()
        self.user_info = ""
        self.contCommit = ["编辑中", "沙发", "感谢分享"]
        self.json_path = f"commit/{self.user_name}.json"

    def get_source(self, key="98色花堂1"):
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

    def get_user_info(self):
        url = f"{self.source_url}/home.php?mod=spacecp&ac=credit&showcredit=1"
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.set_cookies(response)
        # print(response.text)
        self.user_name = re.search(r'访问我的空间">(.*?)</a>', response.text).group(1)
        self.user_group = re.search(r'用户组: (.*?)</a>', response.text).group(1)
        self.user_money = re.search(r'金钱: </em>(.*?)  &nbsp;', response.text).group(1)
        self.ji_fei = re.search(r'积分: </em>(.*?) </li>', response.text).group(1)
        forhash, pid = self.get_formhash("1293427")
        self.click_ping(forhash, "1293427", pid, True)
        self.user_info = {
            "用户名": self.user_name,
            "用户组": self.user_group,
            "金钱": self.user_money,
            "积分": re.search(r'积分: </em>(.*?) </li>', response.text).group(1),
            "最大评分": self.last_score,
            "今日剩余分": self.residue_score
        }
        print(f"今日用户信息: {self.user_info}")
        return self.user_info

    def set_cookies(self, response):
        cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in self.cookie.split("; ")}
        c = response.cookies.get_dict()
        cookie_dict.update(c)
        self.cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
        return self.cookie

    def exec_jisuan(self, sunshu):
        res = eval(sunshu)
        print(f"算术答案: {sunshu} = {res}")
        return res

    def get_iphone_suan_shu(self):
        print("获取get_iphone_suan_shu")
        print(f"获取算术内容")
        url = f"{self.source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index&mobile=2',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        cookie = self.set_cookies(response)
        suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
        res = self.exec_jisuan(suanshu)
        params = {
            "id": "dd_sign",
            "mod": "sign",
            "signsubmit": "yes",
            "signhash": "",
            "handlekey": "signform_",
            "inajax": "1",
            "formhash": re.search(r'formhash" value="(.*?)" />', response.text).group(1),
            "signtoken": re.search(r'name="signtoken" value="(.*?)" />', response.text).group(1),
            "secqaahash": re.search(r'secqaahash" type="hidden" value="(.*?)" />', response.text).group(1),
            "secanswer": res,
            "cookie": cookie
        }
        return params

    def get_web_suan_shu(self):
        id_hash = "qSAUcj0"
        url = f"{self.source_url}/misc.php?mod=secqaa&action=update&idhash={id_hash}&0.4640535681735929"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'script',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        self.set_cookies(response)
        suan_shu = re.search(r"'(.*?) = \?'", response.text).group(1)
        suan_res = self.exec_jisuan(suan_shu)
        return {"id_hash": id_hash, "da_an": suan_res}

    def check_web_suanshu(self, params):
        url = f"{self.source_url}/misc.php?mod=secqaa&action=check&inajax=1&modid=&idhash=qSAEn10&secverify=15"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index',
            'user-agent': self.user_agent,
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        self.set_cookies(response)
        print(response.text)

    def get_suanshu(self):
        print(f"获取算术内容")
        url = f"{self.source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index&mobile=2',
            'upgrade-insecure-requests': '1',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        cookie = self.set_cookies(response)
        suanshu = re.search(r'输入下面问题的答案<br />(.*?) = \?</span>', response.text).group(1)
        res = self.exec_jisuan(suanshu)
        params = {
            "id": "dd_sign",
            "mod": "sign",
            "signsubmit": "yes",
            "signhash": "",
            "handlekey": "signform_",
            "inajax": "1",
            "formhash": re.search(r'formhash" value="(.*?)" />', response.text).group(1),
            "signtoken": re.search(r'name="signtoken" value="(.*?)" />', response.text).group(1),
            "secqaahash": re.search(r'secqaahash" type="hidden" value="(.*?)" />', response.text).group(1),
            "secanswer": res,
            "cookie": cookie
        }
        return params

    def start_iphone_sign(self):
        print("开始签到")
        params = self.get_suanshu()
        url = f"{self.source_url}/plugin.php?id=dd_sign&mod=sign&signsubmit=yes&signhash=&handlekey=signform_&inajax=1"
        payload = f"formhash={params.get('formhash')}&signtoken={params.get('signtoken')}&secqaahash={params.get('secqaahash')}&secanswer={params.get('secanswer')}"
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'application/xml, text/xml, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': params.get("cookie"),
            'origin': f'{self.source_url}',
            'referer': f'{self.source_url}/plugin.php?id=dd_sign&mod=sign&mobile=2',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        if "签到成功" in response.text:
            print("签到成功，金钱+2，明天记得来哦")
            return True
        elif "已经签到过啦，请明天再来" in response.text:
            print("已经签到过啦，请明天再来！")
            return True
        else:
            print(f"签到失败：{response.text}")
            return False

    def has_signed(self):
        print("判断是否已经签到了...")
        url = f"{self.source_url}/plugin.php?id=dd_sign:index"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/forum.php',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        if "今日未签到，点击签到" in response.text:
            # print(f"{self.user_name} : 今日已签到")
            return "今日未签到，点击签到"
        elif "您尚未登录" in response.text:
            print("您尚未登录")
            return response.text
        elif "今日已签到" in response.text:
            # print("今日已签到")
            return "今日已签到"
        else:
            print(f"没有检测到已签到：{response.text}")
            return "没有签到"

    def start_web_sign(self):
        print(f"开始web端签到...")
        params = self.get_web_suan_shu()
        id_hash = params.get("id_hash")
        da_an = params.get("da_an")
        url = f"{self.source_url}/misc.php?mod=secqaa&action=check&inajax=1&modid=&idhash={id_hash}&secverify={da_an}"
        payload = {}
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': self.cookie,
            'referer': f'{self.source_url}/plugin.php?id=dd_sign:index',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'x-requested-with': 'XMLHttpRequest'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        if "succeed" in response.text:
            print(f"签到成功")
        else:
            print(f"签到异常:{response.text}")

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

    def get_html(self, page_url):
        print(f"开始获取html: {page_url}")
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        res = requests.request("GET", page_url, headers=headers, data=payload)
        try:
            html = res.content.decode()
            if "立即注册" in html:
                print(html)
                self.send_email(f"{self.user_name}评论异常", html)
                raise Exception("cookie无效...")
            self.set_cookies(res)
            return html
        except Exception as e:
            print(res.text)
            print(f"获取html出错：{e},开始重试新的请求。。。。。。。")
            raise Exception("cookie无效")

    def get_articales(self):
        # 获取前十页内容
        article_list = []
        for i in range(2, 5):
            print(f"获取第{i}页文章列表......")
            page_url = f"{self.source_url}/forum.php?mod=forumdisplay&fid=95&page={i}"
            html = self.get_html(page_url)
            id_list = re.findall(r'tid=.*?class="s xst"', html)
            tid_list = [i.split("&amp")[0].replace("tid=", "") for i in id_list]
            article_list += tid_list
        print(f"得到总的文章链接是:{len(article_list)}")
        return article_list

    def update_commit_json(self):
        commit_json = {
            "id_list": self.id_list,
            "commit_strs": self.commit_strs,
            "score_strs": self.score_strs
        }
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(commit_json, f)

    def get_commit_json(self):
        # 有本地缓存过的文件，就加载，没有就查找
        self.json_path = f"{__file__.replace('auto_commit.py', '')}commit/{self.user_name}.json"
        if os.path.exists(self.json_path):
            with open(self.json_path, "r", encoding="utf-8") as f:
                commit_json = json.load(f)
                self.id_list = commit_json.get("id_list", [])
                self.commit_strs = commit_json.get("commit_strs", [])
                self.score_strs = commit_json.get("score_strs", [])
        else:
            # 给评论过的文章id和评论内容赋值
            # self.id_list = []
            # self.commit_strs = []
            self.get_commenteds()
            commit_json = {
                "id_list": self.id_list,
                "commit_strs": self.commit_strs,
                "score_strs": self.score_strs,
            }
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(commit_json, f)

    def get_commenteds(self):
        print("获取评论过的文章:")
        self.id_list = []
        self.commit_strs = []
        page = 1
        while True:
            url = f"{self.source_url}/forum.php?mod=guide&view=my&type=reply&page={page}"
            html = self.get_html(url)
            comment_list = re.findall(r'tid=.*?class="xst"', html)
            # 获取评论内容
            commit_tag_strs = re.findall(r'class="tl_reply.*?</a></div>', html)
            commit_tag_filter = list(
                set([tag.split('target="_blank">')[1].replace('</a></div>', '') for tag in commit_tag_strs]))
            self.commit_strs += commit_tag_filter
            # print(comment_list)
            # print(len(comment_list))
            ids = [i.split("&amp")[0].replace("tid=", "") for i in comment_list]
            self.id_list += ids
            if "下一页" in html and page <= 25:
                page += 1
            else:
                print(f"评论过的文章有{page}页，总共有{len(self.id_list)}篇文章被评论过")
                return self.id_list

    def get_comment_txt(self):
        print(f"随机获取评论内容:")
        txt_list = ["看起来挺骚的", "评分留下", "典型的大妈脸", "都是猛人", "被吓到了", "还是支持一下",
                    "最近啥情况", "怎么看不了", "感谢大佬", "有磁力的吗", "最近这种有点多啊", "我看到过的",
                    "这也太牛逼了",
                    "感谢大佬的精彩分享", "都是神人", "艺高人胆大", "就是喜欢这样的题材", "这个不太好吧",
                    "也开始拍剧情了",
                    "看着真实", "不知道真的假的", "这么会玩的吗", "这可太刺激了", "看看这次是什么情况", "看着眼熟",
                    "好资源，评分送上", "有够刺激的", "这玩意儿看看就好", "多更新这种题材的", "满足一下幻想",
                    "不会是假的吧",
                    "不好意思发了", "怎么全是链接错误", "但还是很喜欢", "刺激就行啊", "看不到了", "这些资源",
                    "真不错真不错",
                    "笑死我了哈哈哈", "高手在民间", "多谢老哥分享", "看起来挺不错", "先赞后看", "的确是好内容",
                    "真人想多了",
                    "因为我本纯良", "这个主题不错"]
        return txt_list[random.randint(0, len(txt_list) - 1)]

    def get_comment_from_articl(self, tid):
        # 从文章评论列表中随机获取一条评论
        commit_res = []
        page = 1
        while True:
            article_url = f"{self.source_url}/forum.php?mod=viewthread&tid={tid}&extra=page%3D1&page={page}"
            print(f"文章评论链接: {article_url}")
            article_soup = self.get_soup(article_url)
            commit_list = [com.get_text() for com in article_soup.select("td.t_f")[1:]]
            commit_text = [com.split("\r\n")[1] for com in commit_list if "\r\n" in com]
            for com in commit_text:
                if "\n" in com:
                    commit_res.append(com.split("\n")[1].replace("\xa0", "").replace(" ", ""))
                else:
                    com = com.replace("\xa0", "").replace(" ", "")
                    commit_res.append(com)
            if "下一页" in article_soup.decode() and page <= 10:
                page += 1
            else:
                commit_result = list(set(commit_res))
                commit_res = []
                for com in commit_result:
                    for cot in self.contCommit:
                        if com and cot not in com and com not in commit_res:
                            commit_res.append(com)
                break
        # 从评论列表里筛选出一个没有评论过的
        if len(commit_res) < 6:
            return ""
        random_chouse_num = 0
        while True:
            random_commit = commit_res[random.randint(0, len(commit_res) - 1)]
            if random_commit not in self.commit_strs and random_commit not in self.contCommit:
                return random_commit.strip()
            if random_chouse_num >= 10:
                random_commit = self.get_comment_txt()
                return random_commit
            random_chouse_num += 1

    def get_user_article(self, uid, all_page=False):
        page = 1
        article_list = []
        while True:
            url = f"{self.source_url}/home.php?mod=space&uid={uid}&do=thread&view=me&type=thread&order=dateline&from=space&page={page}"
            # url = f"https://www.hghg58.com/home.php?mod=space&uid={uid}&do=thread&view=me&from=space&type=reply"
            payload = {}
            headers = {
                'authority': 'www.hghg58.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'referer': f'{self.source_url}/home.php?mod=space&uid=369910&do=thread&view=me&from=space&type=thread',
                'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'cookie': self.cookie,
                'user-agent': self.user_agent
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            soup = BeautifulSoup(response.content.decode(), "lxml")
            table = soup.select_one("form#delform > table")
            td_list = table.select("td.icn > a")
            type_list = table.select("td > a.xg1")
            for index, td in enumerate(td_list):
                cate = type_list[index].get_text()
                if cate not in ["求片问答悬赏区", "投稿送邀请码", "资源出售区", "禁言申诉区", "投诉建议区",
                                "求片问答悬赏区"]:
                    tid = td.get("href").split("tid=")[1].replace("&highlight=", "")
                    article_list.append(tid)
                    # article_list += [td.get("href").split("tid=")[1].replace("&highlight=", "") for td in td_list]
            # print(article_list)
            if "下一页" in soup.decode() and all_page:
                page += 1
            else:
                return article_list

    def get_user_replay(self, uid, all_page=False):
        # uid = "369910"
        page = 1
        replay_list = []
        cate_cont_list = ["求片问答悬赏区", "投稿送邀请码", "资源出售区", "禁言申诉区", "投诉建议区", "求片问答悬赏区"]
        while True:
            url = f"{self.source_url}/home.php?mod=space&uid={uid}&do=thread&view=me&type=reply&order=dateline&from=space&page={page}"
            payload = {}
            headers = {
                'authority': 'www.hghg58.com',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'referer': 'https://www.hghg58.com/home.php?mod=space&uid=369910&do=thread&view=me&from=space&type=thread',
                'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'cookie': self.cookie,
                'user-agent': self.user_agent
            }
            response = requests.request("GET", url, headers=headers, data=payload)
            soup = BeautifulSoup(response.content.decode(), "lxml")
            formhash = soup.select_one("input[name='formhash']").get("value")
            current_type = ""
            icn_img_url = ""
            tr_list = soup.select("form#delform > table > tr")
            for tr in tr_list:
                if tr.get("class") == ["bw0_all"]:
                    # 获取文章类型：只要文件夹类型的帖子
                    icn_img_url = tr.select_one("td.icn > a > img").get("src")
                    current_type = tr.select_one("td > a.xg1").get_text()
                    print(f"是分类:{current_type} ， 文章类型图标：{icn_img_url}")
                elif tr.get("class") == ["th"]:
                    continue
                else:
                    if current_type not in cate_cont_list and "folder_new.gif" in icn_img_url:
                        td_a = tr.select_one("td.xg1 > a")
                        if td_a:
                            tid = td_a.get("href").split("tid=")[1].split("&pid=")[0]
                            pid = td_a.get("href").split("tid=")[1].split("&pid=")[1]
                            replay_list.append((formhash, tid, pid))
            # print(replay_list)
            if "下一页" in soup.decode() and all_page:
                page += 1
            else:
                return replay_list

    def get_soup(self, page_url):
        # 获取单张我的评论页面中的所有评论过的文章id和标题
        time.sleep(1)
        header = {
            "user-agent": self.user_agent,
            "cookie": self.cookie,
            "referer": self.source_url + "/index.php"
        }
        try:
            res = requests.get(page_url, headers=header, timeout=10)
            html = res.content.decode()
        except Exception as e:
            print(f"有错误{e},开始重试新的请求......")
            new_url = page_url.replace(self.source_url, source_url)
            res = requests.get(new_url, headers=header, timeout=10)
            html = res.content.decode()
        soup = BeautifulSoup(html, "lxml")
        if "立即注册" in soup.decode():
            print(f"{self.user_name}Cookie失效............")
            self.send_email(f"{self.user_name}Cookie失效", f"{soup.decode()}")
            return soup
        return soup

    def get_formhash(self, tid):
        url = f"{self.source_url}/forum.php?mod=viewthread&tid={tid}&extra=page%3D1"
        payload = {}
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        if "本帖要求阅读权限高于" in response.text:
            print("阅读权限不够，请换下一篇")
            return "", ""
        # print(response.text)
        form_hash = re.search(r'formhash=(.*?)">退出</a>', response.text).group(1)
        pid = re.search(r'table id="pid(.*?)"', response.text).group(1)
        return form_hash, pid

    def random_sleep_second(self, min_second=2, max_second=30):
        sleep_time = random.randint(min_second * 60, max_second * 60)
        print("当前时间是", datetime.datetime.now())
        print(f"开始随机睡眠{sleep_time} 秒，也就是 {sleep_time / 60} 分钟......")
        time.sleep(sleep_time)

    def post_commit(self, tid, txt, form_hash):
        print(f"开始回复评论：{tid} : {txt} hash:{form_hash}")
        url = f"{self.source_url}/forum.php?mod=post&action=reply&fid=95&tid={tid}&extra=page%3D1&replysubmit=yes&infloat=yes&handlekey=fastpost&inajax=1"
        body = {
            "file": "",
            "message": txt,
            "posttime": "1672656117",
            "formhash": form_hash,
            "usesig": "",
            "subject": ""
        }
        payload = parse.urlencode(body)
        headers = {
            'authority': 'zxfdsfdsf.online',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        self.set_cookies(response)
        html = response.text
        if "回复发布成功" in html:
            print(f"{self.user_name}回复发布成功, 评论完成了....")
            # 更新评论过的json文件
            self.id_list.append(tid)
            self.commit_strs.append(txt)
            self.update_commit_json()
            return True
        else:
            print(response.text)
            print("评论失败了")
            return False

    def click_ping(self, forhash, tid, pid, get=False):
        url = f"{self.source_url}/forum.php?mod=misc&action=rate&tid={tid}&pid={pid}&infloat=yes&handlekey=rate&inajax=1&ajaxtarget=fwin_content_rate"
        # url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&tid=1315802&pid=10966843&infloat=yes&handlekey=rate&inajax=1&ajaxtarget=fwin_content_rate"
        payload = {}
        headers = {
            'authority': 'www.hghg58.com',
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        # print(response.text)
        soup_score = BeautifulSoup(response.content.decode(), "lxml")
        self.last_score = int(soup_score.select_one("ul#scoreoption8 > li").get_text().replace("+", ""))
        self.residue_score = int(soup_score.select_one("table.mbm > tr:last-child > td:last-child").get_text())
        if get is True:
            return self.last_score
        # 判断是否是自己的文章，是否评过分，是否可以评分，是否有权限阅读
        if "评分区间" in response.text:
            print("可以评分")
            if self.residue_score and self.residue_score > 1 and self.residue_score > self.last_score:
                self.send_ping(forhash, tid, pid, self.last_score)
            else:
                print(
                    f"{self.user_name}今日剩余积分不足，评分最大是: {self.last_score}, 但是今日还剩：{self.residue_score}")
        elif "您不能对同一个帖子重复评分" in response.text:
            print("你已经给这个评过分数了")
            self.score_strs.append(tid)
            self.update_commit_json()
        elif "您不能给自己发表的帖子评分" in response.text:
            print("你不能给自己的文章评分")
            self.score_strs.append(tid)
            self.update_commit_json()
        else:
            print(f"{self.user_name}评分文章{tid}点击评分其他原因：{response.text}")

    def send_ping(self, forhash, tid, pid, score=1):
        print("发送评分")
        # url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
        # url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
        # # 欧美
        # url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
        # 综合区
        url = f"{self.source_url}/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
        referer = f"{self.source_url}/forum.php?mod=viewthread&tid={tid}&page=0#pid{pid}"
        payload = f'formhash={forhash}&tid={tid}&pid={pid}&referer={referer}&handlekey=rate&score8={score}&reason='
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://www.hghg58.com',
            'referer': f"{self.source_url}/forum.php?mod=viewthread&tid={tid}&extra=page%3D1",
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'iframe',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'cookie': self.cookie,
            'user-agent': self.user_agent
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        # print(response.text)
        if "感谢您的参与" in response.text:
            print(f"{self.user_name}评分文章{tid}评分成功")
        else:
            print(f"{self.user_name}评分文章{tid}失败: {response.text}")
        # 将评分的tid保存到本地记录
        self.score_strs.append(tid)
        self.update_commit_json()

    def start_commit_one(self, sleep=True):
        # 获取评论过的文章
        self.get_commit_json()
        # 获取前10页的文章链接
        article_list = self.get_articales()
        # 过滤没有评论过的文章链接
        need_post = [i for i in article_list if i not in self.id_list]
        # 发起评论: 随机对列表重新排序
        random.shuffle(need_post)
        for index, tid in enumerate(need_post):
            commit_txt = self.get_comment_from_articl(tid)
            if not commit_txt:
                continue
            form_hash, pid = self.get_formhash(tid)
            if not form_hash:
                continue
            print(f"开始评论：{tid} : {commit_txt} : {form_hash}")
            if sleep:
                self.random_sleep_second()
            # 评论文章
            res = self.post_commit(tid, commit_txt, form_hash)
            if res:
                # 文章评分
                # self.click_ping(form_hash, tid, pid)
                break
            else:
                continue


def auto_sign_tang(user_name, cookie, user_agent, sleep=True):
    tang = TangTang()
    tang.user_name = user_name
    tang.cookie = cookie
    tang.user_agent = user_agent
    tang.get_user_info()
    qiandao = tang.has_signed()
    if qiandao == "今日未签到，点击签到":
        if sleep:
            tang.random_sleep_second()
        tang.start_iphone_sign()
    elif "今日已签到" in qiandao:
        print(qiandao)
    else:
        print(f"签到异常: {qiandao}")


def check_white_day(run_time):
    print("判断是不是白天....")
    current_hour = datetime.datetime.now().hour
    if 6 <= current_hour <= 14 and run_time == "White":
        print(f"{current_hour} 点是白天")
        return True
    elif 15 <= current_hour <= 23 and run_time == "Black":
        print(f"{current_hour} 点是下午")
        return True
    else:
        print(f"{run_time}点不符合执行时间，所以退出")
        return False


def auto_commit_tang(user_name, cookie, user_agent, sleep=True, run_time="White"):
    # 定时评论的函数
    print(f"{user_name}只评论一个文章，定时评论任务: {user_name}")
    # 判断是不是白天，是的话再评论，否则退出
    if not check_white_day(run_time) and sleep:
        print(f"是黑夜，所以不参与发表评论，直接退出.......")
        return
    tang = TangTang()
    tang.contCommit = ["编辑中", "沙发", "感谢分享", "板凳"]
    tang.user_name = user_name
    tang.cookie = cookie
    tang.user_agent = user_agent
    tang.get_user_info()
    tang.start_commit_one(sleep)


def auto_ping_score(user_name, cookie, user_agent, uid_list, category, all_page=False, sleep=True):
    print("自动给文章或者评论评分")
    tang = TangTang()
    tang.contCommit = ["编辑中", "沙发", "感谢分享", "板凳"]
    tang.user_name = user_name
    tang.cookie = cookie
    tang.user_agent = user_agent
    tang.get_user_info()
    # 获取评论过的文章
    tang.get_commit_json()
    # 随机睡眠
    ping_sleep = [i for i in range(6, 60)]
    # 开启随机睡眠
    if sleep:
        tang.random_sleep_second()
    if category == "全部":
        print("评分所有的文章和评论")
        for uid in uid_list:
            # 评分文章
            tid_list = tang.get_user_article(uid, all_page)
            print(f"开始评分文章：{len(tid_list)} 篇文章, 文章列表: {tid_list}")
            for tid in tid_list:
                if tid not in tang.score_strs:
                    form_hash, pid = tang.get_formhash(tid)
                    if not form_hash:
                        continue
                    else:
                        tang.click_ping(form_hash, tid, pid)
                        time.sleep(random.choice(ping_sleep))
            # 评分评论内容
            tid_list = tang.get_user_replay(uid, all_page)
            print(f"开始评分评论内容：{len(tid_list)} 篇文章, 文章列表: {tid_list}")
            for formhash_tid_pid in tid_list:
                formhash, tid, pid = formhash_tid_pid
                if tid not in tang.score_strs:
                    tang.click_ping(formhash, tid, pid)
                    time.sleep(random.choice(ping_sleep))
    elif category == "文章":
        print("评分文章")
        for uid in uid_list:
            # 评分文章
            tid_list = tang.get_user_article(uid, all_page)
            print(f"开始评分文章：{len(tid_list)} 篇文章, 文章列表: {tid_list}")
            for tid in tid_list:
                if tid not in tang.score_strs:
                    form_hash, pid = tang.get_formhash(tid)
                    if not form_hash:
                        continue
                    else:
                        tang.click_ping(form_hash, tid, pid)
                        time.sleep(random.choice(ping_sleep))
    elif category == "评论":
        for uid in uid_list:
            tid_list = tang.get_user_replay(uid, all_page)
            print(f"开始评分评论内容：{len(tid_list)} 篇文章, 文章列表: {tid_list}")
            for formhash_tid_pid in tid_list:
                formhash, tid, pid = formhash_tid_pid
                if tid not in tang.score_strs:
                    tang.click_ping(formhash, tid, pid)
                    time.sleep(random.choice(ping_sleep))
    else:
        print("分类错误")


def run():
    tang = TangTang()
    tang.user_name = name
    tang.cookie = cookie
    tang.user_agent = user_agent
    tang.get_user_info()
    tang.start_commit_one()
    # qiandao = tang.has_signed()
    # if qiandao == "今日未签到，点击签到":
    #     # tang.start_web_sign()
    #     tang.start_iphone_sign()
    # elif "今日已签到" in qiandao:
    #     print(qiandao)
    # else:
    #     print(f"签到异常: {qiandao}")


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        name = "无敌小浪货"
        cookie = "cPNj_2132_saltkey=LYgJ7Ts5; _safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_lastvisit=1679708908; cPNj_2132_atarget=1; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_auth=c1fdCTCyxO5zbM52EYUfgKrC8SYmJzAQcNrBvmRwdllFLF4r%2B%2Fp1kEH%2F0PiW8iXpYz1kFXnqnB4GUa6Ky7%2BBDqeHDbs; cPNj_2132_smile=1D1; cPNj_2132_nofavfid=1; cPNj_2132_resendemail=1679713392; PHPSESSID=7djspibh5jpi4171lgd9v626pt; cPNj_2132_secqaaqSAmbi0=5813.11e7d3d12c2ffefbf9; cPNj_2132_home_diymode=1; cPNj_2132_sid=0; cPNj_2132_st_t=446206%7C1680696197%7Ca5408b579d6983a3ecd53f857c7fc017; cPNj_2132_forum_lastvisit=D_95_1680696197; cPNj_2132_visitedfid=95D155D143D96D150D142; cPNj_2132_st_p=446206%7C1680696207%7C704b0e8c270d019db2e2dbed088c7ca9; cPNj_2132_viewid=tid_1247942; cPNj_2132_ulastactivity=1680703122%7C0; cPNj_2132_lastact=1680703123%09home.php%09spacecp; cPNj_2132_checkpm=1"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    else:
        name = sys.argv[1]
        cookie = sys.argv[2]
        user_agent = sys.argv[3]
    source_url = "https://www.hghg58.com/"
    run()
