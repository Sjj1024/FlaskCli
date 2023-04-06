import json
import re
import time
from urllib.parse import urlencode
import ddddocr
import requests
from bs4 import BeautifulSoup

source_url = ""
time_sleep = 3


# 获取回家地址
def get_source():
    global source_url
    if source_url:
        return source_url
    print("获取源地址")
    url = "https://get.xunfs.com/app/listapp.php"
    data = {"a": "get18", "system": "android"}
    res = requests.post(url=url, headers={}, data=data)
    res_json = json.loads(res.content.decode("utf-8"))
    # print(res_json)
    # 打印出地址信息和更新时间
    home_url = [res_json["url1"], res_json["url2"], res_json["url3"], res_json["update"]]
    for i in home_url:
        url = "https://" + i
        try:
            res = requests.get(url, headers={
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"},
                               timeout=5)
            if res.status_code == 200:
                print(f"得到的源地址是: {url}")
                source_url = url
                return url
        except:
            continue


def get_all_caoliu_home():
    print("获取源地址")
    url = "https://get.xunfs.com/app/listapp.php"
    data = {"a": "get18", "system": "android"}
    proxies = {
        'http': None,
        'https': None,
    }
    res = requests.post(url=url, headers={}, data=data, proxies =proxies)
    res_json = json.loads(res.content.decode("utf-8"))
    # 打印出地址信息和更新时间
    urls = [res_json["url1"], res_json["url2"], res_json["url3"]]
    home_urls = ["https://" + i for i in urls]
    return home_urls


def get_all_homes():
    print("获取源地址")
    url = "https://api.github.com/repos/1024dasehn/TestSome/contents/.github/hubsql/deskHuijia.txt"
    res = requests.get(url=url, headers={})
    res_json = res.json()
    return res_json


def get_code(cookie):
    """
    获取验证码
    """
    while True:
        url = f"{get_source()}/require/codeimg.php"
        payload = {}
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': cookie,
            'referer': f"{get_source()}/register.php",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        time.sleep(time_sleep)
        with open("test.jpg", "wb") as f:
            f.write(response.content)
        ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
        res = ocr.classification(response.content)
        print(f"获取一个验证码：{res}")
        if len(res) == 4:
            return res


def check_name_avliable(name):
    # 检查名字是否可用
    while True:
        url = f"{get_source()}/register.php?"
        payload = {
            "username": name,
            "validate": get_code(
                "PHPSESSID=f90v70mknlmihgb3o8q75jj8sm; 227c9_lastvisit=0%091671197001%09%2Fregister.php%3F"),
            "action": "regnameck",
        }
        payload = urlencode(payload)
        headers = {
            'authority': 'cl.7801x.xyz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://cl.7801x.xyz',
            "cookie": "PHPSESSID=f90v70mknlmihgb3o8q75jj8sm; 227c9_lastvisit=0%091671197001%09%2Fregister.php%3F",
            'referer': 'https://cl.7801x.xyz/register.php',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        response = requests.request("POST", url, headers=headers, data=payload).text
        time.sleep(time_sleep)
        print(response)
        name_langth = """<script language="JavaScript1.2">parent.retmsg('0');</script>"""
        name_teshu = """<script language="JavaScript1.2">parent.retmsg('1');</script>"""
        name_xiaoxie = """<script language="JavaScript1.2">parent.retmsg('2');</script>"""
        name_used = """<script language="JavaScript1.2">parent.retmsg('3');</script>"""
        name_good = """<script language="JavaScript1.2">parent.retmsg('4');</script>"""
        name_codeerr = """<script language="JavaScript1.2">parent.retmsg('5');</script>"""
        if response == name_good:
            print("恭喜你，名字可以使用!")
            return True, "恭喜你，名字可以使用"
        elif response == name_langth:
            print("用戶名長度錯誤！")
            return False, "用戶名長度錯誤"
        elif response == name_teshu:
            print("此用戶名包含不可接受字符或被管理員屏蔽,請選擇其它用戶名！")
            return False, "此用戶名包含不可接受字符或被管理員屏蔽,請選擇其它用戶名"
        elif response == name_xiaoxie:
            print("為了避免論壇用戶名混亂,用戶名中禁止使用大寫字母,請使用小寫字母！")
            return False, "為了避免論壇用戶名混亂,用戶名中禁止使用大寫字母"
        elif response == name_used:
            print("該用戶名已經被註冊，請選用其他用戶名！")
            return False, "該用戶名已經被註冊，請選用其他用戶名"
        elif response == name_codeerr:
            print("驗證碼不正確，請重新填寫！")


def check_success(response):
    """
    检查是否注册成功
    """
    if response.find("恭喜您,完成註冊現在可以開始使用您的會員權利了") != -1:
        print("恭喜您,完成註冊現在可以開始使用您的會員權利了")
        return 0
    elif response == "驗證碼不正確，請重新填寫":
        print("驗證碼不正確，請重新填寫")
        return 1
    elif response.find("此用戶名已經被註冊,請選擇其它用戶名") != -1:
        print("此用戶名已經被註冊,請選擇其它用戶名")
        return 2
    elif response.find("邀請碼錯誤") != -1:
        print(f"邀請碼錯誤")
        return 3
    else:
        print(response)
        raise Exception(f"异常：{response}")


def get_soup(page_url, cl_cookie, user_agent):
    headers = {
        'authority': 'cl.6273x.xyz',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': cl_cookie,
        'referer': 'https://cl.6273x.xyz/index.php',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': user_agent
    }
    try:
        res = requests.get(page_url, headers=headers)
        html = res.content.decode()
        soup = BeautifulSoup(html, "lxml")
        if "登 錄" in soup.decode():
            return soup.decode()
        time.sleep(time_sleep)
        return soup
    except Exception as e:
        print(f"get_soup有错误{e},请检查错误......")
        return f"get_soup有错误{e},请检查错误......"


def set_cookies(res, cookie):
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    c = res.cookies.get_dict()
    cookie_dict.update(c)
    cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
    return cookie


def login_get_cookie(username, password,
                     cookie="227c9_lastvisit=0%091671848711%09%2Flogin.php%3F; PHPSESSID=idbl69k98i1nor4esbh6vc0oin",
                     user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'):
    print("开始登陆并获取cookie")
    url = f"{get_source()}/login.php?"
    payload = {
        "pwuser": username,
        "pwpwd": password,
        "hideid": 0,
        "cktime": 31646000,
        "forward": f"{get_source()}/index.php",
        "jumpurl": f"{get_source()}/index.php",
        "step": 2
    }
    payload = urlencode(payload)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'user-agent': user_agent
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(time_sleep)
    cookie_value = set_cookies(response, cookie)
    if "您已經順利登錄" in response.text:
        return cookie_value, user_agent
    elif "您登录尝试次数过多，需要输入验证码才能继续" in response.text:
        print("登陆次数过多")
        cookie, useragent = many_login_code(cookie_value, user_agent)
        return login_get_cookie(username, password, cookie, useragent)
        # return cookie_value, "登陆次数过多"
    elif "密碼錯誤" in response.text:
        print(f"密码错误了")
        return cookie_value, "密码错误"
    elif "該賬號已開啟兩步驗證" in response.text:
        print(f"启用了两步验证")
        return cookie_value, "启用了两步认证"
    else:
        print(f"登陆异常:{response.text}")
        return cookie_value, "异常登陆"


def many_login_code(cookie, useragent):
    url = f"{get_source()}/login.php"
    payload = {
        "validate": get_code(cookie)
    }
    payload = urlencode(payload)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'upgrade-insecure-requests': '1',
        'user-agent': useragent
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(time_sleep)
    if "驗證碼不正確，請重新填寫" in response.text:
        return many_login_code(cookie, useragent)
    elif "刷新不要快於" in response.text:
        time.sleep(time_sleep)
        print("論壇設置:刷新不要快於 2 秒")
        return many_login_code(cookie, useragent)
    else:
        print(response.text)
        print(f"验证成功")
        return cookie, useragent


def get_userinfo_by_cookie(cookie, user_agent, has_email=False):
    print(f"get_userinfo_bycookie：{cookie}, {user_agent}")
    # 获取下一页的链接, 有就返回，没有就返回false
    url = get_source() + "/profile.php"
    soup = get_soup(url, cookie, user_agent)
    if isinstance(soup, str):
        return soup
    liangbu_renzheng = "已設置 停用" in soup.select("#main")[0].get_text()
    if soup:
        # 获取简单信息
        user_name = re.search(r'用戶名: (.*?)[（|<]', soup.decode()).group(1)
        user_id = re.search(r'uid=(.*?)">[查看資料|查看個人資料]', soup.decode()).group(1)
        dengji = re.search(r'頭銜: (.*?)<', soup.decode()).group(1)
        fatie = re.search(r'發帖: (.*?)<', soup.decode()).group(1)
        weiwang = re.search(r'威望: (.*?)點<', soup.decode()).group(1)
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
            "dengji": dengji,
            "jifen": "",
            "fatie": fatie,
            "weiwang": weiwang,
            "money": money,
            "gongxian": gongxian,
            "gongxian_link": "",
            "regist_time": regist_time,
            "email": "",
            "desc": "",
            "able_invate": "",
            "authentication": authentication
        }
        print(f"获取的用户信息:{user_info}")
        # return user_info
        # # 获取详细信息
        gread_span = soup.select("#main > div.t > caoliu > tr > td:nth-child(3) > a")  # 如果没有找到，返回None
        # email_span = soup.select("#main > div.t > caoliu > tr > td:nth-child(2) > a")  # 如果没有找到，返回None
        # # user_name = soup.select('div[colspan="2"] span')[0].get_text()
        info_url = f"{get_source()}/{gread_span[0].get('href')}"
        # email_url = f"{get_source()}/{email_span[0].get('href')}"
        invcode_url = f"{get_source()}/hack.php?H_name=invite"
        info_soup = get_soup(info_url, cookie, user_agent)
        # if not has_email:
        #     email_soup = get_soup(email_url, cookie, user_agent)
        #     if "Mobile" not in email_soup.decode():
        #         email = re.search(r"E-MAIL\n(.*?) \(", email_soup.select("#main > form")[0].get_text()).group(1)
        #     else:
        #         email = re.search(r"E-MAIL\n(.*?)為保?", email_soup.select("#main > form")[0].get_text()).group(1)
        # else:
        #     email = has_email
        invcode_soup = get_soup(invcode_url, cookie, user_agent)
        if info_soup and invcode_soup:
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
            invcode_auth = re.search(r'是否有权限购买\s*(.*)\r', invcode_soup.select("#main")[0].get_text()).group(1)
            if liangbu_renzheng:
                authentication = "已启用："
                if invcode_auth == "有":
                    if int(gongxian) > 300:
                        if dengji not in ["禁止發言", "新手上路"]:
                            invcode_flag = "可以购买"
                        else:
                            invcode_flag = "等级不足"
                    else:
                        invcode_flag = "贡献不足"
                else:
                    invcode_flag = "无权限购买"
            else:
                invcode_flag = "两步认证未启用"
                authentication = "未启用"
            # 判断是否永久禁言在里面
            desc = ""
            if "禁止發言" in all_info:
                dengji = re.search(r'系統頭銜(.*?)\r\n', all_info).group(1)
                desc = re.search(r'\(於(.*?)\)', all_info).group(1)
                if "永久禁言" in desc:
                    invcode_flag = "否:被永久禁言"
            user_info = {
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
                "desc": desc,
                "able_invate": invcode_flag,
                "authentication": authentication
            }
            print(f"获取的用户信息:{user_info}")
            return user_info
        else:
            return {}
    else:
        return {}


def pay_some_invcode(cookie, user_agent, num):
    print(f"购买邀请码：{num} 个")
    url = f"{get_source()}/hack.php?H_name=invite"
    payload = f'action=buy&step=3&invnum={num}'
    headers = {
        'authority': 'cl.2059x.xyz',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': cookie,
        'referer': f'{get_source()}/hack.php?H_name=invite&action=buy',
        'user-agent': user_agent
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    time.sleep(time_sleep)
    print(response.text)
    if "操作完成" in response.text:
        return True
    else:
        print(f"购买邀请码失败: {response.text}")
        return False


def get_invcode_list(cookie, user_agent, page):
    url = f"{get_source()}/hack.php?H_name=invite&page={page}"
    soup = get_soup(url, cookie, user_agent)
    if isinstance(soup, str):
        return soup
    if soup and "購買日期" in soup.get_text():
        res_list = soup.select('tr[class="tr3"]')[10:]
    else:
        res_list = soup.select('tr[class="tr3"]')[8:] if page == 1 else soup.select('tr[class="tr3"]')[1:]
    last = "page" in soup.select('#last')[0].get("href") if soup.select('#last') else soup.select('#last')
    if last:
        total_number = soup.select('#last')[0].get("href").split("&")[1].replace("page=", "")
    else:
        total_number = page
    if len(res_list) <= 2:
        return {"total": 0, "items": []}
    invcode_list = []
    for node in res_list:
        if "購買日期" in node.get_text():
            # PC端过滤
            invcode = node.select("td")[0].get_text().replace("邀請碼：", "")
            paydate = node.select("td")[1].get_text().replace("\xa0\xa0\xa0\xa0購買日期：", "")
            username = node.select("td")[2].get_text()
            registdate = node.select("td")[3].get_text()
            status = node.select("td")[4].get_text()
        else:
            # 手机端过滤
            node_text = node.get_text().split(" ")
            paydate = node_text[0].replace("\n", "") + " " + node_text[1]
            invcode = node_text[2].split("\r\n\r\n")[0]
            status = node_text[2].split("\r\n\r\n")[1].replace("[", "").replace("]", "")
            username = node_text[2].split("\xa0")[1] if "已邀请" in node_text[2] else ""
            registdate = node_text[3] + " " + node_text[4].replace("\n", "") if "已邀请" in node_text[2] else ""
        invcode_list.append({
            "invcode": invcode,
            "paydate": paydate,
            "username": username,
            "registdate": registdate,
            "status": status
        })
    print(invcode_list)
    if total_number:
        return {"total": int(total_number) * 10, "items": invcode_list}
    return {"total": 0, "items": invcode_list}


def get_article_list(cookie, user_agent, page):
    url = f"{get_source()}/personal.php?action=&keyword=&page={page}"
    soup = get_soup(url, cookie, user_agent)
    if isinstance(soup, str):
        return soup
    if soup and "所在版塊" in soup.get_text():
        # web端
        res_list = soup.select("tr.tr3.tac")
    else:
        # 手机端
        res_list = soup.select("tr.tr3")[1:]
    last = "page" in soup.select('#last')[0].get("href") if soup.select('#last') else soup.select('#last')
    if last:
        total_number = soup.select('#last')[0].get("href").split("page=")[1]
    else:
        total_number = page
    article_list = []
    for node in res_list:
        if "時間" not in node.get_text():
            # PC端过滤
            title = node.select("a.a2")[1].get_text()
            link = node.select("a.a2")[1].get("href")
            category = node.select("a")[2].get_text()
            category_link = node.select("a")[2].get("href")
            replay = node.select("td")[2].get_text()
            like = node.select("td")[3].get_text()
            pub_time = node.select("td")[4].get_text()
        else:
            # 手机端过滤
            title = node.select("a.a2")[1].get_text()
            link = node.select("a.a2")[1].get("href")
            category = node.select("a.tac")[0].get_text()
            category_link = node.select("a.tac")[0].get("href")
            replay = node.select("span")[0].get_text().split("時間")[1].split("回")[1].replace(": ", "")
            like = "*"
            pub_time = node.select("span")[0].get_text().split("時間")[1].split("回")[0].replace(": ", "")
        article_list.append({
            "title": title,
            "link": link,
            "category": category,
            "category_link": category_link,
            "replay": replay,
            "like": like,
            "pub_time": pub_time
        })
    print(article_list)
    if total_number:
        return {"total": int(total_number) * 10, "items": article_list}
    return {"total": 0, "items": article_list}


def get_commit_list(cookie, user_agent, page):
    # 获取评论列表
    url = f"{get_source()}/personal.php?action=post&page={page}"
    soup = get_soup(url, cookie, user_agent)
    if isinstance(soup, str):
        return soup
    if soup and "Mobile" not in soup.decode():
        # web端
        res_list = soup.select("tr > td > div")[2:]
    else:
        # 手机端
        res_list = soup.select("tr > td > div")[4:]
    last = "page" in soup.select('#last')[0].get("href") if soup.select('#last') else soup.select('#last')
    if last:
        total_number = soup.select('#last')[0].get("href").split("page=")[1]
    else:
        total_number = page
    article_list = []
    for node in res_list:
        if "上一頁" in node.get_text() or not node.get_text():
            continue
        title = node.select("a")[1].get_text()
        link = node.select("a")[1].get("href")
        author = node.select("a")[2].get_text()
        author_link = node.select("a")[2].get("href")
        category = node.select("div.fr")[0].get_text()
        category_link = node.select("div.fr")[0].select("a")[0].get("href")
        replay = node.select("div")[2].get_text()
        pub_time = node.select("div.fl")[0].get_text()
        article_list.append({
            "title": title,
            "link": link,
            "author": author,
            "author_link": author_link,
            "category": category,
            "category_link": category_link,
            "replay": replay,
            "pub_time": pub_time
        })
    print(article_list)
    if total_number:
        return {"total": int(total_number) * 10, "items": article_list}
    return {"total": 0, "items": article_list}


def get_ref_commit_list(cookie, user_agent, page):
    # 获取点评列表
    url = f"{get_source()}/personal.php?action=comment&page={page}"
    soup = get_soup(url, cookie, user_agent)
    if isinstance(soup, str):
        return soup
    if soup and "Mobile" not in soup.decode():
        # web端
        res_list = soup.select("tr > td > div")[2:]
    else:
        # 手机端
        res_list = soup.select("tr > td > div")[4:]
    last = "page" in soup.select('#last')[0].get("href") if soup.select('#last') else soup.select('#last')
    if last:
        total_number = soup.select('#last')[0].get("href").split("page=")[1]
    else:
        total_number = page
    article_list = []
    for node in res_list:
        if "上一頁" in node.get_text() or not node.get_text():
            continue
        title = node.select("a")[1].get_text()
        link = node.select("a")[1].get("href")
        category = node.select("div.fr")[0].get_text()
        category_link = node.select("div.fr")[0].select("a")[0].get("href")
        re_replay = node.select("div")[2].select("i")[0].get_text()
        replay = node.select("div")[2].get_text().replace(re_replay, "")
        pub_time = node.select("div.fl")[0].get_text().strip()
        article_list.append({
            "title": title,
            "link": link,
            "category": category,
            "category_link": category_link,
            "re_replay": re_replay,
            "replay": replay,
            "pub_time": pub_time
        })
    print(article_list)
    if total_number:
        return {"total": int(total_number) * 10, "items": article_list}
    return {"total": 0, "items": article_list}


def regist_caoliu(user_name, password, yaoqingma, youxiang):
    print("开始注册")
    while True:
        paylod = {
            "regname": user_name,
            "regpwd": password,
            "regpwdrepeat": password,
            "regemail": youxiang,
            "invcode": yaoqingma,
            "validate": get_code(
                "PHPSESSID=4nh5edfvkj472orqp471q9rs4b;227c9_lastvisit=0%091673152222%09%2Fregister.php%3F"),
            "forward": "",
            "step": "2",
        }
        encode_paylod = urlencode(paylod)
        url = f"{get_source()}/register.php?"
        headers = {
            'authority': 'cl.7801x.xyz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': f"{get_source()}",
            "cookie": "PHPSESSID=4nh5edfvkj472orqp471q9rs4b;227c9_lastvisit=0%091673152222%09%2Fregister.php%3F",
            'referer': f"{get_source()}/register.php",
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        response = requests.request("POST", url, headers=headers, data=encode_paylod)
        time.sleep(time_sleep)
        res = check_success(response.text)
        if res == 0:
            print("注册成功")
            return True
        elif res == 1:
            print("验证码不正确, 开始循环注册...")
        else:
            print(response.text)
            return False


def check_invode():
    url = f"{get_source()}/register.php?"
    use_code = [1, 3, 4, 5, 6, 7, 8, 9, 0, 'a', "b", "c", "d", "e", "f"]
    for i in use_code:
        invcode = "*94659020e*fb*d9".replace("*", str(i))
        payload = f'reginvcode={invcode}&validate={get_code("")}&action=reginvcodeck'
        headers = {
            'authority': 'cl.2059x.xyz',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://cl.2059x.xyz',
            'referer': 'https://cl.2059x.xyz/register.php',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        time.sleep(time_sleep)
        print(f"{invcode}: {response.text}")


def run():
    # cookie = login_get_cookie("我真的很爱你", "1024xiaoshen@gmail.com")
    cookie = "227c9_ck_info=%2F%09;227c9_groupid=8;227c9_winduser=BANcAQZaOQcFUgZWVgcKAARdUlBXVwMBBQRWAgJSB1BcBVdWUwNQPFFaVAAGU1dWUVNYCFcBVFMBUFIDBlZTBFJSBQNYVFNd;PHPSESSID=ji0o1te7qp45uams4fmuifdamd;ismob=1;227c9_lastvisit=0%091673592051%09%2Fpersonal.php%3Faction%3Dcomment "
    useragent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
    # get_userinfo_by_cookie(cookie, useragent)
    get_ref_commit_list(cookie, useragent, 1)


if __name__ == '__main__':
    run()
