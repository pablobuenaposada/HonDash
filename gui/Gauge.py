from Tkinter import *
import math
from Text import *


class Gauge:
    def __init__(self, canvas, x, y, r, start_gauge, end_gauge, step_value, num_mid_lines, max_value, value_color, value_size,
                 value_font, value_weight, small_marks_height, small_marks_width, small_marks_color, big_marks_height,
                 big_marks_width, big_marks_color, needle_tip, needle_base_width, needle_color, needle_stipple,
                 needle_cover_diameter, needle_cover_color, update_class=None, update_function=None, update_args=None):
        self.needleArrow = None
        self.needleBase = None
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.update_function = update_function
        self.update_class = update_class
        self.update_args = update_args
        self.max_value = max_value
        self.startGauge = start_gauge
        self.endGauge = end_gauge
        self.needleBaseWidth = needle_base_width
        self.needleTip = needle_tip
        self.needleColor = needle_color
        self.needleStipple = needle_stipple
        self.idMarks = []
        self.idValues = []

        for i in range(0, self.max_value + 1, step_value):
            degree = self.startGauge + ((i * self.endGauge) / self.max_value)
            start_x = x + (r - big_marks_height) * math.cos(math.radians(degree))
            start_y = y + (r - big_marks_height) * math.sin(math.radians(degree))
            final_x = x + r * math.cos(math.radians(degree))
            final_y = y + r * math.sin(math.radians(degree))
            self.idMarks.append(
                canvas.create_line(start_x, start_y, final_x, final_y, fill=big_marks_color, width=big_marks_width, smooth=0))
            letter_x = x + (r - (big_marks_height + (value_size * 0.75))) * math.cos(math.radians(degree))
            letter_y = y + (r - (big_marks_height + (value_size * 0.75))) * math.sin(math.radians(degree))
            self.idValues.append(
                Text(canvas, letter_x, letter_y, value_font, value_size, value_weight, value_color, "", "", str(i)))

            next_degree = self.startGauge + (((i + step_value) * self.endGauge) / self.max_value)
            if i < self.max_value:
                step = (next_degree + 1 - degree) / (num_mid_lines + 1.0)
                for j in range(0, num_mid_lines + 1, 1):
                    start_x = self.x + (r - small_marks_height) * math.cos(math.radians(degree + (j * step)))
                    start_y = self.y + (r - small_marks_height) * math.sin(math.radians(degree + (j * step)))
                    final_x = self.x + r * math.cos(math.radians(degree + (j * step)))
                    final_y = self.y + r * math.sin(math.radians(degree + (j * step)))
                    self.idMarks.append(
                        canvas.create_line(start_x, start_y, final_x, final_y, fill=small_marks_color, width=small_marks_width))

        # needle cover
        self.needleCover = canvas.create_oval(x - (needle_cover_diameter / 2), y - (needle_cover_diameter / 2),
                                              x + (needle_cover_diameter / 2), y + (needle_cover_diameter / 2),
                                              fill=needle_cover_color)

    def set_value(self, value):
        self.canvas.delete(self.needleArrow)
        self.canvas.delete(self.needleBase)

        speed = self.startGauge + ((value * self.endGauge) / self.max_value)
        finalx = self.x + self.r * math.cos(math.radians(speed))
        finaly = self.y + self.r * math.sin(math.radians(speed))

        self.needleArrow = self.canvas.create_line([self.x, self.y, finalx, finaly], fill=self.needleColor,
                                                   arrow="last", arrowshape=(self.r, self.r, self.needleBaseWidth),
                                                   stipple=self.needleStipple)
        self.needleBase = self.canvas.create_line([self.x, self.y, finalx, finaly], fill=self.needleColor,
                                                  width=self.needleTip, stipple=self.needleStipple)

        self.canvas.tag_raise(self.needleCover)
        self.canvas.pack()

    def set_needle_cover_color(self, color):
        self.canvas.itemconfig(self.needleCover, fill=color)

    def set_color(self, color):
        for mark in self.idMarks:
            self.canvas.itemconfig(mark, fill=color)

        for number in self.idValues:
            number.set_color(color)

    def update(self):
        if self.update_function is not None and self.update_args is None:
            self.set_value(getattr(self.update_class, self.update_function)())
        if self.update_function is not None and self.update_args is not None:
            self.set_value(getattr(self.update_class, self.update_function)(*self.update_args))