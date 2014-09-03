class Text:

    def __init__(self,canvas,x,y,font,size,weight,color,text):
        self.canvas=canvas
        self.font=font
        self.size=size
        self.weight=weight
        self.color=color

        self.id=canvas.create_text(x,y,text=text,font=self.font+" "+str(self.size)+" "+self.weight,fill=self.color)

    def setText(self,text):
        self.canvas.itemconfig(self.id,text=text)
