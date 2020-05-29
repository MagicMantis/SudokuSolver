from puzzle import Puzzle
import csv

class SudokuLoader:

    def __init__(self):
        self.puzzle = []
        self.__solution = []
        self.__puzzle_strings = []
        self.__solution_strings = []

        with open('puzzles/sudoku.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=",")
            next(reader)
            for row in reader:
                self.__puzzle_strings.append(row[0])
                self.__solution_strings.append(row[1])

        self.puzzle_count = len(self.__puzzle_strings)

    def load(self, puzzle_index, solve_queue):
        self.puzzle = Puzzle(self.__puzzle_strings[puzzle_index], solve_queue)
        self.__solution = Puzzle(self.__solution_strings[puzzle_index])

        return self.puzzle

    def check_solution(self, solution):
        return solution == self.__solution
