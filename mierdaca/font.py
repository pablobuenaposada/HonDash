from Tkinter import *
from Text import *

root = Tk()



canvas = Canvas(root, width=800, height=800,bg="red")
canvas.pack()


Text(canvas,400,400,"Helvetica",38,"bold italic","yellow","330")





root.mainloop()
