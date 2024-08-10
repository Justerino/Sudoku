import random
from cell import Cell

class SudokuBoard:
    def __init__(self):
        self.grid = [[Cell() for _ in range(9)] for _ in range(9)]

    def set_value(self, row, col, value):
        """Set the value of a cell."""
        self.grid[row][col].set_value(value)

    def get_value(self, row, col):
        """Get the value of a cell."""
        return self.grid[row][col].value

    def clear_cell(self, row, col):
        """Clear the value of a cell."""
        self.grid[row][col].clear()

    def is_valid(self, row, col, num):
        """Check if placing a number in a specific cell is valid."""
        if any(self.grid[row][i].value == num for i in range(9)):
            return False
        if any(self.grid[i][col].value == num for i in range(9)):
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j].value == num:
                    return False
        return True

    def fill_grid(self):
        """Recursively fill the grid with a valid Sudoku solution."""
        for row in range(9):
            for col in range(9):
                if self.grid[row][col].value is None:
                    numbers = list(range(1, 10))
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid(row, col, num):
                            self.grid[row][col].set_value(num)
                            if self.fill_grid():
                                return True
                            self.grid[row][col].clear()
                    return False
        return True

    def remove_digits(self, difficulty):
        """Remove digits from the filled grid to create the puzzle based on difficulty."""
        cells_to_remove = {'Easy': 20, 'Medium': 40, 'Hard': 60}.get(difficulty, 40)
        while cells_to_remove > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            if self.grid[row][col].value is not None:
                self.clear_cell(row, col)
                cells_to_remove -= 1

    def generate_puzzle(self, difficulty, seed=None):
        """Generate a puzzle with a given difficulty."""
        if seed is not None:
            random.seed(seed)
        self.fill_grid()
        self.remove_digits(difficulty)
