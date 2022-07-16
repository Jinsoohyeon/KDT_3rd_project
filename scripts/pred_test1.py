import mlflow
import pandas as pd
import warnings

place_list = pd.read_csv("../data/Gangwon_place_list.csv", encoding='utf-8-sig')

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    logged_model = 'runs:/42121d8a27cc446eaa368f7eb9a4c7b3/best_estimator'

    loaded_model = mlflow.pyfunc.load_model(logged_model)
    test_x = pd.read_csv("../data/example_user1.csv", encoding='utf-8-sig')
    pred = loaded_model.predict(test_x)
    
    for loc in pred:
        print(place_list.iloc[loc,:])
