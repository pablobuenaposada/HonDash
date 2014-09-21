from Text import *

class Circle:
    
    def __init__(self,canvas,x,y,diameter,width,startDegrees,rangeDegrees,minValue,maxValue,minWrnValue,maxWrnValue,minColor,normalColor,maxColor,fontSize,textSize,textColor,text,backgroundColor):
        self.canvas = canvas
        self.minValue=minValue
        self.maxValue=maxValue
        self.rangeDegrees = rangeDegrees
        self.startDegrees = startDegrees
        self.minWrnValue = minWrnValue
        self.maxWrnValue = maxWrnValue
        self.minColor = minColor
        self.normalColor = normalColor
        self.maxColor = maxColor
        self.canvas.create_arc(x-(diameter/2),y-(diameter/2),x+(diameter/2),y+(diameter/2),style="arc", start=self.startDegrees, extent=-self.rangeDegrees,fill="",outline=backgroundColor,width=width)
        self.idCircle = self.canvas.create_arc(x-(diameter/2),y-(diameter/2),x+(diameter/2),y+(diameter/2),style="arc", start=self.startDegrees, extent=-self.rangeDegrees,fill="",outline=normalColor,width=width)
        
        self.idValue = Text(canvas,x,y,"Helvetica",fontSize,"bold",textColor,"","","80")
        self.idText = Text(canvas,x,y+(diameter/4.5),"Helvetica",textSize,"bold",textColor,"","",text) 

    def setValue(self,value):
        if value > self.maxValue:
           value = self.maxValue
        elif value < self.minValue:
            value = self.minValue
        
        degrees = (((value - self.minValue) * (self.rangeDegrees - 0)) / (self.maxValue - self.minValue)) + 0        
        if (value > self.minWrnValue) and (value < self.maxWrnValue): color=self.normalColor
        elif value >= self.maxWrnValue: color=self.maxColor
        else: color=self.minColor
        
        self.canvas.itemconfig(self.idCircle, extent=-degrees)
        self.canvas.itemconfig(self.idCircle, outline=color)
        self.idValue.setText(value)
        
    

    
