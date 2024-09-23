FROM apache/airflow:slim-2.10.2

ENV AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=False
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV _AIRFLOW_DB_MIGRATE=True
ENV _AIRFLOW_WWW_USER_CREATE=True
ENV _AIRFLOW_WWW_USER_PASSWORD=admin

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
        build-essential libpq-dev \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

# psycopg2 needed to connect to a postgresql database
RUN pip install --no-cache-dir psycopg2 duckdb

USER root
COPY entrypoint.sh /
RUN chown airflow /entrypoint.sh
RUN chmod u+x /entrypoint.sh
USER airflow

EXPOSE 8080
