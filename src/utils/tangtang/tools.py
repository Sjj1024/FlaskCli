import base64
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
import time
import re

source_url = "https://www.hghg58.com"
time_sleep = 3


def get_source(key="98色花堂1"):
    global source_url
    if source_url:
        return source_url
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
            source_url = home.get("url")
            return home.get("url")
    return Exception("没有找到源地址")


def set_cookies(res, cookie):
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    c = res.cookies.get_dict()
    cookie_dict.update(c)
    cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
    return cookie


def get_soup(page_url, tang_cookie, user_agent, ignore=True):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': tang_cookie,
        'Pragma': 'no-cache',
        'Referer': 'https://www.hghg58.com/home.php?mod=spacecp&ac=usergroup',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    try:
        res = requests.get(page_url, headers=headers)
        html = res.content.decode()
        soup = BeautifulSoup(html, "lxml")
        if "立即注册" in soup.decode() and ignore:
            return soup.decode()
        time.sleep(time_sleep)
        return soup
    except Exception as e:
        print(f"get_soup有错误{e},请检查错误......")
        return f"get_soup有错误{e},请检查错误......"


def get_article_list(*kwg):
    print("todo")


def get_commit_list(*kwg):
    print("todo")


def get_invcode_list(*kwg):
    print("todo")


def regist_caoliu(*kwg):
    print("todo")


def get_ref_commit_list(*kwg):
    print("todo")


def pay_some_invcode(*kwg):
    print("todo")


def check_name_avliable(*kwg):
    print("todo")


def get_userinfo_by_cookie(cookie, user_agent, has_email=False):
    print(f"get_userinfo_bycookie：{cookie}, {user_agent}")
    # 获取下一页的链接, 有就返回，没有就返回false
    url = get_source()
    soup = get_soup(url, cookie, user_agent)
    # 如果是字符串，认为是没登陆
    if isinstance(soup, str):
        return soup
    # 获取详情
    if soup:
        user_name = soup.select_one("strong.vwmy").get_text().strip()
        user_id = soup.select_one("div.avt > a").get("href").split("uid=")[1].strip()
        dengji = soup.select_one("a#g_upmine").get_text().replace("用户组: ", "").strip()
        # 通过详情找到更详细的信息：https://www.hghg58.com/home.php?mod=space&uid=446206
        info_url = f"{get_source()}/home.php?mod=space&uid={user_id}"
        soup_info = get_soup(info_url, cookie, user_agent)
        # 如果是字符串，认为是没登陆
        if isinstance(soup_info, str):
            return soup_info
        fatie = soup_info.select("ul.bbda > li > a")[1].get_text().split(" ")[1].strip()
        # 威望=金钱
        weiwang = soup_info.select("ul.pf_l > li")[11].get_text().replace("金钱", "").strip()
        money = soup_info.select("ul.pf_l > li")[12].get_text().replace("色币", "").strip()
        gongxian = soup_info.select("ul.pf_l > li")[10].get_text().replace("积分", "").strip()
        if "注册时间" in soup_info.decode():
            regist_time = soup_info.select("ul.pf_l > li")[1].get_text().replace("注册时间", "").strip()
        else:
            regist_time = re.search(r'註冊: (.*?)<', soup.decode()).group(1)
        # 判断是否可以产邀请码：>lv6就可以
        able_invate = "可以" if re.search('\d', dengji) and int(re.search('\d', dengji).group(0)) > 6 else "不可以"
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
            "able_invate": able_invate,
        }
        print(f"获取的用户信息:{user_info}")
        return user_info


def login_get_cookie(user_name, password, cookie, user_agent):
    print("登陆获取cookie")
    cookie = cookie or '_safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_saltkey=OIWUctit; cPNj_2132_lastvisit=1680915276; cPNj_2132__refer=%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dusergroup; cPNj_2132_lastact=1680918920%09index.php%09'
    url = f"{get_source()}/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1"
    formhash = get_login_form_hash(cookie, user_agent)
    payload = {
        "fastloginfield": "username",
        "username": user_name,
        "cookietime": 2592000,
        "password": password,
        "formhash": formhash,
        "quickforward": "yes",
        "handlekey": "ls"
    }
    payload = urlencode(payload)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': cookie,
        'Origin': get_source(),
        'Pragma': 'no-cache',
        'Referer': get_source(),
        'Sec-Fetch-Dest': 'iframe',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': user_agent,
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    cookie_value = set_cookies(response, cookie)
    # print(response.text)
    if "CDATA" in response.text:
        return cookie_value, user_agent
    else:
        print(f"登陆异常：{response.text}")


def get_login_form_hash(cookie, user_agent):
    url = get_source()
    index_soup = get_soup(url, cookie, user_agent, ignore=False)
    formhash = index_soup.select_one("input[name='formhash']").get("value")
    return formhash


if __name__ == '__main__':
    source_url = "https://zxfdsfdsf.online"
    user_name = "桃花先森"
    pass_word = "uu9k1984@163.COM"
    cookie = '_safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_saltkey=OIWUctit; cPNj_2132_lastvisit=1680915276; cPNj_2132__refer=%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dusergroup; cPNj_2132_lastact=1680918920%09index.php%09'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    login_get_cookie(user_name, pass_word, cookie, user_agent)
