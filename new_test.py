import pymongo
import requests
from bs4 import BeautifulSoup
import time

myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
mydb = myclient['game']
mycollection = mydb['famous_game_new']
thatdb = myclient['game']
this_collection = thatdb['youminScoreNew']
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
    info_dict['userScore'] = game['user_score']
    res2 = ""
    try:
        res2 = requests.get(detail_link)
        res2.encoding = 'utf-8'
    except:
        print("Banned by remote server. stop 10s.")
        time.sleep(10)
        res2 = requests.get(detail_link)
        res2.encoding = 'utf-8'
    soup = BeautifulSoup(res2.text, "html.parser")
    if(len(soup.findAll('div',attrs={'class':'tit_CH'})) > 0):
        cnFullName = soup.findAll('div',attrs={'class':'tit_CH'})[0].string
        enFullName = soup.findAll('div',attrs={'class':'tit_EN'})[0].string
        gameId = soup.findAll('div',attrs={'class':'tit_CH'})[0].attrs['gameid']
        info_dict['cnFullName'] = cnFullName
        info_dict['enFullName'] = enFullName
        info_dict['gameId'] = gameId
    if(len(soup.findAll('ul',attrs={'class':'Bimg'})) <= 0):
        this_collection.insert_one(info_dict)
        continue
    ul = soup.findAll('ul',attrs={'class':'Bimg'})[0]
    if(len(ul.findAll('span',attrs={'class':'t1'})) > 0):
        t = ul.findAll('a')
        li = []
        for k in t:
            text = str(k.attrs['data-txt'])
            if(text == None):
                text = ""
            else:
                text = text.strip()
                text = text[3:-4]
            i = k.find('span',attrs={'class':'t1'})
            j = k.find('span',attrs={'class':'t2'})
            it = {}
            at_1 = i.find('em').string
            at_2 = i.find('i').string
            at_3 = j.text
            it["real_score"] = float(at_1)
            it["full_score"] = float(at_2[1:])
            it["website"] = at_3
            it["comment"] = text
            li.append(it)
        # 机构评分
        info_dict['score'] = li
    if(len(soup.findAll('div', attrs={'class':'Slidepic'})) > 0):
        comp_li = []
        compete_list = soup.findAll('div', attrs={'class':'Slidepic'})[0]
        compete_list = compete_list.findAll('li')
        for i in compete_list:
            comp_di = {}
            link = i.find('a').attrs['href']
            img = i.find('img').attrs['src']
            name = i.find('p').string
            comp_di['link'] = link
            comp_di['img']  = img
            comp_di['name'] = name
            comp_li.append(comp_di)
        info_dict['competitorInfo'] = comp_li
    this_collection.insert_one(info_dict)
print("finished")

