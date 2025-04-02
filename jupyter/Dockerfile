# https://github.com/jupyter/docker-stacks/blob/main/images/base-notebook/Dockerfile
# https://docs.docker.com/guides/use-case/jupyter/#define-your-environment-in-a-dockerfile
FROM quay.io/jupyter/base-notebook

ENV DUCKDB_VERSION=1.2.1

USER root
RUN apt-get update && apt-get install -y wget unzip
# install required duckdb extensions in the image to avoid downloading the extension on each docker run
RUN wget https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-linux-aarch64.zip \
    && unzip duckdb_cli-linux-aarch64.zip \
    && mv duckdb /usr/local/bin/ \
    && rm duckdb_cli-linux-aarch64.zip
RUN duckdb -c "INSTALL spatial"
USER ${NB_UID}

RUN python -m pip install --upgrade pip
RUN python -m pip install --force-reinstall -v "duckdb==${DUCKDB_VERSION}"

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# disable popups
RUN jupyter labextension disable "@jupyterlab/apputils-extension:announcements"
