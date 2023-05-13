import random

import requests
from bs4 import BeautifulSoup


def click_ping(forhash, tid, pid):
    # tid = "1310835"
    # pid = "10930776"
    url = f"https://www.hghg58.com/forum.php?mod=misc&action=rate&tid={tid}&pid={pid}&infloat=yes&handlekey=rate&inajax=1&ajaxtarget=fwin_content_rate"
    # url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&tid=1315802&pid=10966843&infloat=yes&handlekey=rate&inajax=1&ajaxtarget=fwin_content_rate"
    payload = {}
    headers = {
        'authority': 'www.hghg58.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cookie': 'cPNj_2132_sid=0; cPNj_2132_smile=1D1; _safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_saltkey=LYgJ7Ts5; cPNj_2132_lastvisit=1679708908; cPNj_2132_atarget=1; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_auth=c1fdCTCyxO5zbM52EYUfgKrC8SYmJzAQcNrBvmRwdllFLF4r%2B%2Fp1kEH%2F0PiW8iXpYz1kFXnqnB4GUa6Ky7%2BBDqeHDbs; cPNj_2132_nofavfid=1; cPNj_2132_resendemail=1679713392; PHPSESSID=7djspibh5jpi4171lgd9v626pt; cPNj_2132_secqaaqSAmbi0=5813.11e7d3d12c2ffefbf9; cPNj_2132_home_diymode=1; cPNj_2132_visitedfid=95D155D143D96D150D142; cPNj_2132_ulastactivity=1683862993%7C0; cPNj_2132_checkpm=1; cPNj_2132_st_t=446206%7C1683863391%7C8766b8300a76f59e4a7b88f7e37a555e; cPNj_2132_forum_lastvisit=D_95_1683863391; cPNj_2132_lastact=1683863394%09forum.php%09viewthread; cPNj_2132_st_p=446206%7C1683863394%7C617b645f6fac1b207d4693e414fb79c2; cPNj_2132_viewid=tid_1216314; cPNj_2132_lastact=1683863514%09forum.php%09misc; cPNj_2132_sid=0',
        'referer': 'https://www.hghg58.com/forum.php?mod=viewthread&tid=1216314&extra=page%3D1%26filter%3Dtypeid%26typeid%3D715',
        'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.text)
    # 判断是否是自己的文章，是否评过分，是否可以评分，是否有权限阅读
    if "评分区间" in response.text:
        print("可以评分")
        send_ping(forhash, tid, pid)
    elif "您不能对同一个帖子重复评分" in response.text:
        print("你已经给这个评过分数了")
    elif "您不能给自己发表的帖子评分" in response.text:
        print("你不能给自己的文章评分")
    else:
        print(f"其他原因：{response.text}")


def send_ping(forhash, tid, pid):
    print("发送评分")
    url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
    url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
    # 欧美
    url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
    # 综合区
    url = "https://www.hghg58.com/forum.php?mod=misc&action=rate&ratesubmit=yes&infloat=yes&inajax=1"
    # forhash = "a2149df6"
    # tid = "1315802"
    # pid = "10966843"
    referer = f"https://www.hghg58.com/forum.php?mod=viewthread&tid={tid}&page=0#pid{pid}"
    score = "1"
    payload = f'formhash={forhash}&tid={tid}&pid={pid}&referer={referer}&handlekey=rate&score8={score}&reason='
    headers = {
        'authority': 'www.hghg58.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        'content-type': 'application/x-www-form-urlencoded',
        'cookie': '_safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_nofavfid=1; cPNj_2132_secqaaqSAzip0=2747.037610c1ed32934a87; cPNj_2132_atarget=1; cPNj_2132_smile=1D1; cPNj_2132_resendemail=1679713392; cPNj_2132_secqaaqSAmbi0=5813.11e7d3d12c2ffefbf9; cPNj_2132_home_diymode=1; cPNj_2132_checkpm=1; cPNj_2132__refer=%252Fhome.php%253Fmod%253Dspacecp%2526ac%253Dusergroup; cPNj_2132_checkfollow=1; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_sid=0; cPNj_2132_lastcheckfeed=418590%7C1680927923; cPNj_2132_lip=101.86.79.224%2C1680927923; cPNj_2132_saltkey=LYgJ7Ts5; cPNj_2132_lastvisit=1679708908; cPNj_2132_auth=c1fdCTCyxO5zbM52EYUfgKrC8SYmJzAQcNrBvmRwdllFLF4r%2B%2Fp1kEH%2F0PiW8iXpYz1kFXnqnB4GUa6Ky7%2BBDqeHDbs; PHPSESSID=7djspibh5jpi4171lgd9v626pt; cPNj_2132_visitedfid=95D155D143D96D150D142; cPNj_2132_ulastactivity=1683780231%7C0; cPNj_2132_st_t=446206%7C1683780235%7Cbe25bf8d86265d0b4577631bbcc6092b; cPNj_2132_forum_lastvisit=D_95_1683780235; cPNj_2132_st_p=446206%7C1683780254%7C46c57bbb8013116693cb3bccdd90d08e; cPNj_2132_viewid=tid_1315802; cPNj_2132_lastact=1683780272%09forum.php%09misc; cPNj_2132_lastact=1683780396%09forum.php%09misc; cPNj_2132_sid=0',
        'origin': 'https://www.hghg58.com',
        'referer': 'https://www.hghg58.com/forum.php?mod=viewthread&tid=1315802&extra=page%3D1',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'iframe',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)
    if "感谢您的参与" in response.text:
        print("评分成功")
    else:
        print(f"评分失败: {response.text}")


def get_user_article(uid, all_page=False):
    # uid = "369910"
    page = 1
    article_list = []
    while True:
        url = f"https://www.hghg58.com/home.php?mod=space&uid={uid}&do=thread&view=me&type=thread&order=dateline&from=space&page={page}"
        # url = f"https://www.hghg58.com/home.php?mod=space&uid={uid}&do=thread&view=me&from=space&type=reply"
        payload = {}
        headers = {
            'authority': 'www.hghg58.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': 'cPNj_2132_sid=0; cPNj_2132_smile=1D1; cPNj_2132_saltkey=LYgJ7Ts5; _safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_lastvisit=1679708908; cPNj_2132_atarget=1; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_auth=c1fdCTCyxO5zbM52EYUfgKrC8SYmJzAQcNrBvmRwdllFLF4r%2B%2Fp1kEH%2F0PiW8iXpYz1kFXnqnB4GUa6Ky7%2BBDqeHDbs; cPNj_2132_nofavfid=1; cPNj_2132_resendemail=1679713392; PHPSESSID=7djspibh5jpi4171lgd9v626pt; cPNj_2132_secqaaqSAmbi0=5813.11e7d3d12c2ffefbf9; cPNj_2132_home_diymode=1; cPNj_2132_st_t=446206%7C1680831148%7C998ac1568b1dc68d52557bc0a774c7db; cPNj_2132_forum_lastvisit=D_95_1680831148; cPNj_2132_ulastactivity=1683887769%7C0; cPNj_2132_noticeTitle=1; cPNj_2132_st_p=446206%7C1683888228%7C829a1ff684aa681224f7e9fff2a3a599; cPNj_2132_visitedfid=141D95D155D143D96D150D142; cPNj_2132_viewid=tid_1317131; cPNj_2132_lastact=1683888228%09home.php%09spacecp; cPNj_2132_lastact=1683863514%09forum.php%09misc; cPNj_2132_sid=0',
            'referer': 'https://www.hghg58.com/home.php?mod=space&uid=369910&do=thread&view=me&from=space&type=thread',
            'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
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
        print(article_list)
        if "下一页" in soup.decode() and all_page:
            page += 1
        else:
            return article_list


def get_user_replay(uid, all_page=False):
    uid = "369910"
    page = 1
    replay_list = []
    while True:
        url = f"https://www.hghg58.com/home.php?mod=space&uid={uid}&do=thread&view=me&type=reply&order=dateline&from=space&page={page}"
        # url = f"https://www.hghg58.com/home.php?mod=space&uid={uid}&do=thread&view=me&from=space&type=reply"
        payload = {}
        headers = {
            'authority': 'www.hghg58.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie': 'cPNj_2132_sid=0; cPNj_2132_smile=1D1; cPNj_2132_saltkey=LYgJ7Ts5; _safe=vqd37pjm4p5uodq339yzk6b7jdt6oich; cPNj_2132_lastvisit=1679708908; cPNj_2132_atarget=1; cPNj_2132_lastfp=66abe79b56fe4d1db0defa055279da8b; cPNj_2132_auth=c1fdCTCyxO5zbM52EYUfgKrC8SYmJzAQcNrBvmRwdllFLF4r%2B%2Fp1kEH%2F0PiW8iXpYz1kFXnqnB4GUa6Ky7%2BBDqeHDbs; cPNj_2132_nofavfid=1; cPNj_2132_resendemail=1679713392; PHPSESSID=7djspibh5jpi4171lgd9v626pt; cPNj_2132_secqaaqSAmbi0=5813.11e7d3d12c2ffefbf9; cPNj_2132_home_diymode=1; cPNj_2132_st_t=446206%7C1680831148%7C998ac1568b1dc68d52557bc0a774c7db; cPNj_2132_forum_lastvisit=D_95_1680831148; cPNj_2132_ulastactivity=1683887769%7C0; cPNj_2132_noticeTitle=1; cPNj_2132_st_p=446206%7C1683888228%7C829a1ff684aa681224f7e9fff2a3a599; cPNj_2132_visitedfid=141D95D155D143D96D150D142; cPNj_2132_viewid=tid_1317131; cPNj_2132_lastact=1683888228%09home.php%09spacecp; cPNj_2132_lastact=1683863514%09forum.php%09misc; cPNj_2132_sid=0',
            'referer': 'https://www.hghg58.com/home.php?mod=space&uid=369910&do=thread&view=me&from=space&type=thread',
            'sec-ch-ua': '"Microsoft Edge";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        soup = BeautifulSoup(response.content.decode(), "lxml")
        formhash = soup.select_one("input[name='formhash']").get("value")
        current_type = ""
        tr_list = soup.select("form#delform > table > tr")
        for tr in tr_list:
            if tr.get("class") == ["bw0_all"]:
                current_type = tr.select_one("td > a.xg1").get_text()
                print(f"是分类:{current_type}")
            elif tr.get("class") == ["th"]:
                continue
            else:
                if current_type not in ["求片问答悬赏区", "投稿送邀请码", "资源出售区", "禁言申诉区", "投诉建议区",
                                        "求片问答悬赏区"]:
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


if __name__ == '__main__':
    formhash = "a2149df6"
    tid = "1317218"
    pid = "10975945"
    # click_ping(formhash, tid, pid)
    all_tid = get_user_article("369910", True)
    # all_tid = get_user_replay("438864")
    print(len(all_tid))
