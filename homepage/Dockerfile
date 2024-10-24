FROM python:3.12.4-slim

RUN python -m pip install --upgrade pip

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /src

EXPOSE 3000
