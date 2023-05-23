import requests
import threading
from bs4 import BeautifulSoup


def f3_news_():
    with open("Racing_Hub\\F3\\F3 News\\News.txt", 'w', encoding="utf-8") as f3news:
        news_url = "https://www.fiaformula3.com/Latest"
        news_content = requests.get(news_url)
        soup = BeautifulSoup(news_content.content, "html5lib")

        news_class = soup.find_all("p", class_="font-text-body")
        news_list = []
        for newzz in news_class:
            news_list.append(newzz.text)

        img_news = soup.find_all("img", class_="f1-cc--photo")
        img_list = []
        for news_image in img_news:
            source = news_image['data-src']
            img_list.append(source)

        all_news = list(zip(img_list, news_list,))
        for i in all_news:
            f3news.write(f"{i}\n ")
    f3news.close()


def f3_Drivernames_standings():
    with open("Racing_Hub\F3\Standings\Team Standings.txt", 'w', encoding="utf-8") as f3drivers:
        driverstand_url = "https://www.fiaformula3.com/Standings/Driver?seasonId=180"
        driverstand_content = requests.get(driverstand_url)
        soup = BeautifulSoup(driverstand_content.content, "html5lib")

        driverposition_class = soup.find_all("div", class_="pos")
        driverposition_list = []
        for positions_driver in driverposition_class:
            driverposition_list.append(positions_driver.text)

        driverstand_class = soup.find_all("span", class_="visible-desktop-up")
        driverstand_list = []
        for driver_standing in driverstand_class:
            driverstand_list.append(driver_standing.text)

        driverpoints_class = soup.find_all("div", class_="total-points")
        driverpoints_list = []
        for points_driver in driverpoints_class:
            driverpoints_list.append(points_driver.text)
        driver_stats = list(
            zip(driverposition_list, driverstand_list, driverpoints_list))

        for i in driver_stats:
            f3drivers.write(f"{i}\n")
    f3drivers.close()


def f3_teamstandings_():
    with open("Racing_Hub\F3\Standings\Team Standings.txt", 'w', encoding="utf-8") as f3team:
        teamstand_url = "https://www.fiaformula3.com/Standings/Team?seasonId=180"
        teamstand_content = requests.get(teamstand_url)
        soup = BeautifulSoup(teamstand_content.content, "html5lib")

        teamposition_class = soup.find_all("div", class_="pos")
        teamposition_list = []
        for position_team in teamposition_class:
            teamposition_list.append(position_team.text)

        teamname_class = soup.find_all("span", class_="visible-desktop-down")
        teamname_list = []
        for namesof_team in teamname_class:
            teamname_list.append(namesof_team.text)

        teampoints_class = soup.find_all("div", class_="total-points")
        teampoints_list = []
        for points_per_team in teampoints_class:
            teampoints_list.append(points_per_team.text)

        teamstandings = list(
            zip(teamposition_list, teamname_list, teampoints_list))

        for i in teamstandings:
            f3team.write(f"{i}\n ")

    f3team.close()


def _f3dates_():
    with open("Racing_Hub\F3\Calendar\F3 Calendar.txt", 'w', encoding="utf-8") as f3calendar:
        calendar_url = "https://www.fiaformula3.com/Calendar"
        calendar_content = requests.get(calendar_url)
        soup = BeautifulSoup(calendar_content.content, "html5lib")

        all_card_class = soup.find("div", class_="container calendar-layout")
        round_class = all_card_class.find_all("p", class_="h6")
        round_list = []
        for noof_rounds in round_class:
            round_list.append(noof_rounds.text)

        calendar_class = all_card_class.find_all("p", class_="date")
        calendar_list = []
        for calendar in calendar_class:
            calendar_list.append(calendar.text)

        # Finished races
        card_class = soup.find_all("div", class_="container wrapper card-post")
        location_list = []
        for card in card_class:
            location_class = card .find(class_="ellipsis")
            for race_location in location_class:
                location_list.append(race_location.text)

        # Upcoming class
        upcoming_card_class = soup.find_all(
            "div", class_="container wrapper card-upcoming")
        upcoming_location_class_list = []
        for upcoming_card in upcoming_card_class:
            upcoming_location_class = upcoming_card.find_all(
                class_="ellipsis")
            for this_upcoming in upcoming_location_class:
                upcoming_location_class_list.append(this_upcoming.text)

        racefixtures = location_list+upcoming_location_class_list

        allcalendar = list(zip(round_list, calendar_list, racefixtures))

        for i in allcalendar:
            f3calendar.write(f"{i}\n ")

    f3calendar.close()

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
