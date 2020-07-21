from sudoku_loader import SudokuLoader
from sudoku_solver import SudokuSolver
from datetime import datetime
from puzzle import Puzzle
from multiprocessing import Pool


# correct = 0

def solve_puzzle(puzzle_strings):

    puzzle_id = puzzle_strings[0]

    solve_set = set()
    puzzle = Puzzle(puzzle_strings[1][0], solve_set)
    solution = Puzzle(puzzle_strings[1][1])

    solver = SudokuSolver(puzzle, solve_set)
    solver.solve()

    if solver.puzzle == solution:
        print("Puzzle",puzzle_id, "Complete!")
        return 1
    else:
        print("Bad Solution for",puzzle_id)
        return 0

if __name__ == "__main__":

    # Load the puzzles
    loader = SudokuLoader()
    print(loader.puzzle_count, "puzzles loaded")

    now = datetime.now()
    limit = 10000

    # solve them
    workers = Pool(16)
    jobs = enumerate(loader.get_strings(limit))
    result = workers.map(solve_puzzle, jobs)
    print("Correctly Completed:", sum(result), "out of", limit)
    print("Took ", datetime.now()-now, "to solve", limit)