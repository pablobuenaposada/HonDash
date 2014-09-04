from Text import *

class Circle:
    
    def __init__(self,canvas,x,y,diameter,width,startDegrees,rangeDegrees,minValue,maxValue,color,fontSize,text):
        self.canvas = canvas
        self.minValue=minValue
        self.maxValue=maxValue
        self.rangeDegrees = rangeDegrees
        self.startDegrees = startDegrees
        self.idCircle = self.canvas.create_arc(x-(diameter/2),y-(diameter/2),x+(diameter/2),y+(diameter/2),style="arc", start=self.startDegrees, extent=-self.rangeDegrees,fill="",outline=color,width=width)
        
        self.idValue = Text(canvas,x,y,"Helvetica",fontSize,"bold","black","80")
        self.idText = Text(canvas,x,y+(diameter/4.5),"Helvetica",int(0.371*fontSize),"bold","black",text) 

    def setValue(self,degreesFill):
        if degreesFill > self.maxValue:
           degreesFill = self.maxValue
        elif degreesFill < self.minValue:
            degreesFill = self.minValue
        
        degrees = (((degreesFill - self.minValue) * (self.rangeDegrees - 0)) / (self.maxValue - self.minValue)) + 0
        
        self.canvas.itemconfig(self.idCircle, extent=-degrees)
        self.canvas.itemconfig(self.idValue, text = degreesFill)
    
    

    
