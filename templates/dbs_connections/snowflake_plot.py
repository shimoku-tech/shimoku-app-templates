from os import getenv

import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
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


# TODO set your snowflake connection
url = URL(
    account='xxxx',
    user='xxxx',
    password='xxxx',
    database='xxx',
    schema='xxxx',
    warehouse='xxx',
    role='xxxxx',
    authenticator='https://xxxxx.okta.com',
)
engine = create_engine(url)
connection = engine.connect()

query = 'select * from MYDB.MYSCHEMA.MYTABLE LIMIT 10;'
df = pd.read_sql(query, connection)

# Load data to Shimoku
s = init_sdk()
s.plt.line(data=df, x='status', y=['total'], menu_path='Snowflake', order=0)
