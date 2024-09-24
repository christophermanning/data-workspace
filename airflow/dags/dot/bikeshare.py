from datetime import datetime
import duckdb

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.http.operators.http import HttpOperator

from extract_operator import ExtractOperator

@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1),
)
def bikeshare():
    @task()
    def load(filename):
        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql(f"""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE OR REPLACE TABLE raw.bikeshare AS
                SELECT * FROM read_csv('{filename}', delim = ',', header = true)
            """)

    filename = "/data/bikeshare.csv"
    # https://data.bts.gov/Bicycles-and-Pedestrians/Locations-of-Docked-Bikeshare-Stations-by-System-a/7m5x-ubud/about_data
    uri = "https://data.bts.gov/resource/7m5x-ubud.csv?$limit=70000"

    ExtractOperator(task_id="extract", uri=uri, filename=filename)
    load(filename)
    HttpOperator(task_id="transform", http_conn_id="dbt", endpoint="run", data={"select":"bikeshare"}, log_response=True)

bikeshare()
