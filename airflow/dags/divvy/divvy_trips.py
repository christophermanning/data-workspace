from datetime import datetime
import duckdb
import zipfile
import os

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
def divvy_trips():
    dbpath = BaseHook.get_connection("duckdb_dev").host

    @task()
    def setup():
        with duckdb.connect(dbpath) as conn:
            result = conn.sql(
                f"""
                CREATE SCHEMA IF NOT EXISTS raw;

                CREATE TABLE IF NOT EXISTS raw.divvy_trips (
                    ride_id VARCHAR PRIMARY KEY,
                    rideable_type VARCHAR,
                    started_at TIMESTAMP,
                    ended_at TIMESTAMP,
                    start_station_name VARCHAR,
                    start_station_id VARCHAR,
                    end_station_name VARCHAR,
                    end_station_id VARCHAR,
                    start_lat DOUBLE,
                    start_lng DOUBLE,
                    end_lat DOUBLE,
                    end_lng DOUBLE,
                    member_casual VARCHAR,
                )
            """
            )

    @task()
    def load(filename):
        with zipfile.ZipFile(filename, "r") as zipf:
            zipf.extractall("/data/divvy")

        csv_file = f"/data/divvy/{os.path.basename(filename).replace('zip', 'csv')}"

        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql(
                f"""
                INSERT OR REPLACE INTO raw.divvy_trips
                SELECT * FROM read_csv('{csv_file}', delim = ',', header = true)
            """
            )
            print(f"{conn.rowcount} rows inserted/updated")

    setup_task = setup()

    extract_task = None
    transform_task = None

    # https://divvybikes.com/system-data
    files = [
        "202408-divvy-tripdata.zip",
        "202407-divvy-tripdata.zip",
        "202406-divvy-tripdata.zip",
        "202405-divvy-tripdata.zip",
        "202404-divvy-tripdata.zip",
        "202403-divvy-tripdata.zip",
    ]
    for file in files:
        filename = f"/data/{file}"
        extract_task = ExtractOperator(
            task_id=f"extract-{file}",
            uri=f"https://divvy-tripdata.s3.amazonaws.com/{file}",
            filename=filename,
            trigger_rule="none_failed",
        )
        load_task = load.override(task_id=f"load-{file}", trigger_rule="none_failed")(
            filename
        )
        setup_task >> extract_task >> load_task

    transform_task = HttpOperator(
        task_id="transform",
        http_conn_id="dbt",
        endpoint="run",
        data={"select": "*divvy*"},
        log_response=True,
        trigger_rule="none_failed",
    )

    setup_task >> extract_task >> load_task >> transform_task


divvy_trips()
