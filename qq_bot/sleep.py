import datetime
import time


def sleep_until_enabled():
    while not active():
        time.sleep(10)


def active():
    t = datetime.datetime.now().time()
    if t < datetime.time(11, 7, 0):
        return False
    if t > datetime.time(21, 0, 0):
        return False
    return True
