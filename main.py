from Tkinter import *
from gui.Rpm import Rpm
from gui.Text import *
from gui.Bar import *
from gui.Circle import *
from gui.Arrow import *
from gui.Gforce import *
from controller.Controller import *
from devices.CromeQD2 import *
from devices.MCP3208 import *

#ratio constants
root = Tk()
winWidth=root.winfo_screenwidth()
winHeight=root.winfo_screenheight()
speedFontSize=int(0.09*winHeight)
circleFontSize=int(0.05*winHeight)

#init canvas
canvas = Canvas(root,width=winWidth,height=winHeight,bg="white")
canvas.pack()

#init graphics
rpm = Rpm(canvas,winWidth/2,winHeight/4,winWidth/1.25,winHeight/4,50,"orange","yellow",20,140,0,10000)
speed = Text(canvas,winWidth/2,winHeight/4,"Helvetica",speedFontSize,"bold italic","black","137")
mileage = Text(canvas,winWidth/2,(winHeight/10)*3,"Helvetica",10,"bold ","black","162.372 KM")
clutch=Bar(canvas,winWidth-92,winHeight,30,30,0,150,0,200,"blue")
brake=Bar(canvas,winWidth-61,winHeight,30,30,0,150,0,200,"red")
throttle=Bar(canvas,winWidth-30,winHeight,30,30,0,150,0,200,"green")
temp1 = Circle(canvas,(winWidth/4)*1,(winHeight/2)*1,100,25,240,300,0,4096,"#28cfbc",circleFontSize,"OIL T.")
temp2 = Circle(canvas,(winWidth/4)*2,(winHeight/2)*1,100,25,240,300,0,4096,"#28cfbc",circleFontSize,"OIL P.")
temp3 = Circle(canvas,(winWidth/4)*3,(winHeight/2)*1,100,25,240,300,0,4096,"#28cfbc",circleFontSize,"H2O T.")
temp4 = Circle(canvas,(winWidth/4)*1,(winHeight/4)*3,100,25,240,300,0,4096,"#28cfbc",circleFontSize,"H2O T.2")
temp5 = Circle(canvas,(winWidth/4)*2,(winHeight/4)*3,100,25,240,300,20,100,"#28cfbc",circleFontSize,"IAT")
#temp6 = Circle(canvas,(winWidth/4)*3,(winHeight/4)*3,100,25,240,300,20,100,"#28cfbc",circleFontSize,"BAT")
arrowLeft=Arrow(canvas,(winWidth/3)*1,winHeight/4,0.15,"green","left")
arrowRight=Arrow(canvas,(winWidth/3)*2,winHeight/4,0.15,"green","right")
g = Gforce(canvas,(winWidth/4)*3,(winHeight/4)*3,125,2,1,"gray",4,"red")

#init devices
serial = CromeQD2()
mcp3208 = MCP3208()

#update graphics
#canvas.after(100,updateRpm,canvas,serial,rpm)
#canvas.after(100,updateAnalog,canvas,mcp3208,7,temp1)
#canvas.after(100,updateAnalog,canvas,mcp3208,6,temp2)
#canvas.after(100,updateAnalog,canvas,mcp3208,5,temp3)
#canvas.after(100,updateAnalog,canvas,mcp3208,4,temp4)

#canvas.after(10,updateTps,canvas,mcp3208,4,throttle)
canvas.after(10,updateAll,canvas,mcp3208,serial,rpm,speed,temp1,temp2,temp3,temp4,throttle,clutch,brake)
#main loop
root.mainloop()



