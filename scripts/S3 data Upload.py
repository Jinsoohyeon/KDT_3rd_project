# BOTO3 VERSION : 1.24.18  : 라이브러리 import트가 안됨
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html
# 설치 라이브러리
# pip install boto3
# pip install pandas

import boto3
from botocore.exceptions import ClientError
import json

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


# 파일 업로딩
bucket = str("kdt-project")
filepath = "./"
filename = str("analysis_data_review8.csv")
# s3.upload_file(bucket, filename, filename)
s3.upload_file(filename, bucket, filename)