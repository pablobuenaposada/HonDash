class Gforce:
    
    def __init__(self,canvas,x,y,diameter,maxG,outlineWidth,outlineColor,lineWidth,lineColor):
        self.x=x
        self.y=y
        self.diameter=diameter
        self.maxG=maxG
        self.canvas = canvas
        self.idG=self.canvas.create_oval(x-(diameter/2),y-(diameter/2),x+(diameter/2),y+(diameter/2),outline=outlineColor, width=outlineWidth)
        self.idLine=self.canvas.create_line(x,y,x+100,y+100,fill=lineColor,width=lineWidth)
        
    
    def setGforce(self,xForce,yForce):        
    
        self.canvas.coords(self.idLine,self.x,self.y,self.x+xForce,self.y+yForce)
        
