import tkinter as tk
from tkinter import messagebox
from copy import deepcopy
import numpy as np
import random


class SudokuApp:
    def __init__(self):

        # Create a new Tkinter object
        self.root = tk.Tk()
        # Add a window title
        self.root.title("Sudoku")
        
        # Initialise the required variables
        self.timer_running = False
        self.elapsed_time = 0
        self.mistakes = 0
        self.board = None

        # Show the main menu
        self.__main_menu()
        # Run the main loop for Tkinter
        self.root.mainloop()


    def __main_menu(self):
        """
        Function to display the main menu for the game.
        """
        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the Title and instructions
        tk.Label(self.root, text="Sudoku", font=("Arial", 24, "bold")).pack(pady=20)
        tk.Label(self.root, text="Select Difficulty Level", font=("Arial", 16)).pack(pady=10)

        # Add the three Difficulty buttons
        for difficulty, text in enumerate(["Easy", "Medium", "Hard"]):
            tk.Button(self.root, text=text, font=("Arial", 14), command=lambda d=difficulty: self.__start_game(d)).pack(pady=5)


    def __start_game(self, difficulty):
        """
        Function to start a new game.
        
        Parameters:
        difficulty : int, difficulty level
        """
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

        # Add control buttons Solve, Reset and Main Menu
        tk.Button(self.root, text="Solve", command=self.board.solve_board).grid(row=10, column=0, columnspan=3, pady=10)
        tk.Button(self.root, text="Reset", command=self.board.reset_board).grid(row=10, column=3, columnspan=3, pady=10)
        tk.Button(self.root, text="Main Menu", command=self.__return_to_menu).grid(row=11, column=0, columnspan=9, pady=10)

        # Start the timer
        self.__update_timer()


    def __update_timer(self):
        """
        Function to update the timer every second.
        """
        # Check if the timer is running
        if self.timer_running:
            # Increment elapsed time with 1
            self.elapsed_time += 1
            # Get the minutes and seconds from elapsed time
            minutes, seconds = divmod(self.elapsed_time, 60)
            # Show the elapsed time
            self.timer_label.config(text=f"Time: {minutes}:{seconds:02}")
            # Call this function after 1 second
            self.root.after(1000, self.__update_timer)


    def update_mistakes(self):
        """
        Function to increment mistakes and handle game over if necessary.
        """
        # Update the number of mistakes
        self.mistakes += 1
        # Show the updated number of mistakes
        self.mistakes_label.config(text=f"Mistakes: {self.mistakes}/3")
        # Check if the number of mistakes if more than or equal to 3
        if self.mistakes >= 3:
            # Then display game over
            self.__game_over()


    def won_game(self):
        """
        Function to handle game win logic, shows won the game message and disables all the inputs on entries.
        """
        # Stop the timer
        self.timer_running = False
        # Show won the game message
        messagebox.showinfo("Won", f"You have won the game! \nTime taken: {self.elapsed_time} seconds \nMistakes: {self.mistakes}")
        # Disable all the inputs on entries
        self.board.disable_all_inputs()
        # Return to the main menu
        self.__return_to_menu()


    def __game_over(self):
        """
        Function to handle game-over logic, shows Game over message and disables all the inputs on entries.
        """
        # Stop the timer
        self.timer_running = False
        # Show game over message
        messagebox.showinfo("Game Over", "You've made 3 mistakes. Game Over!")
        # Disable all the inputs on entries
        self.board.disable_all_inputs()
        # Return to the main menu
        self.__return_to_menu()


    def __return_to_menu(self):
        """
        Function to return to the main menu.
        """
        # Stop the timer
        self.timer_running = False
        # Show the main menu
        self.__main_menu()


class SudokuBoard:
    def __init__(self, root, app, difficulty):

        # Initialise the required variables
        self.root = root
        self.app = app
        self.difficulty = difficulty
        self.sudoku = None
        self.sudoku_solved = None

        # Entries for user input
        self.entries = [[None for _ in range(9)] for _ in range(9)]

        # Generate the sudoku board
        self.__generate_board()


    def __generate_board(self):
        """
        Function to generate a Sudoku puzzle and display it on the board.
        """
        
        # Generate puzzle
        self.__generate_random_sudoku(self.difficulty)

        # Create Sudoku grid
        for box_row in range(3):
            for box_col in range(3):
                # Create a frame for the box
                frame = tk.Frame(self.root, highlightbackground="black", highlightthickness=1)
                frame.grid(row=box_row * 3 + 1, column=box_col * 3, rowspan=3, columnspan=3, padx=1, pady=1)
                for row in range(3):
                    for col in range(3):
                        r, c = box_row * 3 + row, box_col * 3 + col
                        # Create a 'Entry' for user input
                        entry = tk.Entry(frame, width=2, font=("Arial", 18), justify="center")
                        entry.grid(row=row, column=col, padx=1, pady=1)
                        # Check if the there is a value at this place
                        if self.sudoku[r][c] != 0:
                            # If value is there, insert it and disable user input for it
                            entry.insert(0, str(self.sudoku[r][c]))
                            entry.config(state="disabled", disabledforeground="black")
                        else:
                            # If value isn't there, then bind entry to a 'KeyRelease' to check the user input
                            entry.bind('<KeyRelease>', lambda _, e=entry, r=r, c=c: self.__is_entry_valid(e, r, c))
                        # Add the entry to entries list
                        self.entries[r][c] = entry


    def __is_number_valid(self, r, c, val):
        """
        Function to check if the number (value) corresponding to the row and column is valid. It checks in the row, column and same box for the same number.

        Parameters:
        sudoku : entry
        row : row number
        col : column number
        """
        for row in range(9):
            if self.sudoku[row][c] == val:
                return False
        for col in range(9):
            if self.sudoku[r][col] == val:
                return False
        r_start = (r // 3) * 3
        c_start = (c // 3) * 3
        for row in range(r_start, r_start + 3):
            for col in range(c_start, c_start + 3):
                if self.sudoku[row][col] == val:
                    return False
        return True


    def __solve_sudoku(self, row=0, col=0):
        """
        Function to solve the sudoku puzzle.
        
        Parameters:
        row : row number
        col : column number
        """
        if row == 8 and col == 9:
            return True
        if col == 9:
            row += 1
            col = 0
        if self.sudoku[row][col] != 0:
            return self.__solve_sudoku(row, col + 1)
        for val in range(1, 10):
            if self.__is_number_valid(row, col, val):
                self.sudoku[row][col] = val
                if self.__solve_sudoku(row, col + 1):
                    return True
            self.sudoku[row][col] = 0
        return False


    def __generate_random_sudoku(self, level=0):
        """
        Function to generate a random sudoku puzzle.

        Parameters:
        level : int, level of difficulty
        """
        self.sudoku = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(0, 9, 3):
            nums = np.random.choice(np.arange(1, 10), 9, replace=False).tolist()
            for row in range(3):
                for col in range(3):
                    self.sudoku[row + i][col + i] = nums.pop()
        
        self.__solve_sudoku()
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


    def __is_entry_valid(self, entry, row, col):
        """
        Function to update the background color of any entry based on if it's empty, correct and incorrect.

        Parameters:
        entry : entry
        row : row number
        col : column number
        """
        if entry.get() == '0' or entry.get() == '':
            entry.config(bg='white')
            self.sudoku[row][col] = 0
        elif int(entry.get()) != self.sudoku_solved[row][col]:
            entry.config(bg='red')
            self.app.update_mistakes()
        else:
            entry.config(bg='white')
            self.sudoku[row][col] = self.sudoku_solved[row][col]
            
            if self.check_if_solved():
                self.app.won_game()


    def solve_board(self):
        """
        Function to fill the grid with the solved puzzle.
        """
        for r in range(9):
            for c in range(9):
                self.entries[r][c].delete(0, tk.END)
                self.entries[r][c].insert(0, str(self.sudoku_solved[r][c]))
                self.entries[r][c].config(state="disabled")


    def reset_board(self):
        """
        Function to clear all user inputs and reset the grid.
        """
        for r in range(9):
            for c in range(9):
                if self.entries[r][c].cget('state') != 'disabled':
                    self.entries[r][c].delete(0, tk.END)
                    self.entries[r][c].config(bg="white", state="normal")


    def disable_all_inputs(self):
        """
        Function to disable all inputs on editable cells.
        """
        for row in self.entries:
            for entry in row:
                if entry["state"] != "disabled":
                    entry.config(state="disabled")

    
    def check_if_solved(self):
        return self.sudoku == self.sudoku_solved