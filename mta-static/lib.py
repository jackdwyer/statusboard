import csv
import datetime
import pickle
import os
import time
from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

DEFAULT_STOP = "G30"

STOPTIMES_FILE = 'google_transit/stop_times.txt'
GENERATED_SCHEDULE = 'schedule.pkl'


def generate_week(date=datetime.datetime.now(), num_days=7):
    """
    generates weeks worth of arrow (datetime) objects, starting at the
    next sunday
    """
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    sunday_diff = 6 - date.weekday()
    start_date = date + datetime.timedelta(days=sunday_diff)
    week = list()
    for i in range(0, num_days):
        week.append(start_date + datetime.timedelta(days=i))
    return week


def get_schedule():
    if not os.path.isfile(GENERATED_SCHEDULE):
        print("Loading schedule in...")
        start_time = time.time()
        schedule = load_schedule()
        with open(GENERATED_SCHEDULE, 'wb') as f:
            pickle.dump(schedule, f)
        print("time taken: {}".format(time.time() - start_time))

    with open(GENERATED_SCHEDULE, 'rb') as f:
        schedule = pickle.load(f)

    return schedule


# trip_id, arrival_time, departure_time, stop_id
def load_schedule():
    schedule = dict()
    with open(STOPTIMES_FILE) as f:
        schedule_reader = csv.DictReader(f)
        for row in schedule_reader:
            direction = row['stop_id'][-1]
            # remove N/S bound
            stop_id = row['stop_id'][:-1]
            # who cares about every line, so just skip not G30
            if stop_id != DEFAULT_STOP:
                continue
            arrival_time = parse_arrival_time(row['arrival_time'])
            trip_type = parse_trip_id(row['trip_id'])
            try:
                schedule[stop_id][trip_type][direction].append(arrival_time)
            except KeyError:
                schedule[stop_id] = {"weekday": {"N": [], "S": []},
                                     "saturday": {"N": [], "S": []},
                                     "sunday": {"N": [], "S": []}}
                schedule[stop_id][trip_type][direction].append(arrival_time)
    # sort the schedules
    # TODO: convert to tuple
    for stop in schedule:
        schedule[stop]['weekday']['N'].sort()
        schedule[stop]['weekday']['S'].sort()
        schedule[stop]['saturday']['S'].sort()
        schedule[stop]['saturday']['N'].sort()
        schedule[stop]['sunday']['S'].sort()
        schedule[stop]['sunday']['N'].sort()
    return schedule


def parse_arrival_time(time):
    # takes time string, returns datetime.time object
    # TODO: ahh so this is shit, doesn't deal with WKD->SAT etc
    # https://developers.google.com/transit/gtfs/reference/stop_times-file
    # probably shouldnt use datetime.time :cry:, yeah defs should be datetime
    if time.split(":")[0] == '24':
        time = time.replace('24', '00', 1)
    if time.split(":")[0] == '25':
        time = time.replace('25', '01', 1)
    if time.split(":")[0] == '26':
        time = time.replace('26', '02', 1)
    if time.split(":")[0] == '27':
        time = time.replace('27', '03', 1)
    return datetime.datetime.strptime(time, "%H:%M:%S").time()


def parse_trip_id(trip_id):
    # returns human readable name
    if trip_id.split('_')[0][-3:] == 'SUN':
        return 'sunday'
    if trip_id.split('_')[0][-3:] == 'SAT':
        return 'saturday'
    if trip_id.split('_')[0][-3:] == 'WKD':
        return 'weekday'


# http://flask.pocoo.org/snippets/56/
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


if __name__ == "__main__":
    get_schedule()
