import mlflow
import pandas as pd
import warnings

place_list = pd.read_csv("../data/Gangwon_place_list.csv", encoding ="utf-8-sig")

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    logged_model = 'runs:/e47700ff63224201a8473eb7fc3380f5/best_estimator'

    loaded_model = mlflow.pyfunc.load_model(logged_model)
    test_x = pd.read_csv("../data/example_user1.csv")
    pred = loaded_model.predict(test_x)
    
    for loc in pred:
        print(place_list.iloc[loc,:])
