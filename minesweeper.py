import random


ROWS = 5
COLS = 5
MINES = 5


def create_board():
    board = []

    for i in range(ROWS):
        row = []

        for j in range(COLS):
            row.append(0)

        board.append(row)

    return board


def place_mines(board):

    count = 0

    while count < MINES:

        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)

        if board[row][col] != -1:

            board[row][col] = -1
            count += 1


def count_mines(board):

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == -1:
                continue

            mines = 0

            for i in range(row - 1, row + 2):
                for j in range(col - 1, col + 2):

                    if i >= 0 and i < ROWS:
                        if j >= 0 and j < COLS:

                            if board[i][j] == -1:
                                mines += 1

            board[row][col] = mines


def display_board(board, visible):

    print()

    print("   ", end="")

    for col in range(COLS):
        print(col + 1, end=" ")

    print()

    for row in range(ROWS):

        print(row + 1, end="  ")

        for col in range(COLS):

            if visible[row][col]:

                if board[row][col] == -1:
                    print("*", end=" ")

                else:
                    print(board[row][col], end=" ")

            else:
                print("#", end=" ")

        print()

    print()


def reveal(board, visible, row, col):

    visible[row][col] = True

    if board[row][col] != 0:
        return

    for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):

            if i >= 0 and i < ROWS:
                if j >= 0 and j < COLS:

                    if not visible[i][j]:
                        reveal(board, visible, i, j)


def check_win(board, visible):

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] != -1:
                if not visible[row][col]:
                    return False

    return True


board = create_board()

visible = []

for i in range(ROWS):

    row = []

    for j in range(COLS):
        row.append(False)

    visible.append(row)


place_mines(board)

count_mines(board)


print("===== MINESWEEPER =====")
print("Find all the safe cells!")
print("There are", MINES, "mines.")
print()

while True:

    display_board(board, visible)

    print("Enter -1 to quit.")

    row = int(input("Enter row (1-5): "))

    if row == -1:
        print("Game ended.")
        break

    col = int(input("Enter column (1-5): "))

    if row < 1 or row > ROWS:
        print("Invalid row.")
        continue

    if col < 1 or col > COLS:
        print("Invalid column.")
        continue

    row = row - 1
    col = col - 1

    if visible[row][col]:
        print("You already opened this cell.")
        continue

    if board[row][col] == -1:

        visible[row][col] = True

        print()
        print("BOOM!")
        print("You hit a mine!")
        print()

        for i in range(ROWS):
            for j in range(COLS):
                visible[i][j] = True

        display_board(board, visible)

        print("Game Over!")
        break

    else:

        reveal(board, visible, row, col)

        if check_win(board, visible):

            print()
            display_board(board, visible)

            print("Congratulations!")
            print("You found all the safe cells!")
            break
