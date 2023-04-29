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
    with open("News/newst.txt","w") as nw:
        news_url = 'https://www.indycar.com/News'
        page_news = re.get(news_url)
        soup = BeautifulSoup(page_news.content,'html5lib')
        news_card = soup.find_all('li', class_ = 'media-grid-module__media-item')
        for num,card in enumerate(news_card):
            title = (card.find(class_ = 'media-grid-module__secondary-heading').text).replace("\n","").rstrip(" ").lstrip(" ")
            pic = card.find('img')['src']
            nw.write(f"{title},{pic}\n")
            if num == 14:break
    nw.close()

def indy_driver_standings():
    with open("Standings/drivers.txt", "w") as dw:
        drivers_url = 'https://www.indycar.com/Drivers'
        drivers_page = re.get(drivers_url)
        soup = BeautifulSoup(drivers_page.content, 'html5lib')
        driver_card = soup.find_all('div',class_ = 'driver-listing__driver-profile')
        for rank,card in enumerate(driver_card,1):
            pic = card.find('img')["src"]
            name = card.find(class_ = 'secondary-heading').text.replace("\n","").lstrip(" ").rstrip(" ").replace("                                \xa0"," ")
            team = card.find(class_ = 'tertiary-heading').text.replace("\n"," ").lstrip(" ").rstrip(" ")
            points = card.find_all("span",class_ = 'number')[1].text
            dw.write(f"{rank},{name},{points},{pic},{team}\n")

    dw.close()

def indy_calendar():
    with open("Calendar/race_schedule.txt","w") as rs:
        schedule_url = 'https://www.indycar.com/Schedule'
        schedule_page = re.get(schedule_url)
        soup = BeautifulSoup(schedule_page.content,'html5lib')
        race_card = soup.find_all('li',class_ = 'schedule-list__item')
        for card in race_card:
            pic = [pics["src"] for num,pics in enumerate(card.find_all('img')) if num<2]
    ## incomplete

    rs.close()

indy_calendar()