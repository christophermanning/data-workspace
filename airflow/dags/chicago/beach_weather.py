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
def beach_weather():
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
        # https://data.cityofchicago.org/Parks-Recreation/Beach-Water-and-Weather-Sensor-Locations/g3ip-u8rb/
        "chicago_beach_weather_stations": "https://data.cityofchicago.org/resource/g3ip-u8rb.csv",
        # https://data.cityofchicago.org/Parks-Recreation/Beach-Weather-Stations-Automated-Sensors/k7hf-8y75/
        "chicago_beach_weather_measurements": "https://data.cityofchicago.org/resource/k7hf-8y75.csv?$limit=200000",
        # https://data.cityofchicago.org/Parks-Recreation/Beach-Water-Quality-Automated-Sensors/qmqz-2xku/
        "chicago_beach_water_measurements": "https://data.cityofchicago.org/resource/qmqz-2xku.csv?$limit=50000",
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
        data={"select": "*beach_weather*"},
        log_response=True,
    )


beach_weather()
