from tkinter import *
from Grid import Grid
from Pixel import Pixel
import time
from direction import Direction


### complete class Snake

class Snake(Grid):

     def __init__(self,root,numberOfObstacles,numberofFruits):          
        
        self._shouldPause = False
        self._isGameOver = False 

        self.direction = Direction.Right

        super().__init__(root,50,30,20)

        #create snake
        self.snakePixels = self.__createSnake(4,[0,1])

        
        #draw random obstacles
        self.random_pixels(numberOfObstacles,1) 

        self.availableNumberOfFruits = numberofFruits
        #draw fruits at random positions
        self.random_pixels(self.availableNumberOfFruits,3) 

        
     def __getSnakeHead(self) -> Pixel :
        #get head pixel of the snake
            pixel = self.snakePixels[len(self.snakePixels)-1]
            return pixel

     '''
        return direction in which snake is moving
        Current direction of the head pixel is the diretion of the snake
        [0,0] not moving - not applicable 
        [1,0] => down [-1,0] => up
        [0,1] => right [0,-1] => left
     '''       
     def __getSnakeDirection(self) -> Direction:
          
          headPixel = self.__getSnakeHead()
          if headPixel.vector[0] == 1:
               return Direction.Down
          
          if headPixel.vector[0] == -1:
               return Direction.Up

          if headPixel.vector[1] == 1:
               return Direction.Right 
          
          if headPixel.vector[1] == -1:
               return Direction.Left


     '''
        If the color of pixel is red, then it's fruit
     '''
     def __isFruit(self,i,j):
         return self._dataMatrix[j,i] == 3   

     '''
        if the colof of pixel is white, then it's an obstacle
     '''
     def __isObstacle(self,i,j):
         return self._dataMatrix[j,i] == 1   

     '''
        set the direction in which snake should move
        to set the direction of the snake, update direction of head pixel
     '''
     def __setSnakeDirection(self,direction):
        
        headPixel = self.__getSnakeHead()
        self.__setSentinelValue(headPixel.i,headPixel.j,direction)
        self.direction = direction
        
     def __setSentinelValue(self,i,j,direction):
        #set sentinel value indicating turn according to the  direction
        self._dataMatrix[j, i] = direction.value * -1
    
     def __setPixelDirection(self,pixel,direction):
        
        pixel.vector = [0,0]
        if direction == Direction.Down:
            pixel.down()
        if direction == Direction.Up:
            pixel.up()
        if direction == Direction.Right:
            pixel.right()
        if direction == Direction.Left:
            pixel.left()

     def __isTurningPoint(self,i,j):
         if self._dataMatrix[j,i] < 0:
             return True
         else:
             return False

     def __getTurningPointDirection(self,i,j) -> Direction:
         direction = None
         if self._dataMatrix[j,i] == -1 :
             direction = Direction.Right
         elif self._dataMatrix[j,i] == -2 :
             direction = Direction.Up
         elif self._dataMatrix[j,i] == -3 :
             direction = Direction.Left
         elif self._dataMatrix[j,i] == -4 :
             direction = Direction.Down 
         return direction

     def __clearSentinelValue(self,i,j):
         self._dataMatrix[j, i] = 0

     def isGameOver(self):
         return self._isGameOver == True
     
     def shouldPauseGame(self):
          return self._shouldPause == True
     
     def pause(self):
          self._shouldPause = not self._shouldPause

     def right(self):
          
          if self.direction == Direction.Right or self.direction == Direction.Left: 
            return 
          self.__setSnakeDirection(Direction.Right)
          
          
     def left(self):
          
          if self.direction == Direction.Right or self.direction == Direction.Left: 
            return 
          self.__setSnakeDirection(Direction.Left)
          

     def up(self):
          
          if self.direction == Direction.Up or self.direction == Direction.Down: 
            return 
          self.__setSnakeDirection(Direction.Up)

     def down(self):
          
          if self.direction == Direction.Up or self.direction == Direction.Down: 
            return 
          self.__setSnakeDirection(Direction.Down)

     def next(self):

        for index, pixel in enumerate(reversed(self.snakePixels)):
            if self.__isTurningPoint(pixel.i,pixel.j) == True:
               direction = self.__getTurningPointDirection(pixel.i,pixel.j)            
               self.__setPixelDirection(pixel,direction)
               
               #if this is the last pixel, reached the turning point, rest the turning point
               if index == len(self.snakePixels) - 1:
                   self.__clearSentinelValue(pixel.i,pixel.j)

            pixel.next()

        #moved snake by one position
        
         
        headOfSnake = self.__getSnakeHead()

        #check if head of the snake hit an obstacle
        if (self.__isObstacle(headOfSnake.i,headOfSnake.j)):
             self.__gaemOver(2)

        #check if snake can eat fruit
        if(self.__isFruit(headOfSnake.i,headOfSnake.j)):
            self.__eatFruit(headOfSnake.i,headOfSnake.j) 
     
     def __eatFruit(self,i,j):
          
          #remove fruit
          self.delxy(i * self.scale,j * self.scale )

          #decrement fruit count 
          self.availableNumberOfFruits -= 1
          
          #depending on the direction  of the last pixel of the snake body, add new pixel
          #1st element of the array indicate up/down direction 1 => down -1 => up
          #2nd element of the array indicate left/right direction 1 => right -1 => left
          #if direction is up, add new pixel below
          #if direction is down, add new pixel above
          #if direction is right, add new pixel to the left
          #if direction is left, add new pixel to the right
          bodyPixel = self.snakePixels[0]
          newi = bodyPixel.i + bodyPixel.vector[1] * -1  
          newj = bodyPixel.j + bodyPixel.vector[0] * -1 
          
          self.snakePixels.insert(0,Pixel(self.canvas,newj,newi,self.rows,self.columns,self.scale,5,bodyPixel.vector))    

          #eat all fruits? game over - won
          if (self.availableNumberOfFruits == 0):
              self.__gaemOver(1)  

     '''
        game is over 1 = player won the game 2 player lost the game
     '''          
     def __gaemOver(self,gameOverReason):
         
         if gameOverReason == 2:
            self.__displayGameLostText()
         if gameOverReason == 1:
            self.__displayGameWonText()

         self._isGameOver = True
     

     def __displayGameWonText(self):
         i = (int(self.columns / 2) - 4 ) * self.scale
         j = int(self.rows / 2) * self.scale
         self.canvas.create_text(i,j,fill="green",font="arial 20 bold", text="WON -- Game Over")

     
     def __displayGameLostText(self):
         i = (int(self.columns / 2) - 4 ) * self.scale
         j = int(self.rows / 2) * self.scale
         self.canvas.create_text(i,j,fill="red",font="arial 20 bold", text="Lost -- Game Over")

     def __createSnake(self,length,direction) -> []:
        
        snake = []
        i = int(self.rows / 2)
        j = int(self.columns / 2)

        
        for _ in range(length):
             snake.append(Pixel(self.canvas,i,j,self.rows,self.columns,self.scale,5,direction))
             j += 1
        
        #draw head
        snake.append(Pixel(self.canvas,i,j,self.rows,self.columns,self.scale,4,direction))

        return snake

#########################################################
############# Main code #################################
#########################################################
    

  
def main(): 
        
        ##### create a window, canvas 
        root = Tk() # instantiate a tkinter window
        python = Snake(root,20,20) #20 obstacles, and 20 fruits
        #python = Snake(root,5,5,25,25,30) # 5 obstacles/fruits, 25 row, 25 column, 30 scale
        
        
        ####### Tkinter binding mouse actions
        root.bind("<Right>",lambda e:python.right())
        root.bind("<Left>",lambda e:python.left())
        root.bind("<Up>",lambda e:python.up())
        root.bind("<Down>",lambda e:python.down())
        root.bind("<p>",lambda e:python.pause())
       
        while True:
            if not python.shouldPauseGame(): python.next()
            root.update()
            #temp
            time.sleep(0.15)
            #time.sleep(0.30)  # wait few second (simulation)
            if python.isGameOver(): break
            
        
        root.mainloop() # wait until the window is closed
        

if __name__=="__main__":
    main()

