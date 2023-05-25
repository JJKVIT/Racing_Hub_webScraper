import requests
import threading
from bs4 import BeautifulSoup
import json


def f3_news_():
    try:
        with open("Racing_Hub/F3/F3News/News.json", 'w', encoding="utf-8") as f3news:
            news_url = "https://www.fiaformula3.com/Latest"
            news_content = requests.get(news_url)
            soup = BeautifulSoup(news_content.content, "html5lib")
            out = {}

            news_class = soup.find_all("p", class_="font-text-body")
            for i, newzz in enumerate(news_class):
                out[str(i+1)] = {"news": newzz.text}

            img_news = soup.find_all("img", class_="f1-cc--photo")
            for i, news_image in enumerate(img_news):
                source = news_image['data-src']
                out[str(i+1)]["image"] = source

            f3news.write(json.dumps(out, ensure_ascii=False))
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")


f3_news_()


def f3_Drivernames_standings():
    try:
        with open("Racing_Hub/F3/Standings/DriverStandings.json", 'w', encoding="utf-8") as f3drivers:
            driverstand_url = "https://www.fiaformula3.com/Standings/Driver?seasonId=180"
            driverstand_content = requests.get(driverstand_url)
            soup = BeautifulSoup(driverstand_content.content, "html5lib")
            out = {}

            driverstand_class = soup.find_all(
                "span", class_="visible-desktop-up")
            for i, driver_standing in enumerate(driverstand_class):
                out[str(i+1)] = {"name": driver_standing.text}

            driverpoints_class = soup.find_all("div", class_="total-points")
            for i, points_driver in enumerate(driverpoints_class):
                out[str(i+1)]["points"] = points_driver.text

            f3drivers.write(json.dumps(out, ensure_ascii=False))
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")


f3_Drivernames_standings()


def f3_teamstandings_():
    try:
        with open("Racing_Hub/F3/Standings/TeamStandings.json", 'w', encoding="utf-8") as f3team:
            teamstand_url = "https://www.fiaformula3.com/Standings/Team?seasonId=180"
            teamstand_content = requests.get(teamstand_url)
            soup = BeautifulSoup(teamstand_content.content, "html5lib")
            out = {}

            teamname_class = soup.find_all(
                "span", class_="visible-desktop-down")
            teamname_list = [
                namesof_team.text for namesof_team in teamname_class]
            for i, teamname in enumerate(teamname_list):
                out[str(i+1)] = {"teamname": teamname}

            teampoints_class = soup.find_all("div", class_="total-points")
            for i, points_per_team in enumerate(teampoints_class):
                out[str(i+1)]["points"] = points_per_team.text

            f3team.write(json.dumps(out, ensure_ascii=False))
    except FileNotFoundError:
        print("File not found.")
    except PermissionError:
        print("Permission denied.")


f3_teamstandings_()


def _f3dates_():
    with open("Racing_Hub\F3\Calendar\F3 Calendar.txt", 'w', encoding="utf-8") as f3calendar:
        calendar_url = "https://www.fiaformula3.com/Calendar"
        calendar_content = requests.get(calendar_url)
        soup = BeautifulSoup(calendar_content.content, "html5lib")
        out = dict()

        all_card_class = soup.find("div", class_="container calendar-layout")
        round_class = all_card_class.find_all("p", class_="h6")
        round_list = []

        # Finished races
        card_class = soup.find_all("div", class_="container wrapper card-post")
        location_list = []
        for i, card in enumerate(card_class, 1):
            location_class = card .find(class_="ellipsis")
            for race_location in location_class:
                out[str(i)] = {"loc": race_location.text, "status": "finished"}

        # Upcoming class
        upcoming_card_class = soup.find_all(
            "div", class_="container wrapper card-upcoming")
        upcoming_location_class_list = []
        for upcoming_card in upcoming_card_class:
            upcoming_location_class = upcoming_card.find_all(
                class_="ellipsis")
            for i, this_upcoming in enumerate(upcoming_location_class, i+1):
                upcoming_location_class_list.append(this_upcoming.text)
                out[str(i)] = {"loc": this_upcoming.text, "status": "upcoming"}
        calendar_class = all_card_class.find_all("p", class_="date")
        calendar_list = []
        for i, calendar in enumerate(calendar_class, 1):
            out[str(i)]["date"] = calendar.text
        print(out)
        racefixtures = location_list+upcoming_location_class_list

        allcalendar = list(zip(round_list, calendar_list, racefixtures))

        for i in allcalendar:
            f3calendar.write(f"{i}\n ")

    f3calendar.close()


# _f3dates_()
# Started Threading for efficient running


def f3_thread():
    t1 = threading.Thread(target=_f3dates_, name="t1")
    t2 = threading.Thread(target=f3_news_, name="t2")
    t3 = threading.Thread(target=f3_Drivernames_standings, name='t3')
    t4 = threading.Thread(target=f3_teamstandings_, name="t4")
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
