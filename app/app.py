# Infrastructure test page.
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from sqlalchemy.types import DateTime, FLOAT
import sqlite3
import sqlalchemy
from datetime import datetime
import pandas as pd
from sqlalchemy.types import DateTime
from utils import get_tickers

app = dash.Dash(__name__)

engine = sqlalchemy.create_engine("sqlite:///db.sqlite")
nsdq = pd.read_csv('tickers.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{} {}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})


app.layout = html.Div([
    
    html.H1('Stock Ticker Dashboard'),
    html.Div(children=[
        html.H3('Enter a stock symbol:'),
        dcc.Dropdown(
              className='stock-picker',
              id='my_stock_picker',
              options= options,
              value=['AAPL'],
              multi=True,
              )
              ]),
    html.Div(className='date-picker', children=[
        html.Div([html.H3('Select a start and end date:'), 
                 dcc.DatePickerRange(id='my_date_picker',
                                    min_date_allowed=datetime(2015,1,1),
                                    max_date_allowed=datetime.today(),
                                    start_date = datetime(2018, 1, 1),
                                    end_date = datetime.today())

        ],),
    html.Div([
        html.Button(id='submit-button',
                    className='button',
                    n_clicks=0,
                    children='Submit',
                    )
    ],)]),
    
    dcc.Graph(id='my_graph',
                figure={'data':[
                    {'x':[1,2], 'y':[3,1]}
                ], 'layout':{'title': ''}})       
])

@app.callback(Output('my_graph', 'figure'),
            [Input('submit-button', 'n_clicks')],
            [State('my_stock_picker', 'value'),
             State('my_date_picker', 'start_date'),
             State('my_date_picker', 'end_date')
             ])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    traces = []
    for tic in stock_ticker:
        sql_DF = pd.read_sql_table(tic,
                                index_col='Date',
                                con=engine)
        sql_DF = sql_DF.loc[start:end]
        traces.append({'x':sql_DF.index, 'y': sql_DF['Close'], 'name': tic})
    fig = {'data': traces,
            'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
          }
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)