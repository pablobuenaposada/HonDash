class Arrow:
    def __init__(self, canvas, x, y, scale, color, way, init, update_class=None, update_function=None, update_args=None):
        self.color = color
        self.canvas = canvas
        if way == "left":
            points = [-150, 0, 0, 125, 0, 50, 150, 50, 150, -50, 0, -50, 0, -125]
        else:
            points = [-150, 50, 0, 50, 0, 125, 150, 0, 0, -125, 0, -50, -150, -50]

        delete_id = self.canvas.create_polygon(points, fill=color, state="hidden")
        self.canvas.scale(delete_id, 0, 0, scale, scale)
        points = self.canvas.coords(delete_id)

        for pos in range(0, len(points)):
            if pos % 2 == 0:
                points[pos] = points[pos] + x
            else:
                points[pos] = points[pos] + y

        self.id = self.canvas.create_polygon(points, fill=color)
        self.canvas.delete(delete_id)
        self.set_status(init)
        self.update_class = update_class
        self.update_function = update_function
        self.update_args = update_args

    def set_status(self, status):
        if not status:
            self.canvas.itemconfig(self.id, fill='')
        else:
            self.canvas.itemconfig(self.id, fill=self.color)

    def update(self):
        if self.update_function is not None and self.update_args is None:
            self.set_status(getattr(self.update_class, self.update_function)())
        if self.update_function is not None and self.update_args is not None:
            self.set_status(getattr(self.update_class, self.update_function)(*self.update_args))