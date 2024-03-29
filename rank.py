import requests
import io
import sys
from bs4 import BeautifulSoup
from selenium import webdriver
import pymongo
import time

def url(year):
    return "http://ku.gamersky.com/sp/0-0-" + year + "-0-0-0.html"

years = ['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005']
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
myclient = pymongo.MongoClient('mongodb://139.155.103.174:27017/')
mydb = myclient['game_backup']
this_collection = mydb['famous_game_new']

for year in years:
    driver = webdriver.PhantomJS()
    driver.get(url(year))
    time.sleep(5)
    gamelist = driver.find_elements_by_class_name("gamelist")
    for game in gamelist:
        game_name = game.find_element_by_tag_name('p').text
        link = game.find_element_by_tag_name('a').get_attribute('href')
        driver.get(link)
        game_name_zh = driver.find_element_by_class_name('tit_CH').text
        game_name_en = driver.find_element_by_class_name('tit_EN').text
        game_id = driver.find_element_by_class_name('tit_CH').get_attribute('gameid')
        img = game.find_element_by_tag_name('a').find_element_by_tag_name('img').get_attribute('src')
        user_score = 0.0
        try:
            user_score = float(game.find_element_by_class_name('num').text)
        except:
            print("a no score error occur, ",year,game_name)
            pass
        this_collection.insert_one({'cnName':game_name_zh,'enName': game_name_en, 'gameId': game_id, 'year':year,'link':link, 'img':img, 'user_score':user_score})
    # 找到下一页按钮进行点击
    try:
        driver.find_element_by_class_name("nexe").click()
    except Exception:
        print("a page error occur, ",year)
        time.sleep(5)
        driver.find_element_by_class_name("nexe").click()
        time.sleep(5)
    gamelist = driver.find_elements_by_class_name("gamelist")
    for game in gamelist:
        game_name = game.find_element_by_tag_name('p').text
        link = game.find_element_by_tag_name('a').get_attribute('href')
        driver.get(link)
        game_name_zh = driver.find_element_by_class_name('tit_CH').text
        game_name_en = driver.find_element_by_class_name('tit_EN').text
        game_id = driver.find_element_by_class_name('tit_CH').get_attribute('gameid')
        img = game.find_element_by_tag_name('a').find_element_by_tag_name('img').get_attribute('src')
        user_score = 0.0
        try:
            user_score = float(game.find_element_by_class_name('num').text)
        except:
            print("a no score error occur, ",year,game_name)
            pass
        this_collection.insert_one({'cnName':game_name_zh,'enName': game_name_en, 'gameId': game_id, 'year':year,'link':link, 'img':img, 'user_score':user_score})
    try:
        driver.find_element_by_class_name("nexe").click()
    except Exception:
        print("a page error occur, ",year)
        time.sleep(5)
        driver.find_element_by_class_name("nexe").click()
        time.sleep(5)
    gamelist = driver.find_elements_by_class_name("gamelist")
    for game in gamelist:
        game_name = game.find_element_by_tag_name('p').text
        link = game.find_element_by_tag_name('a').get_attribute('href')
        driver.get(link)
        game_name_zh = driver.find_element_by_class_name('tit_CH').text
        game_name_en = driver.find_element_by_class_name('tit_EN').text
        game_id = driver.find_element_by_class_name('tit_CH').get_attribute('gameid')
        img = game.find_element_by_tag_name('a').find_element_by_tag_name('img').get_attribute('src')
        user_score = 0.0
        try:
            user_score = float(game.find_element_by_class_name('num').text)
        except:
            print("a no score error occur, ",year,game_name)
            pass
        this_collection.insert_one({'cnName':game_name_zh,'enName': game_name_en, 'gameId': game_id, 'year':year,'link':link, 'img':img, 'user_score':user_score})
    
    

