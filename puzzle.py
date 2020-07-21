from square import Square
import numpy as np
from collections import deque
from logger import Logger

class Puzzle:

    def __init__(self, puzzle_string, solve_set = None):
        self.squares = [[Square(int(puzzle_string[i*9+x])) for x in range(0, 9)] for i in range(0, 9)]
        s = np.array(self.squares)

        self.rows = [Row(x) for x in s]
        self.cols = [Column(s[:, i]) for i in range(0, 9)]
        box_arrays = [[] for _ in range(0,9)]
        for row in range(0,9):
            for col in range(0,9):
                box_arrays[Puzzle.get_box(row, col)].append(self.squares[row][col])
        self.boxes = [Box(array) for array in box_arrays]

        self.solve_set = solve_set
        for row in self.squares:
            for square in row:
                square.solve_set = self.solve_set


    def get_unsolved(self):
        unsolved = 0
        for row in self.squares:
            for square in row:
                if square.value == 0:
                    unsolved += 1
        return unsolved

    @staticmethod
    def get_box(row, col):
        return int(row / 3) * 3 + int(col / 3)

    def __str__(self):
        s = ""
        for row_index in range(0, 9):
            for col_index in range(0, 9):
                value = self.squares[row_index][col_index].value
                s += str(value if value > 0 else ' ')
                if (col_index+1) % 3 == 0:
                    s += " | "
                else:
                    s += " "
            s += "\n"
            if (row_index + 1) % 3 == 0:
                s += "- "*12 + "\n"
        return s

    def __eq__(self, other):
        for row in range(9):
            for col in range(9):
                if self.squares[row][col].value != other.squares[row][col].value:
                    return False
        return True


class Group:

    def __init__(self, squares):
        # references to the squares in the group
        self.squares = squares

        # numbers left to complete this group
        self.nums = {}
        for i in range(1, 10):
            self.nums[i] = [x for x in range(9)]

        # Trim keys where number already exist in the group
        for square in squares:
            if square.value != 0 and square.value in self.nums:
                del self.nums[square.value]

        # Trim available locations
        for i in range(9):
            square = squares[i]
            if square.value != 0:
                for value in self.nums.values():
                    value.remove(i)

    # called whenever a square in this group has its value set
    def on_value_set(self, index, value):
        if Logger.logging:
            print("On value set called for this", type(self), self.nums)

        # delete this value (number 0-9) from list of numbers still needed by this group
        if value in self.nums:
            del self.nums[value]

        # delete the index of this number as an option for all the remaining numbers
        for options in self.nums.values():
            if index in options:
                options.remove(index)

        # for each other square in the box, invalidate this number as an option
        for i in range(9):
            if self.squares[i].value == 0:
                self.squares[i].invalidate(value)

        # check if any numbers required by this group only have 1 option for location
        for key, options in self.nums.items():
            if len(options) == 1:
                i = options[0]
                self.squares[i].set(key)

    def on_invalidate(self, index, value):
        if Logger.logging:
            print("On invalidate called for this", type(self), self.nums)
        if value in self.nums:
            v = self.nums[value]
            if index in v:
                v.remove(index)
                if len(v) == 1:
                    i = v[0]
                    self.squares[i].set(value)


class Row(Group):

    def __init__(self, squares):
        super().__init__(squares)
        for i in range(len(squares)):
            squares[i].row = self
            squares[i].row_index = i


class Column(Group):

    def __init__(self, squares):
        super().__init__(squares)
        for i in range(len(squares)):
            squares[i].col = self
            squares[i].col_index = i

class Box(Group):

    def __init__(self, squares):
        super().__init__(squares)
        for i in range(len(squares)):
            squares[i].box = self
            squares[i].box_index = i

    def __str__(self):
        s = "Box:\n"
        for index in range(0,9):
            s += str(self.squares[index].value) + " "
            if index % 3 == 2:
                s += "\n"
        return s