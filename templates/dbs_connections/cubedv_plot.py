from os import getenv

import pandas
from sqlalchemy import create_engine
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


# Get data from a SQL database
connection_string = 'mysql+pymysql://user:password@host/db'  # TODO set the user, pass, host, db
conn = create_engine(connection_string)
df = pandas.read_sql_query('SELECT MEASURE(total_sum) total, status from orders GROUP BY status', conn)

# Load data to Shimoku
s = init_sdk()
s.plt.line(data=df, x='status', y=['total'], menu_path='Cube', order=0)
