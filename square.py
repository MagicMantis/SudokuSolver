from logger import Logger

class Square:

    def __init__(self, value):
        self.row = None;
        self.row_index = None;
        self.col = None;
        self.col_index = None;
        self.box = None;
        self.box_index = None;
        self.solve_queue = None;

        self.value = value;
        if value == 0:
            self.valid = [x for x in range(1, 10)]
        else:
            self.valid = []

    def set(self, x):
        self.value = x
        self.valid = []

        self.solve_set.add((self.row, self.row_index, x, True))
        self.solve_set.add((self.col, self.col_index, x, True))
        self.solve_set.add((self.box, self.box_index, x, True))

    def invalidate(self, x):
        if x in self.valid:
            self.valid.remove(x)
            if Logger.logging:
                print(self.row, self.col, "removed: ", x, self.valid)
            if len(self.valid) == 1:
                if Logger.logging:
                    print(self.row, self.col, "Invalidate led to setting to ", self.valid)
                self.set(self.valid[0])

        self.solve_set.add((self.row, self.row_index, x, False))
        self.solve_set.add((self.col, self.col_index, x, False))
        self.solve_set.add((self.box, self.box_index, x, False))

    # Return valid values
    def options(self):
        return self.valid

    def __str__(self):
        return self.value

    def dump(self):
        print("Value", self.value)
        print("Row Index", self.row_index)
        print("Row", self.row)
        print("Col Index", self.col_index)
        print("Col", self.col)
        print("Box Index", self.box_index)
        print("Box", self.box)

