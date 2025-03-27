# data-workspace

A workspace for data engineering, data analytics, and data science workflows.

## Architecture

![](/goat/architecture.svg)

## Components

- Airflow
  - http://localhost:8080/home
- Jupyter
  - http://localhost:8888/lab
- Docker and Docker Compose
- dbt
- DuckDB
- Observable Framework
  - http://localhost:3000

## Running

- `make dev` to start a tmux session with windows for vim and docker-compose to run the services
- `make shell` to open an console for interacting with `dbt`
- `make dbt-build` to run `dbt build`
- `make dbt-test` to run `dbt test`
- `make format` to autoformat sql files with sqlfluff
- http://localhost:3000 to list services

## Notes

- Geo data is stored in the EPSG:3857 format i.e. `POINT(longitude, lattitude)`
