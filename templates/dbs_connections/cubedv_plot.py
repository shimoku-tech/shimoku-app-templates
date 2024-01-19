import pandas
from sqlalchemy import create_engine
from app_shimoku import init_sdk

# Get data from a SQL database
connection_string = 'mysql+pymysql://user:password@host/db'  # TODO set the user, pass, host, db
conn = create_engine(connection_string)
df = pandas.read_sql_query('SELECT MEASURE(total_sum) total, status from orders GROUP BY status', conn)

# Load data to Shimoku
s = init_sdk()
s.plt.line(data=df, x='status', y=['total'], menu_path='Cube', order=0)
s.run()