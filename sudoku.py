import numpy as np
import copy
import random


class SudokuState:
    def __init__(self, puzzle):
        """
        Loads a given sudoku puzzle into the model
        Initialises the possible values and final values variables
        """
        # Set the half-completed sudoku board to the final_values var
        self.final_values = puzzle

        # Record the dimensions
        self.n = puzzle.shape[0]

        # Makes a list from [1..9]
        temp = []
        for i in range(1, self.n + 1):
            temp.append(i)

        # Create a (n x n) matrix
        self.possible_values = np.zeros((self.n, self.n), dtype=object)
        for i in range(self.n):
            for j in range(self.n):
                # Set each value to the list temp
                self.possible_values[i][j] = temp

        # Loop through existing/given values
        for i in range(self.n):
            for j in range(self.n):
                # Update the possible_values to properly import the given sudoku board
                value = self.final_values[i][j]
                if value != 0:
                    self.update(i, j, value)
                    self.possible_values[i][j] = [value]

    def is_invalid(self):
        """
        Returns True if the board ever reaches a point where there are no possible values for a given cell
        If this returns True, the path the algorithm is trying is invalid
            and the algorithm must backtrack to try new values
        False if the board is valid
        """
        # If there are any cells with no possible values, the board is invalid
        for x in range(self.n):
            for y in range(self.n):
                if len(self.possible_values[x][y]) == 0:
                    return True
        return False

    def is_goal(self):
        """
        Returns True/False depending on if the given state is a goal state
        Uses sudoku check function to determine if the board is a legal board
        """
        # Gets the positions there is not a final value yet
        temp = np.where(self.final_values == 0)

        # Checks to see if there are any positions with a 0 still in them
        # And checks the sudoku
        if temp[0].size == 0 \
                and temp[1].size == 0 \
                and self.check_sudoku():
            return True
        else:
            return False

    def check_sudoku(self):
        """
        Returns True if the completed board is a legal sudoku board
        False otherwise

        If all columns and all rows are valid, then the board is valid
        """
        #print(self.final_values)
        if self.check_sudoku_row() and self.check_sudoku_col():
            return True
        else:
            return False

    def check_sudoku_row(self):
        """
        Checks each row in the board to see if there is a repeated value in the row
        Returns False if there is a repeated value
            i.e. it is an invalid board
        """
        for i in range(self.n):
            nums = []
            for j in range(self.n):
                #print(nums)
                if self.final_values[i][j] != 0:
                    if self.final_values[i][j] in nums:
                        #print("Row: False @ ", self.final_values[i][j])
                        return False
                    else:
                        nums.append(self.final_values[i][j])
        #print("Row: True")
        return True

    def check_sudoku_col(self):
        """
        Checks each column in the board to see if there is a repeated value in the column
        Returns False if there is a repeated value
            i.e. it is an invalid board
        """
        for j in range(self.n):
            nums = []
            for i in range(self.n):
                if self.final_values[i][j] != 0:
                    if self.final_values[i][j] in nums:
                        #print("Col: False")
                        return False
                    else:
                        nums.append(self.final_values[i][j])
        #print("Col: True")
        return True

    def only_choice_row(self):
        """
        Returns a tuple (row, col, value) containing the positions of the only choice for the row
            iterates through all rows in the puzzle

        i.e. given (1,4,5,7), (1,2,7), (4,5) the algorithm will return [(0, 1, 2)]
            This is the only choice for this 3x1 row (applies to a 9x1 row as well)
            We know 2 must be in the row somewhere (as sudoku roles specify) and the only place it could be
                is in the 2nd column so this algorithm returns that
        """
        values = []

        # Loop over rows
        for i in range(self.n):
            # Reset for each row
            row_choices = []
            # Using a set over a list will ensure there are no repeated values
            seen = set()
            # Loop over column
            for j in range(self.n):
                # Check it's not set
                if self.final_values[i][j] == 0:
                    # Get the possible values for the current cell
                    possibles = self.possible_values[i][j]
                    # Loop over the possible values for the cell
                    for k in range(len(possibles)):
                        # If the value hasn't already been added for the row
                        # AND it's not been seen
                        if possibles[k] not in row_choices and possibles[k] not in seen:
                            row_choices.append(possibles[k])
                        # If this is the second time we're encountering this value,
                        # it shouldn't be returned & it should be 'blacklisted'
                        elif possibles[k] not in seen:
                            row_choices.remove(possibles[k])
                            seen.add(possibles[k])

            # Loop over the list of choices for this row
            for n in range(len(row_choices)):
                # Loop over the column
                for j in range(9):
                    # Find the coordinates of the values we've decided to return
                    cell = self.possible_values[i][j]
                    if row_choices[n] in cell:
                        values.append((i, j, row_choices[n]))
        return values

    def only_choice_col(self):
        """
        Returns a tuple (row, col, value) containing the positions of the only choice for the column
            iterates through all columns in the puzzle
        """
        values = []

        # Loop over columns
        for j in range(self.n):
            # Reset for each column
            col_possibles = []
            duplicates = set()
            # Loop over each row
            for i in range(self.n):
                if self.final_values[i][j] == 0:
                    possibles = self.possible_values[i][j]
                    # Loop through cell's possible values
                    for k in range(len(possibles)):
                        if possibles[k] not in col_possibles and possibles[k] not in duplicates:
                            col_possibles.append(possibles[k])
                        elif possibles[k] not in duplicates:
                            col_possibles.remove(possibles[k])
                            duplicates.add(possibles[k])

            # Find the coordinates of values we've decided to return
            for n in range(len(col_possibles)):
                for i in range(9):
                    cell = self.possible_values[i][j]
                    if col_possibles[n] in cell:
                        values.append((i, j, col_possibles[n]))
        return values

    def only_choice_box(self):
        """
        Returns a tuple (row, col, value) containing the positions of the only choice for the box
            iterates through all boxes in the puzzle
        """
        values = []

        # Loop over every box (row)
        for i in range(0, self.n, 3):
            duplicates = set()
            # Loop over every box (col)
            for j in range(0, self.n, 3):
                box_possibles = []
                # Loop through the cells in the box
                for r in range(3):
                    for c in range(3):
                        if self.final_values[i + r][j + c] == 0:
                            possibles = self.possible_values[i + r][j + c]
                            # Loop through the possible values for each cell
                            for k in range(len(possibles)):
                                if possibles[k] not in box_possibles and possibles[k] not in duplicates:
                                    box_possibles.append(possibles[k])
                                elif possibles[k] not in duplicates:
                                    box_possibles.remove(possibles[k])
                                    duplicates.add(possibles[k])

                # Find the coordinates of the values we've decided to return
                for n in range(len(box_possibles)):
                    for r in range(3):
                        for c in range(3):
                            cell = self.possible_values[i + r][j + c]
                            if box_possibles[n] in cell:
                                values.append((i + r, j + c, box_possibles[n]))
        return values

    def get_singleton(self):
        """
        Returns the the positions in a list [(x1,y1), (x2,y2),...] of all cells
            that have one possible value
        They have one possible value as a result of propagating the restraints
        Using this greatly optimises the algorithm
        """
        singles = []

        # Returns any cells with exactly one possibility that hasn't been set yet
        for row in range(0, self.n):
            for col in range(0, self.n):
                cell = self.possible_values[row][col]
                if len(cell) == 1 and self.final_values[row][col] == 0:
                    singles.append((row, col))
        return singles

    def update(self, row, col, value):
        """
        Takes cell position and the value it's being set to
        Then iterates through all rows/columns/boxes to remove the value from the possibilities

        i.e. placing a 1 in the top left corner (0,0) would:
            - remove 1 as a possible value from top row
            - remove 1 as a possible value from far left column
            - remove 1 as a possible value from the top left box
        """

        # Remove value from columns to the left
        for update_col in range(0, col):
            temp = self.possible_values[row][update_col].copy()
            if value in temp:
                temp.remove(value)
                self.possible_values[row][update_col] = temp
        # Remove value from columns to the right
        for update_col in range(col + 1, self.n):
            temp = self.possible_values[row][update_col].copy()
            if value in temp:
                temp.remove(value)
                self.possible_values[row][update_col] = temp

        # Remove value from rows above
        for update_row in range(0, row):
            temp = self.possible_values[update_row][col].copy()
            if value in temp:
                temp.remove(value)
                self.possible_values[update_row][col] = temp
        # Remove value from rows below
        for update_row in range(row + 1, self.n):
            temp = self.possible_values[update_row][col].copy()
            if value in temp:
                temp.remove(value)
                self.possible_values[update_row][col] = temp

        # Remove value from box
        r = row - row % 3
        c = col - col % 3
        for i in range(r, r + 3):
            for j in range(c, c + 3):
                temp = self.possible_values[i][j].copy()
                #print("(", i, ",", j, "): ", temp)
                if value in temp:
                    temp.remove(value)
                    #print(temp)
                    self.possible_values[i][j] = temp

    def set_value(self, row, col, value):
        """
        Takes a cell and sets it to the given value
        Then propagates the restraints
        Then looks for single cells
            Recursively calls itself to set the values of the singletons
        Then looks for 'only choice' cells
            Recursively calls itself to set the values of the only choices

        Returns the current state of the puzzle after setting the value to the cell
        """
        if value not in self.possible_values[row][col]:
            raise ValueError(f"{value} is not a valid choice for ({row},{col})")

        global stateCount
        stateCount += 1

        # Creates a copy of the state to change
        state = copy.deepcopy(self)

        # Propagates the constraints throughout the board
        state.update(row, col, value)

        # Sets the values in the possible & final values
        state.possible_values[row][col] = [value]
        state.final_values[row][col] = value

        # Gets and sets the single values
        singles = state.get_singleton()
        while len(singles) > 0:
            (r, c) = singles[0]
            state = state.set_value(r, c, state.possible_values[r][c][0])
            singles = state.get_singleton()

        row_choices = state.only_choice_row()
        while len(row_choices) > 0:
            (r, c, value) = row_choices[0]
            state = state.set_value(r, c, value)
            row_choices = state.only_choice_row()

        col_choices = state.only_choice_col()
        while len(col_choices) > 0:
            (r, c, value) = col_choices[0]
            state = state.set_value(r, c, value)
            col_choices = state.only_choice_col()

        box_choices = state.only_choice_box()
        while len(box_choices) > 0:
            (r, c, value) = box_choices[0]
            state = state.set_value(r, c, value)
            box_choices = state.only_choice_box()

        return state

def pick_next_cell(state):
    """
    Chooses the next cell for the depth search algorithm to 'fill in'
    If the cell has more than one possible value
        and the cell has less possible values than the current minimum
    then keep track of it's position
    Iterate through the whole board

    Returns the position of the cell with the least number of possibilities
    """
    to_return = (0, 0)
    minimum = state.n

    for i in range(state.n):
        for j in range(state.n):
            cell = state.possible_values[i][j]
            possibilities = len(cell)
            if 1 < possibilities < minimum:
                to_return = (i, j)
                minimum = possibilities
    return to_return

def order_values(state, row, col):
    """
    Orders the values for a given cell in the order to 'try' them in the depth first search
    Currently orders the values in a random order
        Potential for optimisation at this stage

    Returns a list of values
    """

    values = state.possible_values[row][col]
    random.shuffle(values)
    return values

def depth_first_search(puzzle, state):
    """
    The depth first search that calls the setting value function
    If the state is ever invalid, the algorithm will backtrack and try new values for cells
    Will return None if there is no solution
    """
    global depthStarts
    depthStarts += 1
    cell = pick_next_cell(state)
    row = cell[0]
    col = cell[1]
    values = order_values(state, row, col)

    # Loops through the values
    # Returns None if it ever reaches end of loop
    for value in values:
        # Sets the cell to the value & takes the new state
        new_state = state.set_value(row, col, value)
        # Checks if the new state is the goal
        if new_state.is_goal():
            return new_state
        # Checks it's not invalid
        if not new_state.is_invalid():
            # Recursively calls itself to set the next value
            deep_state = depth_first_search(puzzle, new_state)
            # If it returned None or it isn't the goal state, go to next loop iteration
            if deep_state is not None and deep_state.is_goal():
                return deep_state
    return None

def sudoku_solver(puzzle):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
        It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    
    ### YOUR CODE HERE
    global depthStarts
    depthStarts = 0
    global stateCount
    stateCount = 0

    solution = np.zeros((9, 9), dtype=int) - 1
    state = SudokuState(puzzle)

    if state.check_sudoku():
        completed_state = depth_first_search(puzzle, state)
        if completed_state is not None and completed_state.is_goal():
            solution = completed_state.final_values

    #print("Depth:", depthStarts)
    #print("States:", stateCount)
    return solution


depthStarts = 0
stateCount = 0


"""
# Load sudoku's
number = 0

sudoku = np.load("data/easy_puzzle.npy")
print("medium_puzzle has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[number], "\n")

answer = sudoku_solver(sudoku[number])
print(answer)

"""

SKIP_TESTS = False

if not SKIP_TESTS:
    import time

    difficulties = ['very_easy', 'easy', 'medium', 'hard']
    #difficulties = ['hard']
    total_time = 0
    total_right = 0

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for puzzle_num in range(len(sudokus)):
            #for j in range(0,1):
            #x = 14
            sudoku = sudokus[puzzle_num].copy()
            print(f"This is {difficulty} sudoku number", puzzle_num)
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", puzzle_num)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[puzzle_num]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[puzzle_num])

            print("This sudoku took", end_time - start_time, "seconds to solve.")
            print("\n")
            #total_time += end_time - start_time
        total_right += count

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        #print("Total time:", total_time)
        if count < len(sudokus):
            break
    print(total_right, "/", 4 * 15)
