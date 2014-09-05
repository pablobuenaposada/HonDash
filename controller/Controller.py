def updateRpm(canvas,serial,rpm):
    rpm.setRpm(serial.getRpm())
    canvas.after(10,updateRpm,canvas,serial,rpm)
    
def updateBattery(canvas,serial,circle):
    circle.setValue(serial.getBattery())
    canvas.after(10,updateBattery,canvas,serial,circle)

def updateTps(canvas,mcp3208,channel,bar):
    bar.setHeight(mcp3208.getADC(channel))
    canvas.after(10,updateTps,canvas,mcp3208,channel,bar)
    
def updateAnalog(canvas,mcp3208,channel,circle):
    circle.setValue(mcp3208.getADC(channel))    
    canvas.after(10,updateAnalog,canvas,mcp3208,channel,circle)

def updateAll(canvas,mcp3208,serial,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake):
    rpm.setRpm(serial.getRpm())
    speed.setText(serial.getVss())
    oilTemp.setValue(mcp3208.getADC(7)) 
    oilPressure.setValue(mcp3208.getADC(6))
    fuel.setWidth(mcp3208.getADC(7))
    h2o.setValue(mcp3208.getADC(5))
    h2oEcu.setValue(int(serial.getEct()))
    battery.setValue(round(serial.getBattery(),1))
    throttle.setHeight(mcp3208.getADC(8))
    clutch.setHeight(mcp3208.getADC(4))
    brake.setHeight(mcp3208.getADC(3))
    canvas.after(10,updateAll,canvas,mcp3208,serial,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake)
