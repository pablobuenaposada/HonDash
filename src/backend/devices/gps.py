from concurrent.futures import TimeoutError

import gpsd
from pebble import concurrent


@concurrent.process(timeout=2)
def connect():
    gpsd.connect()


class Gps:
    def __init__(self):
        try:
            connect().result()
        except (TimeoutError, ConnectionRefusedError):
            pass

    @property
    def status(self):
        try:
            if len(gpsd.state["devices"]["devices"]) > 0:
                return True
        except KeyError:
            return False

    @property
    def speed(self):
        if self.status:
            return gpsd.speed()
        return 0
