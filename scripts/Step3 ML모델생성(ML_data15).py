import os
import warnings
import sys
import time
import pandas as pd
import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

print("시작")
data = pd.read_csv("./data/ML_data15.csv")
print(f"data 다운로드 완료")

# target 데이터 라벨링
place_list = data.place.unique().tolist()
data.insert(0,"places",data.place.map(lambda x:place_list.index(x)))
data.drop("place",axis = 1,inplace = True)
print(f'데이터 라벨링 완료')

# 리뷰 수
copy_data = data.copy()
filter_place_cnt = copy_data.places.value_counts()
value_cnt_over38 = filter_place_cnt[filter_place_cnt>38].index
review_cnt_over38_list = copy_data.loc[copy_data.places == value_cnt_over38[0]]
for num in range(1,len(value_cnt_over38)):
    dummy = copy_data[copy_data.places == value_cnt_over38[num]]
    review_cnt_over38_list = pd.concat([review_cnt_over38_list,dummy])

# target, feature 나누기
X = review_cnt_over38_list.iloc[:,1::]
y = review_cnt_over38_list.places
print(f"target,feature 생성 완료")

# Import mlflow
import mlflow
import mlflow.sklearn

mlflow.sklearn.autolog()

if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    np.random.seed(16)

    # 훈련,테스트셋 만들기
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train,y_test = train_test_split(X,y, test_size = 0.2, stratify=y, random_state = 16)
    print(f'훈련,데이트셋 생성 완료')

    # 모델 생성
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GridSearchCV
    from sklearn.metrics import f1_score
    from sklearn.naive_bayes import GaussianNB
    from xgboost import XGBClassifier
    from sklearn.neural_network import MLPClassifier    
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import SVC


    # 로지스틱
    lr_param = [{"C" : [0.01,0.5,1]}]
    lr = GridSearchCV(LogisticRegression(random_state =16, multi_class = "multinomial", solver = "lbfgs"), lr_param, cv =5)
    

    # 나이브 베이즈
    gnb_param = [{"var_smoothing" : [0,1,2]}]
    gnb = GridSearchCV(GaussianNB(), gnb_param, cv = 5)

    # 인공신경망
    mlpc_param = [{"hidden_layer_sizes" : [2,3,4], "solver" : ["sgd"], "activation" : ["logistic"]}]
    mlpc = GridSearchCV(MLPClassifier(), mlpc_param, cv = 5)
    
    # XGB
    xgb_param = [{"max_depth" : [2,4,6]}]
    xgbc = GridSearchCV(XGBClassifier(), xgb_param, cv =5)

    # RandomForest
    rfc_param = [{"max_features" : ["sqrt"], "n_estimators" : range(100,1000,100)}]
    rfc = GridSearchCV(RandomForestClassifier(), rfc_param, cv =5)

    # SVC
    svc_param = [{"kernel" : ["rbf"], "C": [0.5,1], "gamma" : [0.5,1]}]
    svc = GridSearchCV(SVC(), svc_param, cv = 5)

    print("모델 생성 완료")
    start = time.time()
    print("모델 fitting 시작")
    svc.fit(X_train,y_train)
    end = time.time()
    X_pred = svc.predict(X_test)

    print(f"속도 : {end - start} sec")
    print(f'Best Parameter: {str(svc.best_params_)}')
    print(f'Best Score: {round(svc.best_score_,4)}')
    print(f"F1-score : {round(f1_score(y_test,X_pred, average = 'micro'),4)}")
    print((f'Test Score : {round(svc.score(X_test,y_test))}'))