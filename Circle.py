class Circle:
    
    def __init__(self,canvas,x,y,diameter,width,startDegrees,rangeDegrees,minValue,maxValue,color):
        self.canvas = canvas
        self.minValue=minValue
        self.maxValue=maxValue
        self.rangeDegrees = rangeDegrees
        self.startDegrees = startDegrees
        self.idCircle = self.canvas.create_arc(x,y,diameter,diameter,style="arc", start=self.startDegrees, extent=-self.rangeDegrees,fill="",outline=color,width=width)

        self.idText = canvas.create_text(x+(diameter/3),y+(diameter/3),text="x")
         

    def setFill(self,degreesFill):
        if degreesFill > self.maxValue:
           degreesFill = self.maxValue
        elif degreesFill < self.minValue:
            degreesFill = self.minValue
        
        degrees = (((degreesFill - self.minValue) * (self.rangeDegrees - 0)) / (self.maxValue - self.minValue)) + 0
        
        self.canvas.itemconfig(self.idCircle, extent=-degrees)
        self.canvas.itemconfig(self.idText, text = degreesFill)
    
    

    
