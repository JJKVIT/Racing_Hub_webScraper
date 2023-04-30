import requests as re
from datetime import date,datetime
from bs4 import BeautifulSoup
import json
import pytz
from urllib.request import urlopen
import threading
import time

def Fe_news():
    with open("FormulaE/News/news.txt",'w') as fe_n:

        news_page = 'https://www.fiaformulae.com/en/news'
        request = re.get(news_page)
        soup = BeautifulSoup(request.content,'html5lib')

        hero_wrapper = soup.find(class_ = 'wrapper news-featured-content')
        hero_title = hero_wrapper.find(class_ ="news-featured-content__title").text.replace('\n','').rstrip(' ').lstrip(' ')
        hero_pic = hero_wrapper.find(class_ = 'hero__media-thumbnail-image js-faded-image fade-in-on-load picture__img')['src']
        fe_n.write(f"{hero_title},{hero_pic}\n")

        latest_news_card = soup.find(class_ = 'news-listing-grid__item-wrapper js-list news-listing-grid__item-wrapper--two-column')
        latest_news_titles = [title.text for title in latest_news_card.find_all('h2',class_ = 'news-item__title')]
        latest_news_pic = [pic['src'] for pic in latest_news_card.find_all('img')]
        latest_news = list(zip(latest_news_titles,latest_news_pic))
        for part in latest_news:
            fe_n.write(f"{part[0]},{part[1]}\n")

        news_cards = soup.find_all('ul',class_ = 'news-listing-grid__item-wrapper js-list')

        analysis_titles = [title.text for title in news_cards[1].find_all('h2',class_ = 'news-item__title')]
        analysis_pics = [pic['src'] for pic in news_cards[1].find_all('img')]
        analysis_news = list(zip(analysis_titles,analysis_pics))
        for part in analysis_news:
            fe_n.write(f"{part[0]},{part[1]}\n")

        race_report_titles = [title.text for title in news_cards[2].find_all('h2',class_ = 'news-item__title')]
        race_report_pics = [pic['src'] for pic in news_cards[2].find_all('img')]
        race_report_news = list(zip(race_report_titles,race_report_pics))
        for part in race_report_news:
            fe_n.write(f"{part[0]},{part[1]}\n")

        ev_tech_titles = [title.text for title in news_cards[3].find_all('h2',class_ = 'news-item__title')]
        ev_tech_pics = [pic['src'] for pic in news_cards[3].find_all('img')]
        ev_tech_news = list(zip(ev_tech_titles,ev_tech_pics))
        for part in ev_tech_news:
            fe_n.write(f"{part[0]},{part[1]}\n")

    fe_n.close()

def Fe_calendar():
    with open('FormulaE/Calendar/races.text',"w") as FE_r:
        page_url = 'https://www.fiaformulae.com/en/races'
        request = re.get(page_url)
        soup = BeautifulSoup(request.content,'html5lib')
        ### unfinished


    FE_r.close()