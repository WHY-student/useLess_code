from datetime import datetime
import random
import time
import requests
import json
import re
from bs4 import BeautifulSoup
from 微博.repost import getMonth


def getToutiao():
    url = "https://www.toutiao.com/api/search/content/"
    keyWord = '新冠'
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': '0',
        'format': 'json',
        'keyword': keyWord,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time())
    }
    headers = {
        'Cookie': 'tt_webid=6947194654355359262; MONITOR_WEB_ID=82f89c9d-cc79-41a9-a696-b58db5c2386a; csrftoken=60c6773a2c932d51f69d3bdac03f4a88; ttcid=2958efb7994a462ab77a8ce56eb6fedd41; tt_webid=6947194654355359262; csrftoken=60c6773a2c932d51f69d3bdac03f4a88; s_v_web_id=verify_kn2yyu1q_iyDo58dt_srfD_45Z9_BCMd_SNVhx9VGz8F5; passport_csrf_token_default=d6842d9c85b6c906426e5101b399fdc1; passport_csrf_token=d6842d9c85b6c906426e5101b399fdc1; __ac_nonce=060699a1600180a12ecad; __ac_signature=_02B4Z6wo00f012SG-NQAAIDDZiERfpN7XV9ko.xAALlT7sHA1dYxkbq4n6EYYEqoDQRG6qDQURlt7Gi6FBM.ahiARqJAHNsbO1oLA.nTPRxVfT0u7btrvdt5o3RQfh8bVz2rfKlvoys9bO8g5e; __tasessionId=8w64ocbov1617534119924; tt_scid=zffbifMcg-5wNyGFoWzpVK4iSVHZjRrf-Us3y3oy-BzpKVaPQpZEQWkTJC6HD-MS421b',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    response = requests.get(url, params=params, headers=headers)
    print(response.text)
    response_json = json.loads(response.text)
    datas = response_json['data']
    print(len(datas))
    offset = int(response_json['page_count'] / 2) * 20
    print(offset)
    new_params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyWord,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time())
    }
    response = requests.get(url, params=new_params, headers=headers)
    print(response.text)
    response_json = json.loads(response.text)
    datas = response_json['data']
    if datas:
        return len(datas) + offset
    else:
        return offset


def getZhihu():
    contents = 0
    url = 'https://www.zhihu.com/api/v4/search_v3?t=general&q=新冠&correction=1&offset=0&limit=20&lc_idx=0&show_all_topics=0'
    headers = {
        'Cookie': '_zap=ed9bf086-a745-441e-98fe-e3f8f0790468; d_c0="ADBZSSzSqhKPTlcSTQklAVRaYAyy9aQ2i1s=|1613481247"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1614763260,1614763559,1615270835,1616134958; _xsrf=DEZDkmoSKpfcnMTo6FkRCLpStGks3S8x; z_c0=Mi4xaUZENkJRQUFBQUFBTUZsSkxOS3FFaGNBQUFCaEFsVk5nemtaWVFDVlFGQ3A5VUZJWHBsOTh0TDJIcmQ5Y2pvaGZ3|1613491075|75cc5acd482adf41505faac9d6bde657652d8e92; tst=r; q_c1=24fe51b5be2c424798363f9c0e4b61f3|1614100729000|1614100729000; KLBRSID=d6f775bb0765885473b0cba3a5fa9c12|1616134989|1616134957; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1616134995; SESSIONID=LQWTR4hh271ihlOX3779wLkwjszUmEeFFl3mLzYfoNL; JOID=VlEUC0r7RpJRA4hEavdez-GLc-Z9uh_MDFSxJAvMfKsxYuEGOtEExj0LjUVqruknlCVfAq6Sss04gcbthzDrP7I=; osd=WloRCkn3TZdQAIRPb_Zdw-qOcuVxsRrND1i6IQrPcKA0Y-IKMdQFxTEAiERpouIilSZTCauTscEzhMfuizvuPrE=',
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 86.0) Gecko / 20100101Firefox / 86.0',
        'x-ab-param': 'li_sp_mqbk=0;tp_topic_style=0;li_panswer_topic=0;qap_question_author=0;li_vip_verti_search=0;tp_dingyue_video=0;pf_adjust=1;qap_question_visitor= 0;zr_slotpaidexp=1;pf_noti_entry_num=2;li_paid_answer_exp=0;se_ffzx_jushen1=0;tp_zrec=1;li_edu_page=old;zr_expslotpaid=1;top_test_4_liguangyi=1;tp_contents=1',
        'x-ab-pb': 'ClK1C2cAUgu0CgcMCACIAeQKtwDFAI0BaQF0AUwLGwC0AFgBVgyWC+ALagHXCwELQwBAAYkMTwFgC+wKPwDSAc8LRwBrAesBDws3DNwL9As0DJsLEikDAQEAAQEAAAAAAAAAAAAAAgEAAAEAABUBAAAAAQAACwABAAEBAAAAAA==',
        'x-api-version': '3.0.91',
        'x-app-za': 'OS=Web',
        'x-requested-with': 'fetch',
        'x-zse-83': '3_2.0',
        'x-zse-86': '2.0_aTS0nDUBU9FY6TtyhwYBcQ9BHqxf6TOqfHtynh9BFCYf',
    }
    response = requests.get(url, headers=headers)
    response_json = json.loads(response.text)
    headers = {
        'Cookie': '_zap=ed9bf086-a745-441e-98fe-e3f8f0790468; d_c0="ADBZSSzSqhKPTlcSTQklAVRaYAyy9aQ2i1s=|1613481247"; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1616216587,1616218054,1616240315,1616285269; _xsrf=DEZDkmoSKpfcnMTo6FkRCLpStGks3S8x; z_c0=Mi4xaUZENkJRQUFBQUFBTUZsSkxOS3FFaGNBQUFCaEFsVk5nemtaWVFDVlFGQ3A5VUZJWHBsOTh0TDJIcmQ5Y2pvaGZ3|1613491075|75cc5acd482adf41505faac9d6bde657652d8e92; tst=r; q_c1=24fe51b5be2c424798363f9c0e4b61f3|1614100729000|1614100729000; KLBRSID=b5ffb4aa1a842930a6f64d0a8f93e9bf|1616286578|1616285267; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1616286579; SESSIONID=4QMhcULhtJzZSItEpM5iIsW8JZye3KKcPczBLLlUWfT; JOID=UFEXBEmaXy9TUw8EMp9Ed-zb_aUgpQVnPjBRQ1_uHl4MBUZ7fMzfeTZYDwoyPDiAvj7OrjfNvIMN9QHuh2E8gqo=; osd=W1wTA0KRUitUWAQJNphPfOHf-q4rqAFgNTtcR1jlFVMIAk1wccjYcj1VCw05NzWEuTXFozPKt4gA8QbljGw4haE=',
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 86.0) Gecko / 20100101Firefox / 86.0',
        'x-ab-param': 'qap_question_author=0;tp_dingyue_video=0;tp_topic_style=0;li_sp_mqbk=0;se_ffzx_jushen1=0;zr_expslotpaid=1;zr_slotpaidexp=1;li_edu_page=old;li_vip_verti_search=0;pf_noti_entry_num=2;qap_question_visitor= 0;tp_zrec=1;tp_contents=1;pf_adjust=1;li_panswer_topic=0;top_test_4_liguangyi=1;li_paid_answer_exp=0',
        'x-ab-pb': 'ClK1C2cAUgu0CgcMCACIAeQKtwDFAI0BaQF0AUwLGwC0AFgBVgyWC+ALagHXCwELQwBAAYkMTwFgC+wKPwDSAc8LRwBrAesBDws3DNwL9As0DJsLEikDAQEAAQEAAAAAAAAAAAAAAgEAAAEAABUBAAAAAQAACwABAAEBAAAAAA==',
        'x-api-version': '3.0.91',
        'x-app-za': 'OS=Web',
        'x-requested-with': 'fetch',
        'x-zse-83': '3_2.0',
    }
    i = 1
    while not response_json['paging']['is_end']:
        print("正在爬取第{}页".format(i))
        i = i + 1
        url = response_json['paging']['next']
        response = requests.get(url, headers=headers)
        response_json = json.loads(response.text)
    offset = re.findall('&offset=(.*?)&', url)[0]
    return int(offset) + len(response_json['data'])
# 知乎只有总共涉及到的条目数


def getWeibo():
    url = 'https://m.weibo.cn/api/container/getIndex'
    page = 1
    params = {
        'containerid': '100103type=21&q=新冠&t=0',
        'page_type': 'searchall',
        'page': page
    }
    headers = [{
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'ALF=1619497811; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYx-rXCbgZ1krdGbxOcXQ1fLJjjIhxAa-Hz5_tTRYSuGo.; SUB=_2A25NZHYDDeRhGeBI6loT8i3JzjqIHXVupxpLrDV6PUJbktAKLVDNkW1NRot20RKY45JyAxz7sAsz5JVx23hBSNGQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt; XSRF-TOKEN=2080be; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4621309004747832%26luicode%3D10000011%26lfid%3D100103type%253D61%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%2526t%253D0%26fid%3D100103type%253D61%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%2526t%253D0%26uicode%3D10000011; _T_WM=80943054270'
    },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '_T_WM=51445041497; WEIBOCN_FROM=1110006030; SUB=_2A25NYgq1DeRhGeFL41YX-SjFyjmIHXVurJb9rDV6PUJbktAfLWvmkW1NfY0erHDa4_j2145zQOi2WiFiivFmFXHw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5LgfZD7w4Azw1IZam6GTM15JpX5KzhUgL.FoMf1hBc1Kq4eK-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSKnXSo.c1K2f; SSOLoginState=1617328869; MLOGIN=1; BAIDU_SSP_lcr=https://login.sina.com.cn/; XSRF-TOKEN=4fcc43; M_WEIBOCN_PARAMS=oid%3D4620459935269257%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%26fid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%26uicode%3D10000011'
        },
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
         'Accept': 'application/json, text/plain, */*',
         'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
         'Accept-Encoding': 'gzip, deflate, br',
         'Cookie': 'XSRF-TOKEN=d385ee; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D10000011%26fid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592; SSOLoginState=1617330319; ALF=1619922319; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYygB8ChcUh_t0FLscWwcWGf9RshqD4D3wf91Kx03fumQ.; SUB=_2A25NYvDPDeRhGeBI4lEW-SvMzzqIHXVurJCHrDV6PUJbkdAKLUHmkW1NRnwb2ZpGTKzD7KGQQzDwPwd6duZQPHkO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt; loginScene=102003; _T_WM=28240511080'
         }]
    response = requests.get(url, headers=random.choice(headers), params=params)
    print(response.text)
    response_json = json.loads(response.text)
    contents = len(response_json['data']['cards'][0]['card_group'])
    while response_json['ok'] != 0:
        page += 1
        print("正在爬取第{}页".format(page))
        params = {
            'containerid': '100103type=21&q=新冠&t=0',
            'page_type': 'searchall',
            'page': page
        }
        response = requests.get(url, headers=random.choice(headers), params=params)
        print(response.text)
        response_json = json.loads(response.text)
        try:
            contents += len(response_json['data']['cards'][0]['card_group'])
        except:
            pass
    return contents


def getToutiaoHeat():
    rankList = []
    url = "https://www.toutiao.com/api/search/content/"
    keyWord = '新冠'
    params = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': '0',
        'format': 'json',
        'keyword': keyWord,
        'autoload': 'true',
        'count': '20',
        'en_qc': '1',
        'cur_tab': '1',
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': int(time.time())
    }
    headers = {
        'Cookie': 'tt_webid=6947194654355359262; MONITOR_WEB_ID=82f89c9d-cc79-41a9-a696-b58db5c2386a; csrftoken=60c6773a2c932d51f69d3bdac03f4a88; ttcid=2958efb7994a462ab77a8ce56eb6fedd41; tt_webid=6947194654355359262; csrftoken=60c6773a2c932d51f69d3bdac03f4a88; s_v_web_id=verify_kn2yyu1q_iyDo58dt_srfD_45Z9_BCMd_SNVhx9VGz8F5; passport_csrf_token_default=d6842d9c85b6c906426e5101b399fdc1; passport_csrf_token=d6842d9c85b6c906426e5101b399fdc1; __ac_nonce=060699a1600180a12ecad; __ac_signature=_02B4Z6wo00f012SG-NQAAIDDZiERfpN7XV9ko.xAALlT7sHA1dYxkbq4n6EYYEqoDQRG6qDQURlt7Gi6FBM.ahiARqJAHNsbO1oLA.nTPRxVfT0u7btrvdt5o3RQfh8bVz2rfKlvoys9bO8g5e; __tasessionId=8w64ocbov1617534119924; tt_scid=zffbifMcg-5wNyGFoWzpVK4iSVHZjRrf-Us3y3oy-BzpKVaPQpZEQWkTJC6HD-MS421b',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    response = requests.get(url, params=params, headers=headers)
    print(response.text)
    response_json = json.loads(response.text)
    datas = response_json['data']
    print(len(datas))
    for data in datas:
        try:
            content = data['abstract']
            author = data['media_name']
            commentCout = data['comments_count']
            voteCout = data['digg_count']
            contentUrl = data['article_url']
            dateCreate = data['create_time']
            timeArray = time.localtime(int(dateCreate))
            news_date = time.strftime("%Y年%m月%d日 %H:%M:%S", timeArray)
            hotNews_json = {
                "content": content,
                "upper": author,
                "comment": commentCout,
                "thumbUp": voteCout,
                "url": contentUrl,
                "date": news_date,
                "platform": "头条",
                "rank": 0
            }
            print(hotNews_json)
            rankList.append(hotNews_json)
        except:
            continue
    for i in range(1, int(response_json['page_count'] / 2)):
        offset = i * 20
        print(offset)
        new_params = {
            'aid': '24',
            'app_name': 'web_search',
            'offset': offset,
            'format': 'json',
            'keyword': keyWord,
            'autoload': 'true',
            'count': '20',
            'en_qc': '1',
            'cur_tab': '1',
            'from': 'search_tab',
            'pd': 'synthesis',
            'timestamp': int(time.time())
        }
        response = requests.get(url, params=new_params, headers=headers)
        print(response.text)
        response_json = json.loads(response.text)
        datas = response_json['data']
        print("正在爬取第{}页数据".format(i))
        for data in datas:
            try:
                content = data['abstract']
                author = data['media_name']
                commentCout = data['comments_count']
                voteCout = data['digg_count']
                contentUrl = data['article_url']
                dateCreate = data['create_time']
                timeArray = time.localtime(int(dateCreate))
                news_date = time.strftime("%Y年%m月%d日 %H:%M:%S", timeArray)
                hotNews_json = {
                    "content": content,
                    "upper": author,
                    "comment": commentCout,
                    "thumbUp": voteCout,
                    "url": contentUrl,
                    "date": news_date,
                    "platform": "头条",
                    "rank": 0
                }
                print(hotNews_json)
                rankList.append(hotNews_json)
            except:
                continue
        time.sleep(20)
    # 对rankList进行排序
    for i in range(0, len(rankList) - 1):
        for j in range(i, len(rankList) - 1):
            ranka = rankList[i]
            rankb = rankList[j]
            rankaCout = ranka['comment'] + ranka['thumbUp']
            rankbCout = rankb['comment'] + rankb['thumbUp']
            if rankaCout < rankbCout:
                rankList[i] = rankb
                rankList[j] = ranka
    for rank in rankList:
        rank['rank'] = rankList.index(rank) + 1
    # 写数据
    rank_f = open('toutiaoRank.json', 'w+', encoding='utf-8')
    rank_f.write(json.dumps(rankList, ensure_ascii=False))
    rank_f.close()


def getWeiboHeat():
    global detail_url
    url = 'https://m.weibo.cn/api/container/getIndex'
    # 尽量使用params作为参数，因为可以在这里设置卡
    headers = [{
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'ALF=1619497811; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYx-rXCbgZ1krdGbxOcXQ1fLJjjIhxAa-Hz5_tTRYSuGo.; SUB=_2A25NZHYDDeRhGeBI6loT8i3JzjqIHXVupxpLrDV6PUJbktAKLVDNkW1NRot20RKY45JyAxz7sAsz5JVx23hBSNGQ; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt; XSRF-TOKEN=2080be; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4621309004747832%26luicode%3D10000011%26lfid%3D100103type%253D61%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%2526t%253D0%26fid%3D100103type%253D61%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%2526t%253D0%26uicode%3D10000011; _T_WM=80943054270'
    },
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Cookie': '_T_WM=51445041497; WEIBOCN_FROM=1110006030; SUB=_2A25NYgq1DeRhGeFL41YX-SjFyjmIHXVurJb9rDV6PUJbktAfLWvmkW1NfY0erHDa4_j2145zQOi2WiFiivFmFXHw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5LgfZD7w4Azw1IZam6GTM15JpX5KzhUgL.FoMf1hBc1Kq4eK-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSKnXSo.c1K2f; SSOLoginState=1617328869; MLOGIN=1; BAIDU_SSP_lcr=https://login.sina.com.cn/; XSRF-TOKEN=4fcc43; M_WEIBOCN_PARAMS=oid%3D4620459935269257%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%26fid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%26uicode%3D10000011'
        },
        {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
         'Accept': 'application/json, text/plain, */*',
         'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
         'Accept-Encoding': 'gzip, deflate, br',
         'Cookie': 'XSRF-TOKEN=d385ee; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803%26uicode%3D10000011%26fid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592; SSOLoginState=1617330319; ALF=1619922319; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYygB8ChcUh_t0FLscWwcWGf9RshqD4D3wf91Kx03fumQ.; SUB=_2A25NYvDPDeRhGeBI4lEW-SvMzzqIHXVurJCHrDV6PUJbkdAKLUHmkW1NRnwb2ZpGTKzD7KGQQzDwPwd6duZQPHkO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt; loginScene=102003; _T_WM=28240511080'
         }]
    detail_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'ALF=1619891270; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYFx_4Is6A7bc-wwJQ5UP30mXTFGReog8qxjl59Xi3-3I.; XSRF-TOKEN=13099d; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4621338674725435%26luicode%3D20000061%26lfid%3D4621338674725435%26uicode%3D20000061%26fid%3D4621338674725435; _T_WM=80943054270; SSOLoginState=1617299270; SUB=_2A25NYncWDeRhGeBI6loT8i3JzjqIHXVurRlerDV6PUJbktANLVjAkW1NRot20Xl-cPT9vgXqEH5AaO0NwPv5eOR5; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt'
    }
    rankList = []
    idList = []
    for i in range(1, 20):
        params = {
            'containerid': '100103type=61&q=新冠病毒&t=0',
            'page_type': 'searchall',
            'page': i
        }
        print("第{}页".format(i))
        response = requests.get(url, headers=random.choice(headers), params=params)
        print(response)
        print(response.text)
        if response.status_code != 200:
            time.sleep(3 * 60)
            i -= 1
            continue
        response_json = json.loads(response.text)
        datas = response_json['data']['cards']
        for data in datas:
            if data['card_type'] != 9:
                continue
            id = data['mblog']['id']
            print(id)
            if id in idList:
                print("微博已经存在")
                continue
            idList.append(id)
            test = data['mblog']['created_at']
            split = test.split(' ')
            month = split[1]
            month = getMonth(month)
            day = split[2]
            day_time = split[3]
            date = "{}月{}日{}".format(month, day, day_time)
            print(date)
            author = str(data['mblog']['user']['screen_name'])
            detail_url = "https://m.weibo.cn/statuses/extend?id={}".format(id)
            try:
                if data['mblog']['isLongText']:
                    text_json = json.loads(requests.get(detail_url, headers=detail_headers).text)
                    text = text_json['data']['longTextContent']
                    text = BeautifulSoup(text, 'html.parser').text
                else:
                    text = BeautifulSoup(data['mblog']['text'], 'html.parser').text
            except:
                continue
            print(text)
            commentCout = data['mblog']['comments_count']
            voteCout = data['mblog']['attitudes_count']
            repostCout = data['mblog']['reposts_count']
            hotNews_json = {
                "content": text,
                "upper": author,
                "comment": commentCout,
                "thumbUp": voteCout,
                "rePost": str(repostCout),
                "url": detail_url,
                "date": date,
                "platform": "微博",
                "rank": 0
            }
            print(hotNews_json)
            rankList.append(hotNews_json)
        time.sleep(10)
    # 对rankList进行排序
    for i in range(0, len(rankList) - 1):
        for j in range(i, len(rankList) - 1):
            ranka = rankList[i]
            rankb = rankList[j]
            rankaCout = ranka['comment'] + ranka['thumbUp']+int(ranka['rePost'])
            rankbCout = rankb['comment'] + rankb['thumbUp']+int(rankb['rePost'])
            if rankaCout < rankbCout:
                rankList[i] = rankb
                rankList[j] = ranka
    for rank in rankList:
        rank['rank'] = rankList.index(rank) + 1
    # 写数据
    rank_f = open('weiboRank.json', 'w+', encoding='utf-8')
    rank_f.write(json.dumps(rankList, ensure_ascii=False))
    rank_f.close()



if __name__ == '__main__':
    weibo = getWeibo()
    zhihu = getZhihu()
    toutiao = getToutiao()
    total = weibo+zhihu+toutiao
    heat_f = open("../clawerMain/heat/heat.json", "r+", encoding="utf-8")
    heat_json = json.loads(heat_f.read())
    heat_f.close()
    items = heat_json['item']
    dayWeek = datetime.now().weekday()
    new_items = []
    item = items[0]
    item['data'][dayWeek] = weibo
    new_items.append(item)
    item = items[1]
    item['data'][dayWeek] = zhihu
    new_items.append(item)
    item = items[2]
    item['data'][dayWeek] = toutiao
    new_items.append(item)
    item = items[3]
    item['data'][dayWeek] = total
    new_items.append(item)
    heat_json['item'] = new_items
    heat_f2 = open("../clawerMain/heat/heat.json", "w+", encoding='utf-8')
    heat_f2.write(json.dumps(heat_json, ensure_ascii=False))
    getToutiaoHeat()
    getWeiboHeat()
