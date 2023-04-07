import requests
from bs4 import BeautifulSoup
import time
import re

source_url = "https://www.hghg58.com"
time_sleep = 3


def get_source():
    print("获取源地址")
    if source_url:
        return source_url


def set_cookies(res, cookie):
    cookie_dict = {i.split("=")[0]: i.split("=")[1] for i in cookie.split("; ")}
    c = res.cookies.get_dict()
    cookie_dict.update(c)
    cookie = "; ".join([f"{key}={val}" for key, val in cookie_dict.items()])
    return cookie


def get_soup(page_url, tang_cookie, user_agent):
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
        if "立即注册" in soup.decode():
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
    url = get_source() + ""
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
        able_invate = "可以" if int(re.search('\d', dengji).group(0)) > 6 else "不可以"
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


def login_get_cookie(user_name, password):
    print("登陆获取cookie")
    url = "https://zxfdsfdsf.online/member.php?mod=logging&action=login&loginsubmit=yes&frommessage&loginhash=LrcXZ&inajax=1"
    payload = 'formhash=34ae0253&referer=https%3A%2F%2Fzxfdsfdsf.online%2Fforum.php%3Fmod%3Dguide%26view%3Dmy%26type%3Dreply&loginfield=username&username=%E4%B8%80%E4%B8%AA%E5%B0%8F%E4%B9%A6%E7%94%9F&password=521.yigexiaoshuSHENG&gacode=&questionid=0&answer=&cookietime=2592000'
    headers = {
        'authority': 'zxfdsfdsf.online',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': 'cPNj_2132_saltkey=B2TyF8Bk; cPNj_2132_lastvisit=1673917656; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_sendmail=1; cPNj_2132_lastact=1673921270%09member.php%09logging; cPNj_2132_auth=b6a6ZC6rp1w8Mq%2FZfNMnA36yg16heGu2%2Bkb3%2FNfhQN1Uf9Q5gDYGiyEceEvaFxSe8uY6pKswT4nX2mkolilwZVutt9Q; cPNj_2132_checkfollow=1; cPNj_2132_lastact=1673921376%09member.php%09logging; cPNj_2132_lastcheckfeed=438758%7C1673921376; cPNj_2132_lip=123.5.163.159%2C1673921376; cPNj_2132_sid=0; cPNj_2132_ulastactivity=1673921376%7C0',
        'origin': 'https://zxfdsfdsf.online',
        'referer': 'https://zxfdsfdsf.online/forum.php?mod=guide&view=my&type=reply',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def get_login_form_hash():
    url = f"{get_source()}/forum.php?mod=guide&view=my&type=reply"
    payload = {}
    headers = {
        'authority': 'zxfdsfdsf.online',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cache-control': 'max-age=0',
        'cookie': 'cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_saltkey=k7M86DC7; cPNj_2132_lastvisit=1673917899; cPNj_2132_sendmail=1; cPNj_2132_lastact=1673921499%09member.php%09logging; cPNj_2132_auth=b6a6ZC6rp1w8Mq%2FZfNMnA36yg16heGu2%2Bkb3%2FNfhQN1Uf9Q5gDYGiyEceEvaFxSe8uY6pKswT4nX2mkolilwZVutt9Q; cPNj_2132_lastact=1673921835%09forum.php%09guide; cPNj_2132_lastcheckfeed=438758%7C1673921376; cPNj_2132_lip=123.5.163.159%2C1673921376; cPNj_2132_sid=0; cPNj_2132_ulastactivity=1673921376%7C0',
        'referer': 'https://zxfdsfdsf.online/member.php?mod=logging&action=logout&formhash=fe6ee739',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    source_url = "https://zxfdsfdsf.online"
    user_name = "一个小书生"
    pass_word = "521.yigexiaoshuSHENG"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
