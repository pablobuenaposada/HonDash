class Bar:
    def __init__(self, canvas, x, y, min_width, max_width, min_height, max_height, min_value, max_value, range_way, color,
                 background_color, update_class=None, update_function=None, update_args=None):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.minWidth = min_width
        self.maxWidth = max_width
        self.minHeight = min_height
        self.maxHeight = -max_height
        self.minValue = min_value
        self.maxValue = max_value
        self.update_class = update_class
        self.update_function = update_function
        self.update_args = update_args
        self.range_way = range_way
        self.idBackgroundBar = self.canvas.create_rectangle(x, y, x + self.maxWidth, y + self.maxHeight,
                                                            fill=background_color, outline=background_color)
        self.idBar = self.canvas.create_rectangle(x, y, x + self.maxWidth, y + self.maxHeight, fill=color,
                                                  outline=color)

    def set_height(self, value):
        if value > self.maxValue:
            value = self.maxValue
        elif value < self.minValue:
            value = self.minValue

        new_height = (((value - self.minValue) * (self.maxHeight - self.minHeight)) / (
            self.maxValue - self.minValue)) + self.minHeight
        new_height += self.y
        actual_dimension = self.canvas.coords(self.idBar)
        self.canvas.coords(self.idBar, actual_dimension[0], new_height, actual_dimension[2], actual_dimension[3])

    def set_width(self, value):
        if value > self.maxValue:
            value = self.maxValue
        elif value < self.minValue:
            value = self.minValue

        new_width = (((value - self.minValue) * (self.maxWidth - self.minWidth)) / (
            self.maxValue - self.minValue)) + self.minWidth
        new_width += self.x
        actual_dimension = self.canvas.coords(self.idBar)
        self.canvas.coords(self.idBar, actual_dimension[0], actual_dimension[1], new_width, actual_dimension[3])

    def set_background_color(self, color):
        self.canvas.itemconfig(self.idBackgroundBar, fill=color)
        self.canvas.itemconfig(self.idBackgroundBar, outline=color)

    def update(self):
        if self.update_function is not None and self.update_args is None:
            if self.range_way == 'height':
                self.set_height(getattr(self.update_class, self.update_function)())
            else:
                self.set_width(getattr(self.update_class, self.update_function)())
        if self.update_function is not None and self.update_args is not None:
            if self.range_way == 'height':
                self.set_height(getattr(self.update_class, self.update_function)(*self.update_args))
            else:
                self.set_width(getattr(self.update_class, self.update_function)(*self.update_args))