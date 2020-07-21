from sudoku_loader import SudokuLoader
from sudoku_solver import SudokuSolver
from puzzle import Puzzle
from collections import deque
from multiprocessing import Pool


# correct = 0

def solve_puzzle(puzzle_strings):

    puzzle_id = puzzle_strings[0]

    solve_queue = deque()
    puzzle = Puzzle(puzzle_strings[1][0], solve_queue)
    solution = Puzzle(puzzle_strings[1][1])

    solver = SudokuSolver(puzzle, solve_queue)
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

    # solve them
    workers = Pool(16)
    jobs = enumerate(loader.get_strings())
    result = workers.map(solve_puzzle, jobs)
    print("Correctly Completed:", sum(result), "out of", loader.puzzle_count)