import datetime as dt
from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from pandas_datareader.nasdaq_trader import get_nasdaq_symbols
from airflow.models import DAG
from pandas import DataFrame


default_args = {
    'owner': 'Me',
    'depends_on_past': False,
    'start_date': datetime(2015, 6, 1),
    'retries': 3,
    'retry_delay': dt.timedelta(minutes=5),
}

dag = DAG(
    dag_id='init_db',
    default_args=default_args,
    schedule_interval=None,
)

def get_symbols():
    symbols: DataFrame = get_nasdaq_symbols()
    symbols = symbols[['Security Name']]
    symbols.to_csv('nasdaq.csv')

csv_file = PythonOperator(
    task_id='stock_csv',
    python_callable=get_symbols,
    dag=dag)