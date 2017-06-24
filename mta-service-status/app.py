import lib
import logging
import json
import redis
from flask import Flask, jsonify
app = Flask(__name__)

r = redis.StrictRedis(host='redis')

app.logger.setLevel(logging.DEBUG)


@app.route('/')
@lib.crossdomain("*")
def index():
    val = r.get("stations")
    if val is not None:
        data = json.loads(val)
        return jsonify(data)
    return 'waiting for refresh/failed refresh', 500


@app.route('/health')
def health():
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
