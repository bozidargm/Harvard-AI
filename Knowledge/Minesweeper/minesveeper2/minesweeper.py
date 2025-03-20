import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


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
        if len(self.cells) == self.count and self.count != 0:
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

        # List of sets of cells in sentences
        self.knowledge_base = []

        # Neighboring cells of cell with count 1
        self.count1 = set()
                        
    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        temp_cells = set()
        for i in self.knowledge:
            if cell in i.cells:
                temp_cells = i.cells - {cell}
                i.cells = temp_cells
                i.count -= 1

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        temp_cells = set()
        for i in self.knowledge:
            if cell in i.cells:
                temp_cells = i.cells - {cell}
                i.cells = temp_cells
                
    def complete_board(self):
        """
        Returns set of all cells of the board
        """
        complete = set()
        for i in range(self.height):
            for j in range(self.width):
                complete.add((i, j))
        return complete

    def neighbors(self, cell):
        """
        Returns neighboring cells of checked cell
        """
        neighbor_cells = set()

        for i in range(cell[0]-1, cell[0]+2):
            for j in range(cell[1]-1, cell[1]+2):
                neighbour_cell = (i, j)
                if -1 < i < self.height and -1 < j < self.width and neighbour_cell != cell:
                    neighbor_cells.add(neighbour_cell)
        return neighbor_cells

    def undetermined(self, cell):
        """
        Returns neighboring cells which status is unknown
        """
        undetermined_cells = set()
        for i in self.neighbors(cell): 
            if i not in self.safes and i not in self.moves_made and i not in self.mines:
                undetermined_cells.add(i)
        return undetermined_cells
    
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
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        # Mark the cell as safe
        self.mark_safe(cell)

        # If count is 0 then all neighbors are safe too,
        # if count is 8 then all neighbors are mines
        if count == 0:
            for i in self.neighbors(cell):
                self.mark_safe(i)
        elif count == 1:
            self.count1.add(cell)
        elif count == 8:
            for i in self.neighbors(cell):
                self.mark_mine(i)

        # If the cell is a mine and its neighbor's count is 1, 
        # then all neighbors of that cell (except mine) are safe
        for mine in self.mines:
            for j in self.neighbors(mine):
                if j in self.count1:
                    for k in self.neighbors(j):
                        if k != mine:
                            self.mark_safe(k)

        # Updating all sentences in knowledge with information
        # that cell is safe
        if self.knowledge:
            temp_cells = set()
            for i in self.knowledge:
                if cell in i.cells:
                    temp_cells = i.cells - {cell}
                    i.cells = temp_cells
                    self.mark_safe(cell)

        # Creating new sentence  based on the value of `cell` and `count 
        undetermined_neighbors = self.undetermined(cell)
        all_neighbors = self.neighbors(cell)
        knowing_neighbor_mines = 0
        for i in all_neighbors:
            if i in self.mines:
                knowing_neighbor_mines += 1
                undetermined_neighbors = undetermined_neighbors - {i}
                self.mark_mine(i)
            elif i in self.safes:
                self.mark_safe(i)

        # Count of mines among undetermined neighbors
        unknowing_neighbor_mines = count - knowing_neighbor_mines

        # Checking if undetermined neighbors are already in knowledge
        # and appending new sentence to knowledge            
        if undetermined_neighbors and undetermined_neighbors not in self.knowledge_base:
            self.knowledge_base.append(undetermined_neighbors)
            self.knowledge.append(Sentence(undetermined_neighbors, unknowing_neighbor_mines))           
        
        # Looping through knowledge base adding inffered knowledge
        check = True
        while check:
            check = False
            # Removing empty sentence
            for i in self.knowledge.copy():
                if not i.cells:
                    self.knowledge.remove(i)

            # Looking through knowledge
            for i in self.knowledge:
                # If number of cells in the sentence is equal to count
                # than all cells are mines
                if len(i.cells) == i.count and len(i.cells) > 0:
                    for j in i.cells:
                        self.mark_mine(j)
                        check = True

                # If count is 0 then all cells are safe
                if i.cells and i.count == 0:
                    for j in i.cells:
                        self.mark_safe(j)
                        check = True 

                # If count is 8 then all cells are mines
                if i.count == 8:
                    for j in i.cells:
                        self.mark_mine(j)
                        check = True

                # If sentence's cell is neighbor of mine and the count
                # is 1 then all neighbors are safe
                for j in i.cells:
                    if j in self.count1:
                        mine = set()
                        for neighbor in self.neighbors(j):
                            if neighbor in self.mines:
                                mine.add(neighbor)
                                for safe in self.neighbors(j):
                                    if safe not in mine:
                                        self.mark_safe(safe)
                                        check = True

                # Adding new sentences to the AI's knowledge base
                # if they can be inferred from existing knowledge
                for j in self.knowledge:
                    if j.cells.issubset(i.cells):
                        new_cells = i.cells - j.cells
                        new_count = i.count - j.count
                            
                    if new_cells and new_cells not in self.knowledge_base:
                        self.knowledge_base.append(new_cells)
                        self.knowledge.append(Sentence(new_cells, new_count))
                                
    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made - self.mines
        if safe_moves:
            return random.choice(list(safe_moves))
        else:
            return None

    def number_of_neighbors(self,possible_moves):
        """
        Returns move that have minimum knowing neighbors
        """
        possible_moves = list(self.complete_board() - self.moves_made - self.mines)
        num_of_neighbors = {0:[],1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[]}
        for move in possible_moves:
            number = 0
            for neighbor in self.neighbors(move):
                if neighbor in possible_moves:
                    number += 1
            num_of_neighbors[number].append(move)
        sorted_moves = []
        for key, value in num_of_neighbors.items():
            sorted_moves.extend(value)
        return sorted_moves[0]


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = list(self.complete_board() - self.moves_made - self.mines)
        if possible_moves:
            move = self.number_of_neighbors(possible_moves)
            if move not in self.mines:
                return move
        else:
            return None
