# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import random
from 微博.repost import getMonth


class Weibo:
    id = 0
    date = ""
    author = ""
    content = ""
    weiboVedio = ""
    weiboPic = ""

    def __init__(self, id, date, author, content, weiboVedio, weiboPic):
        self.id = id
        self.date = date
        self.author = author
        self.content = content
        self.weiboVedio = weiboVedio
        self.weiboPic = weiboPic



# url = 'https://m.weibo.cn/api/container/getIndex?containerid=100103type=61&q=新冠病毒&t=0&page_type=searchall&page=2'
url = 'https://m.weibo.cn/api/container/getIndex'
# 尽量使用params作为参数，因为可以在这里设置卡
params = {
    'containerid': '100103type=61&q=新冠病毒&t=0',
    'page_type': 'searchall',
    'page': '1'
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
detail_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Cookie': 'ALF=1619891270; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYFx_4Is6A7bc-wwJQ5UP30mXTFGReog8qxjl59Xi3-3I.; XSRF-TOKEN=13099d; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4621338674725435%26luicode%3D20000061%26lfid%3D4621338674725435%26uicode%3D20000061%26fid%3D4621338674725435; _T_WM=80943054270; SSOLoginState=1617299270; SUB=_2A25NYncWDeRhGeBI6loT8i3JzjqIHXVurRlerDV6PUJbktANLVjAkW1NRot20Xl-cPT9vgXqEH5AaO0NwPv5eOR5; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt'
}
weiboList = []
idList = []
for i in range(1, 100):
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
        time.sleep(3*60)
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
        author = str(data['mblog']['user']['id'])
        try:
            if data['mblog']['isLongText']:
                detail_url = "https://m.weibo.cn/statuses/extend?id={}".format(id)
                text_json = json.loads(requests.get(detail_url, headers=detail_headers).text)
                text = text_json['data']['longTextContent']
                text = BeautifulSoup(text, 'html.parser').text
            else:
                text = BeautifulSoup(data['mblog']['text'], 'html.parser').text
        except:
            continue
        print(text)
        source = data['mblog']['source']
        print(source)
        try:
            page_info = data['mblog']['page_info']
            print(data['mblog']['page_info']['type'])
            if data['mblog']['page_info']['type'] == "video":
                weiboVedio = data['mblog']['page_info']['media_info']['stream_url_hd']
                weiboPic = ""
            else:
                weiboPic = data['mblog']['original_pic']
                weiboVedio = ""
        except:
            weiboPic = ""
            weiboVedio = ""
        weibo = Weibo(id, date, author, text, weiboVedio, weiboPic)
        weiboList.append(weibo)
    time.sleep(10)

f = open("content.csv", "w+", encoding="utf-8")
csvWiter = csv.writer(f)
csvWiter.writerow(["该条微博的id", "发布日期", "微博的作者id", "微博内容", "微博内的视频", "微博内的图片"])
for weibo in weiboList:
    csvWiter.writerow([weibo.id, weibo.date, weibo.author, weibo.content, weibo.weiboVedio, weibo.weiboPic])
f.close()
