import os
import django
import csv
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GangwonGangwon_trip_project.settings')
django.setup()

from scraper.models import Location, TouristReview

f = open('./data/place_info.csv', 'r', encoding='utf-8')
rows = csv.reader(f)
next(rows, None)
info = []
for row in rows:
   loc, cat, ot, rt, ad = row
   tuple = (loc, cat, ot, rt, ad)
   info.append(tuple)
f.close()
# print(info[0:10])

#장소,분류,운영시간,관광추천시간,주소

instances = []
for (loc, cat, ot, rt, ad) in info:
   instances.append(Location(location_name= loc, category = cat,ope_time = ot,rec_time = rt, addrs = ad))

Location.objects.bulk_create(instances)

with open('./data/review.csv', 'r', encoding='utf-8') as f:
    rows = csv.reader(f)
    next(rows, None)
    info = []
    for row in rows:
        loc, rate, y, m, d, review = row
        tuple = (loc, rate, y, m, d, review)
        info.append(tuple)
# print(info[0:20])
#장소,평점,작성연도,작성월,작성일,리뷰


instances = []
for (loc, rate, y, m, d, review) in info:
    instances.append(TouristReview(location_name = loc, rate = rate, year = y,month = m,day = d,review = review))

TouristReview.objects.bulk_create(instances)