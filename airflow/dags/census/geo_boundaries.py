from datetime import datetime
import duckdb
import zipfile
import geopandas
import csv
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
def census_geo_boundaries():
    @task()
    def load(filename, table):
        basedir = "/data/census_geo_boundaries"
        destprefix = f"{basedir}/cb_2023_us_state_500k"
        with zipfile.ZipFile(filename, "r") as zipf:
            zipf.extractall(basedir)

        shpfile = geopandas.read_file(f"{destprefix}.shp")
        feature_collection = shpfile.to_geo_dict()

        rows = [["id", "geom"]]
        for feature in feature_collection["features"]:
            if feature["properties"]["STUSPS"] == "IL":
                rows.append(
                    [feature["properties"]["STUSPS"], json.dumps(feature["geometry"])]
                )

        dbpath = BaseHook.get_connection("duckdb_dev").host

        filename = f"{destprefix}.csv"
        with open(filename, "w") as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        with duckdb.connect(dbpath) as conn:
            conn.sql(
                f"""
                CREATE SCHEMA IF NOT EXISTS raw;
                CREATE OR REPLACE TABLE raw.census_geo_boundaries AS
                SELECT * FROM read_csv('{filename}', delim = ',', header = true)
            """
            )

    # https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
    uri = "https://www2.census.gov/geo/tiger/GENZ2023/shp/cb_2023_us_state_500k.zip"
    filename = uri.split("/")[-1]
    extract_task = ExtractOperator(
        task_id=f"extract",
        uri=uri,
        filename=filename,
        trigger_rule="none_failed",
    )

    load_task = load.override(task_id=f"load", trigger_rule="none_failed")(
        filename, "census_geo_boundaries"
    )

    transform_task = HttpOperator(
        task_id="transform",
        http_conn_id="dbt",
        endpoint="run",
        data={"select": "*census* *boundaries*"},
        log_response=True,
    )

    extract_task >> load_task >> transform_task


census_geo_boundaries()
