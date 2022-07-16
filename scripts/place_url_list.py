import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import response
import time
import pandas as pd
import json

with open('../Gangwon_trip_project/config.json', 'r') as f:
    config = json.load(f)

# driver 오류
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# URL 설정
search = "강원도"
url = "https://kr.trip.com/global-search/searchlist/search/?keyword={search}&from=home"
url = url.format(search=search)

# URL 접속
driver = webdriver.Chrome(config["Chromedriver"],options=options)
driver.get(url)


# 크롤링할 정보 들어가기
driver.find_element_by_xpath('//*[@id="__next"]/div[2]/div/div[3]/div/ul/li[3]').click()
time.sleep(2)

# 장소 목록
page = driver.find_elements_by_css_selector("ul.gl-cpt-pager > li")
page_cnt = int(page[-1].text)
place_url_list = []
for page in range(page_cnt):
    places_url = driver.find_elements_by_css_selector("div.gl-search-result_list > div.content > div.gl-search-result_list-content > div > a")
    for place in places_url:
        place_url =place.get_attribute("href")
        place_url_list.append(place_url)
    driver.find_element_by_css_selector("div.gl-search-result_page > div > button.btn-next").send_keys(Keys.ENTER)
    time.sleep(2)

place_url_list = pd.DataFrame(place_url_list, columns = ["URL"])
place_url_list.to_csv("../data/tripcom_place_url_list.csv", index = False)

