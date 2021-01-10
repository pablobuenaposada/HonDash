import threading

import gpsd

CONNECTION_RETRIES = 10


class Gps:
    def __init__(self):
        self.packet = None
        self.status = False

        tries = 0
        while not self.status and tries < CONNECTION_RETRIES:
            conn = gpsd.connect()
            if conn is not None:
                self.status = True
            tries += 1
        threading.Thread(target=self._update).start()

    @property
    def speed(self):
        try:
            return self.packet.speed()
        except (AttributeError, gpsd.NoFixError):
            return -1

    def _update(self):
        try:
            while self.status:
                self.packet = gpsd.get_current()
        except UserWarning:
            self.__init__()
