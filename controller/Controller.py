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

def updateAll(canvas,mcp3208,serial,rpm,speed,temp1,temp2,temp3,temp4,throttle,clutch,brake):
    rpm.setRpm(serial.getRpm())
    speed.setText(serial.getVss())
    temp1.setValue(mcp3208.getADC(7)) 
    temp2.setValue(mcp3208.getADC(6)) 
    temp3.setValue(mcp3208.getADC(5))
    throttle.setHeight(mcp3208.getADC(8))
    clutch.setHeight(mcp3208.getADC(4))
    brake.setHeight(mcp3208.getADC(3))
    canvas.after(10,updateAll,canvas,mcp3208,serial,rpm,speed,temp1,temp2,temp3,temp4,throttle,clutch,brake)
