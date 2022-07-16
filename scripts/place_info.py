from tracemalloc import start
import selenium 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from urllib import response
import time
import pandas as pd
import os

# driver 오류
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# URL 접속
driver = webdriver.Chrome("C:/Users/madda/.ssh/project_3/Gangwon_trip_project/chromedriver.exe",options=options)
driver.get("https://google.com")

# 장소 url 불러오기
place_url_list = pd.read_csv("../data/tripcom_place_url_list.csv")
place_url_list = place_url_list["URL"]



# 페이지 들어가기
start_place_number = 419
end_place_number = 682
place_number = start_place_number
for place in place_url_list[start_place_number:end_place_number]:

    # 데이터 저장
    review_info = []
    place_list = []                # 장소
    place_type_list = []       # 장소 분류
    bnt_list = []                   # 운영시간
    rcm_time_list = []         # 추천관광시간
    address_list = []            # 주소
    place_name = []           # 댓글 장소 구분
    review_page_number = []         # 리뷰 페이지

    place_number += 1
    review_page = 0
    driver.get(place)
    # time.sleep(1)
    time.sleep(3)

    # 장소
    place_css = driver.find_element_by_css_selector("h1.basicName")

    # 장소 분류
    try :
        place_type_css = driver.find_elements_by_css_selector("div.gl-poi-detail_tags > span")
    except selenium.common.exceptions.NoSuchElementException:
        place_type_css = "정보없음"
    
    # info_list = driver.find_elements_by_css_selector('span.field')
    
    # 운영시간
    try :
        bnt_css = driver.find_element_by_xpath('//*[@id="poi.detail.overview"]/div/div[2]/div/div[3]/div[1]/div[1]/div/span[2]')
        # bnt = info_list[0].text
        bnt = bnt_css.text
    except selenium.common.exceptions.NoSuchElementException:
        bnt = "정보없음"
    # 관광 추천시간
    try:
        rcm_time_css = driver.find_element_by_xpath('//*[@id="poi.detail.overview"]/div/div[2]/div/div[3]/div[1]/div[2]/div/span[2]')
        # rcm_time = info_list[1].text
        rcm_time = rcm_time_css.text
    except selenium.common.exceptions.NoSuchElementException:
        rcm_time = "정보없음"
    # 주소
    try :
        address_css = driver.find_element_by_css_selector('div.address > div > div > div > div > span.field')
        # address = info_list[2].text
        address = address_css.text
    except selenium.common.exceptions.NoSuchElementException:
        address = "정보없음"
        
    # 데이터 수집
    ## 장소
    place_list.append(place_css.text)

    ## 장소 분류
    place_types = []
    for type in place_type_css:
        place_types.append(type.text)
    place_type_list.append(place_types)

    ## 운영시간
    bnt_list.append(bnt)
    
    ## 관광 추천시간
    rcm_time_list.append(rcm_time)
    
    ## 주소 
    address_list.append(address)

    # css
    review_pages = driver.find_elements_by_css_selector("div.gl-poi-detail_page ul.gl-cpt-pager > li")
    

    try :
        review_page = review_pages[-1].text
        print(f'총 페이지 수 : {review_page}')
    except IndexError as e:
        print(f'{place_number}번장소 : {place_css.text}')
        print("리뷰 없음")

    try :
        for page in range(int(review_page)):
            print(f'{place_number}번장소 : {place_css.text}')
            print(f'페이지 : {page+1}/{review_page} 실행 중')
            time.sleep(3)

            contents = driver.find_elements_by_css_selector("div.gl-poi-detail_comment-content")
            for content in contents:
                try :
                    point = content.find_element_by_css_selector("span.review_score.score-name")
                    point_value = point.text
                    print(point_value)
                    date = content.find_element_by_css_selector("span.r.c2.create-time")
                    date_value = date.text
                    date_value = date_value.split(" ")
                    date_value = date_value[1] + date_value[2] + date_value[3]
                    print(date_value)
                    comment = content.find_element_by_css_selector("div.gl-poi-detail_comment-content > div > a")
                    comment_value = comment.get_attribute("alt")
                    print(comment_value)
                    comment_trans = content.find_element_by_css_selector("div.gl-poi-detail_comment-content > div > a > p")
                    comment_trans_value = comment_trans.text
                    print(comment_trans_value)
                    review_info.append([place_css.text,page+1,point_value,date_value,comment_value,comment_trans_value])
                except selenium.common.exceptions.NoSuchElementException:
                    point_value = "평가없음"
                    date = content.find_element_by_css_selector("span.r.c2.create-time")
                    date_value = date.text
                    date_value = date_value.split(" ")
                    date_value = date_value[1] + date_value[2] + date_value[3]
                    print(date_value)
                    comment = content.find_element_by_css_selector("div.gl-poi-detail_comment-content > div > a")
                    comment_value = comment.get_attribute("alt")
                    print(comment_value)
                    comment_trans = content.find_element_by_css_selector("div.gl-poi-detail_comment-content > div > a > p")
                    comment_trans_value = comment_trans.text
                    print(comment_trans_value)
                    review_info.append([place_css.text,page+1,point_value,date_value,comment_value,comment_trans_value])
                    

            if page < (int(review_page)-1):
                driver.find_element_by_css_selector('div.gl-poi-detail_page div.gl-cpt-pagination > button.btn-next').send_keys(Keys.ENTER) 

            print(f'페이지 {page+1}/{review_page} 실행 완료')


    except:
        pass   

    info_table = [place_list,place_type_list,bnt_list,rcm_time_list,address_list]
    info_table = pd.DataFrame(info_table).T
    info_table.columns = ["장소","분류","운영시간","관광추천시간","주소"]
    if not os.path.exists("../data/tripcom_place_info_table.csv"):
        info_table.to_csv("../data/tripcom_place_info_table.csv", index = False, mode = "w", encoding = "utf-8-sig")
    else :
        info_table.to_csv("../data/tripcom_place_info_table.csv", index = False, mode = "a", encoding = "utf-8-sig",header = False)


    review_table = review_info
    review_table = pd.DataFrame(review_table, columns = ["장소","리뷰페이지","평점","작성일","리뷰(원문)","리뷰(번역)"])
    review_table["평점"] = review_table["평점"].replace(["완벽해요!","최고에요!","좋아요!","보통이에요","최악이에요"],[5,4,3,2,1])
    if not os.path.exists("../data/tripcom_place_info_table.csv"):
        review_table.to_csv("../data/tripcom_place_review_table.csv", index = False, mode = "w", encoding = "utf-8-sig")
    else :
        review_table.to_csv("../data/tripcom_place_review_table.csv", index = False, mode = "a", encoding = "utf-8-sig",header = False)



