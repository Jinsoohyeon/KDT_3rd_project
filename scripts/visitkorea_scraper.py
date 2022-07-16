from urllib import response
import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
## Python이 실행될 때 DJANGO_SETTINGS_MODULE이라는 환경 변수에 현재 프로젝트의 settings.py파일 경로를 등록합니다.

## 이제 장고를 가져와 장고 프로젝트를 사용할 수 있도록 환경을 만듭니다.
import django
from main.models import TripNews, NewsSummery
from selenium.webdriver.common.by import By
import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "websaver.settings")
django.setup()



def run():
    # slack 설정
    # SLACK_BOT_TOKEN = "xoxb-3633493712596-3670945638306-Xmgav9nuup272bfxAfmhKCj6" # 앱 토큰
    # # slack_token = WebClient(token=SLACK_BOT_TOKEN)
    # slack_channel = "korea_visit_info_scraping" # 채녈명

    # driver 오류
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    url = "https://korean.visitkorea.or.kr/search/search_list.do?keyword="
    keyword = "강원도"
    search_url = url + keyword
    driver = webdriver.Chrome("C:/gitdoc/Gangwon_trip_project/chromedriver102.exe",options=options)
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
            
            
            # slack으로 메세지 보내기
            # message = f"{title}{date}"
            # def post_message(token,channel,message):
            #     response = requests.post("https://slack.com/api/chat.postMessage",
            #     headers={"Authorization": "Bearer "+token},
            #     data={"channel": channel,"text": message}
            #     )
            #     print(response)
            
            # post_message(SLACK_BOT_TOKEN,slack_channel,message)

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

# 변동사항
# 요약글 for문에서 리스트로 받음
# img url 인덱싱 변환