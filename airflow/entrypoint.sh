#!/bin/bash
# the airflow image must be rebuilt when this file changes

airflow connections add 'duckdb_dev' \
    --conn-type 'generic' \
    --conn-host '/duckdb/dev.duckdb'

airflow standalone
