import tkinter as tk
from tkinter import messagebox

import sudoku_board


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

        # Display timer at the top, updated every second
        self.timer_label = tk.Label(self.root, text="Time: 0:00", font=("Arial", 14))
        self.timer_label.grid(row=0, column=0, columnspan=2, pady=10)
        # Display the mistakes count, updated as mistakes made
        self.mistakes_label = tk.Label(self.root, text="Mistakes: 0/3", font=("Arial", 14))
        self.mistakes_label.grid(row=0, column=5, columnspan=4, pady=10)

        # Initialize the Sudoku board
        self.board = sudoku_board.SudokuBoard(self.root, self, difficulty)

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