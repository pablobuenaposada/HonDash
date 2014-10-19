import ImageTk

class Image:

    def __init__(self,canvas,path,x,y):
        self.canvas=canvas
	self.image = ImageTk.PhotoImage(file=path)
	self.id = self.canvas.create_image(x,y,image=self.image)
