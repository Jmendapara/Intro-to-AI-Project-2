import numpy as np
from random import randrange

class Enviornment():

    def __init__(self, gridSize, numberOfMines):
        self.gridSize = gridSize
        self.numberOfMines = numberOfMines

        self.mines = np.zeros((self.gridSize, self.gridSize), dtype = bool)
        self.clues = np.zeros((self.gridSize, self.gridSize))

        self.addMines()
        self.calculateClues()

    #added bombs to the mines array in the form of a True boolean
    def addMines(self):

        minesToAdd = self.numberOfMines

        while(minesToAdd != 0):
            
            randomX = randrange(self.gridSize)
            randomY = randrange(self.gridSize)

            if(self.mines[randomX,randomY] != True):
                self.mines[randomX,randomY] = True
                minesToAdd -= 1

    #checks to see if position (i,j) is a valid position
    def inGrid(self, i,j):

        maxGridPosition = self.gridSize - 1
        if((i < 0) or (i > maxGridPosition) or (j < 0) or (j > maxGridPosition)):
            return False
        return True

    #fills clues array with calue values and -1 if there is a bomb there
    def calculateClues(self):

        for x in range(self.gridSize):
            for y in range(self.gridSize):

                if(self.mines[x, y] == True):
                    self.clues[x,y] = -1
                    continue

                numberOfBombs = 0

                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:

                        if(i == 0 and j == 0):
                            continue

                        xPosition = x + i
                        yPosition = y + j

                        if(self.inGrid(xPosition,yPosition) and self.mines[xPosition, yPosition] == True):
                            numberOfBombs += 1

                self.clues[x,y] = numberOfBombs

    #returns -1 if there is a bomb there, or clue if there is no bomb
    def open(self, i, j):
        return self.clues[i,j]


                    
