board = [
    " ", " ", " ",
    " ", " ", " ",
    " ", " ", " "
]


def display_board():

    print()
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---+---+---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---+---+---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()


def check_winner(player):

    if board[0] == player and board[1] == player and board[2] == player:
        return True

    if board[3] == player and board[4] == player and board[5] == player:
        return True

    if board[6] == player and board[7] == player and board[8] == player:
        return True

    if board[0] == player and board[3] == player and board[6] == player:
        return True

    if board[1] == player and board[4] == player and board[7] == player:
        return True

    if board[2] == player and board[5] == player and board[8] == player:
        return True

    if board[0] == player and board[4] == player and board[8] == player:
        return True

    if board[2] == player and board[4] == player and board[6] == player:
        return True

    return False


def board_full():

    for position in board:
        if position == " ":
            return False

    return True


print("===== TIC TAC TOE =====")
print("Player 1: X")
print("Player 2: O")

current_player = "X"

while True:

    display_board()

    print("Player", current_player)

    position = int(input("Choose a position (1-9): "))

    if position < 1 or position > 9:
        print("Please choose a number between 1 and 9.")
        continue

    position = position - 1

    if board[position] != " ":
        print("That position is already taken.")
        continue

    board[position] = current_player

    if check_winner(current_player):

        display_board()

        print("Player", current_player, "wins!")
        break

    if board_full():

        display_board()

        print("It's a draw!")
        break

    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"
