from datetime import datetime
import duckdb
import json
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
def divvy_stations():
    @task()
    def load(filename, table, partition):
        json_rows = []
        with open(filename) as f:
            json_data = json.load(f)
            key = list(json_data["data"].keys())[0]
            for feature in json_data["data"][key]:
                json_rows.append(feature)

        json_filename = filename.replace("json", "transformed.json")
        with open(json_filename, "w") as f:
            json.dump(json_rows, f)

        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql("CREATE SCHEMA IF NOT EXISTS raw")

            if table == "bikes":
                conn.sql(
                    f"""
                    CREATE TABLE IF NOT EXISTS raw.{table} (
                        partition VARCHAR,
                        is_reserved INTEGER,
                        vehicle_type_id INTEGER,
                        is_disabled INTEGER,
                        lon DECIMAL(11,9),
                        rental_uris JSON,
                        current_range_meters DECIMAL(9,4),
                        bike_id VARCHAR,
                        lat DECIMAL(11,9),
                        PRIMARY KEY (partition, bike_id)
                    )
                """
                )

                query = f"""
                    INSERT OR REPLACE INTO raw.{table}
                    SELECT '{partition}' as partition, *
                    FROM read_json('{json_filename}', columns = {{
                        'is_reserved': 'INTEGER',
                        'vehicle_type_id': 'INTEGER',
                        'is_disabled': 'INTEGER',
                        'lon': 'DECIMAL(11,9)',
                        'rental_uris': 'JSON',
                        'current_range_meters': 'DECIMAL(9,4)',
                        'bike_id': 'VARCHAR',
                        'lat': 'DECIMAL(11,9)'
                    }})
                """
                conn.sql(query)
            else:
                conn.sql(
                    f"""
                    CREATE OR REPLACE TABLE raw.{table} AS
                    SELECT * FROM read_json('{json_filename}')
                """
                )

    # GBFS JSON feeds for realtime data
    # https://divvybikes.com/system-data
    files = {
        # monthly cache
        # the v1 file has additional metadata
        f"station_information.{datetime.now().strftime('%Y-%m')}": "https://gbfs.lyft.com/gbfs/2.3/chi/en/station_information.json",
        f"station_information_v1.{datetime.now().strftime('%Y-%m')}": "https://gbfs.lyft.com/gbfs/1.1/chi/en/station_information.json",
        # hourly cache
        # undocked ebikes/scooters
        f"bikes.{datetime.now().strftime('%Y-%m-%dT%H')}": "https://gbfs.lyft.com/gbfs/2.3/chi/en/free_bike_status.json",
    }

    load_tasks = []

    for basename, uri in files.items():
        extension = urlparse(uri).path.split(".")[-1]
        filename = f"/data/{basename}.{extension}"

        table, partition = basename.split(".")

        extract_task = ExtractOperator(
            task_id=f"extract-{table}",
            uri=f"{uri}",
            filename=filename,
            trigger_rule="none_failed",
        )
        load_task = load.override(task_id=f"load-{table}", trigger_rule="none_failed")(
            filename, table, partition
        )

        extract_task >> load_task
        load_tasks.append(load_task)

    http_task = HttpOperator(
        task_id="transform",
        http_conn_id="dbt",
        endpoint="run",
        data={"select": "*divvy*"},
        log_response=True,
    )

    load_tasks >> http_task


divvy_stations()
