#naver news crawling

import urllib.request
from bs4 import BeautifulSoup
import csv

#Global Var
OUTPUT = 'news.csv' #Name of Output file
Target_URL = 'https://entertain.naver.com/ranking#type=hit_total&date=2020-01-17'

def get_text(URL): #get text from target
    html = urllib.request.urlopen(URL)
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    titles = []
    target = soup.find_all('a','title') # a tag <class = "title">
    for title in target:
        titles.append(str(title.text))
    return titles

def test(URL): #셀레니움으로 직접켜서 제목만 뽑아오는 식으로 해볼것
    html = urllib.request.urlopen(URL)
    soup = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
    titles = []
    target = soup.find_all('li')
    for idx,text in enumerate(target):
        if idx in range(11,87):
            titles.append(text.text)
    return titles

def set_url(month,day): #set url by day
    global Target_URL
    Target_URL = Target_URL[:60]
    Target_URL += '-'+month
    Target_URL += '-'+day

def make_csv(result): #output csv
    global OUTPUT
    csvfile = open(OUTPUT, "w", newline="", encoding="ANSI")
    csvwriter = csv.writer(csvfile)
    for idx,data in enumerate(result):
        try:
            csvwriter.writerow([idx,data])
        except UnicodeEncodeError:
            pass
    csvfile.close()

def main():
    set_url('01', '16') #01-17
    print(Target_URL + '를 크롤링합니다')
    make_csv(test(Target_URL))

if __name__  == '__main__':
    main()

