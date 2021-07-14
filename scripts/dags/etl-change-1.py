from airflow import DAG
from airflow.contrib.operators.snowflake_operator import SnowflakeOperator
from airflow.operators.bash_operator import BashOperator
import os, sys, json
import pandas as pd
import pendulum
# other packages
from datetime import datetime
from datetime import timedelta
local_tz = pendulum.timezone("America/Mexico_City")

PWD = os.environ['pWD']
default_args = {
    'owner': 'lomnbda',
    'depends_on_past': False,
    'start_date': datetime(2021, 7, 13, tzinfo=local_tz),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
    }

dag = DAG(
  dag_id='etl-challenge-1',
  description='dataset-snoflake',
  schedule_interval='0 9 * * *',
  default_args=default_args)

get_csv = BashOperator(
    task_id='get-data-set',
    bash_command= "python3 $pWD/scripts/etl-challenge-1/xscript.py 'download_data'",
    provide_context=True,
    dag=dag)

create_insert = BashOperator(
    task_id='create-insert-file',
    bash_command= "python3 $pWD/scripts/etl-challenge-1/xscript.py 'create_insert'",
    provide_context=True,
    dag=dag)

load_snowflake = SnowflakeOperator(
    task_id='load-data-snowflake',
    sql='/etl-challenge-1/data.sql',
    snowflake_conn_id='snowflake_connection',
    dag=dag
)

get_csv >> create_insert >> load_snowflake

if __name__ == "__main__":

  dag.cli()
