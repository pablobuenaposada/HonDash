from Text import *
import math

class Gforce:
    
    def __init__(self,canvas,x,y,diameter,maxG,outlineWidth,outlineColor,lineWidth,lineColor,textColor):
        self.x=x
        self.y=y
        self.diameter=diameter
        self.maxG=maxG
        self.canvas = canvas
        self.idGauge=self.canvas.create_oval(x-(diameter/2),y-(diameter/2),x+(diameter/2),y+(diameter/2),outline=outlineColor, width=outlineWidth)
        self.idLine=self.canvas.create_line(x,y,x,y+(diameter/2),fill=lineColor,width=lineWidth)
        self.text = Text(canvas,x+(diameter/2.6),y+(diameter/2.1),"Helvetica",int(diameter*0.09),"bold",textColor,"","","1.0 G") 

    
    def setGforce(self,xForce,yForce):       
        g = math.sqrt(xForce * xForce + yForce * yForce)
        xForce=float(xForce)/self.maxG
        yForce=float(yForce)/self.maxG
        self.canvas.coords(self.idLine,self.x,self.y,self.x+((self.diameter/2)*xForce),self.y+((self.diameter/2)*yForce))
        self.text.set_text(str("%.1f" % g) + " G")
        
