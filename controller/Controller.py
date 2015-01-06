from devices.Time import *
import numpy
from controller.Global import *

class Controller:
    
    def __init__(self):
        self.startRecord = -1
        self.endRecord = -1
        self.timer = Time()
	self.fuelCounter = 0
	self.fuelAverage = []
	self.fuelCounterMax = 100

    def adc2fuel(self,adc):
        volts = (adc/4096.000)*4.80
        return (int)(-7.348540077*pow(10,-1)*pow(volts,2)-32.27276861*volts+109.170896) 

    #conversion for VDO 323-057 sensor powered by 4.8v and read with a 56ohms voltage divider
    def adc2oiltemp(self,adc):
        volts = (adc/4096.000)*4.80
        return (int)(-9.805174198*pow(10,-1)*pow(volts,9)+23.4368155*pow(volts,8)-240.7430517*pow(volts,7)+1390.11628*pow(volts,6)-4955.008229*pow(volts,5)+11266.31187*pow(volts,4)-16289.93484*pow(volts,3)+14423.41426*pow(volts,2)-7152.975474*volts+1697.497838)

    def adc2oilpress(self,adc):
	volts = (adc/4096.000)*4.80
	return round(7.671035919*pow(10,-2)*pow(volts,7)-1.077184901*pow(volts,6)+6.295494139*pow(volts,5)-19.62567902*pow(volts,4)+35.08161116*pow(volts,3)-35.51613665*pow(volts,2)+19.52857924*volts-4.551671147,1)

    def things2control(self,canvas,digital4,digital17,digital22,digital23,digital24,digital25,digital27,arrowLeft,arrowRight,fuelIcon,highBeamIcon,trunkIcon,oilIcon,speed,speedUnit,h2oEcu,battery,runTime,inj,duty,vtec,iat,ign,mapp,oilTemp,oilPressure,h2o,fuelText,wallpaper,gear):
	self.digital4 = digital4
	self.digital17 = digital17
	self.digital22 = digital22
	self.digital23 = digital23
	self.digital24 = digital24
	self.digital25 = digital25
	self.digital27 = digital27
	self.arrowLeft = arrowLeft
	self.arrowRight = arrowRight
	self.fuelIcon = fuelIcon
	self.highBeamIcon = highBeamIcon
	self.trunkIcon = trunkIcon
	self.oilIcon = oilIcon
	self.canvas = canvas
	self.speed = speed
	self.speedUnit = speedUnit
	self.h2oEcu = h2oEcu
	self.battery = battery
	self.runTime = runTime
	self.inj = inj
	self.duty = duty
	self.vtec = vtec
	self.iat = iat
	self.ign = ign
	self.mapp = mapp
	self.oilTemp = oilTemp
	self.oilPressure = oilPressure
	self.h2o = h2o
	self.fuelText = fuelText
	self.wallpaper = wallpaper
	self.gear = gear

    def callbackDigital25(self,channel):
    	self.arrowLeft.setFill(self.digital25.getValue())

    def callbackDigital24(self,channel):
	self.arrowRight.setFill(self.digital24.getValue())

    def callbackDigital4(self,channel):
	self.fuelIcon.setHidden(self.digital4.getValue())

    def callbackDigital17(self,channel):
	self.highBeamIcon.setHidden(self.digital17.getValue())	

    def callbackDigital27(self,channel):
	self.trunkIcon.setHidden(self.digital27.getValue())    

    def callbackDigital22(self,channel):
	self.oilIcon.setHidden(self.digital22.getValue())

    def callbackDigital23(self,channel):
	if (self.digital23.getValue()):
	    self.wallpaper.setHidden(True)
	    #self.canvas.configure(bg=Global.ONBgColor)
	    self.speed.setColor(Global.ONtextColor)
	    self.speedUnit.setColor(Global.ONtextColor)
            self.h2oEcu.setColor(Global.ONtextColor)
            self.battery.setColor(Global.ONtextColor)
            self.runTime.setColor(Global.ONtextColor)
            self.inj.setColor(Global.ONtextColor)
            self.duty.setColor(Global.ONtextColor)
            self.vtec.setColor(Global.ONtextColor)
            self.iat.setColor(Global.ONtextColor)
            self.ign.setColor(Global.ONtextColor)
            self.mapp.setColor(Global.ONtextColor)
	    self.oilTemp.setTextColor(Global.ONtextColor)
	    self.oilPressure.setTextColor(Global.ONtextColor)
	    self.h2o.setTextColor(Global.ONtextColor)
	    self.fuelText.setTextColor(Global.ONtextColor)
	    
	else:
	    self.wallpaper.setHidden(False)
	    #self.canvas.configure(bg=Global.OFFBgColor)
	    self.speed.setColor(Global.OFFtextColor)
	    self.speedUnit.setColor(Global.OFFtextColor)
            self.h2oEcu.setColor(Global.OFFtextColor)
            self.battery.setColor(Global.OFFtextColor)
            self.runTime.setColor(Global.OFFtextColor)
            self.inj.setColor(Global.OFFtextColor)
            self.duty.setColor(Global.OFFtextColor)
            self.vtec.setColor(Global.OFFtextColor)
            self.iat.setColor(Global.OFFtextColor)
            self.ign.setColor(Global.OFFtextColor)
            self.mapp.setColor(Global.OFFtextColor)
	    self.oilTemp.setTextColor(Global.OFFtextColor)
            self.oilPressure.setTextColor(Global.OFFtextColor)
            self.h2o.setTextColor(Global.OFFtextColor)
	    self.fuelText.setTextColor(Global.OFFtextColor)

    def updateAll(self,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight,accelerometer,g,fuelText,gear):

	gear.setText(serial.getGear())
	rpm.setRpm(serial.getRpm())
	mapp.setText(serial.getMap())
        ign.setText(int(serial.getIgn()))
	iat.setText(int(serial.getIat()))
	inj.setText(serial.getInj())
	duty.setText(serial.getDutyCycle())
	speed.setText(serial.getVss())
        oilTemp.setValue(self.adc2oiltemp(mcp3208.getADC(7))) 
        oilPressure.setValue(self.adc2oilpress(mcp3208.getADC(5)))
	if self.fuelCounter < self.fuelCounterMax:
	    self.fuelAverage.append(self.adc2fuel(mcp3208.getADC(3)))
	    self.fuelCounter = self.fuelCounter + 1
	else:	    
	    self.fuelAverage = numpy.median(self.fuelAverage)
            fuel.setWidth(int(self.fuelAverage))
	    fuelText.setText(int(self.fuelAverage))
	    self.fuelAverage = []
	    self.fuelCounter = 0
	h2o.setValue(mcp3208.getADC(4))
        h2oEcu.setText(int(serial.getEct()))
        battery.setText(round(serial.getBattery(),1))
        throttle.setHeight(serial.getTps())
        clutch.setHeight(0)#mcp3208.getADC(1))
	if(serial.getVtec()): vtec.setText("on")
	else: vtec.setText("off")
        brake.setHeight(0)#mcp3208.getADC(7))'''
        time = self.timer.getTime()
        runTime.setText(self.timer.getTimeString())
	'''axes = accelerometer.getAxes(True)
	g.setGforce(axes['y'],axes['z'])
	print axes['x'],axes['y'],axes['z']'''
        canvas.after(10,controller.updateAll,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight,accelerometer,g,fuelText,gear)

    def checkSpeedRecord(self,speed):
        now = self.timer.getTime()
        if speed <= 0:
            self.startRecord=self.timer.getTime()
        elif (speed >= 100) and (now - self.startRecord < self.endRecord - self.startRecord):
            self.endRecord=now
        
