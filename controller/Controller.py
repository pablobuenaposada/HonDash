from devices.Time import *

class Controller:
    
    def __init__(self):
        self.startRecord = -1
        self.endRecord = -1
        self.timer = Time()

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

    def things2control(self,digital4,digital17,digital22,digital23,digital24,digital25,digital27,arrowLeft,arrowRight,fuelIcon,highBeamIcon,trunkIcon,oilIcon):
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


    def callbackArrowLeft(self,channel):
    	self.arrowLeft.setFill(self.digital25.getValue())

    def callbackArrowRight(self,channel):
	self.arrowRight.setFill(self.digital24.getValue())

    def callbackFuelIcon(self,channel):
	self.fuelIcon.setHidden(self.digital4.getValue())

    def callbackHighBeamIcon(self,channel):
	self.highBeamIcon.setHidden(self.digital17.getValue())

    def callbackTrunkIcon(self,channel):
	self.trunkIcon.setHidden(self.digital27.getValue())    

    def callbackOilIcon(self,channel):
	self.oilIcon.setHidden(self.digital22.getValue())

    def callbackLights(self,channel):
	print "aaaaaaaa"
	pass

    def updateAll(self,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight,accelerometer,g,fuelText):

	rpm.setRpm(serial.getRpm())
	mapp.setText(serial.getMap())
        ign.setText(int(serial.getIgn()))
	iat.setText(int(serial.getIat()))
	inj.setText(serial.getInj())
	duty.setText(serial.getDutyCycle())
	speed.setText(serial.getVss())
        oilTemp.setValue(self.adc2oiltemp(mcp3208.getADC(7))) 
        oilPressure.setValue(self.adc2oilpress(mcp3208.getADC(5)))
        fuel.setWidth(self.adc2fuel(mcp3208.getADC(3)))
	fuelText.setText(self.adc2fuel(mcp3208.getADC(3)))
        h2o.setValue(mcp3208.getADC(4))
        h2oEcu.setText(int(serial.getEct()))
        battery.setText(round(serial.getBattery(),1))
        throttle.setHeight(serial.getTps())
        clutch.setHeight(mcp3208.getADC(1))
	if(serial.getVtec()): vtec.setText("on")
	else: vtec.setText("off")
        #brake.setHeight(mcp3208.getADC(7))
        time = self.timer.getTime()
        runTime.setText(self.timer.getTimeString())
	#axes = accelerometer.getAxes(True)
	#g.setGforce(axes['x'],axes['y'])

        canvas.after(10,controller.updateAll,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime,inj,duty,vtec,iat,ign,mapp,arrowLeft,arrowRight,accelerometer,g,fuelText)

    def checkSpeedRecord(self,speed):
        now = self.timer.getTime()
        if speed <= 0:
            self.startRecord=self.timer.getTime()
        elif (speed >= 100) and (now - self.startRecord < self.endRecord - self.startRecord):
            self.endRecord=now
        
