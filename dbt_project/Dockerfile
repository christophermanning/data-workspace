FROM python:3.12.4-slim

ENV DUCKDB_VERSION=1.1.2

RUN apt-get update && apt-get install -y wget unzip

RUN python -m pip install --upgrade pip

# install required duckdb extensions in the image to avoid downloading the extension on each docker run
RUN wget https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip \
    && mv duckdb /usr/local/bin/
RUN duckdb -c "INSTALL spatial"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN python -m pip install --force-reinstall -v "duckdb==${DUCKDB_VERSION}"

COPY profiles.example.yml /root/.dbt/profiles.yml

WORKDIR /dbt_project
