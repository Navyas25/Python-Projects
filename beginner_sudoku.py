board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]


def display_board():

    print()

    for i in range(9):

        for j in range(9):

            if board[i][j] == 0:
                print(".", end=" ")
            else:
                print(board[i][j], end=" ")

            if j == 2 or j == 5:
                print("|", end=" ")

        print()

        if i == 2 or i == 5:
            print("---------------------")

    print()


def check_row(row, number):

    for i in range(9):
        if board[row][i] == number:
            return False

    return True


def check_column(column, number):

    for i in range(9):
        if board[i][column] == number:
            return False

    return True


def check_box(row, column, number):

    start_row = row - row % 3
    start_column = column - column % 3

    for i in range(3):
        for j in range(3):

            if board[start_row + i][start_column + j] == number:
                return False

    return True


def is_valid(row, column, number):

    if check_row(row, number) == False:
        return False

    if check_column(column, number) == False:
        return False

    if check_box(row, column, number) == False:
        return False

    return True


def game_complete():

    for i in range(9):
        for j in range(9):

            if board[i][j] == 0:
                return False

    return True


print("===== SUDOKU GAME =====")

while True:

    display_board()

    if game_complete():
        print("Congratulations!")
        print("You completed the Sudoku!")
        break

    print("Enter -1 to quit")

    row = int(input("Enter row (1-9): "))

    if row == -1:
        print("Game ended.")
        break

    column = int(input("Enter column (1-9): "))
    number = int(input("Enter number (1-9): "))

    row = row - 1
    column = column - 1

    if row < 0 or row > 8:
        print("Invalid row.")
        continue

    if column < 0 or column > 8:
        print("Invalid column.")
        continue

    if number < 1 or number > 9:
        print("Number must be between 1 and 9.")
        continue

    if board[row][column] != 0:
        print("That cell is already filled.")
        continue

    if is_valid(row, column, number):

        board[row][column] = number

        print("Correct move!")

    else:

        print("Invalid move!")
