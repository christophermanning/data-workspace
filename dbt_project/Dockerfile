FROM python:3.12.4-slim

RUN apt-get update && apt-get install -y wget unzip

RUN python -m pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# install required duckdb extensions in the image to avoid downloading the extension on each docker run
RUN wget https://github.com/duckdb/duckdb/releases/download/v1.1.1/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip \
    && mv duckdb /usr/local/bin/
RUN duckdb -c "INSTALL spatial"

COPY profiles.example.yml /root/.dbt/profiles.yml

WORKDIR /dbt_project
