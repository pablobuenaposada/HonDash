import time

class Time:
    def __init__(self):
        self.tZero = time.time()

    def getTime(self):
        return time.gmtime(time.time()-self.tZero)

    def getTimeString(self):
        now = time.time()-self.tZero
        return str(time.gmtime(now)[3]).zfill(2)+":"+str(time.gmtime(now)[4]).zfill(2)+":"+str(time.gmtime(now)[5]).zfill(2)
