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


rng) {

    int row = -1;
    int col = -1;
    bool emptyFound = false;

    for (int i = 0; i < 9; i++) {

        for (int j = 0; j < 9; j++) {

            if (board[i][j] == 0) {
                row = i;
                col = j;
                emptyFound = true;
                break;
            }
        }

        if (emptyFound) {
            break;
        }
    }

    if (!emptyFound) {
        return true;
    }

    int numbers[9] = {
        1, 2, 3, 4, 5, 6, 7, 8, 9
    };

    shuffle(numbers, numbers + 9, rng);

    for (int i = 0; i < 9; i++) {

        int num = numbers[i];

        if (isSafe(board, row, col, num)) {

            board[row][col] = num;

            if (solveSudoku(board, rng)) {
                return true;
            }

            board[row][col] = 0;
        }
    }

    return false;
}

int countSolutions(int board[9][9]) {

    int row = -1;
    int col = -1;
    bool emptyFound = false;

    for (int i = 0; i < 9; i++) {

        for (int j = 0; j < 9; j++) {

            if (board[i][j] == 0) {
                row = i;
                col = j;
                emptyFound = true;
                break;
            }
        }

        if (emptyFound) {
            break;
        }
    }

    if (!emptyFound) {
        return 1;
    }

    int totalSolutions = 0;

    for (int num = 1; num <= 9; num++) {

        if (isSafe(board, row, col, num)) {

            board[row][col] = num;

            totalSolutions += countSolutions(board);

            board[row][col] = 0;

            if (totalSolutions > 1) {
                return totalSolutions;
            }
        }
    }

    return totalSolutions;
}

void copyBoard(int source[9][9], int destination[9][9]) {

    for (int i = 0; i < 9; i++) {

        for (int j = 0; j < 9; j++) {
            destination[i][j] = source[i][j];
        }
    }
}

void generatePuzzle(
    int solution[9][9],
    int puzzle[9][9],
    int cellsToRemove,
    mt19937& rng
) {

    copyBoard(solution, puzzle);

    int removed = 0;

    while (removed < cellsToRemove) {

        int row = rng() % 9;
        int col = rng() % 9;

        if (puzzle[row][col] == 0) {
            continue;
        }

        int originalValue = puzzle[row][col];

        puzzle[row][col] = 0;

        int testBoard[9][9];

        copyBoard(puzzle, testBoard);

        int solutions = countSolutions(testBoard);

        if (solutions == 1) {
            removed++;
        }
        else {
            puzzle[row][col] = originalValue;
        }
    }
}

void displayBoard(int board[9][9]) {

    cout << "\n";

    cout << "       1 2 3   4 5 6   7 8 9\n";
    cout << "     +-------+-------+-------+\n";

    for (int i = 0; i < 9; i++) {

        cout << "  " << i + 1 << "  | ";

        for (int j = 0; j < 9; j++) {

            if (board[i][j] == 0) {
                cout << ". ";
            }
            else {
                cout << board[i][j] << " ";
            }

            if ((j + 1) % 3 == 0) {
                cout << "| ";
            }
        }

        cout << "\n";

        if ((i + 1) % 3 == 0) {
            cout << "     +-------+-------+-------+\n";
        }
    }
}

bool isComplete(int board[9][9]) {

    for (int i = 0; i < 9; i++) {

        for (int j = 0; j < 9; j++) {

            if (board[i][j] == 0) {
                return false;
            }
        }
    }

    return true;
}

void resetBoard(int puzzle[9][9], int board[9][9]) {
    copyBoard(puzzle, board);
}

void showTitle() {

    cout << "\n";
    cout << "=====================================\n";
    cout << "              SUDOKU\n";
    cout << "=====================================\n";
}

int chooseDifficulty() {

    int choice;

    while (true) {

        cout << "\nChoose Difficulty\n";
        cout << "-----------------\n";
        cout << "1. Easy\n";
        cout << "2. Medium\n";
        cout << "3. Hard\n";
        cout << "4. Exit\n";
        cout << "\nEnter choice: ";

        cin >> choice;

        if (cin.fail()) {

            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            cout << "\nInvalid input.\n";
            continue;
        }

        if (choice >= 1 && choice <= 4) {
            return choice;
        }

        cout << "\nPlease enter a number between 1 and 4.\n";
    }
}

int getCellsToRemove(int difficulty) {

    if (difficulty == 1) {
        return 35;
    }

    if (difficulty == 2) {
        return 45;
    }

    return 50;
}

void playGame(
    int puzzle[9][9],
    int solution[9][9],
    int board[9][9]
) {

    int mistakes = 0;
    int hints = 0;

    while (true) {

        showTitle();

        displayBoard(board);

        cout << "\nMistakes: " << mistakes;
        cout << "    Hints used: " << hints;

        cout << "\n\n";
        cout << "1. Enter Move\n";
        cout << "2. Hint\n";
        cout << "3. Restart\n";
        cout << "4. Show Solution\n";
        cout << "5. Quit to Main Menu\n";

        cout << "\nChoose option: ";

        int choice;
        cin >> choice;

        if (cin.fail()) {

            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');

            cout << "\nInvalid input.";
            continue;
        }

        if (choice == 1) {

            int row;
            int col;
            int num;

            cout << "\nEnter row (1-9): ";
            cin >> row;

            cout << "Enter column (1-9): ";
            cin >> col;

            cout << "Enter number (1-9): ";
            cin >> num;

            if (cin.fail()) {

                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');

                cout << "\nInvalid input.";
                continue;
            }

            if (row < 1 || row > 9 ||
                col < 1 || col > 9 ||
                num < 1 || num > 9) {

                cout << "\nInvalid row, column, or number.";
                continue;
            }

            row--;
            col--;

            if (puzzle[row][col] != 0) {

                cout << "\nThis is an original number and cannot be changed.";
                continue;
            }

            if (board[row][col] != 0) {

                cout << "\nThis cell is already filled.";
                continue;
            }

            if (solution[row][col] == num) {

                board[row][col] = num;

                cout << "\nCorrect!";

                if (isComplete(board)) {

                    showTitle();
                    displayBoard(board);

                    cout << "\n=====================================\n";
                    cout << "          SUDOKU COMPLETED!\n";
                    cout << "=====================================\n";

                    cout << "\nTotal mistakes: " << mistakes;
                    cout << "\nHints used: " << hints;
                    cout << "\n";

                    cout << "\nPress Enter to continue...";

                    cin.ignore(numeric_limits<streamsize>::max(), '\n');
                    cin.get();

                    return;
                }
            }
            else {

                mistakes++;

                cout << "\nWrong number!";
                cout << "\nMistakes: " << mistakes;
            }
        }

        else if (choice == 2) {

            bool hintAvailable = false;

            for (int i = 0; i < 9; i++) {

                for (int j = 0; j < 9; j++) {

                    if (board[i][j] == 0) {

                        board[i][j] = solution[i][j];

                        hints++;

                        cout << "\nHint added at row "
                             << i + 1
                             << ", column "
                             << j + 1
                             << ".";

                        hintAvailable = true;

                        break;
                    }
                }

                if (hintAvailable) {
                    break;
                }
            }

            if (!hintAvailable) {
                cout << "\nNo hints available.";
            }
        }

        else if (choice == 3) {

            resetBoard(puzzle, board);

            mistakes = 0;
            hints = 0;

            cout << "\nGame restarted.";
        }

        else if (choice == 4) {

            cout << "\nSolution:\n";

            displayBoard(solution);

            cout << "\nPress Enter to continue...";

            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cin.get();
        }

        else if (choice == 5) {

            cout << "\nReturning to main menu...\n";

            return;
        }

        else {

            cout << "\nInvalid option.";
        }

        cout << "\n";
    }
}

int main() {

    random_device rd;
    mt19937 rng(rd());

    while (true) {

        showTitle();

        int difficulty = chooseDifficulty();

        if (difficulty == 4) {

            cout << "\nThank you for playing Sudoku!\n";
            break;
        }

        int cellsToRemove = getCellsToRemove(difficulty);

        int solution[9][9] = {};

        cout << "\nGenerating Sudoku...\n";

        if (!solveSudoku(solution, rng)) {

            cout << "Could not generate Sudoku.\n";
            return 1;
        }

        int puzzle[9][9];

        generatePuzzle(
            solution,
            puzzle,
            cellsToRemove,
            rng
        );

        int board[9][9];

        copyBoard(puzzle, board);

        playGame(
            puzzle,
            solution,
            board
        );
    }

    return 0;
}
