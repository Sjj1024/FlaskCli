import re
import requests
from bs4 import BeautifulSoup


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


def get_invcode_list(cookie, user_agent, page):
    url = f"{source_url}/hack.php?H_name=invite&page={page}"
    soup = get_soup(url, cookie, user_agent)
    res_list = soup.select('tr[class="tr3"]')[10:]
    # <a href="hack.php?H_name=invite&amp;page=9" id="last">＞</a>
    total_number = soup.select('#last')[0].get("href").split(";")[1].replace("page=", "")
    invcode_list = []
    for node in res_list:
        invcode = node.select("td")[0].get_text().replace("邀請碼：", "")
        paydate = node.select("td")[1].get_text().replace("\xa0\xa0\xa0\xa0購買日期：", "")
        username = node.select("td")[2].get_text()
        registdate = node.select("td")[3].get_text()
        status = node.select("td")[4].get_text()
        invcode_list.append({
            "invcode": invcode,
            "paydate": paydate,
            "username": username,
            "registdate": registdate,
            "status": status
        })
    print(invcode_list)


if __name__ == '__main__':
    source_url = "https://cl.2059x.xyz"
    cookie = "PHPSESSID=6ssitq3s09kd07o87pr3etmt9k; 227c9_ck_info=%2F%09; 227c9_winduser=UwkKDwsEaAoNCAdUVlIHXgdeXwJdAgkLAFcBWAUBVQZRWQUMAgFcPloDUwAPWlMCBAFRDQkLAwUABloAWFcMDwcHAgcECAMA; 227c9_groupid=12; 227c9_lastvisit=0%091672996553%09%2Fhack.php%3FH_name%3Dinvite"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    page = 1
    get_invcode_list(cookie, user_agent, page)
