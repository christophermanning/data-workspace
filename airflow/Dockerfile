FROM apache/airflow:slim-2.10.4

ENV DUCKDB_VERSION=1.2.1

ENV AIRFLOW__DATABASE__LOAD_DEFAULT_CONNECTIONS=False
ENV AIRFLOW__CORE__LOAD_EXAMPLES=False
ENV _AIRFLOW_DB_MIGRATE=True
ENV _AIRFLOW_WWW_USER_CREATE=True
ENV _AIRFLOW_WWW_USER_PASSWORD=admin

USER root
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential libpq-dev wget unzip \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# install required duckdb extensions in the image to avoid downloading the extension on each docker run
RUN wget https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip \
    && mv duckdb /usr/local/bin/ \
    && rm duckdb_cli-linux-aarch64.zip
RUN duckdb -c "INSTALL spatial"

USER airflow

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN python -m pip install --force-reinstall -v "duckdb==${DUCKDB_VERSION}"

USER root
COPY entrypoint.sh /
RUN chown airflow /entrypoint.sh
RUN chmod u+x /entrypoint.sh
USER airflow

EXPOSE 8080
