import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
import requests
from scraper.models import Location
#### selenium 3.141.0 version


def exception_pages(driver, url):
    driver.get(url)
    driver.implicitly_wait(10)
    location = driver.find_element_by_css_selector("h1#HEADING").text
    Location(location_name = location).save()
    r_loc, r_rate, r_date, r_member, r_review = [], [], [], [], []
    try: #pagenation 끝나면 except
        while True:
            reviews = driver.find_elements_by_css_selector('div.WAllg')
            for i in range(len(reviews)):
                selector = 'div.FTCTN > div:nth-child(3) > div > div:nth-child({i}) > '.format(i=i+3)
                rate = driver.find_element_by_css_selector(selector + '.WAllg > .IkECb > div > span').get_attribute('class')
                rate = rate[-2:]
                rate = rate[0] + '.' + rate[1]
                # print(rate)
                date = driver.find_element_by_css_selector(selector + 'div.sCZGP > div > div.cRVSd > span').text
                date = date.split('.')[1].strip()
                date = date.replace(' ', '').replace('월', '').split('년')
                year = date[0].strip()
                month = '0' + date[1].strip()
                month= month[-2:]
                date= year+month
                # print(date)
                summury = driver.find_element_by_css_selector(selector + '.WAllg > .KgQgP > a > span').text
                review = driver.find_element_by_css_selector(selector + '.WAllg > div.vTVDc > div._T > div.fIrGe')
                review.click()
                member = driver.find_elements_by_css_selector(selector + '.WAllg > div.vTVDc > span.TDKzw')
                if member != []:
                    member = member[0].text.replace('여행 유형:', '').strip()
                    if '친구' in member:
                        member = '친구'
                    elif '가족' in member:
                        member = '가족'
                    elif '연인' in member:
                        member = '커플'
                    elif '혼자' in member:
                        member = '개인'
                    elif '출장' in member:
                        member = '비지니스'
                else:
                    member = ''
                review = review.text.rstrip('덜 보기')
                review_text = summury + ' ' + review
                # print(review_text[:20])
                # TripadvisorReview(location_name=location, rate=rate, date=date, member=member, review = review_text).save()
                r_loc.append(location)
                r_rate.append(rate)
                r_date.append(date)
                r_member.append(member)
                r_review.append(review_text)
            toNext = driver.find_element_by_css_selector('div.ui_pagination a.next').click()
            driver.implicitly_wait(10)
            time.sleep(1)
    except Exception as e:
        print(e)
        pass
    return r_loc, r_rate, r_date, r_member, r_review


def run():
    # driver 오류
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    url = "https://www.tripadvisor.co.kr/Attractions-g1072105-Activities-a_allAttractions.true-Gangwon_do.html"
    driver = webdriver.Chrome("C:\gitdoc\Gangwon_trip_project\chromedriver102.exe",options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    # get_urls = driver.find_elements_by_css_selector(".bMktZ div.MGdFu a")
    #url 리스트화
    #첫페이지
    # urls = []
    # for url in get_urls:
    #     urls.append(url.get_attribute("href"))
    #두번째 페이지 이후
    # for num in range(30, 727, 30):
    #     add_url = 'https://www.tripadvisor.co.kr/Attractions-g1072105-Activities-oa{num}-Gangwon_do.html'
    #     add_url = add_url.format(num=num)
    #     driver.get(add_url)
    #     get_urls = driver.find_elements_by_css_selector(".bMktZ div.MGdFu a")
    #     for url in get_urls:
    #         urls.append(url.get_attribute("href"))
    
    location_list, rate_list, date_list, member_list, review_list = [],[],[],[],[]
        #장소 상세 페이지
    with open('../tripadvisor_urls_test.txt', 'r') as f:
        urls = f.read().splitlines()
    for url in urls:
        try: # try4 - 페이지 형식 다를 때 있음
            driver.get(url)
            driver.implicitly_wait(10)
            location = driver.find_element_by_css_selector("h1.biGQs").text
            if Location.objects.filter(location_name = location).count() == 0:
                Location(location_name = location).save()
            try: #try1
                while True:
                    try: #try2
                        reviews = driver.find_elements_by_css_selector('.LbPSX div._c')
                        for i in range(len(reviews)):
                            try: #try3 
                                selector = 'div.LbPSX > div:nth-child({i}) > span > div > '.format(i=i+1)
                                rate = driver.find_element_by_css_selector(selector + 'div:nth-child(2) svg').get_attribute('aria-label')
                                print('rate get')
                            except:
                                selector = 'div.LbPSX > div:nth-child({i}) > span > div > '.format(i=i+2)
                                rate = driver.find_element_by_css_selector(selector + 'div:nth-child(2) svg').get_attribute('aria-label')
                                print('ex rate get')
                            rate = rate[8:]
                            date = driver.find_element_by_css_selector(selector + '.TreSq div:nth-last-child(2)').text
                            date = date.split(' ')
                            year = date[0].strip('년')
                            month = '0' + date[1].strip('월')
                            month = month[-2:]
                            day = '0' + date[2].strip('일')
                            day = day[-2:]
                            date = year+month+day
                            try:
                                member = driver.find_element_by_css_selector(selector + '.RpeCd').text.split(' • ')
                                member = member[1].strip()
                            except:
                                member = ''
                            summury = driver.find_element_by_css_selector(selector + 'div.biGQs._P.fiohW.qWPrE.ncFvv.fOtGX').text
                            review = driver.find_element_by_css_selector(selector + 'div._T.FKffI > div.fIrGe._T.bgMZj > div > span')
                            review.click()
                            review = review.text.rstrip('덜 보기')
                            review_text = summury + ' ' + review
                            # print(review_text[0:20])
                            location_list.append(location)
                            rate_list.append(rate)
                            date_list.append(date)
                            member_list.append(member)
                            review_list.append(review_text)
                            # TripadvisorReview(location_name=location, rate=rate, date=date, member=member, review = review_text).save()

                            # except Exception as e:
                            #     loc = url.split('Reviews')
                            #     loc = loc[1].replace('.html', '')
                            #     f = open("./error.txt", 'a')
                            #     error_type = f'try 3 exception - {loc} : {e}\n'
                            #     f.write(error_type)
                            #     f.close()
                            #     continue
                    except Exception as e:
                        loc = url.split('Reviews')
                        loc = loc[1].replace('.html', '')
                        f = open("./error.txt", 'a')
                        error_type = f'try 2 exception - {loc} : {e}\n'
                        f.write(error_type)
                        f.close()
                        pass
                    toNext = driver.find_elements_by_css_selector('.xkSty')
                    toNext[0].click()
                    driver.implicitly_wait(10)
                    time.sleep(1)
            except Exception as e:
                loc = url.split('Reviews')
                loc = loc[1].replace('.html', '')
                f = open("./error.txt", 'a')
                error_type = f'try 1 exception - {loc} : {e}\n'
                f.write(error_type)
                f.close()
                continue
        except Exception as e:
            r_loc, r_rate, r_date, r_member, r_review = exception_pages(driver, url)
            location_list = location_list + r_loc
            rate_list = rate_list + r_rate
            date_list = date_list + r_date
            member_list = member_list + r_member
            review_list = review_list + r_review
            continue
    driver.quit()
    table_list = [location_list, rate_list, date_list, member_list, review_list]
    df = pd.DataFrame(table_list)
    df = df.T
    df.columns = ["장소","평점","작성일","일행","리뷰"]
    df.to_csv('reviewTest.csv')
    print('end')