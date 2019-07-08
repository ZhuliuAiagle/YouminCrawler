# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import io  
import sys
import re
from zhon.hanzi import punctuation
import pymongo
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')


# info_dict = {
#   'name':'',
#   'detail_link':'',
#   'img':'',
#   'rate': <Double>
# }




# 爬取对应游戏的评分：测试用


gamelist =  ["黑暗之魂3","塞尔达传说：荒野之息","英雄联盟",\
    "刺客信条：大革命","星露谷物语","血源","只狼：影逝二度","鬼泣5",\
        "刺客信条：奥德赛","上古卷轴5：天际","赛博朋克2077","超级马里奥：奥德赛",\
            "文明6","APEX英雄"] # 测试用

url = "http://so.gamersky.com/all/ku?s="


for real_name in gamelist:

    # 存储游戏信息的字典
    info_dict = {}

    res = requests.get(url + real_name)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"html.parser")
    myAttrs = {'class':'ImgY'}
    innerAttrs = {'class': 't1'}
    platforms = {'class':'t2'}


    if(len(soup.findAll('ul', attrs=myAttrs )) > 0):
        # print(soup.findAll('ul', attrs=myAttrs )[0])
        s_result = soup.findAll('ul', attrs=myAttrs)[0]
        if(len(s_result.findAll('li')) > 0):
            # 匹配最好的一个
            best_result = s_result.findAll('li')[0]
            rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
            for result in s_result.findAll('li'):
                t_title = result.find('a').find('img')['title']
                # 去除所有双字节特殊符号
                t_title = rule.sub("",t_title)
                real_name = rule.sub("", real_name)
                if(t_title == real_name):
                    best_result = result
                    break
            info_dict['eigenvalue'] = rule.sub("", real_name)
            detail_link = best_result.find('a')['href']
            detail_name = best_result.find('a').find('img')['title']
            img = best_result.find('a').find('img')['src']
            # 数据存入字典
            info_dict['name'] = detail_name
            info_dict['detail_link'] = detail_link
            info_dict['img'] = img
            # 获取到了名称与详细链接
            #访问该详细链接
            res2 = requests.get(detail_link)
            res2.encoding = 'utf-8'
            soup = BeautifulSoup(res2.text, "html.parser")
            ul = soup.findAll('ul',attrs={'class':'Bimg'})[0]
            if(len(ul.findAll('span',attrs=innerAttrs)) > 0):
                t = ul.findAll('a')
                li = []
                for k in t:
                    i = k.find('span',attrs={'class':'t1'})
                    j = k.find('span',attrs={'class':'t2'})
                    it = {}
                    at_1 = i.find('em').string
                    at_2 = i.find('i').string
                    at_3 = j.text
                    it["real_score"] = float(at_1)
                    it["full_score"] = float(at_2[1:])
                    it["website"] = at_3
                    li.append(it)
                # 机构评分
                info_dict['score'] = li
        else:
            print("No corresponding result")

    else:
        print("No corresponding result")

    print(json.dumps(info_dict,indent=1,ensure_ascii=False))
    print("")
    myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
    mydb = myclient['game']
    mycollection = mydb['rate_test']
    x = mycollection.insert_one(info_dict)
