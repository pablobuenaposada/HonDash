from Tkinter import *
from Rpm import *
from Text import *
from Bar import *
from Circle import *

winWidth=700
winHeight=700
speedFontSize=int(0.09*winHeight)
circleFontSize=int(0.05*winHeight)


root = Tk()
canvas = Canvas(root,width=winWidth,height=winHeight,bg="white")
canvas.pack()


rpm = Rpm(canvas,winWidth/2,winHeight/4,winWidth/1.25,winHeight/4,50,"yellow","yellow",20,140,0,10000)
speed = Text(canvas,winWidth/2,winHeight/4,"Helvetica",speedFontSize,"bold italic","black","120")
mileage = Text(canvas,winWidth/2,(winHeight/10)*3,"Helvetica",10,"bold ","black","162.372 KM")

clutch=Bar(canvas,winWidth-92,winHeight,30,-60,"blue")
brake=Bar(canvas,winWidth-61,winHeight,30,-30,"red")
throttle=Bar(canvas,winWidth-30,winHeight,30,-100,"green")

temp1 = Circle(canvas,(winWidth/4)*1,(winHeight/2)*1,100,25,240,300,20,100,"blue",circleFontSize,"OIL T.")
temp2 = Circle(canvas,(winWidth/4)*2,(winHeight/2)*1,100,25,240,300,20,100,"blue",circleFontSize,"OIL P.")
temp3 = Circle(canvas,(winWidth/4)*3,(winHeight/2)*1,100,25,240,300,20,100,"blue",circleFontSize,"H2O T.")

temp4 = Circle(canvas,(winWidth/4)*1,(winHeight/4)*3,100,25,240,300,20,100,"blue",circleFontSize,"H2O T.2")
temp5 = Circle(canvas,(winWidth/4)*2,(winHeight/4)*3,100,25,240,300,20,100,"blue",circleFontSize,"IAT")
temp6 = Circle(canvas,(winWidth/4)*3,(winHeight/4)*3,100,25,240,300,20,100,"blue",circleFontSize,"BAT")


root.mainloop()
