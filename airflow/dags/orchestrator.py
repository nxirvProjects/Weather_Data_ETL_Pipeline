"""
Purpose here is that airflow should call main() every 5 minutes, which will then fetch weather data and insert it into postgres
"""


import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

sys.path.append('/opt/airflow/api-request')


def safe_main_callable():
    from insert_records import main
    return main()

default_args = {
    'description': 'A DAG to orchestrate data',
    'start_date': datetime(2024, 4, 30),
    'catchup': False
}

dag = DAG(
    dag_id='weather-api-orchestrator',
    default_args=default_args,
    schedule=timedelta(minutes=5)
)

with dag:
    task1 = PythonOperator(
        task_id = 'ingest_data_task', 
        python_callable=safe_main_callable
    )
    # task2

