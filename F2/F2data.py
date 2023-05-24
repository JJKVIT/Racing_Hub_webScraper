import requests
from bs4 import BeautifulSoup
import threading
import json


def f2_drivers_():
    with open("Racing_Hub\F2\F2 Standings\Driver Standings.txt", 'w', encoding="utf-8") as drivers:
        stand_url = "https://www.fiaformula2.com/Standings/Driver"
        content_web = requests.get(stand_url)
        soup = BeautifulSoup(content_web.content, 'html.parser')
        final = {}
        drivername = soup.find_all("span", class_="visible-desktop-up")
        for i, driver in enumerate(drivername):

            final[str(i+1)] = {"name": driver.text}

        points = soup.find_all("div", class_="total-points")
        for i, point in enumerate(points):
            final[str(i+1)]["point"] = point.text

        drivers.write(json.dumps(final, ensure_ascii=False))

    drivers.close()


f2_drivers_()


def f2_team_():
    with open("Racing_Hub\F2\F2 Standings\Team Standings.txt", 'w', encoding="utf-8") as team:
        team_url = "https://www.fiaformula2.com/Standings/Team?seasonId=180"
        team_content = requests.get(team_url)
        soup = BeautifulSoup(team_content.content, 'html.parser')
        out = {}

        team_name = soup.find_all("span", class_="visible-desktop-down")
        for i, teams in enumerate(team_name):
            out[str(i+1)] = {"team": teams.text}

        team_points = soup.find_all("div", class_="total-points")
        for i, teamsp in enumerate(team_points):
            out[str(i+1)]["teamsp"] = teamsp.text

        team.write(json.dumps(out, ensure_ascii=False))

    team.close()


f2_team_()


def f2_news_():
    with open("Racing_Hub\F2\F2 News\F2 News.txt", 'w', encoding="utf-8") as news:
        news_url = "https://www.fiaformula2.com/Latest"
        news_content = requests.get(news_url)
        soup = BeautifulSoup(news_content.content, 'html5lib')
        out = {}

        news_link = soup.find_all("p", class_="font-text-body")
        for i, news_article in enumerate(news_link):
            out[str(i+1)] = {"headline": news_article.text}

        news_img = soup.find_all("img", class_="f1-cc--photo")
        img_list = []
        for i, news_image in enumerate(news_img):
            src = news_image['data-src']
            out[str(i+1)]["news_image"] = src
        # print(out)
        news.write(json.dumps(out, ensure_ascii=False))

    news.close()


f2_news_()


def f2_schedule_():
    with open("Racing_Hub\F2\Calender\Race Calendar.txt", 'w', encoding="utf-8") as schedule:
        calendar_url = "https://www.fiaformula2.com/Calendar"
        calendar_content = requests.get(calendar_url)
        soup = BeautifulSoup(calendar_content.content, "html5lib")
        out = {}

        date_start = soup.find_all("span", class_="start-date")
        # date_start_list = []

        date_end = soup.find_all("span", class_="end-date")
        # date_end_list = []

        location = soup.find_all("span", "ellipsis")
        # location_list = []

        month_ = soup.find_all("span", class_="month")
        # month_list = []

        # for i, start in enumerate(date_start):
        #     for i, end in enumerate(date_end):
        #         for i, destination in enumerate(location):
        #             for i, month_date in enumerate(month_):
        #                 out[str(i+1)] = {"month": month_date.text}
        #             out[str(i+1)]["destination"] = destination.text
        #         out[str(i+1)]["end"] = end.text
        #     out[str(i+1)]["start"] = start.text

        for i, destination in enumerate(location):
            for i, month_date in enumerate(month_):
                for i, end in enumerate(date_end):
                    for i, start in enumerate(date_start):
                        out[str(i+1)] = {"startdate": start.text}
                    out[str(i+1)]["end"] = end.text
                out[str(i+1)]["month"] = month_date.text
            out[str(i+1)]["destination"] = destination.text

        schedule.write(json.dumps(out, ensure_ascii=False))
    schedule.close()


f2_schedule_()

# Threading

    def f2thread():
        t1 = threading.Thread(target=f2_drivers_, name=t1)
        t2 = threading.Thread(target=f2_team_, name=t2)
        t3 = threading.Thread(target=f2_news_, name=t3)
        t4 = threading.Thread(target=f2_schedule_, name=t4)
# Start of threading

    t1.start()
    t2.start()
    t3.start()
    t4.start()
# Join threading

    t1.join()
    t2.join()
    t3.join()
    t4.join()
