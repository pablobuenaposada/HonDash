from Tkinter import *
import math
from Text import *
import time
from ClassicGauge import *


root = Tk()
canvas = Canvas(root, width=400, height=400,bg="black")


canvas.pack()
a=ClassicGauge(canvas,200,200,150,135,210,1,6,10,"#c3db7e",22,"Helvetica","bold italic",7,2,"#c3db7e",15,4,"#c3db7e",3,3,"red","gray75",30,"#141416")
a.setValue(7)



def b(speed):
    a.setValue(speed)
    canvas.after(50,b,speed+0.07)


canvas.after(50,b,0)

root.mainloop()
