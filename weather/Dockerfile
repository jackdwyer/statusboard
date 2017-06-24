FROM python:2-alpine

RUN mkdir -p /opt/weather/static
COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

COPY static/ /opt/weather/static/
COPY app.py lib.py worker.py /opt/weather/

WORKDIR /opt/weather/
