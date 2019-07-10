import pymongo
import requests
from bs4 import BeautifulSoup

myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
mydb = myclient['game']
mycollection = mydb['famous_game']
this_collection = mydb['youmin_score']
for game in mycollection.find().batch_size(500):
    game_name = game['name']
    year = game['year']
    detail_link = game['link']
    img = game['img']
    info_dict = {}
    info_dict['name'] = game_name
    info_dict['year'] = year
    info_dict['link'] = detail_link
    info_dict['img'] = img
    res2 = requests.get(detail_link)
    res2.encoding = 'utf-8'
    soup = BeautifulSoup(res2.text, "html.parser")
    if(len(soup.findAll('ul',attrs={'class':'Bimg'})) <= 0):
        this_collection.insert_one(info_dict)
        continue
    ul = soup.findAll('ul',attrs={'class':'Bimg'})[0]
    if(len(ul.findAll('span',attrs={'class':'t1'})) > 0):
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
    this_collection.insert_one(info_dict)
print("finished")


