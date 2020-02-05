import pandas as pd
import sqlalchemy
import pandas_datareader.data as web
from datetime import datetime, timedelta
from sqlalchemy.types import DateTime, FLOAT
import asyncio
import uvloop
import fire

engine = sqlalchemy.create_engine("sqlite:///db.sqlite")
nsdq = pd.read_csv("nasdaq.csv")
nsdq.set_index("Symbol", inplace=True)


async def get_stock_data(name):
    TODAY: DateTime = datetime.today()
    YESTERDAY: DateTime = (datetime.today() - timedelta(days=1))
    try:
        df = web.DataReader(name, "yahoo", YESTERDAY, TODAY)
        df.reset_index(inplace=True)
        df.to_sql(
            name,
            engine,
            if_exists="append",
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

def main():
    uvloop.install()
    task = asyncio.run(run_tasks())

if __name__ == "__main__":
    fire.Fire(main)