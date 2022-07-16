import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import response
import time
import pandas as pd


# driver 오류
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 3개
# url = "https://kr.trip.com/travel-guide/attraction/chuncheon-si/gangwon-provincial-botanic-garden-13632218/"


# 5개
# url = "https://kr.trip.com/travel-guide/attraction/goseong-gun/hwajinpo-beach-13626715/"

# 6개 이상
url = "https://kr.trip.com/travel-guide/attraction/gangneung-si/jumunjin-beach-18106593/"

# URL 접속
driver = webdriver.Chrome("C:/Users/madda/.ssh/project_3/Gangwon_trip_project/chromedriver.exe",options=options)
driver.get(url)


# 데이터 저장
score_list = []                # 리뷰 평점 
score_date_list = []       # 리뷰 작성일
coment_list = []            # 리뷰(원문)
coment_trans_list = []  # 리뷰(번역)


# 평점,평점 작성일
# score_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > span')

# 리뷰
# coment_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a')

# 리뷰 번역
# coment_trans_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a > p')


# 리뷰 page만큼 for문 돌리기
review_pages = driver.find_elements_by_css_selector("div.gl-poi-detail_page   ul.gl-cpt-pager > li.number")
review_page = review_pages[-1].text
print(review_page)

for page in range(int(review_page)):
    score_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > span.review_score')
    date_css = driver.find_elements_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/ul/div[1]/li/div[2]/div[3]/span/span')
    coment_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a')
    coment_trans_css = driver.find_elements_by_css_selector('div.gl-poi-detail_comment-content > div > a > p')


    ## 리뷰 평점,작성일
    for point in score_css:
        score = point.text
        score_list.append(score)
    
    for point in date_css:
        date = point.text
        date = date.split(" ")
        print(date)
        date = date[1] + date[2] + date[3]
        score_date_list.append(date)


    ## 리뷰(원문)
    for place in coment_css :
        coment = place.get_attribute("alt")
        coment_list.append(coment)


    ## 리뷰(번역)
    for place in coment_trans_css:
        coment_trans = place.text
        coment_trans_list.append(coment_trans)
    
    print(coment_trans_list)
    try :
        if page < (review_page-1):
            driver.find_element_by_xpath('//*[@id="reviews"]/div/div/div[3]/div[2]/div/div/div/div/button[2]').send_keys(Keys.ENTER)
            time.sleep(1)
    except Exception as e:
        print(e)
        pass 
        

review_table = [score_list,score_date_list,coment_list,coment_trans_list]
review_table = pd.DataFrame(review_table).T
review_table.columns = ["평점","작성일","리뷰(원문)","리뷰(번역)"]

print(review_table)