import requests
from bs4 import BeautifulSoup
stand_url = "https://www.fiaformula2.com/Standings/Driver"
content_web = requests.get(stand_url)
soup = BeautifulSoup(content_web.content, 'html.parser')

drivername = soup.find_all("span", class_="visible-desktop-down")
driver_list = []
for driver in drivername:
    driver_list.append(driver.text)

points = soup.find_all("div", class_="total-points")
points_list = []
for point in points:
    points_list.append(point.text)

positions = []
for post in range(len(driver_list)):
    post += 1
    positions.append(post)

all_list = list(zip(positions, driver_list, points_list))


team_url = "https://www.fiaformula2.com/Standings/Team?seasonId=180"
team_content = requests.get(team_url)
soup = BeautifulSoup(team_content.content, 'html.parser')

team_name = soup.find_all("span", class_="visible-desktop-down")
team_list = []
for teams in team_name:
    team_list.append(teams.text)

team_points = soup.find_all("div", class_="total-points")
team_points_list = []
for teamsp in team_points:
    team_points_list.append(teamsp.text)

positions = []
for post in range(len(team_list)):
    post += 1
    positions.append(post)

all_team_list = list(zip(positions, team_list, team_points_list))



news_url="https://www.fiaformula2.com/Latest"
news_content=requests.get(news_url)
soup=BeautifulSoup(news_content.content,'html.parser')

news_link=soup.find_all("p",class_="font-text-body")
news_list=[ ]
for news in news_link:
    news_list.append(news.text)


news_img=soup.find_all("img",class_="f1-cc--photo")
img_list = []
for news_image in news_img:
    src = news_image['data-src']
    img_list.append(src)

all_news_list=list(zip(img_list,news_list))
# print(all_news_list)



with open("F2\F2 Standings\Driver Standings.txt", 'w') as drivers:
    content_web = requests.get(stand_url)
    soup = BeautifulSoup(content_web.content, 'html.parser')

    drivername = soup.find_all("span", class_="visible-desktop-down")
    driver_list = []
    for driver in drivername:
        driver_list.append(driver.text)

    points = soup.find_all("div", class_="total-points")
    points_list = []
    for point in points:
        points_list.append(point.text)

    positions = []
    for post in range(len(driver_list)):
        post += 1
        positions.append(post)

    all_list = list(zip(positions, driver_list, points_list))

    for i in all_list:
        drivers.write(f"{i}\n ")
drivers.close()


with open("F2\F2 Standings\Team Standings.txt", 'w') as team:
    team_content = requests.get(team_url)
    soup = BeautifulSoup(team_content.content, 'html.parser')

    team_name = soup.find_all("span", class_="visible-desktop-down")
    team_list = []
    for teams in team_name:
        team_list.append(teams.text)

    team_points = soup.find_all("div", class_="total-points")
    team_points_list = []
    for teamsp in team_points:
        team_points_list.append(teamsp.text)

    positions = []
    for post in range(len(team_list)):
        post += 1
        positions.append(post)

    all_team_list = list(zip(positions, team_list, team_points_list))

    for i in all_team_list:
        team.write(f"{i}\n")
team.close()



with open("F2\F2 News\F2 News.txt",'w') as news:
    news_content=requests.get(news_url)
    soup=BeautifulSoup(news_content.content,'html5lib')

    news_link=soup.find_all("p",class_="font-text-body")
    news_list=[]
    for news_article in news_link:  
        news_list.append(news_article.text)
    
    news_img=soup.find_all("img",class_="f1-cc--photo")
    img_list = []
    for news_image in news_img:
        src = news_image['data-src']
        img_list.append(src)

    all_news_list=list(zip(img_list,news_list))
   

    for article in all_news_list:
        news.write(f"{article}\n")

news.close()
