#!/bin/bash

# initialize superset database
superset fab create-admin \
    --username admin \
    --firstname admin \
    --lastname admin \
    --email admin@example.com \
    --password admin && \
superset db upgrade && superset init

# create database connection to local DuckDB database
superset set-database-uri -d DuckDB -u duckdb:////duckdb/dev.duckdb

# start superset
/usr/bin/run-server.sh
