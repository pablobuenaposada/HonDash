from Tkinter import *
#from Rpm import *
from Gforce import *


root = Tk()

index=0
def set(canvas,a):
    a.setGforce(0,-2)
    canvas.after(10,set,canvas,a)
    None


  

canvas = Canvas(root, width=800, height=800,bg="white")
canvas.pack()



a=Gforce(canvas,500,500,200,2,1,"gray",4,"red")
a.setGforce(-1,-1)

canvas.after(10,set,canvas,a)

root.mainloop()
