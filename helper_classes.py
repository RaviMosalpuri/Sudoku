import tkinter as tk
from tkinter import messagebox
from copy import deepcopy

import helper_functions


class SudokuApp:
    """
    Sudoku game class.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.timer_running = False
        self.elapsed_time = 0
        self.mistakes = 0
        self.main_menu()
        self.root.mainloop()


    def main_menu(self):
        """
        Main menu for the game. Adds 'Easy', 'Medium' and 'Hard' level buttons for the game.
        """

        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add the 'Sudoku' text
        title = tk.Label(self.root, text="Sudoku", font=("Arial", 24, "bold"))
        title.pack(pady=20)

        # Add the 'Select Difficulty level' text
        instruction = tk.Label(self.root, text="Select Difficulty Level", font=("Arial", 16))
        instruction.pack(pady=10)

        # Add the button for 'Easy' level difficulty
        easy_button = tk.Button(self.root, text="Easy", font=("Arial", 14), command=lambda: self.start_game(0))
        easy_button.pack(pady=5)

        # Add the button for 'Medium' level difficulty
        medium_button = tk.Button(self.root, text="Medium", font=("Arial", 14), command=lambda: self.start_game(1))
        medium_button.pack(pady=5)

        # Add the button for 'Hard' level difficulty
        hard_button = tk.Button(self.root, text="Hard", font=("Arial", 14), command=lambda: self.start_game(2))
        hard_button.pack(pady=5)


    def start_game(self, difficulty):
        """
        Start the game. Generates sudoku board, and adds 'Solve', 'Reset' and 'Main Menu' buttons.

        Parameters:
        self : self
        difficulty : int, difficulty level
        """

        # Generate a new puzzle
        self.sudoku = helper_functions.generate_sudoku(difficulty)
        self.sudoku_solved = deepcopy(self.sudoku)
        helper_functions.solve_sudoku(self.sudoku_solved, 0, 0)

        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Reset the timer
        self.elapsed_time = 0
        self.mistakes = 0
        self.timer_running = True

        # Create the timer label
        self.timer_label = tk.Label(self.root, text="Time: 0:00", font=("Arial", 14))
        self.timer_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.update_timer()

        self.mistakes_label = tk.Label(self.root, text="Mistakes: 0/3", font=("Arial", 14))
        self.mistakes_label.grid(row=0, column=5, columnspan=10, pady=10)

        # Create the Sudoku grid
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for box_row in range(3):
            for box_col in range(3):
                frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
                frame.grid(row=box_row * 3 + 1, column=box_col * 3, rowspan=3, columnspan=3, padx=1, pady=1)
                for row in range(3):
                    for col in range(3):
                        r = box_row * 3 + row
                        c = box_col * 3 + col
                        entry = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                        entry.grid(row=row, column=col, padx=1, pady=1)
                        if self.sudoku[r][c] != 0:
                            entry.insert(0, str(self.sudoku[r][c]))
                            entry.config(state="disabled", disabledforeground="black")
                        entry.bind('<KeyRelease>', lambda event, e=entry, r=r, c=c: self.is_entry_valid(e, r, c))
                        self.entries[r][c] = entry


        # Add control buttons
        solve_button = tk.Button(self.root, text="Solve", command=self.solve)
        solve_button.grid(row=10, column=0, columnspan=4, pady=10)

        reset_button = tk.Button(self.root, text="Reset", command=self.reset)
        reset_button.grid(row=10, column=4, columnspan=4, pady=10)

        menu_button = tk.Button(self.root, text="Main Menu", command=self.return_to_menu)
        menu_button.grid(row=11, column=0, columnspan=9, pady=10)


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
            self.update_mistakes()
        else:
            entry.config(bg='white')


    def update_mistakes(self):
        """
        Updates the number of mistakes.
        """
        self.mistakes += 1
        self.mistakes_label.config(text=f"Mistakes: {self.mistakes}/3")


    def update_timer(self):
        """
        Updates the timer label for the game.
        """
        if self.timer_running:
            self.elapsed_time += 1
            minutes = self.elapsed_time // 60
            seconds = self.elapsed_time % 60
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02}")
            self.root.after(1000, self.update_timer)


    def solve(self):
        """
        Solves the sudoku game and displays the solved game.
        """
        self.timer_running = False
        puzzle = [[0 if self.entries[r][c].get() == "" else int(self.entries[r][c].get()) for c in range(9)] for r in range(9)]
        if helper_functions.solve_sudoku(puzzle, 0, 0):
            for r in range(9):
                for c in range(9):
                    self.entries[r][c].delete(0, tk.END)
                    self.entries[r][c].insert(0, str(puzzle[r][c]))
        else:
            messagebox.showerror("Error", "This puzzle cannot be solved.")


    def reset(self):
        """
        Resets the sudoku board.
        """
        for r in range(9):
            for c in range(9):
                if self.sudoku[r][c] == 0:
                    self.entries[r][c].delete(0, tk.END)


    def return_to_menu(self):
        """
        Return to the main menu.
        """
        self.timer_running = False
        self.main_menu()