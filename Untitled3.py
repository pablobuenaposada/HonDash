from Tkinter import *


root = Tk()

    

canvas = Canvas(root, width=200, height=1000,bg="red")
canvas.pack()



line = canvas.create_line(100,100,100,5,fill="blue")
#canvas.after(10,setBarValue,canvas,rect)





root.mainloop()
