class Text:
    def __init__(self, canvas, x, y, font, size, weight, color, prefix, suffix, text, update_class=None, update_function=None, update_args=None):
        self.x = x
        self.y = y
        self.font = font
        self.size = size
        self.weight = weight
        self.color = color
        self.prefix = str(prefix)
        self.suffix = str(suffix)
        self.text = text
        self.update_function = update_function
        self.update_class = update_class
        self.update_args = update_args
        self.canvas = canvas
        self.id = self.canvas.create_text(self.x, self.y, text=self.prefix + self.text + self.suffix,
                                          font=self.font + " " + str(self.size) + " " + self.weight, fill=self.color)

    def set_text(self, text):
        self.canvas.itemconfig(self.id, text=self.prefix + str(text) + self.suffix)

    def set_color(self, color):
        self.canvas.itemconfig(self.id, fill=color)

    def update(self):
        if self.update_function is not None and self.update_args is None:
            self.set_text(getattr(self.update_class, self.update_function)())
        if self.update_function is not None and self.update_args is not None:
            self.set_text(getattr(self.update_class, self.update_function)(*self.update_args))

