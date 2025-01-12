import numpy as np
import random


def is_valid(sudoku, r, c, val):
    for row in range(9):
        if sudoku[row][c] == val:
            return False
    for col in range(9):
        if sudoku[r][col] == val:
            return False
    r_start = (r // 3) * 3
    c_start = (c // 3) * 3
    for row in range(r_start, r_start + 3):
        for col in range(c_start, c_start + 3):
            if sudoku[row][col] == val:
                return False
    return True


def solve_sudoku(sudoku, row, col):
    if row == 8 and col == 9:
        return True
    if col == 9:
        row += 1
        col = 0
    if sudoku[row][col] != 0:
        return solve_sudoku(sudoku, row, col + 1)
    for val in range(1, 10):
        if is_valid(sudoku, row, col, val):
            sudoku[row][col] = val
            if solve_sudoku(sudoku, row, col + 1):
                return True
        sudoku[row][col] = 0
    return False


def generate_sudoku(level=0):
    sudoku = [[0 for _ in range(9)] for _ in range(9)]
    for i in range(0, 9, 3):
        nums = np.random.choice(np.arange(1, 10), 9, replace=False).tolist()
        for row in range(3):
            for col in range(3):
                sudoku[row + i][col + i] = nums.pop()
    solve_sudoku(sudoku, 0, 0)
    if level == 0:
        num_empty_cells = random.randint(32, 36)
    elif level == 1:
        num_empty_cells = random.randint(37, 41)
    else:
        num_empty_cells = random.randint(42, 46)
    for _ in range(num_empty_cells):
        row, col = random.randint(0, 8), random.randint(0, 8)
        sudoku[row][col] = 0
    return sudoku