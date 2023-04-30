import requests as re
from datetime import date,datetime
from bs4 import BeautifulSoup
import json
import pytz
from urllib.request import urlopen
import threading
import time
#import alive_progress as ap

year = str(date.today())[0:4]

lon_lat_url = 'http://ipinfo.io/json'
data = str(json.load(urlopen(lon_lat_url))['loc'])
request_data = data.split(",")
response = re.get(f"https://timeapi.io/api/Time/current/coordinate?latitude={request_data[0]}&longitude={request_data[1]}")
user_timezone = response.json()['timeZone']

def indy_news():
    # include IndyCar/ after completion to the file path
    with open("IndyNXT/News/news.txt","w") as nw:
        news_url = 'https://www.indycar.com/INDYNXT/News'
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
    with open("IndyNXT/Standings/drivers.txt", "w") as dw:
        drivers_url = 'https://www.indycar.com/INDYNXT/Drivers'
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
    with open("IndyNXT/Calendar/race_schedule.txt","w") as rs:
        schedule_url = 'https://www.indycar.com/INDYNXT/Schedule'
        schedule_page = re.get(schedule_url)
        soup = BeautifulSoup(schedule_page.content,'html5lib')
        race_card = soup.find_all('li',class_ = 'schedule-list__item')
        for card in race_card:
            race_finished = "Upcoming"
            pic = [pics["src"] for num,pics in enumerate(card.find_all('img')) if num<2]
            winner_name_card = card.find(class_ = 'schedule-list__race-winner')
            try:
                winner_name = winner_name_card.find(class_ = 'schedule-list__race-winner-name').text.replace('\n','').lstrip(' ').rstrip(' ').replace('                                                                                            ',' ')
                winner_flag = card.find(class_ = 'schedule-list__race-winner-flag')['src']
                pic.append(winner_flag)
                race_finished = "Finished"
                rs.write(f"{race_finished},{winner_name},{pic}\n")
                continue
            except:
                month_list = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
                month = card.find(class_ = 'schedule-list__date').text.replace('\n','').lstrip(' ').rstrip(' ').replace("                                                                                    ","-")
                race_name = card.find(class_ = "panel-trigger schedule-list__title").text.replace("\n",'').lstrip(' ').rstrip(' ')
                time_est = card.find(class_ = 'timeEst').text[0:-3]
                if time_est[-2::] == 'PM':
                    hr_min = time_est.split(":")
                    hrs = hr_min[0]
                    conv_hrs = str(int(hrs)+11)
                    if conv_hrs == "24":
                        conv_hrs = "00"
                    time_est = f"{conv_hrs}:{hr_min[1][0:-3]}"
                else:
                    time_est = time_est[0:-3]

                month_num = month_list.index(month[0:3])+1
                date_time_conv = f"{year}-{month_num}{month[3::]} {time_est}:00"
                datetime_object = datetime.strptime(date_time_conv,'%Y-%m-%d %H:%M:%S')
                current_timezone = pytz.timezone('EST')
                target_timezone = pytz.timezone(f"{user_timezone}")
                localized_time = current_timezone.localize(datetime_object)
                datetime_user = localized_time.astimezone(target_timezone)
                time_date = str(datetime_user.replace(tzinfo=None))
                brodcasters_card = card.find(class_ = 'schedule-list__broadcast-logos')
                brodcasters = [card['src'] for card in brodcasters_card.find_all("img")]
                rs.write(f"{race_finished},{race_name},{time_date},{brodcasters}\n")
    rs.close()

def run_NXT_multi():
    # attempting multithreading to increase speed
    t1 = threading.Thread(target=indy_news, name='t1')
    t2 = threading.Thread(target=indy_driver_standings, name='t2')
    t3 = threading.Thread(target=indy_calendar, name='t3')

    #starting threads
    t1.start()
    t2.start()
    t3.start()

    #joining threads to make sure all tasks are finished
    t1.join()
    t2.join()
    t3.join()