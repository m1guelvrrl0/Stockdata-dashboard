import pandas as pd
import sqlalchemy
import pandas_datareader.data as web
from datetime import datetime
from sqlalchemy.types import DateTime, FLOAT
import fire
import asyncio
import uvloop

engine = sqlalchemy.create_engine("sqlite:///db.sqlite")
nsdq = pd.read_csv("nasdaq.csv")
nsdq.set_index("Symbol", inplace=True)


async def get_stock_data(name):
    try:
        df = web.DataReader(name, "yahoo", datetime(1970, 1, 1), datetime.today())
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


async def run_tasks():
    task = [asyncio.create_task(get_stock_data(name)) for name in nsdq.index]
    await asyncio.wait(task, timeout=1)
    return task


def main():
    uvloop.install()
    task = asyncio.run(run_tasks())


if __name__ == "__main__":
    fire.Fire(main)
