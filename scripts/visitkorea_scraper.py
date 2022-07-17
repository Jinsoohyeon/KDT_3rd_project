from urllib import response
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import django
from main.models import TripNews, NewsSummery
from selenium.webdriver.common.by import By
import requests
from pyvirtualdisplay import Display

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
django.setup()

# driver 오류
options = webdriver.ChromeOptions() # 크롬 옵션 객체 생성
options.add_argument('headless') # headless 모드 설정
options.add_argument("window-size=1920x1080") # 화면크기(전체화면)
options.add_argument("disable-gpu") 
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("lang=ko_KR") # 사용 언어
# 속도 향상을 위한 옵션 해제
prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}   
options.add_experimental_option('prefs', prefs)
# 가상 웹브라우저 설정
display = Display(visible =0, size = (1024,768))
# 가상 웹브라우저 실행
display.start()
# 하드웨어 가속 사용 여부
# options.add_argument("disable-gpu")

def run():
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    url = "https://korean.visitkorea.or.kr/search/search_list.do?keyword="
    keyword = "강원도"
    search_url = url + keyword
    driver = webdriver.Chrome("../chromedriver",options=options)
    driver.get(search_url)

    driver.find_element_by_css_selector(".search_menu li#tabView2").click()
    driver.find_element_by_xpath('//*[@id="2"]').click()
    time.sleep(2)
    article_list = driver.find_elements_by_css_selector(".search_body ul li div.area_txt div.tit a")

    ## javascript 제거하고 url 가져오기
    url_list = []
    for article in article_list:
        try :
            article_url = article.get_attribute("href")
            article_url = article_url[27::]
            article_url = article_url[0:36]
            url_list.append(article_url)
        except : 
            continue


    # 기사 url로 들어가기
    article_url = "https://korean.visitkorea.or.kr/detail/rem_detail.do?cotid="
    try:
        for article in url_list:
            url = article_url + article
            driver.get(url)
            time.sleep(2)

            # 제목
            title = driver.find_element_by_css_selector("#topTitle").text
            loc = driver.find_element_by_css_selector("#topAddr span:nth-child(1)").text
            date = driver.find_element_by_css_selector("#topAddr span:nth-child(2)").text[6::]
            likeCnt = driver.find_element_by_css_selector("#conLike").text
            shareCnt = driver.find_element_by_css_selector("#conShare").text
            readCnt = driver.find_element_by_css_selector("#conRead").text

            #요약보기
            try:
                cards = driver.find_elements(By.CSS_SELECTOR, '.summary_info .card')
                i = 0
                summary_set = []
                for card in cards:
                    i=i+1
                    webdriver.ActionChains(driver).move_to_element(card).perform() 
                    time.sleep(1)
                    #요약글 제목 가져오기
                    select2 = '.swiper-wrapper li:nth-child({i}) strong span'
                    select2= select2.format(i=i)
                    card_title = driver.find_element_by_css_selector(select2).text
                    print(card_title)
                    #img링크 가져오기
                    select1 = '.swiper-wrapper li:nth-child({i})'
                    select1 = select1.format(i=i)
                    img_url = driver.find_element_by_css_selector(select1).get_attribute('style')
                    img_url = img_url[23:-3]
                    #요약글 가져오기
                    select = 'li:nth-child({i}) .card .view_cont p'
                    select = select.format(i=i)
                    sumText = driver.find_element(By.CSS_SELECTOR, select).text
                    set_list = [card_title ,img_url, sumText]
                    # print(set_list)
                    summary_set.append(set_list)
                # print(summary_set)
                print('get data')
            except Exception as e:
                print(e)

                # DB 저장
            if (TripNews.objects.filter(title__iexact = title).count() == 0):
                TripNews.objects.create(news_url=url, title=title, loc=loc, date=date, likeCnt=likeCnt, shareCnt=shareCnt, readCnt=readCnt)  # URL 테이블에 저장한 객체를 받아서 News 테이블에 저장
                if summary_set != None:
                    for summary in summary_set:
                        #summary의 index 0 => summary title / index 1 => img url / index 2 => summary text
                        NewsSummery.objects.create(post_url=url, card_title=summary[0], img_url=summary[1], summary_info=summary[2]).save()
                else:
                    pass
    except Exception as e:
        print(e)