from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get('https://www.youtube.com/watch?v=4QXDo2t-gJI')

#여기서부터
time.sleep(5)
endk = 5
while endk:
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(2)
    endk -= 1

page = driver.page_source
soup = BeautifulSoup(page,'lxml')

all_title = soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer') #리스트로 받음
title = [soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(all_title))]
print(title)
thread = soup.find_all('ytd-comment-renderer', attrs={'class': 'style-scope ytd-comment-thread-renderer'})
cmtlist = []
for items in thread:
    div = items.find_all('yt-formatted-string', attrs={'id': 'content-text'})
    div2 = items.find_all('yt-formatted-string > a')[0].get_text()

    for lists in div:
        if lists != None:
            try:
                cmt = lists.string
                textcmt = re.sub(r'[^\w]', '', cmt)
                cmtlist.append([textcmt, div2])

            except TypeError as e:
                pass
        else:
            pass

print(cmtlist)