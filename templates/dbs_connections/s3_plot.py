from os import getenv, environ

import boto3
import pandas as pd
from aux import init_sdk

environ["AWS_ACCESS_KEY_ID"] = getenv('AWS_ACCESS_KEY_ID')
environ["AWS_SECRET_ACCESS_KEY"] = getenv('AWS_SECRET_ACCESS_KEY')
bucket = 'my_bucket'
filename = 'filename.csv'

# Extract from S3
s3_client = boto3.client('s3')
response = s3_client.get_object(Bucket=bucket, Key=filename)
file = response["Body"]
df = pd.read_csv(file, header=14, delimiter="\t", low_memory=False)


# Load data to Shimoku
s = init_sdk()
s.plt.line(data=df, x='status', y=['total'], menu_path='S3', order=0)
