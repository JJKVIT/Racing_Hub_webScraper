import requests as re
from datetime import date,datetime
from bs4 import BeautifulSoup
import json
import pytz
from urllib.request import urlopen
import threading
import time
#import alive_progress as ap

def indy_news():
    # include IndyCar/ after completion to the file path
    with open("News/news","w") as nw:
        news_list = []
        news_url = 'https://www.indycar.com/News'
        page_news = re.get(news_url)
        soup = BeautifulSoup(page_news.content,'html5lib')
        news_card = soup.find_all('li', class_ = 'media-grid-module__media-item')
        for num,card in enumerate(news_card):
            title = (card.find(class_ = 'media-grid-module__secondary-heading').text).replace("\n","").rstrip(" ").lstrip(" ")
            pic = "https://www.indycar.com/"+card.find('img')['src']
            nw.write(f"{title},{pic}\n")
            if num == 14:break
    nw.close()

def indy_driver_standings():
    pass