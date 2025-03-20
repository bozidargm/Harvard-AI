import sys
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            dischard = set()
            for word in self.domains[var]:
                if var.length != len(word):
                    dischard.add(word)
            self.domains[var] -= dischard

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # First remove unary constraints to cut unnecessary calculations
        self.enforce_node_consistency()

        x_neighbors = self.crossword.neighbors(x)
        revision = False
        dischard = set()
        
        if y in x_neighbors:
            # Looking for inconsistent words in x domain with
            # words in y domain if x and y are neighbors
            for word_x in self.domains[x]:
                consistent = False
                for word_y in self.domains[y]:
                    letter_x, letter_y = self.crossword.overlaps[x, y]
                    # Words must be different and if in their intersection
                    # is the same letter then those words are consistent
                    if word_x != word_y and word_x[letter_x] == word_y[letter_y]:
                        consistent = True

                # Inconsistent word should be removed from x domain
                if consistent == False:
                    dischard.add(word_x)
    
        if dischard:        
            self.domains[x] -= dischard
            revision = True

        return revision

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Making list of arcs if "arcs" is None
        queue = []
        if arcs == None:
            # Finding  overlaping variable pairs 
            for arc, overlap in self.crossword.overlaps.items():
                if overlap != None:
                    queue.append(arc)

        else:
            arcs = queue

        # Checking arc consistency one by one
        while queue:
            var1, var2 = queue[0]
            queue.remove((var1, var2))
            # Function revise remove values from var1 domain
            # not consistent with values from var2 domain
            if self.revise(var1, var2):
                # No sulution if variable domain is empty
                if len(self.domains[var1]) == 0:
                    return False
            # Adding arcs to neighbors
            for neighbor in self.crossword.neighbors(var1):
                if neighbor != var2:
                    queue.append((neighbor, var1))

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Checking if all crossword variables are in assignment
        for var in self.domains:
            if var not in assignment:
                return False
        # Checking if all variables have at least one word in their domain
        for var in assignment:
            if not assignment[var]:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        consistent = True
        distinct = []

        for var in assignment:
            word = assignment[var]
            # Checking if words fits by their lenght
            if var.length != len(word):
                consistent = False
            # Checking if words are distinct
            if word in distinct:
                consistent = False
            distinct.append(word)

            # Checking if there overlaping words and
            # if their overlaping letters are the same
            neighbor_vars = self.crossword.neighbors(var) 
            for neighbor in neighbor_vars:
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        v, n = overlap
                        if word[v] != assignment[neighbor][n]:
                            consistent = False
        return consistent

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Dictionary for assigning heuristic value to words in var domain
        heuristic = {}
        for word in self.domains[var]:
            heuristic[word] = 0

        neighbor_vars = self.crossword.neighbors(var)

        for word in self.domains[var]:
            for neighbor in neighbor_vars:
                for neighbor_word in self.domains[neighbor]:
                    # Checking if word from var domain and
                    # word from neighbors domain overlaps
                    overlap = self.crossword.overlaps[var, neighbor]
                    if overlap:
                        i, j = overlap
                        # Calculating heuristic value for word in
                        # var domain
                        if word[i] != neighbor_word[j]:
                            heuristic[word] += 1
        # Sorting and returning heuristic list for words in var domain
        return sorted([i for i in heuristic], key=lambda a: heuristic[a])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Creating list of sorted variables by lenght of their domain
        # that are not in assignment
        unassigned_list = [(i[0], len(i[1])) for i in self.domains.items()\
                           if i not in assignment.items()]

        unassigned_list = sorted(unassigned_list, key=lambda a: a[1])

        # Creating list of variables with minimum domain lenght 
        min_unassigned = [i for i in unassigned_list if i[1] == unassigned_list[0][1]]

        neighbors_number = {}
        # If no multiple variables with minimum domain lenght,
        # return the one with minimum domain lenght
        if len(min_unassigned) == 1:
            return min_unassigned[0][0]
        # Looking for variable with the most neighbors if 
        # multiple variables with minimum domain lenght
        else:
            for i in min_unassigned:
                neighbor = self.crossword.neighbors(i[0])
                neighbors_number[i[0]] = len(neighbor)
        most_neighbors = sorted(neighbors_number.items(), key=lambda a: a[1])

        return most_neighbors[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.
        `assignment` is a mapping from variables (keys) to words (values).
        If no assignment is possible, return None.
        """        
        if self.assignment_complete(assignment):
            return assignment

        check = assignment.copy()

        # Looping until finding possible solution
        while len(assignment) < len(self.domains):
            for var in self.domains:
                if var not in check:
                    # Checking if there is right word for given variable
                    for word in self.order_domain_values(var, check):
                        check[var] = word
                        # If the word is correct, add them to assignment
                        if self.consistent(check):
                            assignment = check

            # If complete assignment, return it
            if len(assignment) == len(self.domains) and self.consistent(assignment):
                return assignment
            else:   
                return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()  