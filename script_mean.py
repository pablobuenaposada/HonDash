import math
import time
import random
from matplotlib import pyplot
import numpy
from datetime import datetime

window_size = 5
LOSER = 0

def append_buffer(buffer, val):
    buffer += (val,)
    return buffer[-window_size:]

def formula1(volts):
    return volts

def gauge_value1():
    global LOSER
    LOSER += 1
    sin_val = math.sin(4*LOSER/ 10.0)
    noise = random.randint(0, 10) / 10.0
    return sin_val + noise

def running_mean(x, N):
    cumsum = numpy.cumsum(numpy.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)

def buffered_forumla(buffer, volts, formula):
    buffer = append_buffer(buffer, volts)
    raw_val = formula(volts)
    nice_val = running_mean(buffer, window_size)[0]
    return buffer, nice_val

def plot(data_list):
    for data in data_list:
        pyplot.plot(data)
    pyplot.ylabel('some numbers')
    pyplot.show()

def main():
    list_sensors = [
        {
            'sensor': gauge_value1,
            'formula': formula1,
            'buffer': (0,) * window_size,
        },
    ]
    plot_buffer = tuple()
    plot_buffer_raw = tuple()
    for sensors in list_sensors:
        for i in range(200):
            gauge_value = sensors['sensor']
            buffer = sensors['buffer']
            formula = sensors['formula']
            val = gauge_value()
            buffer, nice_val = buffered_forumla(buffer, val, formula)
            sensors['buffer'] = buffer
            plot_buffer += (nice_val,)
            plot_buffer_raw += (val,)
            # print(fe_val)
        # print(plot_buffer)
    plot((plot_buffer, plot_buffer_raw))

main()
