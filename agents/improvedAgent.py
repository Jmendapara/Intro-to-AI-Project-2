import numpy as np
from .MineVisualization import game
import random 
import copy

class ConstraintEquation():

    def __init__(self, neighbors, clue):
        self.neighbors = set(neighbors)
        self.clue = clue

    #mark a cell as a mine by removing it from set
    def markAsMine(self, cell):
        if cell in self.neighbors:
            self.neighbors.remove(cell)
            self.clue -= 1
        else:
            pass

    #mark a cell as a safe by removing it from set
    def markAsSafe(self, cell):
        if cell in self.neighbors:
            self.neighbors.remove(cell)
        else:
            pass

    #returns known mines in the neighbors set
    def getIdentifiedMines(self):
        if self.clue == len(self.neighbors):
            return self.neighbors

    #returns known safe neighbors in the neighbors set
    def getIdentifiedSafes(self):
        if self.clue == 0:
            return self.neighbors


class ImprovedAgent():

    def __init__(self, env):

        self.env = env
        self.gridSize = env.gridSize

        self.movesTaken = set()

        self.mines = set()
        self.safes = set()
        
        self.movesVisualization = []
        self.movesAvaliable = []
        self.populateMovesAvaliable()

        # List of constraint equations
        self.knowledgeBase = []
        self.minesHit = 0

    def populateMovesAvaliable(self):
        for x in range(self.env.gridSize):
                for y in range(self.env.gridSize):
                    self.movesAvaliable.append((x,y))

    def execute(self):

        gameRunning = True

        while(gameRunning):

            move = self.openSafeCell()
            if move is None:
                move = self.openRandomCell()
                if move is None:

                        flags = self.mines.copy()
                        gameRunning = False

                        print(self.env.clues)

                        print("Mines Hit: " + str(self.minesHit))
                        print("Moves Made: " + str(self.movesTaken))
                        print("Length of Moves Made: " + str(len(self.movesTaken)))
                        print("Mines Identified: " + str(len(self.mines)))

                        #game(len(self.env.clues), self.env.clues,  self.env.clues, self.movesVisualization)

                        print("No moves left")

                        return len(self.mines) - self.minesHit
                else:
                    print("No safe neighbors. Opening a random cell.")
            else:
                print("Opening a safe cell.")

            x = move[0]
            y = move[1]

            clue = self.env.open(move[0],move[1])

            self.movesTaken.add((x,y))

            if(clue == -1):
                self.minesHit += 1
                self.markAsMine((x,y))

            else:
                self.makeEquation(move, clue)


    def openSafeCell(self):
        for i in self.safes - self.movesTaken:
            return i
        return None

    def openRandomCell(self):
        
        for cell in self.mines:
            if(cell in self.movesAvaliable):
                self.movesAvaliable.remove(cell)

        for cell in self.movesTaken:
            if(cell in self.movesAvaliable):
                self.movesAvaliable.remove(cell)

        if(len(self.movesAvaliable) == 0):
            return None

        else:
            return self.movesAvaliable[random.randrange(len(self.movesAvaliable))]

    def markAsMine(self, cell):
        
        if(cell in self.movesAvaliable):
            self.movesAvaliable.remove(cell)

        self.mines.add(cell)
        for sentence in self.knowledgeBase:
            sentence.markAsMine(cell)

    def markAsSafe(self, cell):
        self.safes.add(cell)
        for sentence in self.knowledgeBase:
            sentence.markAsSafe(cell)

    #checks to see if position (i,j) is a valid position
    def inGrid(self, i,j):

        maxGridPosition = self.env.gridSize - 1
        if((i < 0) or (i > maxGridPosition) or (j < 0) or (j > maxGridPosition)):
            return False
        return True

    def makeEquation(self, cell, clue):

        self.markAsSafe(cell)
        self.movesVisualization.append(cell)
        if(cell in self.movesAvaliable):
            self.movesAvaliable.remove(cell)

        neighbors = set()
        clue = copy.deepcopy(clue)
        neighborCells = self.getNeighborCells(cell) 
        for neighbor in neighborCells:
            if neighbor in self.mines:
                clue -= 1
            if neighbor not in self.mines | self.safes:
                neighbors.add(neighbor)                           

        newEquation = ConstraintEquation(neighbors, clue)

        if len(newEquation.neighbors) > 0:                 
            self.knowledgeBase.append(newEquation)

        self.updateKnowledgeBase()
        self.makeInference()

    def getNeighborCells(self, cell):

        neighborCells = set()

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:

                if(i == 0 and j == 0):
                        continue

                xPosition = cell[0] + i
                yPosition = cell[1] + j

                if(self.inGrid(xPosition,yPosition)):
                    neighborCells.add((xPosition, yPosition))

        return neighborCells

    def updateKnowledgeBase(self):

        knowledgeBaseCopy = copy.deepcopy(self.knowledgeBase)

        for equation in knowledgeBaseCopy:

            if len(equation.neighbors) == 0:
                if(equation in self.knowledgeBase):
                    self.knowledgeBase.remove(equation)
                
            mines = equation.getIdentifiedMines()
            if mines:
                for mine in mines:
                    self.markAsMine(mine)
                    self.updateKnowledgeBase()

            safes = equation.getIdentifiedSafes()
            if safes:
                for safe in safes:
                    self.markAsSafe(safe)
                    self.updateKnowledgeBase()

    def makeInference(self):

        # iterate through pairs of sentences
        for tempEquation1 in self.knowledgeBase:
            for tempEquation2 in self.knowledgeBase:
                # check if sentence 1 is subset of sentence 2
                if tempEquation1.neighbors.issubset(tempEquation2.neighbors):
                    new_cells = tempEquation2.neighbors - tempEquation1.neighbors
                    new_count = tempEquation2.clue - tempEquation1.clue
                    newEquation = ConstraintEquation(new_cells, new_count)
                    mines = newEquation.getIdentifiedMines()
                    safes = newEquation.getIdentifiedSafes()
                    if mines:
                        for mine in mines:
                            self.markAsMine(mine)

                    if safes:
                        for safe in safes:
                            self.markAsSafe(safe)
