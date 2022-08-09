

import random


board = [[" " for _ in range(9)] for _ in range(9)]
possible_board = [[["1", "2", "3", "4", "5", "6", "7", "8", "9"] for _ in range(9)] for _ in range(9)]

def print_board(board):
    for line in board:
        print(line)

#print_board(board)

def is_legal(to_check: list):
    to_check = [val for val in to_check if val != ' ']
    return len(to_check) == len(set(to_check))

def is_board_legal(board):
    for i in range(9):
        # Lines
        if not is_legal(board[i]):
            return False
        # Cols
        elif not is_legal([board[j][i] for j in range(9)]):
            return False
        # Cells
        j = i % 3 * 3
        i //= 3
        cell = [
            board[i][j], board[i][j+1], board[i][j+2],
            board[i+1][j], board[i+1][j+1], board[i+1][j+2],
            board[i+2][j], board[i+2][j+1], board[i+2][j+2]
        ]
        if not is_legal(cell):
            return False
    return True

def cells_with_no_choice(board):
    for line in possible_board:
        for possible in possible_board:
            if len(possible) == 0:
                return True
    return False


def update_cell_possibilities(modified_cell):
    pass

'''
board = [
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " ", " ", " "],
    
]
'''

while True:
    best_len = 10
    best = []
    for l, line in enumerate(board):
        for c, cell in enumerate(line):
            if len(possible_board[l][c]) < best_len:
                best_len = len(possible_board[l][c])
                best = [[l, c]]
            elif len(possible_board[l][c]) == best_len:
                best.append([l, c])
    
    chosen = random.choice(best)
    board[chosen[0]][chosen[1]] = random.choice(possible_board[chosen[0]][chosen[1]])
