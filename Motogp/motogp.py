import requests
from bs4 import BeautifulSoup

news_url="https://www.motogp.com/"
news_content=requests.get(news_url)
soup=BeautifulSoup(news_content.content,"html5lib")

news_class=soup.find_all("h2")
news_list=[]
for heading in news_class:
    news_list.append(heading.text)

news_para_class=soup.find_all("p",class_="summary hidden-xs")
news_para_llist=[]
for article in news_para_class:
    news_para_llist.append(article.text)

# news_img_class=soup.find_all("img",class_='src')
# news_img_list=[]
# for image in news_img_class:
#     sorce=image['src']
#     news_img_list.append(sorce)
# print(news_img_class)

driverranking_url="https://www.motogp.com/en/world-standing"
worldranking_content=requests.get(driverranking_url)
soup=BeautifulSoup(worldranking_content.content,"html5lib")

standings_class=soup.find_all("tr",class_="table_row")
# standing_list=[]  Getting wrong or no output
for driver_standing in standing_list:
    standing_list.append(driver_standing)
# print(standings_class)