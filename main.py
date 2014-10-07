# -*- coding: utf-8 -*-
from Tkinter import *
from gui.Rpm import *
from gui.Text import *
from gui.Bar import *
from gui.Circle import *
from gui.Arrow import *
from gui.Gforce import *
from controller.Controller import *
from devices.CromeQD2 import *
from devices.MCP3208 import *
from devices.Digital import *

#ratio constants
root = Tk()
root.attributes('-fullscreen', True)
root.focus_set()
def close(self):
    root.destroy()
root.bind('<Escape>',close)
root.config(cursor='none')


winWidth=root.winfo_screenwidth()
winHeight=root.winfo_screenheight()
speedFontSize = 120
circleValueSize = 60
circleTextSize = 25

#init canvas
canvas = Canvas(root,width=winWidth,height=winHeight,bg="black")
canvas.pack()

#init graphics
rpm = Rpm(canvas,winWidth/2,winHeight/4.0,winWidth/1.00,winHeight/2.75,100,"#ffa500","yellow",20,140,0,10000)
speed = Text(canvas,winWidth/2,winHeight/4,"Helvetica",speedFontSize,"bold italic","white","","","137")
speedUnit = Text(canvas,(winWidth/4)*2.5,(winHeight/4)+50,"Helvetica",15,"bold italic","white","","","km/h")
mileage = Text(canvas,winWidth/2,(winHeight/10)*3,"Helvetica",10,"bold ","white","","","162.372 KM")
fuel = Bar(canvas,(winWidth/2)-200,(winHeight/16)*5.75,0,400,0,25,0,4096,"#efbbff","DeepPink4")
canvas.create_text(winWidth/2,50,text="1926",font="Helvetica 70 bold",fill="#ee9b02",stipple='gray25')


clutch = Bar(canvas,winWidth-182,winHeight,60,60,0,200,0,200,"blue","midnight blue")
brake = Bar(canvas,winWidth-121,winHeight,60,60,0,200,0,200,"red","firebrick4")
throttle = Bar(canvas,winWidth-60,winHeight,60,60,0,200,0,200,"green","dark green")

oilTemp = Circle(canvas,(winWidth/8)*1,(winHeight/32)*18,225,60,240,300,0,255,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"white","OIL T","gray30")
oilPressure = Circle(canvas,(winWidth/8)*3,(winHeight/32)*18,225,60,240,300,0,255,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"white","OIL P","gray30")
h2o = Circle(canvas,(winWidth/8)*5,(winHeight/32)*18,225,60,240,300,0,255,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"white","H2O T","gray30")
g = Gforce(canvas,(winWidth/8)*7,(winHeight/32)*18,285,2,1,"gray",4,"red","white")

arrowLeft = Arrow(canvas,(winWidth/3)*1,winHeight/4,0.25,"green","left")
arrowRight = Arrow(canvas,(winWidth/3)*2,winHeight/4,0.25,"green","right")

runTime = Text(canvas,(winWidth/7),(winHeight/64)*1,"Helvetica",30,"bold italic","white","Run Time ","","00:00:00")
h2oEcu = Text(canvas,(winWidth/7)*3,(winHeight/64)*52,"Helvetica",30,"bold italic","white","H2O: ","cº","44")
inj = Text(canvas,(winWidth/7)*3,(winHeight/64)*56,"Helvetica",30,"bold italic","white","INJ: ","ms","4")
duty = Text(canvas,(winWidth/7)*3,(winHeight/64)*60,"Helvetica",30,"bold italic","white","DTY: ","ms","4")
vtec = Text(canvas,(winWidth/7)*3,(winHeight/64)*64,"Helvetica",30,"bold italic","white","VTC: ","","off")
battery = Text(canvas,(winWidth/7)*1,(winHeight/64)*52,"Helvetica",30,"bold italic","white","BAT: ","v","12.4")
iat = Text(canvas,(winWidth/7)*1,(winHeight/64)*56,"Helvetica",30,"bold italic","white","ITK: ","cº","44")
ign = Text(canvas,(winWidth/7)*1,(winHeight/64)*60,"Helvetica",30,"bold italic","white","IGN: ","º","30")
mapp = Text(canvas,(winWidth/7)*1,(winHeight/64)*64,"Helvetica",30,"bold italic","white","MAP: ","mBar","433")

#init devices
controller = Controller()
serial = CromeQD2()
mcp3208 = MCP3208()
digital = Digital()
digital.setInput(27)

def f1(channel):
    arrowLeft.setFill(digital.getValue(27))
    
digital.addEvent(27,f1)

#update graphics
canvas.after(10,controller.updateAll,canvas,mcp3208,serial,controller,digital,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight)

#main loop
root.mainloop()



