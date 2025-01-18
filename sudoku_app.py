import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

import base64
import json
import os

import sudoku_board


class SudokuApp:
    def __init__(self):

        # Create a new Tkinter object
        self.root = tk.Tk()
        # Add a window title
        self.root.title("Sudoku")
        
        # Set window size and position
        window_width = 380
        window_height = 450
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate position coordinates
        center_x = int((screen_width - window_width) / 2)
        center_y = int((screen_height - window_height) / 2)
        
        # Set window size and position
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Prevent window resizing
        self.root.resizable(False, False)
        
        # Initialise the required variables
        self.timer_running = False
        self.elapsed_time = 0
        self.mistakes = 0
        self.board = None
        self.level = None
        
        # Load statistics from file or initialize if file doesn't exist
        self.stats = self.__load_statistics()

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
            
        # Add Statistics button
        tk.Button(self.root, text="Statistics", font=("Arial", 14), command=self.__show_statistics).pack(pady=60)


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
        self.level = difficulty

        # Display timer at the top, updated every second
        self.timer_label = tk.Label(self.root, text="Time: 0:00", font=("Arial", 14))
        self.timer_label.grid(row=0, column=0, columnspan=4, pady=10, padx=10, sticky='w')
        
        # Display the mistakes count, updated as mistakes made
        self.mistakes_label = tk.Label(self.root, text="Mistakes: 0/3", font=("Arial", 14))
        self.mistakes_label.grid(row=0, column=4, columnspan=5, pady=10, padx=10, sticky='e')

        # Initialize the Sudoku board
        self.board = sudoku_board.SudokuBoard(self.root, self, difficulty)
        
        # Create a frame for the buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=10, column=0, columnspan=9, pady=10)
        
        # Add control buttons Solve, Reset and Main Menu in the frame
        tk.Button(button_frame, text="Main Menu", width=10, command=self.__return_to_menu).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Solve", width=10, command=self.board.solve_board).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Reset", width=10, command=self.board.reset_board).pack(side=tk.LEFT, padx=5)

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
        
        # Get difficulty level name
        difficulty = ['easy', 'medium', 'hard'][self.level]
        
        # Update statistics for current difficulty
        self.stats[difficulty]['games_played'] += 1
        self.stats[difficulty]['games_won'] += 1
        self.stats[difficulty]['total_time'] += self.elapsed_time
        self.stats[difficulty]['average_time'] = self.stats[difficulty]['total_time'] / self.stats[difficulty]['games_won']
        self.stats[difficulty]['best_time'] = min(self.stats[difficulty]['best_time'], self.elapsed_time)
        
        # Save statistics to file
        self.__save_statistics()
        
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
        
        # Update statistics for current difficulty
        difficulty = ['easy', 'medium', 'hard'][self.level]
        self.stats[difficulty]['games_played'] += 1
        
        # Save statistics to file
        self.__save_statistics()
        
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


    def __show_statistics(self):
        """
        Function to display game statistics.
        """
        # Clear the current window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Set the Title
        tk.Label(self.root, text="Statistics", font=("Arial", 24, "bold")).pack(pady=20)

        # Function to update the statistics based on the difficulty level selected
        def update_stats_display(_=None):
            difficulty = combo_box.get().lower()
            stats = self.stats[difficulty]
            
            stats_text = f"""
            Difficulty: {difficulty.title()}
            Games Played: {stats['games_played']}
            Games Won: {stats['games_won']}
            Win Rate: {(stats['games_won'] / stats['games_played'] * 100 if stats['games_played'] > 0 else 0):.1f}%
            Best Time: {int(stats['best_time']) if stats['best_time'] != float('inf') else 'N/A'} seconds
            Average Time: {int(stats['average_time']) if stats['average_time'] > 0 else 'N/A'} seconds
            """
            stats_label.config(text=stats_text)

        # Create a Combobox for difficulty selection with state='readonly'
        combo_box = ttk.Combobox(self.root, values=["Easy", "Medium", "Hard"], state='readonly')
        combo_box.pack(pady=10)
        combo_box.set("Easy")  # Set default value
        
        # Create label for statistics
        stats_label = tk.Label(self.root, text="", font=("Arial", 14), justify=tk.LEFT)
        stats_label.pack(pady=20)
        
        # Bind the combobox selection to update stats
        combo_box.bind("<<ComboboxSelected>>", update_stats_display)
        
        # Show initial statistics
        update_stats_display()

        # Add back button
        tk.Button(self.root, text="Back to Main Menu", font=("Arial", 14), command=self.__main_menu).pack(pady=20)


    def __obfuscate_data(self, data):
        """
        Obfuscate the data using XOR with a simple key and base64 encoding

        Parameters:
        data : str, string

        Returns:
        str : string of encoded data
        """
        key = b'sudoku'  # Simple encryption key
        data_bytes = data.encode('utf-8')
        xored = bytes(a ^ b for a, b in zip(data_bytes, key * (len(data_bytes) // len(key) + 1)))
        return base64.b64encode(xored).decode('utf-8')


    def __deobfuscate_data(self, encoded_data):
        """
        Deobfuscate the data using base64 decoding and XOR with the same key

        Parameters:
        encoded_data : str, encoded data string

        Returns:
        str : string of deobfuscated data
        """
        key = b'sudoku'  # Same key as encryption
        decoded = base64.b64decode(encoded_data.encode('utf-8'))
        xored = bytes(a ^ b for a, b in zip(decoded, key * (len(decoded) // len(key) + 1)))
        return xored.decode('utf-8')


    def __load_statistics(self):
        """
        Load statistics from file or return default values if file doesn't exist
        """
        default_stats = {
            'easy': {
                'games_played': 0,
                'games_won': 0,
                'best_time': float('inf'),
                'average_time': 0,
                'total_time': 0
            },
            'medium': {
                'games_played': 0,
                'games_won': 0,
                'best_time': float('inf'),
                'average_time': 0,
                'total_time': 0
            },
            'hard': {
                'games_played': 0,
                'games_won': 0,
                'best_time': float('inf'),
                'average_time': 0,
                'total_time': 0
            }
        }
        
        try:
            if os.path.exists('sudoku_stats.dat'):
                with open('sudoku_stats.dat', 'r') as f:
                    encoded_data = f.read()
                    json_str = self.__deobfuscate_data(encoded_data)
                    stats = json.loads(json_str)
                    # Convert best_time back to float('inf') if it was saved as "inf"
                    for difficulty in ['easy', 'medium', 'hard']:
                        if stats[difficulty]['best_time'] == "inf":
                            stats[difficulty]['best_time'] = float('inf')
                    return stats
        except Exception as e:
            print(f"Error loading statistics: {e}")
        
        return default_stats


    def __save_statistics(self):
        """
        Save current statistics to file
        """
        try:
            # Create a copy of stats to modify for saving
            stats_to_save = self.stats.copy()
            # Convert float('inf') to "inf" string for JSON serialization
            for difficulty in ['easy', 'medium', 'hard']:
                if stats_to_save[difficulty]['best_time'] == float('inf'):
                    stats_to_save[difficulty]['best_time'] = "inf"
                
            # Convert to JSON string and obfuscate
            json_str = json.dumps(stats_to_save)
            encoded_data = self.__obfuscate_data(json_str)
            
            with open('sudoku_stats.dat', 'w') as file:  # Changed extension to .dat
                file.write(encoded_data)
        
        except Exception as exception:
            print(f"Error saving statistics: {exception}")