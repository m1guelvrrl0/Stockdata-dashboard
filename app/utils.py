from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from pandas import DataFrame

def get_symbols():
    symbols: DataFrame = get_nasdaq_symbols()
    symbols = symbols[['Security Name']]
    symbols.to_csv('nasdaq.csv')
    