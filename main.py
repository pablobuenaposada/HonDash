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
from devices.DigitalInput import *
from devices.ADXL345 import *
from gui.Icon import *
import sys

fsock = open('error.log', 'w')
sys.stderr = fsock

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

fuelIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/fuel.png",1220,256,45,50,False)
lightsIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/lights.png",375,270,83,51,False)
trunkIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/rear.png",125,270,84,48,False)
#handbrakeIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/handbrake.png",850,750,109,88,True)
oilIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/oil.png",250,270,109,41,False)

#init graphics
rpm = Rpm(canvas,winWidth/2,(winHeight/4.0)+10,winWidth/1.00,winHeight/2.75,100,"#ffa500","yellow",20,140,0,10000)
speed = Text(canvas,(winWidth/2)-15,winHeight/4,"Helvetica",speedFontSize,"bold italic","white","","","137")
speedUnit = Text(canvas,800,243,"Helvetica",20,"bold italic","white","","","km/h")
mileage = 1 #Text(canvas,winWidth/2,(winHeight/10)*3,"Helvetica",10,"bold ","white","","","162.372 KM")
fuel = Bar(canvas,923,280,0,250,0,50,0,100,"#efbbff","DeepPink4")
fuelText = Text(canvas,1050,256,"Helvetica",30,"bold italic","#a10f62","","%","100") 

#pedals
clutch = Bar(canvas,1100,798,60,60,0,200,0,200,"blue","midnight blue")
brake = Bar(canvas,1159,798,60,60,0,200,2100,2400,"red","firebrick4")
throttle = Bar(canvas,1220,798,60,60,0,200,0,100,"green","dark green")

#circles
oilTemp = Circle(canvas,(winWidth/8)*1,(winHeight/32)*18,225,60,240,300,0,150,80,120,"blue","#28cfbc","red",circleValueSize,circleTextSize,"white","OIL T","gray30")
oilPressure = Circle(canvas,(winWidth/8)*3,(winHeight/32)*18,225,60,240,300,0,8,3,6,"blue","#28cfbc","red",circleValueSize,circleTextSize,"white","OIL P","gray30")
h2o = Circle(canvas,(winWidth/8)*5,(winHeight/32)*18,225,60,240,300,0,255,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"white","H2O T","gray30")
g = Gforce(canvas,(winWidth/8)*7,(winHeight/32)*18,283,2,2,"gray",6,"red","white")

#turn lights
arrowLeft = Arrow(canvas,426,200,0.25,"green","left",False)
arrowRight = Arrow(canvas,852,200,0.25,"green","right",False)

#info
runTime = Text(canvas,244,215,"Helvetica",30,"bold italic","white","Run ","","00:00:00")
h2oEcu = Text(canvas,510,624,"Helvetica",30,"bold italic","white","H2O: ","cº","44")
inj = Text(canvas,495,672,"Helvetica",30,"bold italic","white","INJ: ","ms","4")
duty = Text(canvas,500,720,"Helvetica",30,"bold italic","white","DTY: ","ms","4")
vtec = Text(canvas,480,768,"Helvetica",30,"bold italic","white","VTC: ","","off")
battery = Text(canvas,150,624,"Helvetica",30,"bold italic","white","BAT: ","v","12.4")
iat = Text(canvas,130,672,"Helvetica",30,"bold italic","white","IAT: ","cº","44")
ign = Text(canvas,120,720,"Helvetica",30,"bold italic","white","IGN: ","º","30")
mapp = Text(canvas,182,768,"Helvetica",30,"bold italic","white","MAP: ","mBar","433")

#init devices
serial = CromeQD2()
mcp3208 = MCP3208()
controller = Controller()
digital27 = DigitalInput(27,controller.f2)    
controller.things2control(digital27,arrowLeft)
accelerometer = ADXL345(0.6,0.5,0)

#update graphics
canvas.after(10,controller.updateAll,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight,accelerometer,g)

#main loop
root.mainloop()



