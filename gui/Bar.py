class Bar:
    
    def __init__(self,canvas,x,y,minWidth,maxWidth,minHeight,maxHeight,minValue,maxValue,color,backgroundColor):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.minWidth = minWidth
        self.maxWidth = maxWidth
        self.minHeight = minHeight
        self.maxHeight = -maxHeight
        self.minValue = minValue
        self.maxValue = maxValue
        self.idBackgroundBar = self.canvas.create_rectangle(x,y,x+self.maxWidth,y+self.maxHeight,fill=backgroundColor,outline=backgroundColor)
        self.idBar = self.canvas.create_rectangle(x,y,x+self.maxWidth,y+self.maxHeight,fill=color,outline=color)

    def setHeight(self,value):        
        if value > self.maxValue:
            value = self.maxValue
        elif value < self.minValue:
            value = self.minValue

        newHeight = (((value - self.minValue) * (self.maxHeight - self.minHeight)) / (self.maxValue - self.minValue)) + self.minHeight
        newHeight = self.y + newHeight
	actualDimension = self.canvas.coords(self.idBar)
        self.canvas.coords(self.idBar,actualDimension[0],newHeight,actualDimension[2],actualDimension[3])

    def setWidth(self,value):
        if value > self.maxValue:
            value = self.maxValue
        elif value < self.minValue:
            value = self.minValue

        newWidth = (((value - self.minValue) * (self.maxWidth - self.minWidth)) / (self.maxValue - self.minValue)) + self.minWidth
        newWidth = self.x+newWidth    
        actualDimension = self.canvas.coords(self.idBar)
        self.canvas.coords(self.idBar,actualDimension[0],actualDimension[1],newWidth,actualDimension[3])
        
    def setBackgroundColor(self,color):
    	self.canvas.itemconfig(self.idBackgroundBar,fill=color)
    	self.canvas.itemconfig(self.idBackgroundBar,outline=color)
    	
