# Initialize the board
board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]

# Define a function to display the board
def display_board():
    print(" {} | {} | {} ".format(board[0], board[1], board[2]))
    print("-----------")
    print(" {} | {} | {} ".format(board[3], board[4], board[5]))
    print("-----------")
    print(" {} | {} | {} ".format(board[6], board[7], board[8]))

# Define a function to check if the game is over
def is_game_over():
    # Check for a win
    if (board[0] == board[1] == board[2] != " " or
        board[3] == board[4] == board[5] != " " or
        board[6] == board[7] == board[8] != " " or
        board[0] == board[3] == board[6] != " " or
        board[1] == board[4] == board[7] != " " or
        board[2] == board[5] == board[8] != " " or
        board[0] == board[4] == board[8] != " " or
        board[2] == board[4] == board[6] != " "):
        return True
    # Check for a tie
    elif " " not in board:
        return True
    else:
        return False

# Define a function to play a turn
def play_turn(player):
    print("Player {}'s turn.".format(player))
    position = int(input("Enter a position (1-9): ")) 
    if board[position] == " ":
        board[position] = player
    else:
        print("That position is already taken. Try again.")
        play_turn(player)

# Play the game
player = "X"
while not is_game_over():
    display_board()
    play_turn(player)
    if player == "X":
        player = "O"
    else:
        player = "X"
display_board()
if " " not in board:
    print("Tie game.")
elif(player=="X"):
    print("Player O wins!")
else:
    print("Player X wins!")