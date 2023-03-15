# Solving Sudoku puzzles using AI techniques 

Sudoku readme file 
 To explain the algorithm and how the program solves the puzzle.
 Program structure similar to eight queens revisited from the following moodle link: 
  https://moodle.bath.ac.uk/mod/resource/view.php?id=974662

The program uses constraint propagation with depth first search traversal to find the solution for a given sudoku board.

The constraint propagation part means that when you place a number into a cell, the rules (constraints) are propagated such that it would stop an invalid move. So you know that all moves before the current move have all been legal which means that the current move will also be legal. The program holds a list of possible values for each cell and whenever a cell is filled in, the list of possible values for other cells is reduced, to follow the rules. 
So placing a 1 in the top left cell would remove 1 from the list of possible values in the following cells:
 - All cells in the top row 
 - All cells in the far left column 
 - All cells in the top left 'box'/'sub-square' (3x3)

The depth first search part means that when there are multiple values for a cell, the program will try one of them and continue with the board. If it finds that it reaches an invalid state (there are no possible values for an empty cell) then it will 'backtrack' and try a different value for the cell. If it tries all legal states and finds no solution the board is said to be invalid. 


The program has a class with a variety of methods and attributes to help with solving the puzzle.

Attributes:
 - n: is an int which holds the dimensions of the given sudoku board.
 
 - final_values: is a numpy (n x n) array which holds the completed board.
   Any unknown values are stored with a 0.
 
 - possible_values: holds the possible values at each cell.
   It is initialised with a list [1..9] and values are removed as constraints are propagated.


Methods:
 - __init__(self, puzzle):
  This is the constructor method that takes the given puzzle and sets the model up so that the algorithm can work. 
  Calls the update method on all values in the original, incomplete sudoku board to update the possible values. 

 - is_invalid(self):
   A checker function that returns True if the board contains an empty cell that has no possible values.
   This method is used within the depth first search to check if the board is valid.

 - is_goal(self):
   Returns True if the board is in a completed state and is a valid board (uses check_sudoku function).
   Returns False otherwise.
   Again used within the depth first search.

 - check_sudoku(self): {row/col}
   Uses check_sudoku_row/col to iterate through each row/column respectivley. 
   It ensures there are no repeated values in the rows and columns. 
   If there are no repeated values, this method (check_sudoku) returns True to indicate that it is a legal board. 
   Otherwise returns False. 

 - only_choice_function(self) {row/col/box}:
   Consider the following box
   ---------------------
   |[4,9]   2   [1,4,7]|
   |                   |
   | 3    [4,7]    5   |
   |                   |
   | 8    [7,9]    6   |
   ---------------------
   where the single numbers have already been set in final_values. 
   We know that a 1 must be present in this box and we can see that the only place the 1 could go is in the top right.
   The only_choice_box method would return [(0, 2, 1)] to indicate that 1 can be put in position (0, 2).
   
   There is a seperate only_choice algorithm for rows, columns and boxes. 
   They all evaluate the entire board in their respective search. i.e. rows looks along the rows, etc.
   They return a list of tuples with the (row, column, value) of the only choices. 

 - get_singleton(self): 
   This function is used to return the coordinates of all the cells with exactly one possible value that haven't been set yet. 
   Returns a list of tuples [(x1,y1), (x2,y2),...]. 
   This method greatly improves the efficiency of the overall algorithm as it pairs well with the constraint propagation. 
   	It allows the answers to be filled in when there is only one option for a cell. 
 
 - update(self, row, col, value):
   This is the function that applies the constraints when a given value is inserted at [row, col].
   Removes the given value from the list of the possible values in the following cells
   	- All cells in the same row to the left of the given column
   	- All cells in the same row to the right of the given column
   	- All cells in the same column above the given row
   	- All cells in the same column below the given row
   	- All cells in box that (row, col) is in 
   This allows for the constraint propagation by 'crossing out' the possible values when a new value is inserted. 
   This method is called when loading the initial board so that the values can be updated and whenever a value is set in set_value.

 - set_value(self, row, col, value):
   This is the function which sets a given [row, col] to the given value.
   Additionally, it calls the update method to apply the constraints of the new value. 
   After that the get_singleton method is called to get the singleton coordinates and then recursively calls itself to apply them. 
   Then the only_choice methods are used to find the coordinates and values where it's the only choice. Again, recursively calls itself to apply these. 


Functions:
 - pick_next_cell(state):
   This function returns the coordinates of a cell with the minimum number of possible values that is greater than 1. 
   Originally, the function returned a random empty cell but changing it to use cell with minimum number of values greatly improved performance in the depth first search. 
   
 - order_values(state, row, col):
   This function chooses the order to evaluate each value from a given cell (depth first search uses the cell from pick_next_cell).
   Currently shuffles the order of the cells into a random order. 
   
 - depth_first_search(puzzle, state):
   This function recursively performs a depth first search on the given puzzle. Returns a state with the completed board if it finds a solution and returns None otherwise. 
   Uses pick_next_cell and order_values to choose which cell to start with and in which order to evaluate the values. 
   If at any point it encounters an invalid board it will return None to the previous function call which will then generate another state and so on. 
   Once all (legal) states have been exhausted and a solution has not been found, then the algorithm will return None as no solution. 
   Uses the set_value function to set the values in each state. 
   
 - sudoku_solver(puzzle):
   This is the function that should be called to solve and return the sudoku puzzle.
   It creates a new SudokuState object and calls the depth_first_search function and passes the puzzle and object. 
   Then returns the solution or the null solution. 
