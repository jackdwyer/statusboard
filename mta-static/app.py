#!/usr/bin/env python
import datetime
import lib
from flask import Flask, jsonify


app = Flask(__name__)
schedule = lib.get_schedule()

# only care about G30N weekdays
STATION = "G30"
HEADING = "N"
PERIOD = "weekday"


def get_next(time, schedule=schedule):
    for el in schedule[STATION][PERIOD][HEADING]:
        if el > time:
            date = datetime.datetime.now()
            newdate = date.replace(hour=el.hour,
                                   minute=el.minute, second=el.second)
            return el, newdate
    return schedule[STATION][PERIOD][HEADING][0], datetime.datetime.now()


def get_next_n(num, from_time, schedule=schedule):
    trips = list()
    for i in range(num):
        _next, nice = get_next(from_time)
        trips.append(nice)
        from_time = _next
    return trips


@app.route('/G30')
@lib.crossdomain("*")
def get_upcoming():
    rn = datetime.datetime.now().time()
    trips = [str(x) for x in get_next_n(3, rn)]
    return jsonify({'data': trips})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
