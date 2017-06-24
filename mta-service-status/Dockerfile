FROM python:2-alpine

ENV TZ America/New_York

RUN apk update && apk add libxslt-dev gcc g++

RUN mkdir -p /opt/mta-service-status-api
COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY app.py config.py lib.py worker.py /opt/mta-service-status-api/

WORKDIR /opt/mta-service-status-api
