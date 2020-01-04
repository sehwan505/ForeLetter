from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import csv

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get('https://www.youtube.com/user/BuzzBean11/videos')

#여기서부터
time.sleep(5)
endk = 5
while endk:
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(1)
    endk -= 1

page = driver.page_source
soup = BeautifulSoup(page,'lxml')

all_title = soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer') #리스트로 받음
title = [soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(all_title))]
print(title)

all_video_time = soup.find_all('span','style-scope ytd-thumbnail-overlay-time-status-renderer')
video_time = [soup.find_all('span','style-scope ytd-thumbnail-overlay-time-status-renderer')[n].string.strip() for n in range(0,len(all_video_time))]
print(video_time)


#구독자 수
sub_num = soup.find('yt-formatted-string','style-scope ytd-c4-tabbed-header-renderer').string
print(sub_num)
#조회수, 올린지 얼마나 되었는지(업로드 시점)
c = soup.find_all('span','style-scope ytd-grid-video-renderer')
view_num = [soup.find_all('span','style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(c))]
print(view_num)

youtube_data = []
x = 0
y = 1
youtube_data.append(sub_num)
for i in range(0, len(all_video_time)):
    data_list = []
    data_list.append(title[i])
    data_list.append(video_time[i])
    data_list.append(view_num[x])
    x += 2
    data_list.append(view_num[y])
    y += 2

    youtube_data.append(data_list)


csvfile = open("youtube_data.csv","w",newline="", encoding="UTF-8")
csvwriter = csv.writer(csvfile)
for row in youtube_data:
    csvwriter.writerow(row)
csvfile.close()