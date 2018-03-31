import datetime
import cPickle as pickle
import threading
from controller.Global import *


class Odometer:
    def __init__(self):
        self.lastTime = datetime.datetime.now()
        self.lastSpeed = 0
        try:
            self.total = pickle.load(open("saveOdo.p", "rb"))
        except Exception, e:
            self.total = 0
        self.save_traveled()

    def save_traveled(self):
        threading.Timer(Global.odometerTimer, self.save_traveled).start()
        pickle.dump(self.total, open("saveOdo.p", "wb"))

    def getValue(self, speed):
        try:
            now = datetime.datetime.now()
            diff = (now - self.lastTime).microseconds + (now - self.lastTime).seconds * 1000000
            kmTraveled = (speed / 3600000000.0) * diff
            self.lastTime = now
            self.lastSpeed = speed
            self.total = self.total + kmTraveled
            # pickle.dump(self.total,open("saveOdo.p", "wb" ))
            '''with open('mileage', 'r+') as f:
			total = float(f.readline())
			f.seek(0) 
			f.truncate()
			f.write(str(total+kmTraveled))
			f.close()	
		return int(total+kmTraveled)'''
            return int(self.total)
        except Exception, e:
            print str(e)
            # with open('mileage', 'r+') as f:
            #        f.seek(0)
            #        f.truncate()
            #        f.write("43")
            return 43
