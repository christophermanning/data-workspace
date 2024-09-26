from datetime import datetime
import duckdb
import json

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
def divvy_stations():
    @task()
    def load(filename):
        json_rows = []
        with open(filename) as f:
            json_data = json.load(f)
            for feature in json_data["data"]["stations"]:
                json_rows.append(feature)

        json_filename = filename.replace("json", "transformed.json")
        with open(json_filename, "w") as f:
            json.dump(json_rows, f)

        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql(
                f"""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE OR REPLACE TABLE raw.divvy_stations AS
                SELECT * FROM read_json('{json_filename}')
            """
            )

    filename = "/data/station_information.json"

    # https://divvybikes.com/system-data
    # this station information only includes current stations
    uri = "https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json"

    ExtractOperator(task_id="extract", uri=uri, filename=filename)
    load(filename)
    HttpOperator(
        task_id="transform",
        http_conn_id="dbt",
        endpoint="run",
        data={"select": "*divvy*"},
        log_response=True,
    )


divvy_stations()
