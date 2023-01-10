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


def get_article_list(cookie, user_agent, page):
    url = f"{source_url}/hack.php?H_name=invite&page={page}"
    soup = get_soup(url, cookie, user_agent)
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


if __name__ == '__main__':
    source_url = "https://cl.2059x.xyz"
    cookie = "PHPSESSID=6ssitq3s09kd07o87pr3etmt9k; 227c9_ck_info=%2F%09; 227c9_winduser=UwkKDwsEaAoNCAdUVlIHXgdeXwJdAgkLAFcBWAUBVQZRWQUMAgFcPloDUwAPWlMCBAFRDQkLAwUABloAWFcMDwcHAgcECAMA; 227c9_groupid=12; 227c9_lastvisit=0%091672996553%09%2Fhack.php%3FH_name%3Dinvite"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    page = 1
    get_article_list(cookie, user_agent, page)
