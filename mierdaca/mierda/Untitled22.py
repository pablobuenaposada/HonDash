from Tkinter import *


root = Tk()

    

canvas = Canvas(root, width=1000, height=1000,bg="white")
canvas.pack()

a = [-150,0,0,125,0,50,150,50,150,-50,0,-50,0,-125]
b = [-175,50,0,50,0,125,150,0,0,-125,0,-50,-175,-50]
points=[]
for x in a:
    points.append(x+300)




z=canvas.create_polygon(a, outline='red',fill='green', width=2)
canvas.pack(fill=BOTH, expand=1)
canvas.scale( z , 0 , 0 , 0.5 , 0.5)
root.mainloop()
