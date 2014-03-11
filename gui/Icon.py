import Image
import ImageTk


class Icon:
    def __init__(self, canvas, path, x, y, width, height, state):
        self.canvas = canvas
        self.image = Image.open(path)
        self.image = self.image.resize((width, height), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.id = self.canvas.create_image(x, y, image=self.image)
        self.set_status(state)

    def set_status(self, status):
        if status:
            self.canvas.itemconfig(self.id, state='normal')
        else:
            self.canvas.itemconfig(self.id, state='hidden')
