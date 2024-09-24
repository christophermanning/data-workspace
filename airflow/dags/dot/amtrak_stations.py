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
def amtrak_stations():
    @task()
    def load(filename):
        json_rows = []
        with open(filename) as f:
            json_data = json.load(f)
            for feature in json_data["features"]:
                json_rows.append(feature['attributes'])

        new_filename = filename.replace('json','transformed.json')
        with open(new_filename, 'w') as f:
            json.dump(json_rows, f)

        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql(f"""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE OR REPLACE TABLE raw.amtrak_stations AS
                SELECT * FROM read_json('{new_filename}')
            """)

    filename = "/data/amtrak_stations.json"
    # https://geodata.bts.gov/datasets/usdot::amtrak-stations/api
    uri = "https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_Amtrak_Stations/FeatureServer/0/query?where=1%3D1&outFields=*&returnGeometry=false&outSR=4326&f=json"

    ExtractOperator(task_id="extract", uri=uri, filename=filename)
    load(filename)
    HttpOperator(task_id="transform", http_conn_id="dbt", endpoint="run", data={"select":"amtrak_stations"}, log_response=True)

amtrak_stations()
