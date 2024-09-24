from datetime import datetime
import duckdb
import urllib
import os

from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.hooks.base_hook import BaseHook
from airflow.exceptions import AirflowSkipException
from airflow.providers.http.operators.http import HttpOperator

@dag(
    schedule=None,
    start_date=datetime(2024, 1, 1),
)
def bikeshare():
    @task()
    def extract(uri, filename):
        if os.path.isfile(filename):
            raise AirflowSkipException()
            return

        urllib.request.urlretrieve(uri, filename)

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

    extract(uri, filename)
    load(filename)
    HttpOperator(task_id="transform", http_conn_id="dbt", endpoint="run", data={"select":"bikeshare"}, log_response=True)

bikeshare()
