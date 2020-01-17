from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from random import randint
from bs4 import BeautifulSoup
import re
import csv

# 잘 안되네 - 계속 게시판이 업데이트 되는 게 문제인듯
def delay(n):
    time.sleep(randint(2, n))
time1 = time.strftime("%Y%m%d", time.localtime(time.time()))
print(time1)
time2 = int(time1) - 1

data = [] #데이터 저장 리스트

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
def load_content(driver):
    page = driver.page_source
    soup = BeautifulSoup(page, 'lxml')

    items1 = driver.find_elements_by_class_name()

    titles_len1 = soup.find_all("span", attrs={'id':"subject"})
    titles_len2 = []
    for i in titles_len1:
        titles_len2.append(i.find('a').string)
    item_times_len = soup.find_all('td', attrs={'class':'listno'})
    item_times = []
    for n in range(0,len(item_times_len)):
        if(n % 4 == 1 or n % 4 == 2):
            item_times.append(item_times_len[n].string)

    # item_times = [item_times_len[n].string for n in range(1,len(item_times_len))]
    for i in range(0,len(items1)):
        data2 = []
        items = driver.find_elements_by_css_selector('table#mainboard span#subject a')
        if items != items1:
            print('망함')
        driver.implicitly_wait(20)
        if int(item_times[2*i + 31]) < 150:
            continue
        items[i].click()

        driver.implicitly_wait(10)
        # scroll to the bottom in order to load the comments
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        page = driver.page_source
        soup = BeautifulSoup(page,'lxml')

        thread = soup.find_all('div', attrs={'id':'memo_content_1'})
        comment_list = []
        img_list = []
        for div in thread:
            comment = div.find_all('p', attrs={'class':'cafe-editor-text'})
            img = div.find_all('img')
            for c_lists in comment:
                if c_lists != None:
                    try:
                        cmt = c_lists.get_text()
                        if cmt == '':
                            continue
                        textcmt = re.sub(r'[^\w]', '', cmt) #띄어쓰기 없애는 것
                        comment_list.append(cmt)
                    except TypeError as e:
                        pass
                else:
                    pass
            for i_lists in img:
                if i_lists != None:
                    try:
                        img_src = i_lists.get('src')
                        img_list.append(img_src)
                    except TypeError as e:
                        pass
                else:
                    pass
        driver.back()
        data2.append(titles_len2[i])
        data2.append(item_times[2*i+31])
        data2.append(comment_list)
        data2.append(img_list)
        data.append(data2)
    print(data2)
    print(data)

driver = webdriver.Chrome('/Users/sehwa/Downloads/chromedriver.exe')
driver.get("https://enter.dcinside.com/")
print("enter " + driver.title)
delay(5)


search = driver.find_element_by_link_text("기간")
search.click()
term = driver.find_elements_by_css_selector("form#search div#showdetail input")
term[0].send_keys(time2)
term[1].send_keys(time1)
search.submit()
delay(5)
load_content(driver)
for i in range(2,12):
    name = f'{i}'
    index = driver.find_element_by_link_text(name)
    index.click()
    load_content(driver)


# csvfile = open("youtube_data1.csv","w",newline="", encoding="ANSI")
# csvwriter = csv.writer(csvfile)
# for row in youtube_data:
#     try:
#         csvwriter.writerow(row)
#     except UnicodeEncodeError:
#         pass
# csvfile.close()