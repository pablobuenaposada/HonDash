def updateRpm(serial,rpm):    
    rpm.setRpm(serial.getRpm())

def updateBattery(serial,circle):
    circle.setValue(serial.getBattery())

def updateTps(serial,bar):
    bar.setHeight(serial.getTps())

def updateAnalog(mcp3208,channel,circle):
    circle.setValue(mcp3208.getADC(channel))    
 
