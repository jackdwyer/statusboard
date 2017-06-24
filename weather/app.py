import lib
import logging
import json
import redis
from flask import Flask, jsonify

app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)
r = redis.StrictRedis(host='redis')


@app.route('/')
@lib.crossdomain("*")
def index():
    return 'ok'


@app.route('/current')
@lib.crossdomain("*")
def current():
    val = r.get("weather_current")
    if val is not None:
        data = json.loads(val)
        return jsonify(data)
    return 'waiting for refresh/failed refresh', 500


@app.route('/forecast')
@lib.crossdomain("*")
def forecast():
    val = r.get("weather_forecast")
    if val is not None:
        data = json.loads(val)
        return jsonify(data)
    return 'waiting for refresh/failed refresh', 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
