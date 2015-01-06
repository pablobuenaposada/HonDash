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
from controller.Global import *

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


winWidth=root.winfo_screenwidth() #1280
winHeight=root.winfo_screenheight() #800

speedFontSize = 120
circleValueSize = 60
circleTextSize = 25

#init devices
serial = CromeQD2()
mcp3208 = MCP3208()
controller = Controller()

def adc2fuel(self,adc):
    volts = (adc/4096.000)*4.80
    return (int)(-7.348540077*pow(10,-1)*pow(volts,2)-32.27276861*volts+109.170896)

#conversion for VDO 323-057 sensor powered by 4.8v and read with a 56ohms voltage divider
def adc2oiltemp(adc):
    volts = (adc/4096.000)*4.80
    return (int)(-9.805174198*pow(10,-1)*pow(volts,9)+23.4368155*pow(volts,8)-240.7430517*pow(volts,7)+1390.11628*pow(volts,6)-4955.008229*pow(volts,5)+11266.31187*pow(volts,4)-16289.93484*pow(volts,3)+14423.41426*pow(volts,2)-7152.975474*volts+1697.497838)

def adc2oilpress(adc):
    volts = (adc/4096.000)*4.80
    return round(7.671035919*pow(10,-2)*pow(volts,7)-1.077184901*pow(volts,6)+6.295494139*pow(volts,5)-19.62567902*pow(volts,4)+35.08161116*pow(volts,3)-35.51613665*pow(volts,2)+19.52857924*volts-4.551671147,1)

def oilTempSensor():
    return adc2oiltemp(mcp3208.getADC(7))

def oilPressSensor():
    return adc2oilpress(mcp3208.getADC(5))

def waterTempSensor():
    return adc2oiltemp(mcp3208.getADC(1))

#init canvas
canvas = Canvas(root,width=winWidth,height=winHeight,bg=Global.OFFBgColor)
canvas.pack()

wallpaper=Icon(canvas,"/home/pi/Desktop/HonDash/images/camo4.jpg",1280/2,800/2,1280,800,False)

fuelIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/fuel.png",1220,256,45,50,False)
highBeamIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/lights.png",375,270,83,51,False)
trunkIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/rear.png",125,270,84,48,False)
oilIcon = Icon(canvas,"/home/pi/Desktop/HonDash/images/oil.png",250,270,109,41,False)

#init graphics
rpm = Rpm(canvas,winWidth/2,(winHeight/4.0)+10,winWidth/1.00,winHeight/2.75,100,Global.OFFrpmColor,Global.OFFshadeColor,20,140,0,9000)
speed = Text(canvas,(winWidth/2)-15,winHeight/4,"Helvetica",speedFontSize,"bold italic",Global.OFFtextColor,"","","137")
speedUnit = Text(canvas,800,243,"Helvetica",20,"bold italic",Global.OFFtextColor,"","","km/h")
mileage = 1 #Text(canvas,winWidth/2,(winHeight/10)*3,"Helvetica",10,"bold ","white","","","162.372 KM")
fuel = Bar(canvas,923,280,0,250,0,50,0,100,Global.fuelColor,Global.OFFshadeColor)
fuelText = Text(canvas,1050,256,"Helvetica",30,"bold italic",Global.OFFtextColor,"","%","100") 

#p=Text(canvas,640,50,"Helvetica",40,"bold italic","black","","7","")

#pedals
clutch = Bar(canvas,1100,798,60,60,0,200,0,200,Global.clutchColor,Global.OFFclutchBgColor)
brake = Bar(canvas,1159,798,60,60,0,200,2100,2400,Global.brakeColor,Global.OFFbrakeBgColor)
throttle = Bar(canvas,1220,798,60,60,0,200,0,100,Global.throttleColor,Global.OFFthrottleBgColor)

#circles
oilTemp = Circle(canvas,(winWidth/8)*1,(winHeight/32)*18,225,60,240,300,0,150,80,120,Global.circleMinColor,Global.circleNormalColor,Global.circleMaxColor,circleValueSize,circleTextSize,Global.OFFtextColor,"OIL T",Global.OFFshadeColor,oilTempSensor,None)
oilPressure = Circle(canvas,(winWidth/8)*3,(winHeight/32)*18,225,60,240,300,0,8,3,6,Global.circleMinColor,Global.circleNormalColor,Global.circleMaxColor,circleValueSize,circleTextSize,Global.OFFtextColor,"OIL P",Global.OFFshadeColor,oilPressSensor,None)
h2o = Circle(canvas,(winWidth/8)*5,(winHeight/32)*18,225,60,240,300,0,150,80,120,Global.circleMinColor,Global.circleNormalColor,Global.circleMaxColor,circleValueSize,circleTextSize,Global.OFFtextColor,"H2O T",Global.OFFshadeColor,waterTempSensor,None)
g = Gforce(canvas,(winWidth/8)*7,(winHeight/32)*18,283,2,2,"gray",6,"red",Global.OFFtextColor)

#turn lights
arrowLeft = Arrow(canvas,426,200,0.25,Global.signalColor,"left",False)
arrowRight = Arrow(canvas,852,200,0.25,Global.signalColor,"right",False)

#info
runTime = Text(canvas,244,215,"Helvetica",30,"bold italic",Global.OFFtextColor,"Run ","","00:00:00")
h2oEcu = Text(canvas,510,624,"Helvetica",30,"bold italic",Global.OFFtextColor,"H2O: ","cº","44")
inj = Text(canvas,495,672,"Helvetica",30,"bold italic",Global.OFFtextColor,"INJ: ","ms","4")
duty = Text(canvas,500,720,"Helvetica",30,"bold italic",Global.OFFtextColor,"DTY: ","ms","4")
vtec = Text(canvas,480,768,"Helvetica",30,"bold italic",Global.OFFtextColor,"VTC: ","","off")
battery = Text(canvas,150,624,"Helvetica",30,"bold italic",Global.OFFtextColor,"BAT: ","v","12.4")
iat = Text(canvas,130,672,"Helvetica",30,"bold italic",Global.OFFtextColor,"IAT: ","cº","44")
ign = Text(canvas,120,720,"Helvetica",30,"bold italic",Global.OFFtextColor,"IGN: ","º","30")
mapp = Text(canvas,182,768,"Helvetica",30,"bold italic",Global.OFFtextColor,"MAP: ","mBar","433")
gear = Text(canvas,800,672,"Helvetica",30,"bold italic",Global.OFFtextColor,"GEAR: ","","N")


digital4 = DigitalInput(4,controller.callbackDigital4)
digital17 = DigitalInput(17,controller.callbackDigital17)
digital22 = DigitalInput(22,controller.callbackDigital22)
digital23 = DigitalInput(23,controller.callbackDigital23)
digital24 = DigitalInput(24,controller.callbackDigital24)
digital25 = DigitalInput(25,controller.callbackDigital25)
digital27 = DigitalInput(27,controller.callbackDigital27)    
controller.things2control(canvas,digital4,digital17,digital22,digital23,digital24,digital25,digital27,arrowLeft,arrowRight,fuelIcon,highBeamIcon,trunkIcon,oilIcon,speed,speedUnit,h2oEcu,battery,runTime,inj,duty,vtec,iat,ign,mapp,oilTemp,oilPressure,h2o,fuelText,wallpaper,gear)
accelerometer = ADXL345()

axes = accelerometer.getAxes(True)
print axes['x'],axes['y'],axes['z']
accelerometer.setOffset(axes['x'],axes['y'],axes['z']-1)

#update graphics
canvas.after(10,controller.updateAll,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight,accelerometer,g,fuelText,gear)

#main loop
root.mainloop()



