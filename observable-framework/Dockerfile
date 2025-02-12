FROM node:22-bookworm-slim

RUN apt update

# install duckdb for analysis and data transformations
RUN apt install -y wget unzip
RUN wget https://github.com/duckdb/duckdb/releases/download/v0.10.3/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip \
    && mv duckdb /usr/local/bin/

# sqlite3 for build exports
RUN apt install -y sqlite3

# must be specified before npm install
WORKDIR /app

COPY package*.json .
RUN npm ci
ENV PATH $PATH:node_modules/.bin

EXPOSE 3000
