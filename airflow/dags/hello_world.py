from datetime import datetime
import duckdb

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.hooks.base_hook import BaseHook

@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1),
)
def hello_world():
    """
    ### Hello World
    Basic test for running a DAG
    """
    @task()
    def db_connection():
        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            print(conn.sql("SHOW TABLES"))

    BashOperator(task_id="hello_world", bash_command="echo 'hello world'")

    db_connection()

hello_world()
