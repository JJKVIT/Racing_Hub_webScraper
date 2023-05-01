import requests as re
from datetime import datetime,timedelta
from bs4 import BeautifulSoup
import json
import pytz
from urllib.request import urlopen
import threading
import time

lon_lat_url = 'http://ipinfo.io/json'
data = str(json.load(urlopen(lon_lat_url))['loc'])
request_data = data.split(",")
response = re.get(f"https://timeapi.io/api/Time/current/coordinate?latitude={request_data[0]}&longitude={request_data[1]}")
user_timezone = response.json()['timeZone']

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
    with open('FormulaE/Calendar/calendar.txt','w') as FE_c:

        event_list = []
        page_url = 'https://api.formula-e.pulselive.com/formula-e/v1/races?championshipId=bc4a0209-f233-46c8-afce-842d1c48358f'
        request = re.get(page_url).json()['races']
        count = 0
        for race in request:
            race_name = race['city']
            race_round = race['sequence']
            race_date = race['date']
            race_finished = race['hasRaceResults']
            race_id = race['id']
            race_country = race['country'].lower()
            race_flag = f"https://static-files.formula-e.pulselive.com/flags/{race_country}.svg"
            if count==0 and race_finished == False:
                count+= 1
                race_schedule_url = f"https://api.formula-e.pulselive.com/formula-e/v1/races/{race_id}/sessions?groupQualifyings=true&onlyActualEvents=true"
                race_request = re.get(race_schedule_url).json()['sessions']
                offset_gmt = race_request[0]['offsetGMT']
                for event in race_request:
                    event_name = event['sessionName']
                    event_date = event['sessionDate']
                    offset_gmt_hrs = int(offset_gmt.split(':')[0])
                    offset_gmt_mins = int(offset_gmt.split(':')[1])
                    time_change = timedelta(hours = offset_gmt_hrs,minutes = offset_gmt_mins)
                    event_start = f"{event['startTime']}:00"
                    event_end = f"{event['finishTime']}:00"

                    event_start_datetime_object = (datetime.strptime(f"{event_date} {event_start}", '%Y-%m-%d %H:%M:%S'))-time_change
                    event_end_datetime_object = (datetime.strptime(f"{event_date} {event_end}", '%Y-%m-%d %H:%M:%S'))-time_change

                    current_timezone = pytz.timezone('UTC')
                    target_timezone = pytz.timezone(f"{user_timezone}")
                    localized_time_start = current_timezone.localize(event_start_datetime_object)
                    datetime_user_start = localized_time_start.astimezone(target_timezone)
                    start_time = str(datetime_user_start.replace(tzinfo=None))

                    localized_time_end = current_timezone.localize(event_end_datetime_object)
                    datetime_user_end = localized_time_end.astimezone(target_timezone)
                    end_time = str(datetime_user_end.replace(tzinfo=None))

                    timing_list = [start_time,end_time]
                    event_list.append([event_name,timing_list])
                FE_c.write(f"{race_finished},{race_round},{race_name},{event_list},{race_flag}\n")
                continue
            FE_c.write(f"{race_finished},{race_round},{race_name},{race_date},{race_flag}\n")

    FE_c.close()

def run_FE_multi():
    # attempting multithreading to increase speed
    t1 = threading.Thread(target=FE_news, name='t1')
    t2 = threading.Thread(target=FE_drivers, name='t2')
    t3 = threading.Thread(target=FE_teams, name='t3')
    t4 = threading.Thread(target=FE_calendar, name='t4')

    #starting threads
    t1.start()
    t2.start()
    t3.start()
    t4.start()

    #joining threads to make sure all tasks are finished
    t1.join()
    t2.join()
    t3.join()
    t4.join()

