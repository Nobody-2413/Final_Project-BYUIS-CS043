from gameFunctions import *

def declareWinner(result):
    if result == "player":
        return "Congrudaltions! You won the game!"
    elif result == "computer":
        return "The computer won the game! Try harder next time!"
    elif result == "tie":
        return "Tied Game!"

def printBoard(board):
    print(board[0] + "|" + board[1] + "|" + board[2])
    print("-----")
    print(board[3] + "|" + board[4] + "|" + board[5])
    print("-----")
    print(board[6] + "|" + board[7] + "|" + board[8])

def sideInput():
    side = ""
    while not side in ["X", "O"]:
        side = input("Which side do you want to be (X or O): ").upper()
        if side == "Q":
            return "quit"
    side2 = "X" if side == "O" else "O"
    return (side, side2)

def playerMoveInput(board):
    while True:
        move = input("Enter Move (1 to 9): ").lower()
        if move.isdigit():
            if (int(move)-1 in range(9) and board[int(move)-1] == " "):
                return int(move) - 1
        elif move == "q":
            return "quit"
        print("Please enter valid move!")

def goFirst():
    turn = random.choice(["player", "computer"])
    if turn == "player":
        return (turn, "You will go first!")
    else:
        return (turn, "The computer will go first")
# board = ["X", "O", "X",
#          "", "", "O",
#          "O", "O", "X"]
# player = Player("X", board)
# computer = Computer("O", board)
# print(computer.chooseMove())
# printBoard(board)

def playGame(playerSide, computerSide):
    board = [" " for x in range(9)]
    player = Player(playerSide, board)
    computer = Computer(computerSide, board)
    turn, message = goFirst()
    print(message)
    printBoard(board)

    while not boardFull(board):
        if turn == "player":
            move = playerMoveInput(board)
            if move == "quit":
                return move
            player.makeMove(move)
            print("----------------")
            print()
            if win(playerSide, board):
                printBoard(board)
                return "player"
            turn = "computer"

        elif turn == "computer":
            move = computer.chooseMove();
            computer.makeMove(move)
            print("----------------")
            print()
            if win(computerSide, board):
                printBoard(board)
                return "computer"
            turn = "player"
        printBoard(board)
    return "tie"

print("WELCOME TO TIC-TAC-TOE")
print()
print()
print()
done = False
while not done:
    sides = sideInput()
    if sides == "quit":
        done = True
    else:
        playerSide, computerSide = sides
        result = playGame(playerSide, computerSide)
        if result == "quit":
            done = True
        else:
            print(declareWinner(result))
    print()
    print()
    print()
    again = input("Play Again (y/n): ").lower()
    if again == "n":
        done = True
print("Goodbye, I hope you have a great day!")