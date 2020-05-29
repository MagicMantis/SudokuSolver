from sudoku_loader import SudokuLoader
from collections import deque
from logger import Logger


class SudokuSolver:

    # Globally set logging
    logging = True

    def __init__(self):

        # Load the puzzle
        self.loader = SudokuLoader()
        if SudokuSolver.logging:
            print(self.loader.puzzle_count, "puzzles loaded")

        correct = 0

        for i in range(self.loader.puzzle_count):

            self.solve_queue = deque()
            self.puzzle = self.loader.load(i, self.solve_queue)
            if SudokuSolver.logging:
                self.display()

            # Solve the puzzleS
            self.solve()

            # Check the solution
            if self.loader.check_solution(self.puzzle):
                print("Correct!", i)
                correct += 1
            else:
                print("Bad Solution!", i)

        print("Correctly Completed:", correct, "out of", self.loader.puzzle_count)

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


SudokuSolver()
