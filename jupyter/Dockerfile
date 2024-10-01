# https://docs.docker.com/guides/use-case/jupyter/#define-your-environment-in-a-dockerfile
FROM quay.io/jupyter/base-notebook

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir black black[jupyter] duckdb ipywidgets ipyleaflet pandas matplotlib
