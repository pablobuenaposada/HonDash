class Text:

    def __init__(self,canvas,x,y,font,size,weight,color,prefix,suffix,text):
        self.canvas=canvas
        self.font=font
        self.size=size
        self.weight=weight
        self.color=color
        self.prefix=str(prefix)
        self.suffix=str(suffix)
        
        self.id=canvas.create_text(x,y,text=prefix+text+suffix,font=self.font+" "+str(self.size)+" "+self.weight,fill=self.color)

    def setText(self,text):
        self.canvas.itemconfig(self.id,text=self.prefix+str(text)+self.suffix)

    def setColor(self,color):
	self.canvas.itemconfig(self.id,fill=color)
