from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from pandas import DataFrame
import pandas as pd
import fire



def get_symbols(filename: str = "nasdaq.csv"):
    if not name.endswith('.csv'):
        raise Exception('Filename must end with .csv')
    symbols: DataFrame = get_nasdaq_symbols()
    symbols = symbols[['Security Name']]
    symbols.to_csv(filename)

if __name__ == '__main__':
  fire.Fire(get_symbols)

