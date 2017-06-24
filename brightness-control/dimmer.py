import collections
import datetime
import serial
import subprocess

debug = False

MAX_BRIGHTNESS = 976
DEFAULT_BRIGHTNESS = 100
SERIAL_TTY = '/dev/ttyUSB0'
NUM_SAMPLES = 1


def log_brightness(value):
    with open("./brightness.txt", "a+") as f:
        f.write("{}, {}\n".format(str(datetime.datetime.now()), value))


def set_display(value):
    brightness = DEFAULT_BRIGHTNESS
    if value < 5:
        brightness = 0
    if value > 5 < 75:
        brightness = 300
    if value > 75:
        brightness = MAX_BRIGHTNESS
    subprocess.call(['./set_display_to.sh', str(brightness)])


if __name__ == '__main__':
    ser = serial.Serial(SERIAL_TTY)
    values = collections.deque(maxlen=NUM_SAMPLES)
    while True:
        val = ser.readline().strip()
        try:
            cur_light = int(val)
        except ValueError:
            print("Failed value: {}".format(val))
            continue
        values.append(cur_light)
        average_value = (sum(values) / len(values))
        if debug:
            log_brightness(average_value)
        set_display(average_value)
