import numpy as np
from .MineVisualization import game
import random 

class SimpleAgent():

    def __init__(self, env):

        #CLUES
        # -1 = flagged as mine
        # -2 = hit mine
        # 0-8 = opened and clue value

        self.env = env

        self.clues = np.zeros((env.gridSize, env.gridSize)) 

        self.safeIdentified = np.zeros((env.gridSize, env.gridSize)) 
        self.minesIdentified = np.zeros((env.gridSize, env.gridSize)) 
        self.hidden = np.zeros((env.gridSize, env.gridSize)) 

        self.opened = np.zeros((env.gridSize, env.gridSize), dtype = bool)
        self.minesHit = 0

        self.movesAvaliable = []
        self.movesTaken = []

        
        self.populateMovesAvaliable()

    def populateMovesAvaliable(self):
        for x in range(self.env.gridSize):
                for y in range(self.env.gridSize):
                    self.movesAvaliable.append((x,y))

    def execute(self):

        while(len(self.movesAvaliable) != 0):

            position = random.choice(self.movesAvaliable)

            x = position[0]
            y = position[1]

            self.openPosition(x,y)

        print(self.env.clues)
        print(self.clues)

        correctlyFlagged = 0
        totalFlagged = 0
        realMineHits = 0

        for x in range(self.env.gridSize):
            for y in range(self.env.gridSize):
                if(self.clues[x][y] == -1 and self.env.clues[x][y] == -1):
                    correctlyFlagged += 1
                if(self.clues[x][y] == -1):
                    totalFlagged += 1
                if(self.clues[x][y] == -2):
                    realMineHits += 1
                
                
        print('Correctly Flagged = ', str(correctlyFlagged))
        print('Total Flagged = ', str(totalFlagged))
        print('Mine Hits = ', str(self.minesHit))

        print(self.movesTaken)

        return totalFlagged

        #game(len(self.env.clues), self.env.clues, self.clues, self.movesTaken)

    def openPosition(self, x, y):

        self.movesTaken.append((x,y))
        self.opened[x,y] = True
        self.movesAvaliable.remove((x,y))

        response = self.env.open(x,y)

        #if(self.clues[x][y] == -1 or self.clues[x][y] == -2):
            #print('hmmm')

        if(response == -1):
            self.minesHit += 1
            self.clues[x][y] = -2

        else:
            self.clues[x][y] = response

        self.updateInfo()


    def updateInfo(self):
            
        for x in range(self.env.gridSize):
            for y in range(self.env.gridSize):
                

                if (self.clues[x][y] == -1 or self.opened[x][y] == False):
                   continue

                self.updateIdentified()

                if (self.opened[x][y] == True and self.clues[x][y] >= 0 and (((8 - self.clues[x][y]) - self.safeIdentified[x][y]) == self.hidden[x][y]) ):
                    self.openNeighbors(x, y)

                elif (self.opened[x][y] == True and self.clues[x][y] >= 0 and ((self.clues[x][y] - self.minesIdentified[x][y]) == self.hidden[x][y]) ):
                    self.flagNeighbors(x, y)


    def openNeighbors(self, x, y):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:

                if(i == 0 and j == 0):
                        continue

                xPosition = x + i
                yPosition = y + j

                if(self.inGrid(xPosition,yPosition) and self.opened[xPosition,yPosition] == False and self.clues[xPosition][yPosition] != -1):
                    self.openPosition(xPosition,yPosition)

    def flagNeighbors(self, x, y):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:

                if(i == 0 and j == 0):
                        continue

                xPosition = x + i
                yPosition = y + j


                if(self.inGrid(xPosition,yPosition) and self.opened[xPosition][yPosition] == False):
                    
                    if((xPosition,yPosition) in self.movesAvaliable):
                        self.movesAvaliable.remove((xPosition,yPosition))

                    if(self.clues[xPosition][yPosition] != -1):
                        self.movesTaken.append((xPosition,yPosition))
                        self.clues[xPosition][yPosition] = -1


    #checks to see if position (i,j) is a valid position
    def inGrid(self, i,j):

        maxGridPosition = self.env.gridSize - 1
        if((i < 0) or (i > maxGridPosition) or (j < 0) or (j > maxGridPosition)):
            return False
        return True

    def updateIdentified(self):

        for x in range(self.env.gridSize):
            for y in range(self.env.gridSize):

                if(self.clues[x, y] == -1 or self.clues[x, y] == -2):
                    continue

                safeIdentified = 0
                minesIdentified = 0
                hidden = 0

                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:

                        if(i == 0 and j == 0):
                            continue

                        xPosition = x + i
                        yPosition = y + j

                        if(self.inGrid(xPosition,yPosition) and (self.clues[xPosition, yPosition] == -1 or self.clues[xPosition, yPosition] == -2)):
                            minesIdentified += 1

                        if(self.inGrid(xPosition,yPosition) and self.opened[xPosition,yPosition] and self.clues[xPosition, yPosition] >= 0):
                            safeIdentified += 1

                        if(self.inGrid(xPosition,yPosition) and (self.opened[xPosition,yPosition] == False)):
                            hidden += 1

                self.minesIdentified[x][y] = minesIdentified
                self.safeIdentified[x][y] = safeIdentified
                self.hidden[x][y] = hidden
                
