FROM ubuntu:latest

ENV DUCKDB_VERSION=1.2.1

RUN apt-get update && apt-get install -y wget unzip

RUN wget https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip \
    && mv duckdb /usr/local/bin/ \
    && rm duckdb_cli-linux-aarch64.zip

WORKDIR /duckdb

EXPOSE 4213
