class Arrow:

     def __init__(self,canvas,x,y,scale,color,way):
        if way == "left": points = [-150,0,0,125,0,50,150,50,150,-50,0,-50,0,-125]
        else: points = [-150,50,0,50,0,125,150,0,0,-125,0,-50,-150,-50]

        self.canvas = canvas        
        deleteId = canvas.create_polygon(points,fill=color,state="hidden")
        canvas.scale(deleteId,0,0,scale,scale)
        points = canvas.coords(deleteId)

        for pos in range(0,len(points)):
            if pos%2 == 0:
                points[pos] = points[pos] + x
            else:
                points[pos] = points[pos] + y  

        self.id = canvas.create_polygon(points,fill=color)
        canvas.delete(deleteId)
        
