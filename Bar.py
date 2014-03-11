class Bar:
    
    def __init__(self,canvas,x,y,width,height,color):
        self.canvas = canvas
        self.idBar = self.canvas.create_rectangle(x,y,x+width,y+height,fill=color);


    def setHeight(self,newHeight):
        actualDimension = self.canvas.coords(self.idBar)
        self.canvas.coords(self.idBar,actualDimension[0],newHeight,actualDimension[2],actualDimension[3])

        
    def setWidth(self,newWidth):
        actualDimension = self.canvas.coords(self.idBar)
        self.canvas.coords(self.idBar,actualDimension[0],actualDimension[1],newWidth,actualDimension[3])


