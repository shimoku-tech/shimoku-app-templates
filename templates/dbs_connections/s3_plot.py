import io
from os import getenv, environ

import boto3
import pandas as pd
import shimoku_api_python as shimoku


def init_sdk() -> shimoku.Client:
    api_key: str = getenv('API_TOKEN')
    universe_id: str = getenv('UNIVERSE_ID')

    return shimoku.Client(
        access_token=api_key,
        universe_id=universe_id, business_id=business_id,
        environment='production',
        verbosity='INFO',
        async_execution=async_exec,
    )


os.environ["AWS_ACCESS_KEY_ID"] = os.getenv('AWS_ACCESS_KEY_ID')
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv('AWS_SECRET_ACCESS_KEY')
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
