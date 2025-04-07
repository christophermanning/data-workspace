FROM apache/superset:4.1.2

ENV DUCKDB_VERSION=1.2.1

RUN pip install duckdb==${DUCKDB_VERSION}
RUN pip install duckdb-engine

USER root
COPY entrypoint.sh /
RUN chown superset /entrypoint.sh
RUN chmod u+x /entrypoint.sh

USER superset

EXPOSE 8088
