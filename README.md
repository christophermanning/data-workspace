# data-workspace

An example workspace for data engineering, data analytics, and data science development.

## Components

- Docker
- Docker Compose
- dbt
- DuckDB
- Jupyter

## Running

- `make dev` to start a tmux session with windows for vim and docker-compose to run the services
- `make shell` to open an console for interacting with `dbt`
- `make dbt-build` to run `dbt build`
- `make dbt-test` to run `dbt test`
- `make format` to autoformat sql files with sqlfluff
