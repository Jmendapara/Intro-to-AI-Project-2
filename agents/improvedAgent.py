import numpy as np
from .MineVisualization import game
import random 
import copy

class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        else:
            pass

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        else:
            pass


class ImprovedAgent():

    def __init__(self, env):

        self.env = env

        # Set initial height and width
        self.height = env.gridSize
        self.width = env.gridSize

        self.movesAvaliable = []
        self.populateMovesAvaliable()

        self.moves_made = set()

       # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        
        self.movesVisualization = []


        # List of sentences about the game known to be true
        self.knowledge = []

        self.minesHit = 0


    def populateMovesAvaliable(self):
        for x in range(self.env.gridSize):
                for y in range(self.env.gridSize):
                    self.movesAvaliable.append((x,y))


    def execute(self):

        gameRunning = True

        while(gameRunning):

            move = self.make_safe_move()
            if move is None:
                move = self.make_random_move()
                if move is None:
                        flags = self.mines.copy()
                        gameRunning = False
                        print(self.env.clues)

                        print("Mines Hit: " + str(self.minesHit))
                        print("Moves Made: " + str(self.moves_made))
                        print("Length of Moves Made: " + str(len(self.moves_made)))

                        game(len(self.env.clues), self.env.clues,  self.env.clues, self.movesVisualization)

                        print("No moves left to make.")

                        return
                else:
                    print("No known safe moves, AI making random move.")
            else:
                print("AI making safe move.")

            x = move[0]
            y = move[1]

            clue = self.env.open(move[0],move[1])

            self.moves_made.add((x,y))


            if(clue == -1):
                self.minesHit += 1
                self.mark_mine((x,y))

            else:
                self.add_knowledge(move, clue)



        #game(len(self.env.clues), self.env.clues, self.clues, self.movesTaken)


    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # mark the cell as one of the moves made in the game
        #self.moves_made.add(cell)

        # mark the cell as a safe cell, updating any sequences that contain the cell as well
        self.mark_safe(cell)
        self.movesVisualization.append(cell)

        # add new sentence to AI knowledge base based on value of cell and count
        cells = set()
        count_cpy = copy.deepcopy(count)
        close_cells = self.return_close_cells(cell)     # returns neighbour cells
        for cl in close_cells:
            if cl in self.mines:
                count_cpy -= 1
            if cl not in self.mines | self.safes:
                cells.add(cl)                           # only add cells that are of unknown state

        new_sentence = Sentence(cells, count_cpy)           # prepare new sentence

        if len(new_sentence.cells) > 0:                 # add that sentence to knowledge only if it is not empty
            self.knowledge.append(new_sentence)
            # print(f"Adding new sentence: {new_sentence}")

        # # print("Printing knowledge:")
        # for sent in self.knowledge:
        #     # print(sent)

        # check sentences for new cells that could be marked as safe or as mine
        self.check_knowledge()
        # print(f"Safe cells: {self.safes - self.moves_made}")
        # print(f"Mine cells: {self.mines}")
        # print("------------")

        self.extra_inference()

    def return_close_cells(self, cell):
        """
        returns cell that are 1 cell away from cell passed in arg
        """
        # returns cells close to arg cell by 1 cell
        close_cells = set()
        for rows in range(self.height):
            for columns in range(self.width):
                if abs(cell[0] - rows) <= 1 and abs(cell[1] - columns) <= 1 and (rows, columns) != cell:
                    close_cells.add((rows, columns))
        return close_cells

    def check_knowledge(self):
        """
        check knowledge for new safes and mines, updates knowledge if possible
        """
        # copies the knowledge to operate on copy
        knowledge_copy = copy.deepcopy(self.knowledge)
        # iterates through sentences

        for sentence in knowledge_copy:
            if len(sentence.cells) == 0:
                try:
                    self.knowledge.remove(sentence)
                except ValueError:
                    pass
            # check for possible mines and safes
            mines = sentence.known_mines()
            safes = sentence.known_safes()

            # update knowledge if mine or safe was found
            if mines:
                for mine in mines:
                    # print(f"Marking {mine} as mine")
                    self.mark_mine(mine)
                    self.check_knowledge()
            if safes:
                for safe in safes:
                    # print(f"Marking {safe} as safe")
                    self.mark_safe(safe)
                    self.check_knowledge()

    def extra_inference(self):
        """
        update knowledge based on inference
        """
        # iterate through pairs of sentences
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                # check if sentence 1 is subset of sentence 2
                if sentence1.cells.issubset(sentence2.cells):
                    new_cells = sentence2.cells - sentence1.cells
                    new_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(new_cells, new_count)
                    mines = new_sentence.known_mines()
                    safes = new_sentence.known_safes()
                    if mines:
                        for mine in mines:
                            # print(f"Used inference to mark mine: {mine}")
                            # print(f"FinalSen: {new_sentence}")
                            # print(f"Sent1: {sent1copy}")
                            # print(f"Sent2: {sent2copy}")
                            self.mark_mine(mine)

                    if safes:
                        for safe in safes:
                            # print(f"Used inference to mark safe: {safe}")
                            # print(f"FinalSen: {new_sentence}")
                            # print(f"Sent1: {sent1copy}")
                            # print(f"Sent2: {sent2copy}")
                            self.mark_safe(safe)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.
        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for i in self.safes - self.moves_made:
            # choose first safe cell that wasn't picked before
            # print(f"Making {i} move")
            return i
        
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        maxmoves = self.width * self.height

        while maxmoves > 0:
            maxmoves -= 1

            row = random.randrange(self.height)
            column = random.randrange(self.width)

            if (row, column) not in self.moves_made | self.mines:
                return (row, column)

        return None