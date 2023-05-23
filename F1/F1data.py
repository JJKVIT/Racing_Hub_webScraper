import requests as re
from datetime import date,datetime
from bs4 import BeautifulSoup
import json
import pytz
from urllib.request import urlopen
import threading
import time
#import alive_progress as ap

years = str(date.today())[0:4]

lon_lat_url = 'http://ipinfo.io/json'
data = str(json.load(urlopen(lon_lat_url))['loc'])
request_data = data.split(",")
response = re.get(f"https://timeapi.io/api/Time/current/coordinate?latitude={request_data[0]}&longitude={request_data[1]}")
user_timezone = response.json()['timeZone']

base_url = "https://www.formula1.com/"

calendar_url = f"https://www.formula1.com/en/racing/{years}.html"

standing_drivers=f"https://www.formula1.com/en/results.html/{years}/drivers.html"

standing_teams = f"https://www.formula1.com/en/results.html/{years}/team.html"

# seperating the html code of the base url to title and pictures

def landingpage():
    with open("F1/Landing page/Card 1/list 1.json","w",encoding="utf-8") as c1:
        with open("F1/Landing page/Card 2/list 2.json","w",encoding="utf-8") as c2:
            with open("F1/Landing page/Card 3/list 3.json","w",encoding="utf-8") as c3:
                c1_dict = {}
                c2_dict = {}
                c3_dict = {}

                page = re.get(base_url)
                soup = BeautifulSoup(page.content, "html5lib")


                # f1-homepage--hero is the class containing the main articles
                Card_1 = soup.find(class_="f1-homepage--hero")
                # f1-race-hub--latest is the class containing the editor picks articles
                Card_2 = soup.find(class_="f1-race-hub--latest")
                # collection-preview is the class containing the more news articles
                Card_3 = soup.find(class_="collection-preview")


                # main title card in the webpage
                main_title_card = Card_1.find(class_ ="col-lg-6 left-col")
                main_title_pic = main_title_card.find(class_ = "lazy")['data-src']
                main_title = main_title_card.find(class_ = "f1--title" ).text
                c1_dict["0"] = {"title":main_title,"pic":main_title_pic}

                # rest of card 1 articles
                side_articles_card = Card_1.find(class_ ="col-lg-6 right-col")
                side_articles_list = side_articles_card.find_all('div',class_ = "col-6")

                # seperating the pictures and titles and adding to the Card 1 list
                for num,article in enumerate(side_articles_list,1):
                    title = article.find(class_ = 'f1--s no-margin').text
                    pic = article.find(class_ = 'lazy')['data-src']
                    c1_dict[str(num)] = {"title":title,"pic":pic}
                c1.write(json.dumps(c1_dict, ensure_ascii=False))
                ############END OF CARD 1 PICTURES AND TITLES#############


                #Card 2 parts are divided into 2 a video loop which won't be used(maybe added on later) and atricles
                card_2_parts = Card_2.find_all('div',class_ = 'col-lg-6 col-md-12')

                #first part contains videos in a loop which will not be used
                card_2_articles = card_2_parts[1].find_all('div',class_ = 'col-md-6 col-sm-12')

                for num,article in enumerate(card_2_articles):
                    title = article.find(class_ = 'no-margin').text
                    # some articles don't have pictures
                    try:
                        pic = article.find(class_ = 'lazy')['data-src']
                    except:
                        pic = article.find(class_ = 'lazy')
                    c2_dict[str(num)] = {"title":title,"pic":pic}
                c2.write(json.dumps(c2_dict,ensure_ascii=False))

                #########END OF CARD 2 PICTURES AND TITLES################



                #Card 3 Articles
                card_3_articles = Card_3.find_all('div',class_ = 'f1-latest-listing--grid-item col-md-6 col-xl-3')
                for num,article in enumerate(card_3_articles):
                    title = article.find(class_ = 'no-margin').text
                    pic = article.find(class_ = 'lazy')['data-src']
                    c3_dict[str(num)] = {"title": title,"pic": pic}
                c3.write(json.dumps(c3_dict,ensure_ascii=False))
    c3.close()
    c2.close()
    c1.close()

def race_calendar():
    # complcations in scapring hero event completion at last
    with open("F1/Race Calender/Races.json","w",encoding="utf-8") as R_C:

        page2 = re.get(calendar_url)
        soup = BeautifulSoup(page2.content,'html5lib')

        out_dict = {}
        race_cards = soup.find_all('div',class_ ="col-12 col-sm-6 col-lg-4 col-xl-3")
        hero_race_script = str(soup.find_all('script')[0])
        hero_race_json = hero_race_script[35:len(hero_race_script)-10]
        json_data = json.loads(hero_race_json)
        hero_race_name = json_data["name"]
        hero_race_link = json_data["@id"]
        for num,card in enumerate(race_cards):
            round = card.find(class_ = 'card-title f1-uppercase f1-color--warmRed').text

            date = [card.find(class_ = 'start-date').text,card.find(class_ = 'end-date').text]

            try:
                month = card.find(class_ = 'month-wrapper').text
            except:
                month = "Current race"
            event_details = card.find(class_ = 'event-details')

            event_location = (event_details.find(class_ = 'event-place').text)[0:-1]
            event_title = (event_details.find(class_ = 'event-title f1--xxs').text).rstrip(' ')

            event_pic = event_details.find_all('img', class_="lazy")
            pic_list = [pic['data-src'] for pic in event_pic]
            pic_list.append(card.find(class_='lazy')['data-src'])

            # opening the upcoming races page to obtain all the race events
            if event_title == hero_race_name:
                hero_page = re.get(hero_race_link)
                soup_hero = BeautifulSoup(hero_page.content,'html5lib')
                scripts = ((str(soup_hero.find_all('script')[0]))[35::])[0:-10]
                cards = json.loads(scripts)['subEvent']
                sub_title_list = []
                for card in cards:
                    title = card['name'][0:-24]
                    time_date = [card['startDate'],card['endDate']]
                    for time in time_date:
                        time_str = (str(time).replace("T"," ")).replace("Z","")
                        datetime_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                        current_timezone = pytz.timezone('Zulu')
                        target_timezone = pytz.timezone(f"{user_timezone}")
                        localized_time = current_timezone.localize(datetime_object)
                        datetime_user = localized_time.astimezone(target_timezone)
                        time_date[time_date.index(time)] = str(datetime_user.replace(tzinfo=None))

                    sub_title_list.append([title,time_date])
                out_dict[str(num)] = {"status":"upcoming","round":round,"loc":event_location,"title":event_title,"sub":sub_title_list,"pic":pic_list}
                print(out_dict)
                continue
            if ("#39" in hero_race_name) and (event_title.split("'")[0] == hero_race_name.split(";")[0][0:-4]):
                out_dict[str(num)] = {"status": "Cancelled", "round": round, "loc": event_location, "title": event_title,"date": date, "month": month, "pic": pic_list}
                continue
            out_dict[str(num)] = {"status":"None","round":round,"loc":event_location,"title":event_title,"date":date,"month":month,"pic":pic_list}
                # data for each event has been scraped ,, time conversion remaining
        ## Hero race identified => next find the timings for each event in the hero race ##
        R_C.write(json.dumps(out_dict,ensure_ascii=False))

    R_C.close()

def driver_standings():
    with open("F1/Standings/drivers.json","w",encoding="utf-8") as drivers_standings:
        page3 = re.get(standing_drivers)
        soup = BeautifulSoup(page3.content,'html5lib')

        table = soup.find(class_ = 'table-wrap')

        standings = table.find_all('td',class_ = 'dark')

        name_first = table.find_all('span',class_ = 'hide-for-tablet')
        name_second = table.find_all('span',class_ = 'hide-for-mobile')
        name_list = [str((name_first)[i].text)+" "+str((name_second)[i].text) for i in range(len(name_first))]
        out_dict = {}

        teams = table.find_all('a',class_ = 'grey semi-bold uppercase ArchiveLink')
        team_list = [team.text for team in teams]

        templist = []
        standing = []
        i = 0
        for x,char in enumerate(standings):
            templist.append(char)
            if (x+1)%3 == 0:
                standing.append(templist)
                out_dict[str(i)] = {"pos":templist[0].text,"name":templist[1].text,"team":team_list[i],"point": templist[2].text}
                templist = []
                x = 0
                i += 1
        drivers_standings.write(json.dumps(out_dict,ensure_ascii=False))

    drivers_standings.close()

def team_standings():
    with open('F1/Standings/team.json','w',encoding="utf-8") as teams:
        page4 = re.get(standing_teams)
        soup = BeautifulSoup(page4.content,'html5lib')

        points = soup.find_all('td', class_='dark')
        point_list = [points[i].text for i in range(1, len(points), 2)]

        team_name = soup.find_all('a',class_="dark bold uppercase ArchiveLink")
        team_name_list = [team.text for team in team_name]
        out_dict = {}
        team_point_pairing = dict(zip(team_name_list,point_list))
        for i,team in enumerate(team_name_list):
            out_dict[str(i)] = {"team": team,"point": team_point_pairing[team]}
        teams.write(json.dumps(out_dict,ensure_ascii=False))
    teams.close()

# function to run all the functions using multithreading
def run_F1_multi():
    # attempting multithreading to increase speed
    t1 = threading.Thread(target=landingpage, name='t1')
    t2 = threading.Thread(target=race_calendar, name='t2')
    t3 = threading.Thread(target=driver_standings, name='t3')
    t4 = threading.Thread(target=team_standings, name='t4')

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
