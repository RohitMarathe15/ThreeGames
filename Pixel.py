from tkinter import *
import time
import random
import numpy

class Pixel:

    color=['black','white','yellow','red','blue','green','orange','purple','brown','cyan']

    #pixel direction, default is stationary position
    #1st element of the array indicate up/down direction 1 => down -1 => up
    #2nd element of the array indicate left/right direction 1 => right -1 => left
    vector=[0,0]

    ### to complete        
    #constructor of Pixel class
    #default direction is standstill/no movement
    def __init__(self,canvas : Canvas,y: int,x: int,nrow: int,ncol: int,scale: int,c: int,direction = [0,0] ):
        
        self.canvas = canvas
        self.scale = scale
        self.vector = direction
        self.color = self.color[c]
        

        #total size of the canvas
        self.nrow = nrow 
        self.ncol = ncol 

        #scaled size of the canvas for real world
        self.scalednrow = self.nrow * self.scale
        self.scaledcol = self.ncol * self.scale
        
        #maxEdgeRow, maxEdgeCol are requried to test the pixel reaching edage of the grid
        self.maxEdgeRow = self.scalednrow
        self.maxEdgeCol = self.scaledcol

        #handle pixel cordinates going out of bounds
        if x > self.ncol- 1:
            x = x % self.ncol
        #handle pixel cordinates going out of bounds
        if y > self.nrow - 1:
            y  = y % self.nrow 
        
        self.i = x
        self.j = y

        #scaled colordinates to display in real world
        realX = x * self.scale
        realY = y * self.scale

        #create pixel, store the the id for the pixel i.e. reactagle for movement
        self.pixelId =  self.canvas.create_rectangle(realX, realY
                                            , realX + self.scale , realY + self.scale
                                            , fill= self.color )
        
        
    #string representation of the Pixel instance
    def __str__(self):
        coord = self.canvas.coords(self.pixelId)
        x = int(coord[0]/self.scale)
        y  = int(coord[1] / self.scale)
        return f"( {y},{x} {self.color})"

    '''
        move pixel by one unit per call.
    '''

    def next(self):
        
        '''
            get current pixel coordinates 
            coords method return a list of 4 items representing the position of the pixel i.e. ractangle per below

            from tkinter docs
            https://tkinter-docs.readthedocs.io/en/latest/widgets/canvas.html

            For rectangles, ovals and arcs the returned list of coordinates has a fixed order, 
            namely the left, top, right and bottom coordinates, which may not be the order originally given. 

        '''

        pixelPosition = self.canvas.coords(self.pixelId)

        #calculate new x coordiate
        newLeft = pixelPosition[0] +  self.vector[1] * self.scale
        

        #handle pixel reaching the left edge of the canvas, set the x position to right edge
        if newLeft == -20:
            pixelPosition[0] = self.scaledcol - self.scale
            pixelPosition[2] = self.scaledcol
        #handle pixel reaching right edge of the canvas, set the x position to left edge
        elif newLeft == self.maxEdgeCol :
            pixelPosition[0] = 0 
            pixelPosition[2] = self.scale
        #move pixel by ONE unit - ONE unit => 
        else:
            pixelPosition[0]  = newLeft

            #update new right
            pixelPosition[2]  = pixelPosition[2] +  self.vector[1] * self.scale

        #calculate new Top value 
        newTop = pixelPosition[1] +  self.vector[0] * self.scale

        #handle pixel reaching first row of the canvas, set it to last row 
        if newTop == -20:
            pixelPosition[1]  = self.scalednrow - self.scale
            pixelPosition[3]  = self.scalednrow
        #handle pixel reaching last row of the canvas, set it to first row 
        elif newTop == self.maxEdgeRow: 
            pixelPosition[1]  = 0
            pixelPosition[3]  = self.scale
        else:
            pixelPosition[1]  = newTop
            
            #update new bottom
            pixelPosition[3]  = pixelPosition[3] +  self.vector[0] * self.scale

        self.canvas.coords(self.pixelId,pixelPosition)
        
        #j => row i.e. y axis coordinate
        self.j =  int(pixelPosition[1] // self.scale)
        
        #i => column i.e. x axis coordinate
        self.i =  int(pixelPosition[0] // self.scale)
        


    def right(self):
        self.vector[0] = 0
        self.vector[1] = 1
     
    def left(self):
        self.vector[0] = 0
        self.vector[1] = -1

    def up(self):
        self.vector[0] = -1
        self.vector[1] = 0
    
    def down(self):
        self.vector[0] = 1
        self.vector[1] = 0

    def delete(self):
        self.canvas.delete(self.pixelId)








        
#################################################################
########## TESTING FUNCTION
#################################################################
def delete_all(canvas):
    
    canvas.delete("all")
    print("Delete All")


def test1(canvas,nrow,ncol,scale):
    print("Generate 10 points at random")
    random.seed(4) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1) 
        j=random.randint(0,ncol-1)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(pix)

def test2(canvas,nrow,ncol,scale):
    print("Generate 10 points at random (using modulo)")
    random.seed(5) # for reproducibility
    for k in range(10):
        i=random.randint(0,nrow-1)*34
        j=random.randint(0,ncol-1)*13
        ij=str(i)+","+str(j)
        c=random.randint(1,9)    # color number
        pix=Pixel(canvas,i,j,nrow,ncol,scale,c)
        print(ij,"->",pix)

        
def test3(root,canvas,nrow,ncol,scale):
    print("Move one point along a square")

    pix=Pixel(canvas,35,35,nrow,ncol,scale,3)
    pix.vector=[-1,0] # set up direction (up)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,-1] # set up new direction (left)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[1,0]   # set up new direction (down)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)
        
    pix.vector=[0,1]    # set up new direction (right)
    for i in range(30):
        pix.next()       # next move in the simulation 
        root.update()    # update the graphic
        time.sleep(0.05) # wait in second (simulation)

    #delete point
    pix.delete()


  
def test4(root,canvas,nrow,ncol,scale):
    print("Move four point along a square")

    pixs=[]
    pixs.append(Pixel(canvas,35,35,nrow,ncol,scale,3,[-1,0]))
    
    #orignal commented out as, it's moving the 5,35 point to the left
    #moving it outside of the screen
    pixs.append(Pixel(canvas,5,35,nrow,ncol,scale,4,[0,-1]))
    #pixs.append(Pixel(canvas,5,35,nrow,ncol,scale,4,[0,1]))
    
    pixs.append(Pixel(canvas,5,5,nrow,ncol,scale,5,[1,0]))
    
    
    #orignal commented out as, it's moving the 35,5 point to the right
    #moving it outside of the screen
    pixs.append(Pixel(canvas,35,5,nrow,ncol,scale,6,[0,1]))
    #pixs.append(Pixel(canvas,35,5,nrow,ncol,scale,6,[0,-1]))
    
    print("Starting coords")
    for p in pixs: print(p)

    for i in range(30):
        for p in pixs:
            p.next()       # next move in the simulation     
        root.update()      # update the graphic
        time.sleep(0.05)   # wait in second (simulation)
        
    print("Ending coords")
    for p in pixs:
        print(p)
        p.delete()


        
def test5(root,canvas,nrow,ncol,scale):
    print("Move one point any direction -use arrow commands")

    pix=Pixel(canvas,20,20,nrow,ncol,scale,2)

    ### binding used by test5
    root.bind("<Right>",lambda e:pix.right())
    root.bind("<Left>",lambda e:pix.left())
    root.bind("<Up>",lambda e:pix.up())
    root.bind("<Down>",lambda e:pix.down())

    ### simulation
    while True:
        pix.next()
        root.update()     # update the graphic
        time.sleep(0.05)  # wait in second (simulation)


        

###################################################
#################### Main method ##################
###################################################


def main():
       
        ##### create a window, canvas
        root = Tk() # instantiate a tkinter window
        nrow=40
        ncol=40
        scale=20
        canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black") # create a canvas width*height
        canvas.pack()

        ### general binding events to choose a testing function
        root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
        root.bind("2",lambda e:test2(canvas,nrow,ncol,scale))
        root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
        root.bind("4",lambda e:test4(root,canvas,nrow,ncol,scale))
        root.bind("5",lambda e:test5(root,canvas,nrow,ncol,scale))
        root.bind("<d>",lambda e:delete_all(canvas))
        
       
        
        root.mainloop() # wait until the window is closed
        
if __name__=="__main__":
    main()

