from Tkinter import *
import math
from Text import *
import time

root = Tk()
canvas = Canvas(root, width=400, height=400,bg="black")

r=150
x=200
y=200
maxValue=10
stepValue=1
bigMarksWidth=4
bigMarksHeight=15
bigMarksColor="#c3db7e"
smallMarksColor="#c3db7e"
smallMarksWidth=2
smallMarksHeight=7
valueColor="#c3db7e"
valueSize=22
startGauge=135
endGauge=210
needleCoverDiameter=30
needleCoverColor="#141416"
needleBaseWidth=3
needleTip=3
needleColor="red"
numMidLines=6

for i in range(0,maxValue+1,stepValue):
    degree=startGauge+((i*endGauge)/maxValue)
    startx=x+(r-bigMarksHeight)*math.cos(math.radians(degree))
    starty=y+(r-bigMarksHeight)*math.sin(math.radians(degree))
    finalx=x+r*math.cos(math.radians(degree))
    finaly=y+r*math.sin(math.radians(degree))
    canvas.create_line(startx,starty,finalx,finaly,fill=bigMarksColor,width=bigMarksWidth,smooth=0)
    letterx=x+(r-(bigMarksHeight+(valueSize*0.75)))*math.cos(math.radians(degree))
    lettery=y+(r-(bigMarksHeight+(valueSize*0.75)))*math.sin(math.radians(degree))
    Text(canvas,letterx,lettery,"Helvetica",valueSize,"bold",valueColor,"","",str(i))

    nextDegree=startGauge+(((i+stepValue)*endGauge)/maxValue)
    if(i < maxValue):
        step=(nextDegree+1-degree)/(numMidLines+1.0)
        for j in range(0,numMidLines+1,1):
            startx=x+(r-smallMarksHeight)*math.cos(math.radians(degree+(j*step)))
            starty=y+(r-smallMarksHeight)*math.sin(math.radians(degree+(j*step)))
            finalx=x+r*math.cos(math.radians(degree+(j*step)))
            finaly=y+r*math.sin(math.radians(degree+(j*step)))
            canvas.create_line(startx,starty,finalx,finaly,fill=smallMarksColor,width=smallMarksWidth)
 
global needleCover
needleCover=canvas.create_oval(x-(needleCoverDiameter/2),x-(needleCoverDiameter/2),y+(needleCoverDiameter/2),y+(needleCoverDiameter/2),fill=needleCoverColor)



global needleArrow
global needleBase
needleArrow=None
needleBase=None
canvas.pack()





def a(speed2):
    global needleArrow
    global needleBase
    global needleCover
    canvas.delete(needleArrow)
    canvas.delete(needleBase)

    speed=startGauge+((speed2*endGauge)/maxValue)
    finalx=x+r*math.cos(math.radians(speed))
    finaly=y+r*math.sin(math.radians(speed))    
     
    needleArrow=canvas.create_line([x,y,finalx,finaly], fill=needleColor, arrow="last", arrowshape=(r,r,needleBaseWidth), stipple="gray75")
    needleBase=canvas.create_line([x,y,finalx,finaly], fill=needleColor, width=needleTip, stipple="gray75")

    canvas.tag_raise(needleCover)
    canvas.pack()
    if speed2 < 9:
        canvas.after(50,a,speed2+0.07)

canvas.after(1,a,0)

root.mainloop()






