from Tkinter import *
from Gforce import *
from adxl345 import ADXL345

adxl345 = ADXL345()

root = Tk()

index=0
def set(canvas,a):
    axes = adxl345.getAxes(True)
    a.setGforce(axes['x'],axes['y'])
    canvas.after(5,set,canvas,a)
    None




canvas = Canvas(root, width=800, height=800,bg="white")
canvas.pack()

a=Gforce(canvas,500,500,200,2,1,"gray",4,"red")
a.setGforce(-100,-100)

canvas.after(10,set,canvas,a)

root.mainloop()
