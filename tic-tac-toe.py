from pprint import pprint
import random


class MoveError(Exception):
    pass


class TicTacToe:

    board = [
        ['-', '-', '-'],
        ['-', '-', '-'],
        ['-', '-', '-']
    ]

    wining_combinations = [
        [
            [True, True, True],
            [False, False, False],
            [False, False, False],
        ],
        [
            [False, False, False],
            [True, True, True],
            [False, False, False],
        ],
        [
            [False, False, False],
            [False, False, False],
            [True, True, True],
        ],

    ]

    USER_TOKEN = 'X'
    COMPUTER_TOKEN = 'O'

    def __init__(self):
        pass

    def print_board(self):
        for row in self.board:
            print("|".join(row))

    def user_move(self, row, col):

        if self.board[row][col] == '-':
            self.board[row][col] = self.USER_TOKEN
            return True
        else:
            print("The position is not empty")
            return False

    def is_full(self):
        for row in self.board:
            for col in row:
                if col == '-':
                    return False
        return True

    def computer_move(self):
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if self.board[row][col] != '-':
            raise MoveError('Illegal move')
        self.board[row][col] = self.COMPUTER_TOKEN


tic_tac_toe = TicTacToe()

while not tic_tac_toe.is_full():
    tic_tac_toe.print_board()
    row, col = raw_input("Enter: row col > ").strip().split()
    tic_tac_toe.user_move(int(row), int(col))
    while True:
        try:
            tic_tac_toe.computer_move()
            break
        except MoveError as e:
            print(str(e))
