import math
class Rpm:


    def __init__(self,canvas,x,y,width,height,barWidth,color,backColor,offsetDegrees,totalDegrees,minValue,maxValue):
        self.canvas = canvas
        self.minValue=minValue
        self.maxValue=maxValue
        self.totalDegrees=-totalDegrees
        self.offsetDegrees=-180-offsetDegrees
        self.barWidth=barWidth
        self.canvas.create_arc(x-(width/2),y-(height/2),x+(width/2),y+(height/2),style="arc",outline=backColor,fill="",extent=self.totalDegrees,start=self.offsetDegrees,width=self.barWidth)        
        self.idRpm = self.canvas.create_arc(x-(width/2),y-(height/2),x+(width/2),y+(height/2),style="arc",outline=color,fill="",extent=0,start=self.offsetDegrees,width=self.barWidth)
        z=height*math.sqrt(1-((0**2)/(width**2)))
        self.canvas.create_line(x,z,x,y)
        
    def setRpm(self,valueFill):
        if valueFill > self.maxValue:
           valueFill = self.maxValue
        elif valueFill < self.minValue:
            valueFill = self.minValue
        
        degrees = (((valueFill - self.minValue) * (self.totalDegrees - 0)) / (self.maxValue - self.minValue)) + 0
        self.canvas.itemconfig(self.idRpm, extent=degrees)
        
