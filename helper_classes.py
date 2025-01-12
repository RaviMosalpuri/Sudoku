import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
import numpy as np
import random


class SudokuApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.timer_running = False
        self.elapsed_time = 0
        self.mistakes = 0
        self.board = None
        self.main_menu()
        self.root.mainloop()


    def main_menu(self):
        """Main menu for the game."""
        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title and instructions
        tk.Label(self.root, text="Sudoku", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.root, text="Select Difficulty Level", font=("Arial", 16)).pack(pady=10)

        # Difficulty buttons
        for difficulty, text in enumerate(["Easy", "Medium", "Hard"]):
            tk.Button(self.root, text=text, font=("Arial", 14), command=lambda d=difficulty: self.start_game(d)).pack(pady=5)


    def start_game(self, difficulty):
        """Start a new game."""
        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reset state variables
        self.timer_running = True
        self.elapsed_time = 0
        self.mistakes = 0

        # Display timer and mistakes
        self.timer_label = tk.Label(self.root, text="Time: 0:00", font=("Arial", 14))
        self.timer_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.mistakes_label = tk.Label(self.root, text="Mistakes: 0/3", font=("Arial", 14))
        self.mistakes_label.grid(row=0, column=5, columnspan=4, pady=10)

        # Initialize the Sudoku board
        self.board = SudokuBoard(self.root, self, difficulty)

        # Add control buttons
        tk.Button(self.root, text="Solve", command=self.board.solve_board).grid(row=10, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Reset", command=self.board.reset_board).grid(row=10, column=3, columnspan=3, pady=10)
        tk.Button(self.root, text="Main Menu", command=self.return_to_menu).grid(row=11, column=0, columnspan=9, pady=10)

        # Start the timer
        self.update_timer()


    def update_timer(self):
        """Update the timer every second."""
        if self.timer_running:
            self.elapsed_time += 1
            minutes, seconds = divmod(self.elapsed_time, 60)
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02}")
            self.root.after(1000, self.update_timer)


    def update_mistakes(self):
        """Increment mistakes and handle game over if necessary."""
        self.mistakes += 1
        self.mistakes_label.config(text=f"Mistakes: {self.mistakes}/3")
        if self.mistakes >= 3:
            self.game_over()


    def game_over(self):
        """Handle game-over logic."""
        self.timer_running = False
        messagebox.showinfo("Game Over", "You've made 3 mistakes. Game Over!")
        self.board.disable_all_inputs()
        self.return_to_menu()


    def return_to_menu(self):
        """Return to the main menu."""
        self.timer_running = False
        self.main_menu()


class SudokuBoard:
    def __init__(self, root, app, difficulty):
        self.root = root
        self.app = app
        self.difficulty = difficulty
        self.sudoku = None
        self.sudoku_solved = None
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.generate_board()


    def generate_board(self):
        """Generate a Sudoku puzzle and display it on the board."""
        # Generate puzzle
        self.generate_sudoku(self.difficulty)

        # Create Sudoku grid
        for box_row in range(3):
            for box_col in range(3):
                frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
                frame.grid(row=box_row * 3 + 1, column=box_col * 3, rowspan=3, columnspan=3, padx=1, pady=1)
                for row in range(3):
                    for col in range(3):
                        r, c = box_row * 3 + row, box_col * 3 + col
                        entry = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                        entry.grid(row=row, column=col, padx=1, pady=1)
                        if self.sudoku[r][c] != 0:
                            entry.insert(0, str(self.sudoku[r][c]))
                            entry.config(state="disabled", disabledforeground="black")
                        else:
                            entry.bind('<KeyRelease>', lambda _, e=entry, r=r, c=c: self.is_entry_valid(e, r, c))
                        self.entries[r][c] = entry


    def is_valid(self, sudoku, r, c, val):
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


    def solve_sudoku(self, sudoku, row, col):
        if row == 8 and col == 9:
            return True
        if col == 9:
            row += 1
            col = 0
        if sudoku[row][col] != 0:
            return self.solve_sudoku(sudoku, row, col + 1)
        for val in range(1, 10):
            if self.is_valid(sudoku, row, col, val):
                sudoku[row][col] = val
                if self.solve_sudoku(sudoku, row, col + 1):
                    return True
            sudoku[row][col] = 0
        return False


    def generate_sudoku(self, level=0):
        self.sudoku = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            nums = np.random.choice(np.arange(1, 10), 9, replace=False).tolist()
            for row in range(3):
                for col in range(3):
                    self.sudoku[row + i][col + i] = nums.pop()
        
        self.solve_sudoku(self.sudoku, 0, 0)
        self.sudoku_solved = deepcopy(self.sudoku)
        
        if level == 0:
            num_empty_cells = random.randint(32, 36)
        elif level == 1:
            num_empty_cells = random.randint(37, 41)
        else:
            num_empty_cells = random.randint(42, 46)
        for _ in range(num_empty_cells):
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.sudoku[row][col] = 0


    def is_entry_valid(self, entry, row, col):
        """
        Function to update the background color of any entry based on if it's empty, correct and incorrect.

        Parameters:
        entry : entry
        row : row number
        col : column number
        """
        if entry.get() == '0' or entry.get() == '':
            entry.config(bg='white')
        elif int(entry.get()) != self.sudoku_solved[row][col]:
            entry.config(bg='red')
            self.app.update_mistakes()
        else:
            entry.config(bg='white')


    def solve_board(self):
        """Fill the grid with the solved puzzle."""
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, str(self.sudoku_solved[r][c]))
                self.entries[r][c].config(state="disabled")


    def reset_board(self):
        """Clear all user inputs and reset the grid."""
        for r in range(9):
            for c in range(9):
                if self.sudoku[r][c] == 0:
                    self.entries[r][c].delete(0, tk.END)
                    self.entries[r][c].config(bg="white", state="normal")


    def disable_all_inputs(self):
        """Disable all editable cells."""
        for row in self.entries:
            for entry in row:
                if entry["state"] != "disabled":
                    entry.config(state="disabled")