from Tkinter import *
from Rpm import *


root = Tk()

index=0
def set(canvas,arc):
    global index
    arc.set_status(index)
    index=index+1    
    canvas.after(10,set,canvas,arc)
    None

    

canvas = Canvas(root, width=800, height=800,bg="red")
canvas.pack()




arc = Rpm(canvas,500,200,500,200,50,"yellow","green",0,180,0,1000)


canvas.after(10,set,canvas,arc)



root.mainloop()



