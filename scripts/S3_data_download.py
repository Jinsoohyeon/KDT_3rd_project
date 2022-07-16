import pandas as pd
import numpy as np
import time
import warnings
import boto3
import json
import io
import mlflow

with open('config.json', 'r') as f:
    config = json.load(f)

secret_key_id = config['ACCESS_KEY_ID']
access_key = config['SECRET_KEY']

s3 = boto3.client(
    service_name= "s3",
    region_name = "ap-northeast-2",
    aws_access_key_id = secret_key_id,
    aws_secret_access_key = access_key
)

mybucket = str("kdt-project")
# filename은 s3에 올라가져 있는 데이터
filename = str("analysis_data_review8.csv")

# pandas dataframe 만들기
obj = s3.get_object(Bucket=mybucket, Key=filename)
data = pd.read_csv(io.BytesIO(obj["Body"].read()))


# pandas dataframe 만들기
obj = s3.get_object(Bucket=mybucket, Key=filename)
data = pd.read_csv(io.BytesIO(obj["Body"].read()))