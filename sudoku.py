import tkinter as tk
from tkinter import messagebox
import random
import time


class SudokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        self.root.resizable(False, False)

        self.lives = 3
        self.seconds = 0
        self.running = True
        self.solution = []
        self.board = []
        self.original = []

        self.create_ui()
        self.new_game("Easy")
        self.update_timer()

    def create_ui(self):
        title = tk.Label(
            self.root,
            text="SUDOKU",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=10)

        top_frame = tk.Frame(self.root)
        top_frame.pack()

        tk.Label(
            top_frame,
            text="Difficulty:",
            font=("Arial", 11)
        ).grid(row=0, column=0, padx=5)

        self.difficulty = tk.StringVar(value="Easy")

        difficulty_menu = tk.OptionMenu(
            top_frame,
            self.difficulty,
            "Easy",
            "Medium",
            "Hard"
        )
        difficulty_menu.grid(row=0, column=1, padx=5)

        new_button = tk.Button(
            top_frame,
            text="New Game",
            command=self.start_new_game
        )
        new_button.grid(row=0, column=2, padx=5)

        self.timer_label = tk.Label(
            top_frame,
            text="Time: 00:00",
            font=("Arial", 11, "bold")
        )
        self.timer_label.grid(row=0, column=3, padx=10)

        self.lives_label = tk.Label(
            self.root,
            text="Lives: 3",
            font=("Arial", 12, "bold")
        )
        self.lives_label.pack(pady=5)

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=10, pady=10)

        self.cells = []

        for row in range(9):
            row_cells = []

            for col in range(9):
                cell = tk.Entry(
                    self.board_frame,
                    width=2,
                    font=("Arial", 22),
                    justify="center"
                )

                padx = (3 if col % 3 == 0 else 1,
                        3 if col % 3 == 2 else 1)

                pady = (3 if row % 3 == 0 else 1,
                        3 if row % 3 == 2 else 1)

                cell.grid(
                    row=row,
                    column=col,
                    padx=padx,
                    pady=pady,
                    ipady=5
                )

                cell.bind(
                    "<KeyRelease>",
                    lambda event, r=row, c=col:
                    self.check_input(event, r, c)
                )

                row_cells.append(cell)

            self.cells.append(row_cells)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        tk.Button(
            button_frame,
            text="Check",
            width=10,
            command=self.check_board
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Hint",
            width=10,
            command=self.give_hint
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Reset",
            width=10,
            command=self.reset_game
        ).grid(row=0, column=2, padx=5)

    def create_solution(self):
        board = [[0 for _ in range(9)] for _ in range(9)]

        def solve():
            empty = self.find_empty(board)

            if not empty:
                return True

            row, col = empty
            numbers = list(range(1, 10))
            random.shuffle(numbers)

            for num in numbers:
                if self.valid_number(board, row, col, num):
                    board[row][col] = num

                    if solve():
                        return True

                    board[row][col] = 0

            return False

        solve()
        return board

    def find_empty(self, board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    return row, col

        return None

    def valid_number(self, board, row, col, num):
        for i in range(9):
            if board[row][i] == num:
                return False

        for i in range(9):
            if board[i][col] == num:
                return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if board[i][j] == num:
                    return False

        return True

    def create_puzzle(self, solution, difficulty):
        puzzle = [row[:] for row in solution]

        if difficulty == "Easy":
            remove = 35
        elif difficulty == "Medium":
            remove = 45
        else:
            remove = 55

        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)

        for r, c in positions[:remove]:
            puzzle[r][c] = 0

        return puzzle

    def start_new_game(self):
        self.new_game(self.difficulty.get())

    def new_game(self, difficulty):
        self.lives = 3
        self.seconds = 0
        self.running = True

        self.solution = self.create_solution()
        self.board = self.create_puzzle(
            self.solution,
            difficulty
        )

        self.original = [row[:] for row in self.board]

        self.display_board()

        self.lives_label.config(
            text="Lives: 3"
        )

    def display_board(self):
        for row in range(9):
            for col in range(9):
                cell = self.cells[row][col]

                cell.config(
                    state="normal",
                    bg="white"
                )

                cell.delete(0, tk.END)

                if self.board[row][col] != 0:
                    cell.insert(
                        0,
                        str(self.board[row][col])
                    )

                    cell.config(
                        state="disabled",
                        disabledforeground="black"
                    )

    def check_input(self, event, row, col):
        if not self.running:
            return

        if self.original[row][col] != 0:
            return

        value = self.cells[row][col].get()

        if value == "":
            self.board[row][col] = 0
            return

        if not value.isdigit() or value not in "123456789":
            self.cells[row][col].delete(0, tk.END)
            return

        number = int(value)

        if number == self.solution[row][col]:
            self.board[row][col] = number
            self.cells[row][col].config(
                fg="green"
            )

            if self.is_complete():
                self.win_game()

        else:
            self.cells[row][col].delete(0, tk.END)

            self.lives -= 1

            self.lives_label.config(
                text=f"Lives: {self.lives}"
            )

            self.cells[row][col].config(
                bg="red"
            )

            self.root.after(
                300,
                lambda: self.cells[row][col].config(
                    bg="white"
                )
            )

            if self.lives == 0:
                self.game_over()

    def is_complete(self):
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != self.solution[row][col]:
                    return False

        return True

    def check_board(self):
        if self.is_complete():
            self.win_game()
            return

        incorrect = 0
        empty = 0

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    empty += 1
                elif self.board[row][col] != self.solution[row][col]:
                    incorrect += 1

        if incorrect == 0 and empty > 0:
            messagebox.showinfo(
                "Sudoku",
                "Everything filled so far is correct!"
            )
        else:
            messagebox.showwarning(
                "Sudoku",
                f"You have {incorrect} incorrect cells."
            )

    def give_hint(self):
        empty_cells = []

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    empty_cells.append((row, col))

        if not empty_cells:
            return

        row, col = random.choice(empty_cells)

        number = self.solution[row][col]

        self.board[row][col] = number

        self.cells[row][col].insert(
            0,
            str(number)
        )

        self.cells[row][col].config(
            fg="blue"
        )

        if self.is_complete():
            self.win_game()

    def reset_game(self):
        self.board = [row[:] for row in self.original]

        self.display_board()

        self.lives = 3

        self.lives_label.config(
            text="Lives: 3"
        )

        self.seconds = 0
        self.running = True

    def game_over(self):
        self.running = False

        messagebox.showerror(
            "Game Over",
            "You lost all your lives!"
        )

        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    self.cells[row][col].config(
                        state="disabled"
                    )

    def win_game(self):
        self.running = False

        minutes = self.seconds // 60
        seconds = self.seconds % 60

        messagebox.showinfo(
            "Congratulations!",
            f"You solved the Sudoku!\n\n"
            f"Time: {minutes:02d}:{seconds:02d}"
        )

    def update_timer(self):
        if self.running:
            minutes = self.seconds // 60
            seconds = self.seconds % 60

            self.timer_label.config(
                text=f"Time: {minutes:02d}:{seconds:02d}"
            )

            self.seconds += 1

        self.root.after(
            1000,
            self.update_timer
        )


root = tk.Tk()
game = SudokuGame(root)
root.mainloop()
