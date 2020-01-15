from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as expect
import time
from random import randint
from bs4 import BeautifulSoup
import re
import csv

# https://gist.github.com/aclisp/0c2965af80816bd332b7096a89908ef6 참고함
def delay(n):
    time.sleep(randint(2, n))

youtube_data = [] #데이터 저장 리스트

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get("https://www.instiz.net/pt")
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
time1 = time.strftime("%Y%m%d", time.localtime(time.time()))
print(time1)
time2 = int(time1) - 1
search = driver.find_element_by_link_text("기간")
search.click()
term = driver.find_elements_by_css_selector("form#search div#showdetail input")
term[0].send_keys(time2)
term[1].send_keys(time1)
search.submit()
delay(5)

page = driver.page_source
soup = BeautifulSoup(page, 'lxml')

items = driver.find_elements_by_xpath('//*[@id="subject"]/a')
print(items)
titles_len = soup.find_all("table#mainboard span#subject a")
titles = [titles_len[n].string for n in range(0, len(titles_len))]

item_times_len = soup.find_all('td', width = 45)
item_times = [item_times_len[n].string for n in range(1,len(item_times_len) - 1)]

print(items)
print(item_times)
for i in range(0,len(items)):

    if int(item_times[i]) < 150:
        continue

    items[i].click()
    delay(5)
    # scroll to the bottom in order to load the comments
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    page = driver.page_source
    soup = BeautifulSoup(page,'lxml')

    thread = soup.find_all('div#memo_content_1 p')
    comment_list = []
    img_list = []
    for items in thread:
        comment = items.find_all('span')
        img = items.find_all('img')
        for c_lists, i_lists in comment, img:
            if c_lists != None or i_lists != None:
                try:
                    cmt = c_lists.string
                    textcmt = re.sub(r'[^\w]', '', cmt) #띄어쓰기 없애는 것
                    comment_list.append(cmt)
                    img_list.append(i_lists)
                except TypeError as e:
                    pass
            else:
                pass
    driver.back()
    print(comment_list)
    print(img_list)

# csvfile = open("youtube_data1.csv","w",newline="", encoding="ANSI")
# csvwriter = csv.writer(csvfile)
# for row in youtube_data:
#     try:
#         csvwriter.writerow(row)
#     except UnicodeEncodeError:
#         pass
# csvfile.close()