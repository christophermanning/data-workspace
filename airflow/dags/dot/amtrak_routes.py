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
def amtrak_routes():
    @task()
    def load(filename):
        dbpath = BaseHook.get_connection("duckdb_dev").host
        with duckdb.connect(dbpath) as conn:
            conn.sql(
                f"""
                INSTALL spatial;
                LOAD spatial;
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE OR REPLACE TABLE raw.amtrak_routes AS
                SELECT * FROM ST_Read('{filename}')
            """
            )

    filename = "/data/amtrak_routes.geojson"
    # https://geodata.bts.gov/datasets/usdot::amtrak-routes/explore
    uri = "https://services.arcgis.com/xOi1kZaI0eWDREZv/arcgis/rest/services/NTAD_Amtrak_Routes/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

    ExtractOperator(task_id="extract", uri=uri, filename=filename)
    load(filename)
    HttpOperator(
        task_id="transform",
        http_conn_id="dbt",
        endpoint="run",
        data={"select": "*amtrak_routes*"},
        log_response=True,
    )


amtrak_routes()
