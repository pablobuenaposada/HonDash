import time


class Time:
    def __init__(self):
        self.initial_time = time.time()

    @property
    def time(self):
        now = time.time() - self.initial_time
        return str(time.gmtime(now)[3]).zfill(2) + ":" + str(time.gmtime(now)[4]).zfill(2) + ":" + str(
            time.gmtime(now)[5]).zfill(2)

    def get_time(self):
        return self.time

    def get_time2(self, r):
        return self.time
