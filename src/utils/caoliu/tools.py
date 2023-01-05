import json
import re
from urllib.parse import urlencode
import ddddocr
import requests
from bs4 import BeautifulSoup

source_url = "https://cl.2059z.xyz"


# 获取回家地址
def get_source():
    print("获取源地址")
    global source_url
    if source_url:
        return source_url
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
                print(url)
                source_url = url
                return url
        except:
            continue


def get_code():
    """
    获取验证码
    """
    while True:
        url = f"{get_source()}/require/codeimg.php"
        payload = {}
        headers = {
            'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
            'cookie': 'PHPSESSID=f90v70mknlmihgb3o8q75jj8sm; 227c9_lastvisit=0%091671197001%09%2Fregister.php%3F; 227c9_lastvisit=0%091671197149%09%2Fregister.php%3F',
            'referer': 'https://cl.7801x.xyz/register.php',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        with open("test.jpg", "wb") as f:
            f.write(response.content)
        ocr = ddddocr.DdddOcr(beta=True)
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
            "validate": get_code(),
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
    # 获取单张我的评论页面中的所有评论过的文章id和标题
    print(f"")
    header = {
        "user-agent": user_agent,
        "cookie": cl_cookie
    }
    try:
        res = requests.get(page_url, headers=header, timeout=10)
        html = res.content.decode()
        soup = BeautifulSoup(html, "lxml")
        return soup
    except Exception as e:
        print(f"get_soup有错误{e},请检查错误......")
        return None


def login_get_cookie(username, password,
                     userAgent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"):
    print("开始登陆并获取cookie")
    url = f"{get_source()}/login.php?"
    payload = {
        "pwuser": username,
        "pwpwd": password,
        "hideid": 0,
        "cktime": 31536000,
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
        'cookie': '227c9_lastvisit=0%091671848711%09%2Flogin.php%3F; PHPSESSID=idbl69k98i1nor4esbh6vc0oin',
        'upgrade-insecure-requests': '1',
        'user-agent': userAgent
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if "您已經順利登錄" in response.text:
        cookie_value = ""
        for key, value in response.cookies.items():
            cookie_value += key + '=' + value + ';'
        print(cookie_value)
        return cookie_value, userAgent
    elif "您登录尝试次数过多，需要输入验证码才能继续" in response.text:
        print("登陆次数过多")
        return "", ""
    else:
        print(response.text)
        return "", ""


def many_login_code():
    url = f"{get_source()}/login.php"
    payload = {
        "validate": get_code()
    }
    payload = urlencode(payload)
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '227c9_lastvisit=0%091671848711%09%2Flogin.php%3F; PHPSESSID=idbl69k98i1nor4esbh6vc0oin',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    if "" in response.text:
        print(f"成功")


def get_userinfo_by_cookie(cookie, user_agent):
    print(f"get_userinfo_bycookie：{cookie}, {user_agent}")
    # 获取下一页的链接, 有就返回，没有就返回false
    source_url = get_source()
    url = source_url + "/profile.php"
    soup = get_soup(url, cookie, user_agent)
    if soup:
        gread_span = soup.select("#main > div.t > table > tr > td:nth-child(3) > a")  # 如果没有找到，返回None
        email_span = soup.select("#main > div.t > table > tr > td:nth-child(2) > a")  # 如果没有找到，返回None
        # user_name = soup.select('div[colspan="2"] span')[0].get_text()
        info_url = f"{source_url}/{gread_span[0].get('href')}"
        email_url = f"{source_url}/{email_span[0].get('href')}"
        print(f"您的用户名是：, 您的等级是：{info_url}")
        info_soup = get_soup(info_url, cookie, user_agent)
        email_soup = get_soup(email_url, cookie, user_agent)
        if info_soup and email_soup:
            email = re.search(r"E-MAIL\n(.*?)com",
                              email_soup.select("#main > form")[0].get_text()).group(1) + "com"
            all_info = info_soup.select("#main > div:nth-child(3)")[0].select("table")[0].get_text()
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
            return {
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
        else:
            return {}
    else:
        return {}


def regist_caoliu(user_name, password, yaoqingma, youxiang):
    print("开始注册")
    while True:
        paylod = {
            "regname": user_name,
            "regpwd": password,
            "regpwdrepeat": password,
            "regemail": youxiang,
            "invcode": yaoqingma,
            "validate": get_code(),
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
        response = requests.request("POST", url, headers=headers, data=encode_paylod)
        res = check_success(response.text)
        if res == 0:
            print("注册成功")
            return True
        elif res == 1:
            print("验证码不正确")
        else:
            print(response.text)
            return False


def check_invode():
    url = "https://cl.2059x.xyz/register.php?"
    use_code = [1, 3, 4, 5, 6, 7, 8, 9, 0, 'a', "b", "c", "d", "e", "f"]
    for i in use_code:
        invcode = "*94659020e*fb*d9".replace("*", str(i))
        payload = f'reginvcode={invcode}&validate={get_code()}&action=reginvcodeck'
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
        print(f"{invcode}: {response.text}")


def run():
    # cookie = login_get_cookie("我真的很爱你", "1024xiaoshen@gmail.com")
    # cookie = "227c9_ck_info=%2F%09;227c9_groupid=8;227c9_lastvisit=0%091671851754%09%2Flogin.php%3F;227c9_winduser=VAsAV1daMFcAAQAAAwcEVAIBWg8JAlsHAVRRAgQOUwNTDQBVBlpVaA%3D%3D;"
    useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    # res = get_userinfo_by_cookie(cookie, useragent)
    # print(res)
    # many_login_code()
    # res = get_code()
    check_invode()


if __name__ == '__main__':
    run()
