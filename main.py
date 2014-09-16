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
circleTextSize = 20

#init canvas
canvas = Canvas(root,width=winWidth,height=winHeight,bg="white")
canvas.pack()

#init graphics
rpm = Rpm(canvas,winWidth/2,winHeight/4.0,winWidth/1.00,winHeight/2.75,100,"orange","yellow",20,140,0,10000)
speed = Text(canvas,winWidth/2,winHeight/4,"Helvetica",speedFontSize,"bold italic","black","","137")
mileage = Text(canvas,winWidth/2,(winHeight/10)*3,"Helvetica",10,"bold ","black","","162.372 KM")
fuel = Bar(canvas,(winWidth/2)-200,(winHeight/8)*3,0,400,0,20,0,4096,"#efbbff")

clutch = Bar(canvas,winWidth-182,winHeight,60,60,0,250,0,200,"blue")
brake = Bar(canvas,winWidth-121,winHeight,60,60,0,250,0,200,"red")
throttle = Bar(canvas,winWidth-60,winHeight,60,60,0,250,0,200,"green")

oilTemp = Circle(canvas,(winWidth/8)*1,(winHeight/2)*1,200,50,240,300,0,4096,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"OIL T.")
oilPressure = Circle(canvas,(winWidth/8)*3,(winHeight/2)*1,200,50,240,300,0,4096,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"OIL P.")
h2o = Circle(canvas,(winWidth/8)*5,(winHeight/2)*1,200,50,240,300,0,4096,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"H2O T.")
g = Gforce(canvas,(winWidth/8)*7,(winHeight/2)*1,250,2,1,"gray",4,"red")

h2oEcu = Circle(canvas,(winWidth/4)*1,(winHeight/4)*3,100,25,240,300,0,4096,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"H2O T.2")
battery = Circle(canvas,(winWidth/4)*2,(winHeight/4)*3,100,25,240,300,0,15,200,3000,"blue","#28cfbc","red",circleValueSize,circleTextSize,"BAT")

arrowLeft = Arrow(canvas,(winWidth/3)*1,winHeight/4,0.25,"green","left")
arrowRight = Arrow(canvas,(winWidth/3)*2,winHeight/4,0.25,"green","right")
runTime = Text(canvas,winWidth/2,(winHeight/10)*9,"Helvetica",13,"bold ","black","Run Time ","00:00:00")

#init devices
controller = Controller()
serial = CromeQD2()
mcp3208 = MCP3208()

#update graphics
canvas.after(10,controller.updateAll,canvas,mcp3208,serial,controller,rpm,speed,oilTemp,oilPressure,h2o,h2oEcu,battery,fuel,throttle,clutch,brake,runTime)

#main loop
root.mainloop()



