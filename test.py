import pymongo
import re
import io
import sys
import requests
from bs4 import BeautifulSoup
import json

myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
mydb = myclient['game_backup']
mycollection = mydb['game']
this_collection = mydb['youmin_data']


count = 0
count_result = 0
count_score = 0
good_game = 0
url = "http://so.gamersky.com/all/ku?s="
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
for content in mycollection.find().batch_size(500):
    count += 1
    # 存储游戏信息的字典
    real_name = content['name']
    # 如果游戏名称是空的
    if(('name' not in content.keys()) or len(content['name']) <= 0):
        continue
    info_dict = {}
    # 特征值，选择是用谁的
    eigen = rule.sub("", real_name)
    # 可以选择用特征值搜，也可以用真实名字搜
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
            count_result += 1
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
                if(len(li) >= 7):
                    good_game += 1
                # 机构评分
                info_dict['score'] = li
                count_score += 1
        else:
            continue

    else:
        continue
    # print(json.dumps(info_dict,indent=1,ensure_ascii=False))
    # print("")
    # mycollection.update_one({'_id':content['_id']},{'$set':{ 'youmin_info' : info_dict }})
    this_collection.insert_one(info_dict)
    if( count % 100 == 0 ):
        print(str(good_game), "/" ,str(count_score) , "/" + str(count_result) , "/" , str(count))