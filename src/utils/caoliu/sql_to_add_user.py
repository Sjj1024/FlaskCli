import time

import requests


def add_user_cookie(cookie):
    url = "http://localhost:5050/api1/table/addUser"
    # payload = "{'username':'','password':'','email':'1024xiaoshen@gmail.com','invcode':'','cookie':'227c9_ck_info=%2F%09; 227c9_winduser=AgdVBAVVOQRWAVRcBlFcUFZSBABSBgNTBFZTBAdSUAUMUwNQUwBRPA%3D%3D; 227c9_groupid=8; ismob=1; 227c9_lastvisit=0%091640565159%09%2Findex.php%3','userAgent':'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1','desc':'','important':1}"
    payload = {'username': '',
               'password': '',
               'email': '1024xiaoshen@gmail.com',
               'invcode': '',
               'cookie': cookie,
               'userAgent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
               'desc': '',
               'important': 2
               }
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,zh-HK;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'isOpenMenuStatus=1; sessionToken=dc712b12f699b87694fbd2c2970d34fa; sidebarStatus=1',
        'Origin': 'http://localhost:5050',
        'Referer': 'http://localhost:5050/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'X-Token': 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTY3NDAwNjc1MywiZXhwIjoxNjc0MDEwMzUzfQ.eyJpZCI6MTIxMjEyfQ.x7YlYv32bplP1GG_NMdIgMIKjBkVlSQNW27XNz0AalTgbvK4Pi8GI1nSA9oyn--uKavxFOnLPpy6z6Q0MSMMww',
        'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("POST", url, headers=headers, json=payload)
    print(response.json())
    if response.json().get("code") == 205:
        time.sleep(50)


def open_shen_sql():
    print("打开sql文件")
    with open("db_shen_20221126_053001.sql", "r+", encoding="utf-8") as f:
        content = f.read()
    res_list = content.split("),")
    cookie_list = []
    for i in res_list:
        if "winduser" in i and "Cookie进来了" in i:
            # 5890,0,'2021-12-18 12:13:50','0000-00-00 00:00:00','227c9_ck_info=%2F%09; 227c9_winduser=AglXBgFVOQlQAFdVVA0MUAVdVAhUVwxSAwAHCFtVDQZdAFcDVQcFPA%3D%3D; 227c9_groupid=8; 227c9_lastvisit=0%091639021982%09%2Fread.php%3Ftid%3D4756805; ismob=1<br />感谢来自:1024回家APP的投稿','有Cookie进来了','','draft','open','closed','','','','','2021-12-18 12:13:50','0000-00-00 00:00:00','',0,'https://1024shen.com/?p=5890',0,'post','',0)
            # print(i)
            cookie = i.split("00','")[1].split("<br")[0].replace("'", "")
            if "winduser" in cookie:
                cookie_list.append(cookie)
    middle_num = 1490
    print(f"目前有{len(cookie_list)}个Cookie数据，已添加{middle_num}个，完成率：{(middle_num / len(cookie_list)) * 100}%")
    for index, cookie in enumerate(cookie_list[middle_num:]):
        print(f"{middle_num + index} : {cookie}")
        try:
            add_user_cookie(cookie)
        except Exception as e:
            print(f"出错了: {e}")
            time.sleep(70)
        time.sleep(5)
    print(f"总计cookie: {len(cookie_list)}个")


if __name__ == '__main__':
    open_shen_sql()
