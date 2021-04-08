import requests
import json
import re
import time
import random


class People:
    id = "",
    name = ""
    level = ""

    def __init__(self, id, name, level):
        self.id = id
        self.name = name
        self.level = str(level)

    def getJson(self):
        return {"id": self.id, "name": self.name, "symbolSize": "10", "level": self.level}


class Link:
    sourceId = "",
    targetId = ""

    def __init__(self, sourceId, targetId):
        self.sourceId = sourceId
        self.targetId = targetId

    def getJson(self):
        return {"source": self.sourceId, "target": self.targetId}


class PreLink:
    sourceName = "",
    targetId = ""

    def __init__(self, sourceName, targetId):
        self.sourceName = sourceName
        self.targetId = targetId

    def isSource(self, name):
        return self.sourceName == name


def getMonth(month):
    if month == "Apr":
        return "4"
    else:
        if month == "Mar":
            return "3"
        else:
            print(month)
            return "2"


def getIdByName(name, headers):
    if name == "":
        print("name error")
        return "-1"
    else:
        try:
            url = 'https://m.weibo.cn/n/{}'.format(name)
            response = requests.head(url).headers
            return response['location'].replace('/u/', '')
        except:
            url = 'https://m.weibo.cn/api/container/getIndex'
            params = {
                'containerid': '100103type=3&q={}'.format(name),
                'page_type': 'searchall'
            }
            response = requests.get(url, headers=random.choice(headers), params=params)
            print(response.text)
            while response.status_code != 200:
                time.sleep(3*60)
                response = requests.get(url, headers=random.choice(headers), params=params)
            response_json = json.loads(response.text)
            times = 0
            while response_json['ok'] != 1:
                times += 1
                if times > 1:
                    break
                time.sleep(3 * 60)
                response = requests.get(url, headers=random.choice(headers), params=params)
                print(response.text)
                response_json = json.loads(response.text)
            if times > 1:
                return name
            id = response_json['data']['cards'][1]['card_group'][0]['user']['id']
            return str(id)


def getOnePage(response_json, peopleList, links, newsid, preLinks, levelList, peopleIdList, repostTime_dict):
    datas = response_json['data']['data']
    repeat = 0
    for data in datas:
        id = str(data['user']['id'])
        if id not in peopleIdList:
            repostTime_date = data['created_at']
            repostTime_dates = repostTime_date.split(" ")
            repostYear = repostTime_dates[5]
            repostMonth = getMonth(repostTime_dates[1])
            repostDay = repostTime_dates[2]
            repostDate = "{}年{}月{}日".format(repostYear, repostMonth, repostDay)
            print(repostDate)
            peopleIdList.append(id)
            name = data['user']['screen_name']
            content = data['raw_text']
            print(data['raw_text'])
            for preLink in preLinks:
                if preLink.isSource(name):
                    link = Link(id, preLink.targetId)
                    links.append(link)
                    preLinks.remove(preLink)
            content = content.replace("：", ":")
            items = re.findall('//@(.*?):', content)
            if items:
                if len(items) > 5:
                    continue
                if repostDate in repostTime_dict.keys():
                    repostTime_dict[repostDate] += 1
                    print(repostTime_dict[repostDate])
                else:
                    repostTime_dict[repostDate] = 1
                    print("新添加主键:{}".format(repostDate))
                levelList[len(items)] = str(int(levelList[len(items)]) + 1)
                print("该用户等级为" + str(len(items) + 1))
                item = items[0]
                print(items)
                preLinks.append(PreLink(item, id))
                people = People(id, name, len(items)+1)
            else:
                links.append(Link(str(newsid), id))
                levelList[0] = str(int(levelList[0]) + 1)
                print("该用户等级为1")
                if repostDate in repostTime_dict.keys():
                    repostTime_dict[repostDate] += 1
                else:
                    repostTime_dict[repostDate] = 1
                people = People(id, name, 1)
            peopleList.append(people)
        else:
            repeat += 1
    if repeat == len(datas):
        return False
    else:
        return True


def getOneNew(weibo_id, name, peopleList, links, newsid, news, levelList, peopleIdList, repostTime_dict):
    url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page=1'.format(weibo_id)
    headers = [{
        'Cookie': '_ALF=1619262243; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAY98g1joNY2swIl9kLiAo5-zI2ASFjCWqgIRLQSsv6G6g.; SUB=_2A25NWB5zDeRhGeBI6loT8i3JzjqIHXVuoqI7rDV6PUJbktAfLWbzkW1NRot20TO5flZgAj7zP-QE9XwazxZCo31m; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt; _T_WM=19725237635; XSRF-TOKEN=b4c3bf; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D231522type%253D1%2526t%253D10%2526q%253D%2523%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592%25E7%2596%25AB%25E8%258B%2597%25E5%2585%25A8%25E6%25B0%2591%25E5%2585%258D%25E8%25B4%25B9%2523%26uicode%3D20000061%26fid%3D4588175568407059%26oid%3D4588175568407059',
        'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 86.0) Gecko / 20100101Firefox / 86.0'
    },
        {
            'Cookie': 'ALF=1619892355; SCF=AvS6HupuL_1KkWxlafVcVyhPIZaKxVangJBjtREdcgAYeJh7yvZ_pH_j9WuN4KYNdG87Bruc4OM8Y-BvbQO6foY.; _T_WM=80943054270; SUB=_2A25NYnvTDeRhGeBI6loT8i3JzjqIHXVurQWbrDV6PUJbktAKLVrZkW1NRot20RT5Hy1aMc_Uvg5hVAlPDOfknaTl; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WheurEb4cKqvylaRF0NMCmz5JpX5K-hUgL.FoqceKnEeoefSKq2dJLoI7RLxKnLB.qLBoM4ShM4e5tt; XSRF-TOKEN=0867fa; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592',
            'User-Agent': 'Mozilla / 5.0(Windows NT 10.0;Win64;x64;rv: 86.0) Gecko / 20100101Firefox / 86.0'
        },
        {
            'Cookie': '_T_WM=51445041497; WEIBOCN_FROM=1110006030; XSRF-TOKEN=91e8c6; loginScene=102003; SUB=_2A25NYgq1DeRhGeFL41YX-SjFyjmIHXVurJb9rDV6PUJbktAfLWvmkW1NfY0erHDa4_j2145zQOi2WiFiivFmFXHw; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5LgfZD7w4Azw1IZam6GTM15JpX5KzhUgL.FoMf1hBc1Kq4eK-2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNSKnXSo.c1K2f; SSOLoginState=1617328869; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4620459935269257%26luicode%3D10000011%26lfid%3D100103type%253D1%2526q%253D%25E6%2596%25B0%25E5%2586%25A0%25E7%2597%2585%25E6%25AF%2592; BAIDU_SSP_lcr=https://login.sina.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
        }]
    preLinks = []
    response = requests.get(url, headers=random.choice(headers))
    response_json = json.loads(response.text)
    while response_json['ok'] != 1:
        print("出错了")
        print(response_json)
        time.sleep(3 * 60)
        response = requests.get(url, headers=random.choice(headers))
        response_json = json.loads(response.text)
    max = response_json['data']['max']
    print(max)
    getOnePage(response_json, peopleList, links, newsid, preLinks, levelList, peopleIdList, repostTime_dict)
    i = 2
    while i < max + 1:
        try:
            url = 'https://m.weibo.cn/api/statuses/repostTimeline?id={}&page={}'.format(weibo_id, i)
            response = requests.get(url, headers=random.choice(headers))
            if response.status_code != 200:
                time.sleep(3 * 60)
                i -= 1
                continue
            response_json = json.loads(response.text)
            # print(response_json)
            max = response_json['data']['max']
            if getOnePage(response_json, peopleList, links, newsid, preLinks, levelList, peopleIdList, repostTime_dict):
                print("共{}页".format(max))
                print("第{}页爬取完成".format(i))
            else:
                print("后面均已爬取")
                break
        except:
            print(response_json)
            print("有一个页面出现错误：第{}页".format(i))
        i += 1
        time.sleep(3)
    nonPeople = []
    nonPeopleId = []
    print(len(preLinks))
    for preLink in preLinks:
        print(preLink.sourceName)
        print(preLink.targetId)
        if preLink.sourceName not in nonPeople:
            print(preLink.sourceName)
            print(nonPeople)
            j = getIdByName(preLink.sourceName, headers)
            print(j)
            nonPeopleId.append(j)
            nonPeople.append(preLink.sourceName)
            if j not in peopleIdList:
                print("新出现的人")
                peopleIdList.append(j)
                people = People(j, preLink.sourceName, 1)
                peopleList.append(people)
                levelList[0] = str(int(levelList[0]) + 1)
                links.append(Link(str(newsid), j))
        else:
            j = nonPeopleId[nonPeople.index(preLink.sourceName)]
        print(j)
        links.append(Link(j, preLink.targetId))
    print(len(preLinks))
    news.append({"name": name, "url": "https://m.weibo.cn/detail/{}".format(weibo_id)})
    return True


def getPreData(repostTime_dict, levelList):
    level_f = open("level.json", "r+", encoding="utf-8")
    level_content = level_f.read()
    if not level_content == "":
        level_json = json.loads(level_content)
        levelList[0] = level_json['1']
        levelList[1] = level_json['2']
        levelList[2] = level_json['3']
        levelList[3] = level_json['4']
        levelList[4] = level_json['5']
        levelList[5] = level_json['6']
    level_f.close()
    startDate_f = open("repostSum.json", "r+", encoding="utf-8")
    startDate = startDate_f.read()
    if not startDate == "":
        startDate_json = json.loads(startDate)
        startDate_time = startDate_json['Date']
        startDate_sum = startDate_json['data']
        for i in range(0, len(startDate_time)):
            repostTime_dict[startDate_time[i]] = startDate_sum[i]
    startDate_f.close()


def getOnePreDate(peopleList, links, peopleIdList, newsId):
    peopleList.clear()
    links.clear()
    peopleIdList.clear()
    id_f = open("newsSpread{}.json".format(newsId), "r+", encoding="utf-8")
    newsSpread = id_f.read()
    if not newsSpread == "":
        newsSpread_json = json.loads(newsSpread)
        nodes = newsSpread_json['nodes']
        for node in nodes:
            one_id = node['id']
            one_name = node['name']
            one_level = node['level']
            peopleIdList.append(one_id)
            peopleList.append(People(one_id, one_name, one_level))
        startLinks = newsSpread_json['links']
        for startLink in startLinks:
            links.append(Link(startLink['source'], startLink['target']))
    id_f.close()


def writeToFile(levels, repost_dict):
    level_Json = {
        "1": str(levels[0]),
        "2": str(levels[1]),
        "3": str(levels[2]),
        "4": str(levels[3]),
        "5": str(levels[4]),
        "6": str(levels[5])
    }
    level_f = open('level.json', 'w+', encoding='utf-8')
    level_f.write(json.dumps(level_Json, ensure_ascii=False))
    level_f.close()
    repostDate_f = open('repostSum.json', 'w+', encoding='utf-8')
    keys = []
    values = []
    for key in repost_dict:
        keys.append(str(key))
        values.append(repost_dict[key])
    repostDate = {
        "Date": keys,
        "data": values
    }
    repostDate_f.write(json.dumps(repostDate, ensure_ascii=False))
    repostDate_f.close()


def writeOneToFile(peopleList, links, newsId):
    peopleJsonList = []
    linkJsonList = []
    for people in peopleList:
        peopleJsonList.append(people.getJson())
    for link in links:
        linkJsonList.append(link.getJson())
    total_json = {
        "nodes": peopleJsonList,
        "links": linkJsonList
    }
    f = open('newsSpread{}.json'.format(newsId), 'w+', encoding='utf-8')
    f.write(json.dumps(total_json, ensure_ascii=False))
    f.close()


if __name__ == '__main__':
    weiboList = [
        {
            "id": 4620578218577363,
            "name": "华南海鲜市场不是新冠疫情最初来源"
        },
        {
            "id": 4620219815037861,
            "name": "李梓萌不由自主把打疫苗标语唱了出来"
        },
        {
            "id": 4621235869452542,
            "name": "建议60岁及以上人群接种新冠疫苗"
        },
        {
            "id": 4621074911988625,
            "name": "为什么应尽快接种新冠疫苗"
        },
        {
            "id": 4620749769540859,
            "name": "哪些人不能打新冠疫苗"
        }
    ]
    repostTime_dict = {}
    peopleList = []
    links = []
    news = []
    peopleIdList = []
    levelList = [0, 0, 0, 0, 0, 0]
    getPreData(repostTime_dict, levelList)
    newsid = 0
    for weibo in weiboList:
        print(weiboList.index(weibo))
        getOnePreDate(peopleList, links, peopleIdList, newsid)
        getOneNew(weibo['id'], weibo['name'], peopleList, links, newsid, news, levelList, peopleIdList, repostTime_dict)
        writeOneToFile(peopleList, links, newsid)
        newsid += 1
    print(repostTime_dict)
    writeToFile(levelList, repostTime_dict)
