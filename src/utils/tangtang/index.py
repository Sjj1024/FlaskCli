import requests

source_url = "https://zxfdsfdsf.online"


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
