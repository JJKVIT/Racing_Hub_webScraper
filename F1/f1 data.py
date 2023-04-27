import requests as re
from datetime import date
from bs4 import BeautifulSoup
import json
from time import sleep
#import alive_progress as ap

years = str(date.today())[0:4]

base_url = "https://www.formula1.com/"

calendar_url = f"https://www.formula1.com/en/racing/{years}.html"

standing_drivers=f"https://www.formula1.com/en/results.html/{years}/drivers.html"

standing_teams = f"https://www.formula1.com/en/results.html/{years}/team.html"

# seperating the html code of the base url to title and pictures


with open("Landing page/Card 1/list 1.txt","w") as c1:
    with open("Landing page/Card 2/list 2.txt","w") as c2:
        with open("Landing page/Card 3/list 3.txt","w") as c3:
            Card_1_list = []
            Card_2_list = []
            Card_3_list = []


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
            Card_1_list.append([main_title,main_title_pic])

            # rest of card 1 articles
            side_articles_card = Card_1.find(class_ ="col-lg-6 right-col")
            side_articles_list = side_articles_card.find_all('div',class_ = "col-6")

            # seperating the pictures and titles and adding to the Card 1 list
            for article in side_articles_list:
                title = article.find(class_ = 'f1--s no-margin').text
                pic = article.find(class_ = 'lazy')['data-src']
                c1.write(f"{title}, {pic}\n")

            ############END OF CARD 1 PICTURES AND TITLES#############



            #Card 2 parts are divided into 2 a video loop which won't be used(maybe added on later) and atricles
            card_2_parts = Card_2.find_all('div',class_ = 'col-lg-6 col-md-12')

            #first part contains videos in a loop which will not be used
            card_2_articles = card_2_parts[1].find_all('div',class_ = 'col-md-6 col-sm-12')

            for article in card_2_articles:
                title = article.find(class_ = 'no-margin').text
                # some articles don't have pictures
                try:
                    pic = article.find(class_ = 'lazy')['data-src']
                except:
                    pic = None 
                c2.write(f"{title}, {pic}\n")
            #########END OF CARD 2 PICTURES AND TITLES################



            #Card 3 Articles
            card_3_articles = Card_3.find_all('div',class_ = 'f1-latest-listing--grid-item col-md-6 col-xl-3')
            for article in card_3_articles:
                title = article.find(class_ = 'no-margin').text
                pic = article.find(class_ = 'lazy')['data-src']
                c3.write(f"{title}, {pic}\n")
c3.close()
c2.close()
c1.close()


# complcations in scapring hero event completion at last
with open("Race Calender/Races.txt","w") as R_C:

    month_list = ['Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov']
    page2 = re.get(calendar_url)
    soup = BeautifulSoup(page2.content,'html5lib')

    race_cards = soup.find_all('div',class_ ="col-12 col-sm-6 col-lg-4 col-xl-3")
    round_complete = False
    hero_race_script = str(soup.find_all('script')[0])
    hero_race_json = hero_race_script[35:len(hero_race_script)-10]
    json_data = json.loads(hero_race_json)
    hero_race_name = json_data["name"]
    hero_race_link = json_data["@id"]
    for card in race_cards:
        Upcoming = False
        schedule_list = []
        round = card.find(class_ = 'card-title f1-uppercase f1-color--warmRed').text

        date = [card.find(class_ = 'start-date').text,card.find(class_ = 'end-date').text]

        month = card.find(class_ = 'month-wrapper').text

        event_details = card.find(class_ = 'event-details')

        event_location = (event_details.find(class_ = 'event-place').text)[0:-1]
        event_title = event_details.find(class_ = 'event-title f1--xxs').text

        event_pic = event_details.find_all('img', class_="lazy")
        pic_list = [pic['data-src'] for pic in event_pic]
        pic_list.append(card.find(class_='lazy')['data-src'])

        # opening the upcoming races page to obtain all the race events
        if event_title == hero_race_name:
            Upcoming = True
            hero_page = re.get(hero_race_link)
            soup_hero = BeautifulSoup(hero_page.content,'html5lib')
            scripts = ((str(soup_hero.find_all('script')[0]))[35::])[0:-10]
            cards = json.loads(scripts)['subEvent']
            for card in cards:
                title = card['name'][0:-24]
                time_date = [card['startDate'],card['endDate']]
            # data for each event has been scraped ,, time conversion remaining

    ## Hero race identified => next find the timings for each event in the hero race ##


R_C.close()


with open("Standings/drivers.txt","w") as drivers_standings:
    page3 = re.get(standing_drivers)
    soup = BeautifulSoup(page3.content,'html5lib')

    table = soup.find(class_ = 'table-wrap')

    standings = table.find_all('td',class_ = 'dark')

    name_first = table.find_all('span',class_ = 'hide-for-tablet')
    name_second = table.find_all('span',class_ = 'hide-for-mobile')
    name_list = [str((name_first)[i].text)+" "+str((name_second)[i].text) for i in range(len(name_first))]

    teams = table.find_all('a',class_ = 'grey semi-bold uppercase ArchiveLink')
    team_list = [team.text for team in teams]

    templist = []
    standing = []
    for x,char in enumerate(standings):
        templist.append(char)
        if (x+1)%3 == 0:
            standing.append(templist)
            templist = []
            x = 0
    table_list = [[standing[i][0].text,name_list[i],standing[i][1].text,team_list[i],standing[i][2].text] for i in range(len(name_list))]


    for line in table_list:
        drivers_standings.write(f"{line}\n")
drivers_standings.close()


with open('Standings/team.txt','w') as team:
    page4 = re.get(standing_teams)
    soup = BeautifulSoup(page4.content,'html5lib')

    points = soup.find_all('td', class_='dark')
    point_list = [points[i].text for i in range(1, len(points), 2)]

    team_name = soup.find_all('a',class_="dark bold uppercase ArchiveLink")
    team_name_list = [team.text for team in team_name]

    team_point_pairing = list(zip(team_name_list,point_list))
    for pair in team_point_pairing:
        team.write(f"{pair[0]},{pair[1]}\n")
team.close()