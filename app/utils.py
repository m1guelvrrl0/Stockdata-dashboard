import pandas as pd
from typing import Union, List

def get_tickers() -> Union[List, pd.DataFrame]:
    nsdq = pd.read_csv('tickers.csv')
    nsdq.set_index('Symbol', inplace=True)
    options = []
    for tic in nsdq:
        options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

    return options, nsdq