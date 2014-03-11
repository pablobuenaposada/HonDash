from Tkinter import *
from Bar import *

root = Tk()

index=500
def a(rect,canvas):
    global index
    rect.setHeight(index)
    index=index-1
    canvas.after(10,a,rect,canvas)
    

canvas = Canvas(root, width=1000, height=1000,bg="red")
canvas.pack()

rect=Bar(canvas,10,500,50,0,"blue")
canvas.after(10,a,rect,canvas)

root.mainloop()
