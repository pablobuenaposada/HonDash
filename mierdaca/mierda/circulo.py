# -*- coding: utf-8 -*-
from Tkinter import *
from Circle import *


root = Tk()

index=20
def set(canvas,arc):
    global index
    arc.set_status(index)
    index=index+1    
    canvas.after(10,set,canvas,arc)
    

    

canvas = Canvas(root, width=800, height=800,bg="red")
canvas.pack()




arc = Circle(canvas,50,50,150,15,240,300,20,100,"blue")


canvas.after(10,set,canvas,arc)



root.mainloop()
