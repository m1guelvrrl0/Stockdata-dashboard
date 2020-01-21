import pandas as pd
import sqlalchemy
import os
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from sqlalchemy.types import DateTime, FLOAT
import sqlite3
from utils import get_tickers

engine = sqlalchemy.create_engine("sqlite:///db.sqlite")
nsdq = pd.read_csv('tickers.csv')
nsdq.set_index('Symbol', inplace=True)

for name in nsdq.index:
       try:
              df = web.DataReader(name, 'yahoo', datetime(2017,1,1), datetime.today())
              df.reset_index(inplace=True)
              df.to_sql(name,
                            engine,
                            if_exists='replace',
                            index=False,
                            chunksize=500,
                            dtype={"Date": DateTime,
                                   "Close": FLOAT})
                                   
              sql_DF = pd.read_sql_table(name,
                                   con=engine)
       except Exception:
              print(f'{name} couldn\'t be downloaded')

print(engine.table_names())