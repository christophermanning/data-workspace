from datetime import datetime
import duckdb
from urllib.parse import urlparse

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
def chicago_libraries():
    @task()
    def load(filename, table):
        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql(
                f"""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE OR REPLACE TABLE raw.{table} AS
                SELECT * FROM read_csv('{filename}', delim = ',', header = true)
            """
            )

    files = {
        # https://data.cityofchicago.org/Education/Libraries-Locations-Contact-Information-and-Usual-/x8fc-8rcq
        "chicago_libraries": "https://data.cityofchicago.org/resource/x8fc-8rcq.csv",
    }

    for table, uri in files.items():
        extension = urlparse(uri).path.split(".")[1]
        filename = f"/data/{table}.{extension}"
        extract_task = ExtractOperator(
            task_id=f"extract-{table}",
            uri=f"{uri}",
            filename=filename,
            trigger_rule="none_failed",
        )
        load_task = load.override(task_id=f"load-{table}", trigger_rule="none_failed")(
            filename, table
        )
        extract_task >> load_task

    HttpOperator(
        task_id="transform",
        http_conn_id="dbt",
        endpoint="run",
        data={"select": "*chicago__libraries*"},
        log_response=True,
    )


chicago_libraries()
