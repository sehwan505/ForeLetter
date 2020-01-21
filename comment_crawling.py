from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
from bs4 import BeautifulSoup
import time
import re

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get('https://www.youtube.com/channel/UClBklaAD6Wbkked2eAYa6Vw/videos')

#여기서부터
driver.find_element_by_tag_name('body').send_keys(Keys.END)
time.sleep(5)

endk = 1
while endk:
    driver.find_element_by_tag_name('body').send_keys(Keys.END)
    time.sleep(2)
    endk -= 1
page = driver.page_source
soup = BeautifulSoup(page,'lxml')

all_title =driver.find_elements_by_xpath('//*[@id="video-title"]/yt-formatted-string') #리스트로 받음
title = [soup.find_all('a','yt-simple-endpoint style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(all_title))]
print(title)

for titles in all_title:
    titles.click()
    detail_page = driver.page_source
    endk=4
    time.sleep(8)
    driver.get(f'https://www.youtube.com/channel/UClBklaAD6Wbkked2eAYa6Vw/videos/')
    while endk:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(2)
        endk -= 1

    thread = soup.find_all('ytd-comment-renderer', attrs={'class': 'style-scope ytd-comment-thread-renderer'})
    cmtlist = []
    for items in thread:
        div = items.find_all('yt-formatted-string', attrs={'id': 'content-text'})
        #div2 = items.find_all('yt-formatted-string > a')[0].get_text()

        for lists in div:
            if lists != None:
                try:
                    cmt = lists.string
                    textcmt = re.sub(r'[^\w]', '', cmt)
                    cmtlist.append(textcmt)

                except TypeError as e:
                    pass
            else:
                pass

print(cmtlist)