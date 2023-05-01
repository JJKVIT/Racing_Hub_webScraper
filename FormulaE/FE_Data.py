import requests as re
from datetime import date,datetime
from bs4 import BeautifulSoup
import json
import pytz
from urllib.request import urlopen
import threading
import time

def FE_news():
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


def FE_drivers():
    with open('FormulaE/Standings/drivers.txt','w') as FE_d:

        ## json package containing
        page_url = 'https://api.formula-e.pulselive.com/formula-e/v1/standings/drivers?championshipId=bc4a0209-f233-46c8-afce-842d1c48358f&lastNRaces=4'
        request = re.get(page_url).json()
        for driver in request:
            driver_name = f"{driver['driverFirstName']} {driver['driverLastName']}"
            pos = driver['driverPosition']
            points = driver['driverPoints']
            team_id = driver['driverTeamId']
            team_pic = f"https://static-files.formula-e.pulselive.com/badges/{team_id}.svg"
            FE_d.write(f"{pos},{driver_name},{points},{team_pic}\n")

    FE_d.close()

def FE_teams():
    with open('FormulaE/Standings/teams.txt','w') as FE_t:
        page_url = "https://api.formula-e.pulselive.com/formula-e/v1/standings/teams?championshipId=bc4a0209-f233-46c8-afce-842d1c48358f&lastNRaces=4"
        request = re.get(page_url).json()
        for team in request:
            team_name = team['teamName']
            team_pos = team['teamPosition']
            team_points = team['teamPoints']
            team_id = team['teamId']
            team_pic = f"https://static-files.formula-e.pulselive.com/badges/{team_id}.svg"
            FE_t.write(f"{team_pos},{team_name},{team_points},{team_pic}\n")

    FE_t.close()

def FE_calendar():
    with open('FormulaE/Calendar/calendar','w') as FE_c:

        page_url = 'https://api.formula-e.pulselive.com/formula-e/v1/races?championshipId=bc4a0209-f233-46c8-afce-842d1c48358f'
        request = re.get(page_url).json()['races']
        count = 0
        for race in request:
            race_name = race['city']
            race_round = race['sequence']
            race_date = race['date']
            race_finished = race['hasRaceResults']
            if count==0 and race_finished == False:
                count+= 1
                race_schedule_url = ''

            print(race_finished)

    FE_c.close()
