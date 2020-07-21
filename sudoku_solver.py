from collections import deque
from logger import Logger
from puzzle import Puzzle

class SudokuSolver:

    # Globally set logging
    logging = True

    def __init__(self, puzzle: Puzzle, solve_queue: deque):
        self.puzzle = puzzle
        self.solve_queue = solve_queue

    def solve(self):
        for row_index in range(0, len(self.puzzle.squares)):
            for col_index in range(0, len(self.puzzle.squares[row_index])):
                square = self.puzzle.squares[row_index][col_index]
                if square.value != 0:
                    square.set(square.value)
                self.display()

        while len(self.solve_queue) > 0 and self.puzzle.get_unsolved() > 0:
            solve = self.solve_queue.popleft()
            group = solve[0]
            index = solve[1]
            value = solve[2]
            set_value = solve[3]

            if set_value:
                group.on_value_set(index, value)
            else:
                group.on_invalidate(index, value)

            self.display()


    def display(self):
        if Logger.logging:
            print("Current State:")
            print(self.puzzle)


    @staticmethod
    def get_box(row, col):
        return int(row / 3) * 3 + int(col / 3)