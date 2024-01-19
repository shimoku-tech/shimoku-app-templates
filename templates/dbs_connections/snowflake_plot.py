import pandas as pd
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
from app_shimoku import init_sdk

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
s.run()