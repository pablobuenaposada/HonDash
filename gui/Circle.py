from Text import *


class Circle:
    def __init__(self, canvas, x, y, diameter, width, start_degrees, range_degrees, min_value, max_value, min_wrn_value,
                 max_wrn_value, min_color, normal_color, max_color, font_size, text_size, text_color, text, background_color,
                 update_class=None, update_function=None, update_args=None):
        self.update_function = update_function
        self.update_class = update_class
        self.update_args = update_args
        self.canvas = canvas
        self.minValue = min_value
        self.maxValue = max_value
        self.rangeDegrees = range_degrees
        self.startDegrees = start_degrees
        self.minWrnValue = min_wrn_value
        self.maxWrnValue = max_wrn_value
        self.minColor = min_color
        self.normalColor = normal_color
        self.maxColor = max_color
        self.idBackground = self.canvas.create_arc(x - (diameter / 2), y - (diameter / 2), x + (diameter / 2),
                                                   y + (diameter / 2), style="arc", start=self.startDegrees,
                                                   extent=-self.rangeDegrees, fill="", outline=background_color,
                                                   width=width)
        self.idCircle = self.canvas.create_arc(x - (diameter / 2), y - (diameter / 2), x + (diameter / 2),
                                               y + (diameter / 2), style="arc", start=self.startDegrees,
                                               extent=-self.rangeDegrees, fill="", outline=normal_color, width=width)

        self.idValue = Text(canvas, x, y, "Helvetica", font_size, "bold", text_color, "", "", "80")
        self.idText = Text(canvas, x, y + (diameter / 4.5), "Helvetica", text_size, "bold", text_color, "", "", text)

    def set_value(self, value):
        if value > self.maxValue:
            value = self.maxValue
        elif value < self.minValue:
            value = self.minValue

        degrees = (((value - self.minValue) * (self.rangeDegrees - 0)) / (self.maxValue - self.minValue)) + 0
        if (value > self.minWrnValue) and (value < self.maxWrnValue):
            color = self.normalColor
        elif value >= self.maxWrnValue:
            color = self.maxColor
        else:
            color = self.minColor

        self.canvas.itemconfig(self.idCircle, extent=-degrees)
        self.canvas.itemconfig(self.idCircle, outline=color)
        self.idValue.set_text(value)

    def set_text_color(self, color):
        self.idValue.set_color(color)
        self.idText.set_color(color)

    def set_background_color(self, color):
        self.canvas.itemconfig(self.idBackground, outline=color)

    def update(self):
        if self.update_function is not None and self.update_args is None:
            self.set_value(getattr(self.update_class, self.update_function)())
        if self.update_function is not None and self.update_args is not None:
            self.set_value(getattr(self.update_class, self.update_function)(*self.update_args))
