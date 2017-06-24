import datetime
import json
import logging
import os
import requests
import redis
import time


logger = logging.getLogger('worker')
fmt_str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(fmt_str)
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

r = redis.StrictRedis(host='redis')

FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
CURRENT_URL = "http://api.openweathermap.org/data/2.5/weather"
TIMEOUT = 60


def get_current(city_id, api_token):
    logger.info("weather current update")
    payload = {'id': city_id, 'APPID': api_token, 'units': 'metric'}
    resp = requests.get(CURRENT_URL, params=payload)
    data = resp.json()
    data[u'last_updated'] = unicode(datetime.datetime.now())
    r.set("weather_current", json.dumps(data))


def get_forecast(city_id, api_token):
    logger.info("weather forecast update")
    payload = {'id': city_id, 'APPID': api_token}
    resp = requests.get(FORECAST_URL, params=payload)
    data = resp.json()
    data[u'last_updated'] = unicode(datetime.datetime.now())
    r.set("weather_forecast", json.dumps(data))


if __name__ == '__main__':
    logger.info("Weather worker has started")
    city_id = os.environ['CITY_ID']
    api_token = os.environ['OPENWEATHERMAP_API_TOKEN']
    while True:
        logger.info("Starting update of weather")
        get_forecast(city_id, api_token)
        get_current(city_id, api_token)
        time.sleep(TIMEOUT)
