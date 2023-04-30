import requests
from bs4 import BeautifulSoup
# with open("F3\F3 News\News.txt",'w') as f3news:
    # news_url="https://www.fiaformula3.com/Latest"
    # news_content=requests.get(news_url)
    # soup=BeautifulSoup(news_content.content,"html5lib")

    # news_class=soup.find_all("p",class_="font-text-body")
    # news_list=[]
    # for newzz in news_class:
    #     news_list.append(newzz.text)

    # img_news=soup.find_all("img",class_="f1-cc--photo")
    # img_list=[]
    # # for news_image in img_news:
    #     # source=news_image['src']
    #     # img_list.append[src]
    # # print(source) Showing source doesnot exist
    # all_news=list(zip(img_list,news_list))
    # for i in all_news:
    #     f3news.write(f"{i}\n ")
# f3news.close()


with open("F3\Standings\Driver Standings.txt",'w') as f3drivers:
    driverstand_url="https://www.fiaformula3.com/Standings/Driver?seasonId=180"
    driverstand_content=requests.get(driverstand_url)
    soup=BeautifulSoup(driverstand_content.content,"html5lib")

    driverposition_class=soup.find_all("div",class_="pos")
    driverposition_list=[]
    for positions_driver in driverposition_class:
        driverposition_list.append(positions_driver.text)


    driverstand_class=soup.find_all("span",class_="visible-desktop-up")
    driverstand_list=[]
    for driver_standing in driverstand_class:
        driverstand_list.append(driver_standing.text)

    driverpoints_class=soup.find_all("div",class_="total-points")
    driverpoints_list=[]
    for points_driver in driverpoints_class:
        driverpoints_list.append(points_driver.text)
    driver_stats=list(zip(driverposition_list,driverstand_list,driverpoints_list))

    for i in driver_stats:
        f3drivers.write(f"{i}\n")
f3drivers.close()


with open("F3\Standings\Team Standings.txt",'w') as f3team:
    teamstand_url="https://www.fiaformula3.com/Standings/Team?seasonId=180"
    teamstand_content=requests.get(teamstand_url)
    soup=BeautifulSoup(teamstand_content.content,"html5lib")

    teamposition_class=soup.find_all("div",class_="pos")
    teamposition_list=[]
    for position_team in teamposition_class:    
        teamposition_list.append(position_team.text)

    teamname_class=soup.find_all("span",class_="visible-desktop-down")
    teamname_list=[]
    for namesof_team in teamname_class:
        teamname_list.append(namesof_team.text)

    teampoints_class=soup.find_all("div",class_="total-points")
    teampoints_list=[]
    for points_per_team in teampoints_class:
        teampoints_list.append(points_per_team.text)
    
    
    teamstandings=list(zip(teamposition_list,teamname_list,teampoints_list))
    
    for i in teamstandings:
            f3team.write(f"{i}\n ")


f3team.close()

with open("F3\Calendar\F3 Calendar.txt",'w') as f3calendar:
    calendar_url="https://www.fiaformula3.com/Calendar"
    calendar_content=requests.get(calendar_url)
    soup=BeautifulSoup(calendar_content.content,"html5lib")

    round_class=soup.find_all("p",class_="h6")
    round_list=[]
    for noof_rounds in round_class:
        round_list.append(noof_rounds.text)


    calendar_class=soup.find_all("p",class_="date")
    calendar_list=[]
    for calendar in calendar_class:
        calendar_list.append(calendar.text)

    location_class=soup.find_all("span",class_="ellipsis")
    location_list=[]    
    for race_location in location_class:
        location_list.append(race_location.text)

    allcalendar=list(zip(round_list,calendar_list,location_list))

    for i in allcalendar:
        f3calendar.write(f"{i}\n ")

f3calendar.close()

results_url="https://www.fiaformula3.com/Results?raceid=1039"
results_content=requests.get(results_url)
soup=BeautifulSoup(results_content.content,"html5lib")

basicinfo_class=soup.find_all("div",class_="circuit-col")
basicinfo_list=[]
for information in basicinfo_class:
    basicinfo_list.append(information.text)
    # basicinfo_list.append(' ')
# print(basicinfo_list) #It works but everything is cramped up so need to find a way to add spaces

finalresults_class=soup.find_all("div",class_="driver-name-wrapper")
finalresults_list=[]
for race_results in finalresults_class:
    finalresults_list.append(race_results.text)

race_time_class=soup.find_all("div",class_="score-wrapper")
race_time_list=[]
for timedrivers in race_time_class:
    race_time_list.append(timedrivers.text)
driver_overall=list(zip(finalresults_list,race_time_list))
# print(driver_overall)