import random

class Player(object):
    def __init__(self, side, board, name):
        self.side = side
        self.board = board
        self.name = name

    def validMove(self, move):
        if move in range(9) and self.board[move] == "~":
            return True
        else:
            return False

    def makeMove(self, move):
        if self.validMove(move):
            self.board[move] = self.side


class Computer(Player):
    def __init__(self, side, board, name):
        super().__init__(side, board, name)

    def findValidMove(self):
        empties = []
        for i in range(len(self.board)):
            if self.validMove(i):
                empties.append(i)
        return empties

    def chooseMove(self):
        boardCopy = self.board[:]
        validMoves = self.findValidMove()
        for m in validMoves:
            boardCopy[m] = self.side
            if win(self.side, boardCopy):
                return m
            else:
                boardCopy[m] = "~"

        opponentSide = "X" if self.side != "X" else "O"
        for m in validMoves:
            boardCopy[m] = opponentSide
            if win(opponentSide, boardCopy):
                return m
            else:
                boardCopy[m] = "~"

        if self.validMove(4):
            return 4

        move = random.choice([0,2,6,8])
        if self.validMove(move):
            return move

        move = random.choice([1,3,5,7])
        if self.validMove(move):
            return move


def boardFull(board):
    for x in board:
        if x == "~":
            return False
    return True


def win(side, board):
    return ((board[0] == side and board[3] == side and board[6] == side) # 1 column
         or (board[1] == side and board[4] == side and board[7] == side) # 2 column
         or (board[2] == side and board[5] == side and board[8] == side) # 3 column
         or (board[0] == side and board[1] == side and board[2] == side) # 1 row
         or (board[3] == side and board[4] == side and board[5] == side) # 2 row
         or (board[6] == side and board[7] == side and board[8] == side) # 3 row
         or (board[0] == side and board[4] == side and board[8] == side) # left cross
         or (board[2] == side and board[4] == side and board[6] == side)) # right cross

def gofirst():
    return random.choice(['X', 'O'])