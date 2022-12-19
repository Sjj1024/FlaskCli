import json
from urllib.parse import urlencode
import ddddocr
import requests


def get_source():
    print("获取源地址")
    url = "https://get.xunfs.com/app/listapp.php"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"a": "get18", "system": "android"}
    res = requests.post(url=url, headers=header, data=data)
    res_json = json.loads(res.content.decode("utf-8"))
    # print(res_json)
    # 打印出地址信息和更新时间
    home_url = [res_json["url1"], res_json["url2"], res_json["url3"], res_json["update"]]
    for i in home_url:
        url = "https://" + i
        print(url)
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                print(url)
                return url
        except:
            continue


def get_code():
    url = f"{get_source()}/require/codeimg.php"
    payload = {}
    headers = {
        'authority': 'cl.7801x.xyz',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'cookie': 'PHPSESSID=f90v70mknlmihgb3o8q75jj8sm; 227c9_lastvisit=0%091671197001%09%2Fregister.php%3F; 227c9_lastvisit=0%091671197149%09%2Fregister.php%3F',
        'referer': 'https://cl.7801x.xyz/register.php',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    with open("test.jpg", "wb") as f:
        f.write(response.content)
    ocr = ddddocr.DdddOcr(beta=True)
    res = ocr.classification(response.content)
    print(f"获取一个验证码：{res}")
    return res


def check_success(response):
    # print(f"检查是否注册成功：{response}")
    if response.find("恭喜您,完成註冊現在可以開始使用您的會員權利了") != -1:
        print("恭喜您,完成註冊現在可以開始使用您的會員權利了")
        return True
    elif response == "驗證碼不正確，請重新填寫":
        print("驗證碼不正確，請重新填寫")
        return False
    elif response.find("此用戶名已經被註冊,請選擇其它用戶名") != -1:
        raise Exception(f"异常：此用戶名已經被註冊,請選擇其它用戶名")
    elif response.find("邀請碼錯誤") != -1:
        raise Exception(f"异常：邀請碼錯誤")
    else:
        raise Exception(f"异常：{response}")


def get_userinfo_by_cookie(cookie, user_agent):
    print("get_userinfo_bycookie-----")


def regist(user_name, yaoqingma, youxiang, validate):
    print("开始注册")
    paylod = {
        "regname": user_name,
        "regpwd": youxiang,
        "regpwdrepeat": youxiang,
        "regemail": youxiang,
        "invcode": yaoqingma,
        "validate": validate,
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
    return check_success(response.text)


def run():
    for i in range(0, 5):
        user_name = "我的大宝贝"
        yaoqingma = "a79508224ea8dbc9"
        youxiang = "1024xiaoshen@gmail.com"
        validate = get_code()
        res = regist(user_name, yaoqingma, youxiang, validate)
        if res:
            print("注册成功")
            return


if __name__ == '__main__':
    run()
