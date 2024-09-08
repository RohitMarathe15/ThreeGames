from tkinter import *
from Grid import Grid
from Tetrominoes import Tetrominoes, Cube
import numpy as np
import time

        
class Tetris (Grid):
     
     def __init__ (self, root, rows, columns, scale):
          
          self.__shouldPause = False
          self.__gameOver = False

          super().__init__(root,rows,columns,scale)


          self.__block = None


     '''

     '''
     def next(self):
     
        if self.__block == None:
            self.__block = Tetrominoes.random_select(self.canvas,self.rows,self.columns,self.scale)
            #self.__block = Cube(self.canvas,self.rows,self.columns,self.scale)
            self.__block.activate()
        else:

            if self.hasBlockReachedBottom() == False :
                if self.__isOverlapping(self.__block.i +1, self.__block.j)  == True :
                    self.__placeBlock()

                    if self.__reachedTop() == True:
                        self.__gameOver = True
                        self.__displayGameOverText()
                    return        

                self.__block.down()
            else:
                self.__placeBlock()

     '''
     '''
     def up(self):
        
        if self.__block == None:
            return
        
        self.__block.rotate()
          
     '''
        fastforward the 'place' action
     '''
     def down(self):
        
        if self.__block == None:
            return
        
        while self.__block != None:

           self.next()


     '''
        move the current block by one pixel to right
     '''
     def right(self):
        
        if self.__block == None:
            return
        
        if self.__block.j == self.columns - 3:
            return
        
        self.__block.right()
        print(f"i {self.__block.i} j {self.__block.j}")

     '''
        move the current block by one pixel to left
     '''
     def left(self):
        
        if self.__block == None:
            return
        
        if self.__block.j == 0:
            return

        self.__block.left()
        print(f"i {self.__block.i} j {self.__block.j}")

     '''
        Pause the game, if already paused strat the game
     '''
     def pause(self):

        self.__shouldPause = not self.__shouldPause

     
     def is_pause(self):
         return self.__shouldPause
     
     def is_game_over(self):
         return self.__gameOver

     '''
        return True if current Tetromino has reached the bottom
     '''
     def hasBlockReachedBottom(self):
         
         if self.__block == None:
             return
         
         if self.__block.i == self.rows - 3:
             return True
         else:
             return False

     '''
        method to place a block, at block's current position.
        To place the block, apply non-black colors to the the grid
        Delete the Tetromiono shape.
        Clear the block instance variable

        After placing the block, check if the block reasulted in filling row(s) completly
        Delete completely filled rows
     '''
     def __placeBlock(self):
         
        if self.__block == None:
            return
        
        rowsToCheck = []

        currentPattern = self.__block.getCurrentPattern()
        for row_idx, row in enumerate(currentPattern):
            pixelRow = self.__block.i + row_idx
            for column, color in enumerate(row):
                pixelColumn = self.__block.j + column
                if (color != 0):
                    column = pixelColumn * self.scale
                    row =  pixelRow * self.scale
                    self.addxy(column,row,color)
            
            #check if all columns are filled
            allColumnsFilled = True
            for columnToCheck in range(self.columns - 1):
              if self._dataMatrix[self.__block.i + row_idx,columnToCheck] == 0:
                    allColumnsFilled = False
                    break
            
            if allColumnsFilled == True:
                rowsToCheck.append(self.__block.i + row_idx)
            

        self.__block.delete()
        self.__block = None

        rowsToCheck.sort()
        for rowToFlush in rowsToCheck:
            self.flushRow(rowToFlush)

     '''
        check whether there is any shape at a 3x3 matrix. The matrix top left row,column index is passed as an 
        argument. 

        function failing when red reverse T shapeis drooped on blue

     '''
     def __isOverlapping(self,i,j):
         
        currentj = 0
        currentPattern = self.__block.getCurrentPattern()
        currenti = 0

        for row in range(3):
            currenti = row + i  
            for column in range(3):
                currentj =  column + j
                if currentPattern [row, column] > 0:   
                    if self._dataMatrix[currenti, currentj ] > 0  :
                        return True
        
        return False
     

     '''
        The pattern is planced on the matrix
        check whether the placement is in any of the top 3 rows.
     '''
     def __reachedTop(self):
         
         for row in range(3):
             for column in range(self.columns - 1):
                if self._dataMatrix[row,column] > 0:
                    return True

         return False


     '''
        diplay game over mesasge
     '''    
     def __displayGameOverText(self):
         i = int(self.columns / 2)  * self.scale
         j = int(self.rows / 2) * self.scale
         self.canvas.create_text(i,j,fill="white",font="arial 20 bold", text="Game Over ...")

#########################################################
############# Main code #################################
#########################################################
    

    
def main():
    ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        game=Tetris(root,36,12,25) 
        
        ####### Tkinter binding mouse actions
        root.bind("<Up>",lambda e:game.up())
        root.bind("<Left>",lambda e:game.left())
        root.bind("<Right>",lambda e:game.right())
        root.bind("<Down>",lambda e:game.down())
        root.bind("<p>",lambda e:game.pause())        

        while True:
            if not game.is_pause(): game.next()
            root.update()   # update the graphic
            time.sleep(0.25)  # wait few second (simulation)
            if game.is_game_over(): break
        
        root.mainloop() # wait until the window is closed


        

if __name__=="__main__":
    main()

