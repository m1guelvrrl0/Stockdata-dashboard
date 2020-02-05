import pandas as pd
import sqlalchemy
import os
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime
from sqlalchemy.types import DateTime, FLOAT
import sqlite3
import asyncio
import uvloop

engine = sqlalchemy.create_engine("sqlite:///db.sqlite")
nsdq = pd.read_csv("nasdaq.csv")
nsdq.set_index("Symbol", inplace=True)


df = web.DataReader('AAPL', 'yahoo', datetime(2020,1,20), datetime(2020,1,27))
df.reset_index(inplace=True)
df.to_sql('AAPL',
            engine,
            if_exists='replace',
            index=False,
            chunksize=500,
            dtype={"date": DateTime,
                    "Close": FLOAT})

sql_DF = pd.read_sql_table('AAPL',
                    con=engine)
print(sql_DF)



# print(engine.table_names())
async def get_stock_data(name):
    try:
        df = web.DataReader(name, "yahoo", datetime(2017, 1, 1), datetime.today())
        df.reset_index(inplace=True)
        df.to_sql(
            name,
            engine,
            if_exists="replace",
            index=False,
            chunksize=500,
            dtype={"Date": DateTime, "Close": FLOAT},
        )
        print(df)
    except Exception:
        print(f"{name} couldn't be downloaded")


async def main():
    task = [asyncio.create_task(get_stock_data(name)) for name in nsdq.index]
    await asyncio.wait(task, timeout=1)
    return task


uvloop.install()
task = asyncio.run(main())
