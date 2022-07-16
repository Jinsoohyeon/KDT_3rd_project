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
data = pd.read_csv("../data/analysis_unsamplingdata_review8.csv", encoding='utf-8-sig')
print(f"data 다운로드 완료")

# target 데이터 라벨링
place_list = data.장소.unique().tolist()
data.insert(0,"place",data.장소.map(lambda x:place_list.index(x)))
data.drop("장소",axis = 1,inplace = True)
print(f'데이터 라벨링 완료')

# target, feature 나누기
X = data.iloc[:,1::]
y = data.place
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
    lr_param = [{"C" : [0.5,0.6]}]
    lr = GridSearchCV(LogisticRegression(random_state = 16), lr_param, cv =5)
    print("모델 생성 완료")

    start = time.time()
    print("모델 fitting 시작")
    lr.fit(X_train,y_train)
    end = time.time()
    X_pred = lr.predict(X_test)

    print(f"속도 : {end - start} sec")
    print(f'Best Parameter: {str(lr.best_params_)}')
    print(f'Best Score: {round(lr.best_score_,4)}')
    print(f"F1-score : {round(f1_score(y_test,X_pred, average = 'micro'),4)}")
    print((f'Test Score : {round(lr.score(X_test,y_test))}'))