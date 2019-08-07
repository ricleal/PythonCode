from pprint import pprint
import random


class TicTacToe:
    board = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]

    def __init__(self):
        pass

    def print_board(self):
        for row in self.board:
            print("|".join(row))

    def add_token(self, token, row, col):
        if token.capitalize() == 'X' or token.capitalize() == 'O':
            if self.board[row][col] == '-':
                self.board[row][col] = token
            else:
                print("The position is not empty")
        else:
            print("Use X or O")

    def is_full(self):
        for row in self.board:
            for col in row:
                if col == '-':
                    return False
        return True

    def ai_move(self):
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if self.board[row][col] != '-':
            raise Exception('Illegal move')
        self.add_token('O', row, col)


tic_tac_toe = TicTacToe()
tic_tac_toe.add_token('X', 0, 1)
tic_tac_toe.print_board()

print("Is the board full?", tic_tac_toe.is_full())
while not tic_tac_toe.is_full():
    try:
        tic_tac_toe.ai_move()
    except Exception as e:
        print(str(e))

print("Is the board full?", tic_tac_toe.is_full())
print(tic_tac_toe.is_full())
tic_tac_toe.print_board()
