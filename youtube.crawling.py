from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from random import randint
from bs4 import BeautifulSoup
import re

# https://gist.github.com/aclisp/0c2965af80816bd332b7096a89908ef6 참고함
def delay(n):
    time.sleep(randint(2, n))

youtube_data = [] #데이터 저장 리스트

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get("https://www.youtube.com")
print("enter " + driver.title)
delay(5)


# item = driver.find_element_by_css_selector("ytd-masthead div#buttons ytd-button-renderer a")
# item.click()
# delay(5)
#
# # login google account
# driver.find_element_by_id("identifierId").send_keys("sehwan505@gmail.com")
# driver.find_element_by_id("identifierNext").click()
# delay(5)
#
# password_locator = (By.CSS_SELECTOR, 'div#password input[name="password"]')
# time.sleep(5)
# password = driver.find_element(*password_locator)
# password.send_keys("password")
# driver.find_element_by_id("passwordNext").click()
# delay(5)
#
# print("wait for login ...")
# time.sleep(5)
# print("login ok")


search = driver.find_element_by_css_selector("ytd-masthead form#search-form input#search")
search.click()
search.send_keys("아이유")
search.submit()
delay(5)
#
# page = driver.page_source
# soup = BeautifulSoup(page,'lxml')
#
# c=soup.find_all('yt-formatted-string','style-scope ytd-video-renderer')
# titles=[c[n].string for n in range(0,len(c))]
item = driver.find_elements_by_css_selector("ytd-search a#video-title")
print(item)
for i in range(0,len(item)):
    item[i].click()
    delay(5)
    # scroll to the bottom in order to load the comments
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(6)
    endk = 5
    while endk:
        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        time.sleep(1)
        endk -= 1

    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')

    thread = soup.find_all('ytd-comment-renderer', attrs={'class': 'style-scope ytd-comment-thread-renderer'})
    cmtlist = []
    for items in thread:
        div = items.find_all('yt-formatted-string', attrs={'id': 'content-text'})
        for lists in div:
            if lists != None:
                try:
                    cmt = lists.string
                    textcmt = re.sub(r'[^\w]', '', cmt) #띄어쓰기 없애는 것
                    cmtlist.append(cmt)

                except TypeError as e:
                    pass
            else:
                pass

    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')

    title = soup.find('yt-formatted-string','style-scope ytd-video-primary-info-renderer').string
    video_time = soup.find('span','ytp-time-duration').string
    view_count = soup.find('span','short-view-count style-scope yt-view-count-renderer').string

    data_list = []
    data_list.append(title)
    data_list.append(view_count)
    data_list.append(video_time)
    data_list.append(cmtlist)

    youtube_data.append(data_list)
    print(youtube_data)
    driver.back()
# #
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# item = driver.find_element_by_css_selector("ytd-comments ytd-comment-simplebox-renderer div#placeholder-area")
# item.click()
# item = driver.find_element_by_css_selector(("ytd-comments ytd-comment-simplebox-renderer "
#                                             "iron-autogrow-textarea #textarea"))
# item.click()
# item.send_keys("I like it!\n")
# item.send_keys("This is the most amazing things ever seen.\n")
# item.send_keys("Wanna see more~\n")
# item.send_keys(Keys.CONTROL, Keys.ENTER)