from tkinter import *
from Pixel import Pixel
import time, random
import numpy as np



class Tetrominoes:

    '''
        constructor
    '''
    def __init__(self,canvas,numberOfRows,numberOfColumns,scale,color = 2,patterns = None ):

        self.currentPixels = []
        self.color = 2

        self.canvas = canvas
        self.scale = scale
        self.numberOfRows = numberOfRows
        self.numberOfColumns = numberOfColumns

        self.patterns = patterns
        if (patterns == None ): 
            self.name = "Basic"
            self.patterns = [np.array([[2,2,2],[2,0,2],[2,2,2]])]
        else:
            self.name = "Custom"

        self.i = 0
        self.j = np.nan
        '''
            requirement: For this project, we are assuming that even if you add 
                         more matrix patterns for the same Tetromino family into the list, they should all have the same 
                         height and width. 
        '''
        
        
        self.setActivePattern(0)

        self.color = color
        
        self.nbpattern  = len(self.patterns)


    '''
        return current pattern
    '''
    def get_pattern(self):
        return self.patterns[self.currentPattern]

    '''
        method to activate current pattern start at row and column
        if column value is not passed generate a random, such that the shape does not go out of bounds

    '''
    def activate(self,row = 0, column = np.nan):

        self.i = row
        #no column position specified calculate default column position
        self.j = column
        if (np.isnan(self.j) == True):
            '''
                if height of the current shape is '3' and numberOfColumns of the canvas is '30'
                then for the shape to not go outof bounds, it can not start beyond row 30 - 3 = 27
            '''
            maxStartForColumn = self.numberOfColumns - self.w
            self.j = random.randint(0, maxStartForColumn)
        
        self.drawTetrominoes()
        
    
    '''
        Draws active Tetrominoe
    '''
    def drawTetrominoes(self):
        shapePixels = []
        currentPattern = self.getCurrentPattern()
        for row_idx, row in enumerate(currentPattern):
            pixelRow = self.i + row_idx
            for column, color in enumerate(row):
                pixelColumn = self.j + column
                if (color != 0): 
                    pixel =  Pixel(self.canvas,pixelRow,pixelColumn
                                        ,self.numberOfRows,self.numberOfColumns,self.scale
                                            ,self.color)
                    shapePixels.append(pixel)
        
        self.currentPixels = shapePixels

    def getCurrentPattern(self):
        return self.patterns[self.currentPattern]
    
    '''
        Assuming 2 patterns, switch from one pattern to another, i.e. swap current pattern with the other one in the list
    '''
    def rotate(self):

        #delete active pattern display  
        self.delete()

        #swap patterns
        swapPatternIndex = 0 if ( self.currentPattern + 1  == self.nbpattern )  else self.currentPattern + 1
        self.setActivePattern(swapPatternIndex)
        
        #display active pattern
        self.activate(self.i,self.j)

    '''
        Set the active pattern to the passed index
    '''
    def setActivePattern(self,activatePatternIndex):
       
        self.currentPattern = activatePatternIndex
        self.h, self.w =  self.patterns[self.currentPattern].shape



    def delete(self):

        self.deleteActivePattern()

    '''
        delete active pattern and related properties
    '''
    def deleteActivePattern(self):
        
        for pixel in self.currentPixels:
            pixel.delete()
        self.currentPixels.clear()

    def left(self):

        self.deleteActivePattern()

        if self.j == 0:
            self.j = self.numberOfColumns - self.w
        else:
            self.j -= 1

        self.drawTetrominoes()

    
    def right(self):

        self.deleteActivePattern()

        if self.j == self.numberOfColumns - self.w:
            self.j =0
        else:
            self.j += 1

        self.drawTetrominoes()

    def up(self):

        self.deleteActivePattern()

        if self.i == 0:
            self.i = self.numberOfRows - self.h
        else:
            self.i -= 1

        self.drawTetrominoes()

    def down(self):

        self.deleteActivePattern()

        if self.i == self.numberOfRows - self.h:
            self.i = 0
        else:
            self.i += 1

        self.drawTetrominoes()


    @staticmethod
    def random_select(canv,nrow,ncol,scale):
        t1=TShape(canv,nrow,ncol,scale)
        t2=TripodA(canv,nrow,ncol,scale)
        t3=TripodB(canv,nrow,ncol,scale)
        t4=SnakeA(canv,nrow,ncol,scale)
        t5=SnakeB(canv,nrow,ncol,scale)
        t6=Cube(canv,nrow,ncol,scale)
        t7=Pencil(canv,nrow,ncol,scale)        
        return random.choice([t1,t2,t3,t4,t5,t6,t7,t7]) #a bit more change to obtain a pencil shape
        


#########################################################
############# All Child Classes #########################
#########################################################

class TShape(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[0,3,0],[0,3,0],[3,3,3]]))
        patterns.append(np.array([[3,3,3],[0,3,0],[0,3,0]]))
        patterns.append(np.array([[0,0,3],[3,3,3],[0,0,3]]))
        patterns.append(np.array([[3,0,0],[3,3,3],[3,0,0]]))

        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=3, patterns= patterns)

        self.name = "TShape"

class TripodA(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[0,4,0],[0,4,0],[4,0,4]]))
        patterns.append(np.array([[4,0,4],[0,4,0],[0,4,0]]))
        patterns.append(np.array([[0,0,4],[4,4,0],[0,0,4]]))
        patterns.append(np.array([[4,0,0],[0,4,4],[4,0,0]]))

        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=4,patterns= patterns)

        self.name = "TripodA"

class TripodB(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[0,5,0],[5,0,5],[5,0,5]]))
        patterns.append(np.array([[5,0,5],[5,0,5],[0,5,0]]))
        patterns.append(np.array([[0,5,5],[5,0,0],[0,5,5]]))
        patterns.append(np.array([[5,5,0],[0,0,5],[5,5,0]]))



        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=5, patterns= patterns)

        self.name = "TripodB"

class SnakeA(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[6,6,0],[0,6,0],[0,6,6]]))
        patterns.append(np.array([[0,0,6],[6,6,6],[6,0,0]]))
        
        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=6 ,patterns= patterns)

        self.name = "SnakeA"


class SnakeB(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[0,7,7],[0,7,0],[7,7,0]]))
        patterns.append(np.array([[7,0,0],[7,7,7],[0,0,7]]))
        
        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=7, patterns= patterns)

        self.name = "SnakeB"


class Cube(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[8,8,8],[8,8,8],[8,8,8]]))
        patterns.append(np.array([[0,8,0],[8,8,8],[0,8,0]]))
        patterns.append(np.array([[8,0,8],[0,8,0],[8,0,8]]))
       
        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=8,patterns= patterns)

        self.name = "Cube"

class Pencil(Tetrominoes):

    def __init__(self,canvas,numberOfRows,numberOfColumns,scale):

        patterns = []
        patterns.append(np.array([[0,9,0],[0,9,0],[0,9,0]]))
        patterns.append(np.array([[0,0,0],[0,0,0],[9,9,9]]))
        patterns.append(np.array([[0,0,9],[0,0,9],[0,0,9]]))
        patterns.append(np.array([[9,0,0],[9,0,0],[9,0,0]]))
       
        super().__init__(canvas,numberOfRows,numberOfColumns,scale,color=9 ,patterns= patterns)

        self.name = "Pencil"


#########################################################
############# Testing Functions #########################
#########################################################
def delete_all(canvas):
    canvas.delete("all")
    print("Delete All")


def test1(canvas,nrow,ncol,scale):
    print("Generate a Tetromino (basic shape)- different options")
    
    tetro1=Tetrominoes(canvas,nrow,ncol,scale) # instantiate
    print("Tetro1",tetro1.name)
    print("  number of patterns:",tetro1.nbpattern)
    print("  current pattern:\n",tetro1.get_pattern()) # retrieve current pattern
    print("  height/width:",tetro1.h,tetro1.w)
    tetro1.activate(nrow//2,ncol//2)        # activate and put in the middle
    print("  i/j coords:  ",tetro1.i,tetro1.j)

    pattern=np.array([[0,3,0],[3,3,3],[0,3,0],[3,0,3],[3,0,3]]) # matrix motif
    tetro2=Tetrominoes(canvas,nrow,ncol,scale,3,[pattern]) # instantiate (list of patterns-- 1 item here)
    print("\nTetro2",tetro2.name)
    print("  number of patterns:",tetro2.nbpattern)
    print("  current pattern:\n",tetro2.get_pattern()) # retrieve current pattern
    print("  height/width:",tetro2.h,tetro2.w)
    tetro2.activate()        # activate and place at random at the top
    print("  i/j coords:  ",tetro2.i,tetro2.j)

    
    
def test2(root,canvas,nrow,ncol,scale):
    print("Generate a 'square' Tetromino (with double shape) and rotate")
    
    print("My Tetro")
    pattern1=np.array([[4,0,0],[0,4,0],[0,0,4]]) # matrix motif
    pattern2=np.array([[0,0,4],[0,4,0],[4,0,0]]) # matrix motif
    tetro=Tetrominoes(canvas,nrow,ncol,scale,4,[pattern1,pattern2]) # instantiate (list of patterns-- 2 items here)
    print("  number of patterns:",tetro.nbpattern)
    print("  height/width:",tetro.h,tetro.w)
    
    tetro.activate(nrow//2,ncol//2)        # activate and place in the middle
    
    print("  i/j coords:  ",tetro.i,tetro.j)

    for k in range(10): # make 10 rotations
        tetro.rotate() # rotate (change pattern)
        print("  current pattern:\n",tetro.get_pattern()) # retrieve current pattern
        root.update()
        time.sleep(0.5)
    
    tetro.delete() # delete tetro (delete every pixels)


def rotate_all(tetros): #auxiliary routine
    for t in tetros:
        t.rotate()
    
       
def test3(root,canvas,nrow,ncol,scale):
    print("Dancing Tetrominoes")

    t0=Tetrominoes(canvas,nrow,ncol,scale)
    t1=TShape(canvas,nrow,ncol,scale)
    t2=TripodA(canvas,nrow,ncol,scale)
    t3=TripodB(canvas,nrow,ncol,scale)
    t4=SnakeA(canvas,nrow,ncol,scale)
    t5=SnakeB(canvas,nrow,ncol,scale)
    t6=Cube(canvas,nrow,ncol,scale)
    t7=Pencil(canvas,nrow,ncol,scale)
    tetros=[t0,t1,t2,t3,t4,t5,t6,t7]

    for t in tetros:
        print(t.name)

    # place the tetrominos
    for i in range(4):
        for j in range(2):
            k=i*2+j
            tetros[k].activate(5+i*10,8+j*10)
            
    ####### Tkinter binding for this test
    root.bind("<space>",lambda e:rotate_all(tetros))     

    
      
def test4(root,canvas,nrow,ncol,scale):
    print("Moving Tetromino")
    tetro=Tetrominoes.random_select(canvas,nrow,ncol,scale) # choose at random
    print(tetro.name)
        
    ####### Tkinter binding for this test
    root.bind("<space>",lambda e:tetro.rotate())
    root.bind("<Up>",lambda e:tetro.up())
    root.bind("<Down>",lambda e:tetro.down())
    root.bind("<Left>",lambda e:tetro.left())
    root.bind("<Right>",lambda e:tetro.right())

    tetro.activate()

    

#########################################################
############# Main code #################################
#########################################################

def main():
    
        ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        nrow=45
        ncol=30
        scale=20
        canvas = Canvas(root,width=ncol*scale,height=nrow*scale,bg="black") # create a canvas width*height
        canvas.pack()

        ### general binding events to choose a testing function
        root.bind("1",lambda e:test1(canvas,nrow,ncol,scale))
        root.bind("2",lambda e:test2(root,canvas,nrow,ncol,scale))
        root.bind("3",lambda e:test3(root,canvas,nrow,ncol,scale))
        root.bind("4",lambda e:test4(root,canvas,nrow,ncol,scale))
        root.bind("<d>",lambda e:delete_all(canvas))

        
        root.mainloop() # wait until the window is closed        

if __name__=="__main__":
    main()

