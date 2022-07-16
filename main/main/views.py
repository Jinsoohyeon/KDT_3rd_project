from django.shortcuts import redirect, render
from .models import TripNews, NewsSummery, InputKeyword
import pandas as pd
import mlflow
import warnings
import pickle
import numpy as np

# Create your views here.


def about(request):
    datas = TripNews.objects.all().order_by("created_at")
    summ = NewsSummery.objects.all()
    return render(request, 'about.html', {'news' : datas, 'summ': summ})


def index(request):
    return render(request, 'index.html')
def post(request):
    return render(request, 'post.html')
def contact(request):
    return render(request, 'contact.html')
def recommend(request):
    return render(request, 'recommend.html')


def chart_data(request):
    df = pd.read_csv("./data/place_review_cnt_data.csv")
    df2 = pd.read_csv('./data/word_cnt_info.csv')
    word_dict = pd.read_csv("./data/word_list.csv")
    cnt_review = list(df['리뷰수'][:7])
    names = list(df['장소'][:7])
    cnt_word = list(df2['빈도수'][:7])
    words = list(df2['단어'][:7])
    word_dict = list(word_dict["장소"])
    word_dict = word_dict
    input_keywords = InputKeyword.objects.all().order_by("-count")
    if len(input_keywords) < 7:
        input_keywords = input_keywords[:len(input_keywords)]
    else:
        input_keywords = input_keywords[:7]
        
    if request.method == 'POST':
        selected_place =  request.POST.getlist("CheckboxName")
        print(selected_place)

        if selected_place != []:    # 선택한 단어 DB에 저장
            for keyword in selected_place:
                if InputKeyword.objects.filter(keyword = keyword).count() != 0: # 기존 데이터가 존재할 경우 +1
                    update_row = InputKeyword.objects.get(keyword = keyword)
                    update_row.count = update_row.count +1
                    update_row.save()
                else:
                    InputKeyword(keyword = keyword, count = 1).save()

        place_list = pd.read_csv("./data/Gangwon_place_list.csv", encoding ="utf-8-sig")
        user = pd.read_csv("./data/user_answer_form.csv")
        for place in selected_place:
            if place in user.columns:
                user.at[0,place] = 1
        loaded_model = pickle.load(open('./models/model.pkl', 'rb'))
        pred = loaded_model.predict(user)
        predict_places = []
        for loc in pred:
            predict_places.append(place_list.iloc[loc,:])
        
        # print(predict_places[0].str.split(" ")[0])
        # print('type:', type(predict_places[0].str.split(" ")[0]))            
        predict_places = predict_places[0].str.split(" ")[0]
        if type(predict_places) == float:
            predict_places = ["키워드를 다시 입력해주세요"] 
        else : 
            pred_place = predict_places[0]
        
        return render(request,"recommend.html",{"predict_places" : predict_places})

    else :    
        return render(request, 'post.html',
                        {'cnt_review': cnt_review, 'names' : names, 'cnt_word' : cnt_word, 'words' : words,"word_dict" : word_dict,  'input_keywords' : input_keywords
                        })
