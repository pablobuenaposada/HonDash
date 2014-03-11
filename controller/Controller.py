from Tkinter import *

import devices.Time
import numpy
from controller.Global import *
import locale


class Controller:
    locale.setlocale(locale.LC_ALL, 'en_GB.utf8')

    def __init__(self, canvas):
        self.objects = []
        self.canvas = canvas

    def add_object(self, gui_object):
        self.objects.append(gui_object)

    def _new_update_all(self):
        for gui_object in self.objects:
            gui_object.update()
        self.canvas.after(10, self._new_update_all)

    def start(self):
        self.canvas.after(10, self._new_update_all())

