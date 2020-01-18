from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv

data = [] #데이터 저장 리스트

item = []
titles_len2 = []
def load_content_gall(driver):
    for i in range(1,16):
        if(i != 1):
            name = f'{i}'
            index = driver.find_element_by_link_text(name)
            index.click()

        page = driver.page_source
        soup = BeautifulSoup(page, 'lxml')

        titles_len1 = soup.find_all("td", attrs={'class': "gall_tit ub-word"})
        for i in titles_len1:
            titles_len2.append(i.get_text())

        item_times_len = soup.find_all('tr', attrs={'class': 'ub-content us-post'})
        for n in range(0, len(item_times_len)):
            item.append(item_times_len[n].find('td', attrs={'class': 'gall_date'}).get_text())
            item.append(item_times_len[n].find('td', attrs={'class': 'gall_count'}).get_text())
            item.append(item_times_len[n].find('td', attrs={'class': 'gall_recommend'}).get_text())

        print(titles_len2)
        print(item)
    data.append([titles_len2,item])
    # item_times = [item_times_len[n].string for n in range(1,len(item_times_len))]

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
print("enter " + driver.title)
delay(5)
driver.get("https://enter.dcinside.com/")

for i in range(0,4):
    driver.get("https://enter.dcinside.com/")
    search = driver.find_elements_by_css_selector('div#cateList2 a')
    search[i].click()
    load_content_gall(driver)
    driver.back()

for i in range(0,12):
    driver.get("https://enter.dcinside.com/")
    search = driver.find_elements_by_css_selector('div#cateList26 a')
    search[i].click()
    load_content_gall(driver)
    driver.back()

# csvfile = open("youtube_data1.csv","w",newline="", encoding="ANSI")
# csvwriter = csv.writer(csvfile)
# for row in youtube_data:
#     try:
#         csvwriter.writerow(row)
#     except UnicodeEncodeError:
#         pass
# csvfile.close()