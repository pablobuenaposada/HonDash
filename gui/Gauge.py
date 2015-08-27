from Tkinter import *
import math
from Text import *

class Gauge:

    def __init__(self,canvas,x,y,r,startGauge,endGauge,stepValue,numMidLines,maxValue,valueColor,valueSize,valueFont,valueWeight,smallMarksHeight,smallMarksWidth,smallMarksColor,bigMarksHeight,bigMarksWidth,bigMarksColor,needleTip,needleBaseWidth,needleColor,needleStipple,needleCoverDiameter,needleCoverColor):
        self.needleArrow = None
        self.needleBase = None
        self.canvas = canvas
        self.x = x
        self.y = y
        self.r = r
        self.maxValue = maxValue
        self.startGauge = startGauge
        self.endGauge = endGauge
        self.needleBaseWidth = needleBaseWidth
        self.needleTip= needleTip
        self.needleColor= needleColor
        self.needleStipple = needleStipple
	self.idMarks = []
	self.idValues = []

        for i in range(0,self.maxValue+1,stepValue):
            degree=self.startGauge+((i*self.endGauge)/self.maxValue)
            startx=x+(r-bigMarksHeight)*math.cos(math.radians(degree))
            starty=y+(r-bigMarksHeight)*math.sin(math.radians(degree))
            finalx=x+r*math.cos(math.radians(degree))
            finaly=y+r*math.sin(math.radians(degree))
            self.idMarks.append(canvas.create_line(startx,starty,finalx,finaly,fill=bigMarksColor,width=bigMarksWidth,smooth=0))
            letterx=x+(r-(bigMarksHeight+(valueSize*0.75)))*math.cos(math.radians(degree))
            lettery=y+(r-(bigMarksHeight+(valueSize*0.75)))*math.sin(math.radians(degree))
            self.idValues.append(Text(canvas,letterx,lettery,valueFont,valueSize,valueWeight,valueColor,"","",str(i)))

            nextDegree=self.startGauge+(((i+stepValue)*self.endGauge)/self.maxValue)
            if(i < self.maxValue):
                step=(nextDegree+1-degree)/(numMidLines+1.0)
                for j in range(0,numMidLines+1,1):
                    startx=self.x+(r-smallMarksHeight)*math.cos(math.radians(degree+(j*step)))
                    starty=self.y+(r-smallMarksHeight)*math.sin(math.radians(degree+(j*step)))
                    finalx=self.x+r*math.cos(math.radians(degree+(j*step)))
                    finaly=self.y+r*math.sin(math.radians(degree+(j*step)))
                    self.idMarks.append(canvas.create_line(startx,starty,finalx,finaly,fill=smallMarksColor,width=smallMarksWidth))
 
        #needle cover
        self.needleCover=canvas.create_oval(x-(needleCoverDiameter/2),y-(needleCoverDiameter/2),x+(needleCoverDiameter/2),y+(needleCoverDiameter/2),fill=needleCoverColor)

    def setValue(self,value):
	self.canvas.delete(self.needleArrow)
        self.canvas.delete(self.needleBase)

        speed=self.startGauge+((value*self.endGauge)/self.maxValue)
        finalx=self.x+self.r*math.cos(math.radians(speed))
        finaly=self.y+self.r*math.sin(math.radians(speed))    
     
        self.needleArrow=self.canvas.create_line([self.x,self.y,finalx,finaly], fill=self.needleColor, arrow="last", arrowshape=(self.r,self.r,self.needleBaseWidth), stipple=self.needleStipple)
        self.needleBase=self.canvas.create_line([self.x,self.y,finalx,finaly], fill=self.needleColor, width=self.needleTip, stipple=self.needleStipple)

        self.canvas.tag_raise(self.needleCover)
        self.canvas.pack()
    
    def setNeedleCoverColor(self,color):
	self.canvas.itemconfig(self.needleCover, fill=color)

    def setColor(self,color):
	for mark in self.idMarks:
	    self.canvas.itemconfig(mark,fill=color)

	for number in self.idValues:
	    number.setColor(color)












