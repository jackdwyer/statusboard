FROM python:2-alpine

RUN apk update && apk add curl make

RUN mkdir -p /opt/mta-static/google_transit
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY app.py lib.py Makefile /opt/mta-static/

WORKDIR /opt/mta-static

RUN make get-latest-static-data
RUN make generate_schedule
