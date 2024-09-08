from tkinter import *
from Pixel import Pixel
import numpy as np
import random, time


class Grid:
    

        def __init__(self,root,rows,columns,scale) -> None:
        
          self.scale = scale

          self.rows = rows
          self.columns = columns
          
          #initialize a [rows,columns] matrix with zeros 
          self._dataMatrix = np.zeros((rows,columns),dtype=np.int8)          
          self.pixels = {}

          self.canvas = Canvas(root,width=columns*self.scale,height=rows*self.scale,bg="black")
          self.canvas.pack()

          self.drawGrid(columns,rows,scale)

          
        def drawGrid(self,columns, rows, sizeOfCell):
              
              #draw verticle lines
              verticleLineLength =  rows*sizeOfCell

              for column in range(1,columns):
                columnPosition = column* sizeOfCell
                self.canvas.create_line(columnPosition,0,columnPosition,verticleLineLength, fill="gray")

              #draw horizontal lines
              horizontalLineLength = columns * sizeOfCell

              for row in range(1,rows):
                rowPosition = row * sizeOfCell
                self.canvas.create_line(0,rowPosition,horizontalLineLength, rowPosition, fill="gray")
   

        '''
          fill empty cell of the canvas. 
          Empty cell of the canvas is filled with an instance of the Pixel class
          the pixel instance is stored in the instance varaible pixels dictionary
                key of the dictionary is of the format row_column 
        '''
        def fillCell(self,column,row, color=1):
             
             isCellFilled = self.isFilled(row,column)
             if isCellFilled == True:
                  return
             
             pixel = self.createPixel(column,row,color)
             self._dataMatrix[row , column ] = color

        def createPixel(self, column, row, color=1):
            
             dictionaryKey = f'{row}_{column}'
            
             pixel = Pixel(self.canvas,row,column,self.rows,self.columns,self.scale,color)
             self.pixels[dictionaryKey] = pixel

             
        #left mouse click event handler
        def addxy(self,column,row, color = 1):
             
             columnNumber = column // self.scale
             rowNumber = row // self.scale

             isCellFilled = self.isFilled(rowNumber, columnNumber)

             cellColor = color
             if not (isCellFilled):
                  cellColor = 0
                  self.fillCell(columnNumber,rowNumber, color)

             print(f'insert {row} {column} {rowNumber} {columnNumber} {cellColor}')

         
            
        #right mouse click event handler
        def delxy(self,column,row):
             
             columnNumber = column // self.scale
             rowNumber = row // self.scale

             isCellFilled = self.isFilled(rowNumber, columnNumber)

             if isCellFilled == True:
                
                print(f'delete {row} {column} {rowNumber} {columnNumber}  1')

                self.clearCell(columnNumber,rowNumber)
                self.reset()
             else:
                print(f'delete {row} {column} {rowNumber} {columnNumber}  0')
                self.flushRow(rowNumber)

        #return true if the cell is filled i.e. cotains a pixel
        def isFilled(self,row,column) -> bool:
             
             #if the value is 0 or less => not filled
             #-ve condition to handle 'turn' functionality of 'snake'
             if(self._dataMatrix[row, column]) <= 0:
                  return False
             else:
                  return True


        '''
          Set the metrix cell to 0
        '''
        def clearCell(self,column,row):
             
             isCellFilled = self.isFilled(row,column)
             if isCellFilled == False:
                  return
             self._dataMatrix[row , column ] = 0

        def reset(self):
             
             #delete pixels
             for pixel in self.pixels.values():
                  pixel.delete()
              
             #clear the dictionary
             self.pixels.clear()

             #let's scan the matrix and repaint
             for (row, column), pixelColor in np.ndenumerate(self._dataMatrix):
               
               if pixelColor > 0:
                   self.createPixel(column, row, pixelColor)

        '''
          if the color of current cell is black - delete contents of the row, 
          shift contents of all rows above the delete down by 1
          
        '''
        def flushRow(self,row):
            
            for column in range(self.columns):
                self.clearCell(column,row)
           

            if row != 0:
               
               self.runFlusAnimation(row)

               self._dataMatrix[1:row + 1,:] = self._dataMatrix[0:row,:]

               #nullify top row
               for column in range(self.columns):
                   self._dataMatrix[0,column] = 0
            
            self.reset()
            
        def runFlusAnimation(self,row):
            
          #6 pixels for animation
          animantionPixels = []
          animantionPixels.append(Pixel(self.canvas,row,0,self.rows,self.columns,self.scale,7,[0,1])) 
          animantionPixels.append(Pixel(self.canvas,row,1,self.rows,self.columns,self.scale,7,[0,1])) 
          animantionPixels.append(Pixel(self.canvas,row,2,self.rows,self.columns,self.scale,7,[0,1])) 
          animantionPixels.append(Pixel(self.canvas,row,self.columns-1,self.rows,self.columns,self.scale,7,[0,-1]))
          animantionPixels.append(Pixel(self.canvas,row,self.columns-2,self.rows,self.columns,self.scale,7,[0,-1]))
          animantionPixels.append(Pixel(self.canvas,row,self.columns-3,self.rows,self.columns,self.scale,7,[0,-1]))

          main_window = self.canvas.winfo_toplevel()
          #repeate so that animation pixels reach the center of the grid
          for _ in range((self.columns - 6) // 2): 
               for pixel in range(6):
                    animantionPixels[pixel].next()
               main_window.update()
               time.sleep(0.02)

          #delete animation pixels
          for pixel in range(6):
               animantionPixels[pixel].delete()


        def random_pixels(self,numberOfPixels,color=1):
            
          
            for k in range(numberOfPixels):
               row=random.randint(0,self.rows-1) 
               column=random.randint(0,self.columns-1)

               #self.addxy(column*self.scale,row*self.scale,color)
               self.fillCell(column,row,color)

#########################################################
############# Main code #################################
#########################################################

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk()                # instantiate a tkinter window
        mesh = Grid(root,50,30,20) # instantiate a Grid object
        
        #temp
        mesh.random_pixels(25,1) # generate 25 random (white) pixels in the Grid

        
        ####### Tkinter binding mouse actions
        root.bind("<Button-1>",lambda e:mesh.addxy(e.x,e.y))
        root.bind("<Button-3>",lambda e:mesh.delxy(e.x,e.y))
        

        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

