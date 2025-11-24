import copy
import math
import random
import numpy
X = "X";
O = "O";
EMPTY = None
user = None
ai = None
def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],]
def player(board):
    count = 0
    for i in board:
        for j in i:
            if j:
                count += 1
    if count % 2 != 0:
        return ai
    return user

def actions(board):
    res = set()
    board_len = len(board)
    for i in range(board_len):
        for j in range(board_len):
            if board[i][j] == EMPTY:
                res.add((i, j))
    return res

def result(board, action):
    curr_player = player(board)
    result_board = copy.deepcopy(board)
    (i, j) = action
    result_board[i][j] = curr_player
    return result_board

def get_horizontal_winner(board):
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        winner_val = board[i][0]
        for j in range(board_len):
            if board[i][j] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_vertical_winner(board):
    winner_val = None
    board_len = len(board)
    for i in range(board_len):
        winner_val = board[0][i]
        for j in range(board_len):
            if board[j][i] != winner_val:
                winner_val = None
        if winner_val:
            return winner_val
    return winner_val

def get_diagonal_winner(board):
    winner_val = None
    board_len = len(board)
    winner_val = board[0][0]
    for i in range(board_len):
        if board[i][i] != winner_val:
            winner_val = None
    if winner_val:
        return winner_val
    winner_val = board[0][board_len - 1]
    for i in range(board_len):
        j = board_len - 1 - i
        if board[i][j] != winner_val:
            winner_val = None
    return winner_val

def winner(board):
    winner_val = get_horizontal_winner(board) or get_vertical_winner(board) or get_diagonal_winner(board) or None
    return winner_val

def terminal(board):
    if winner(board) != None:
        return True
    for i in board:
        for j in i:
            if j == EMPTY:
                return False
    return True

def utility(board):
    winner_val = winner(board)
    if winner_val == X:
        return 1
    elif winner_val == O:
        return -1
    return 0

def maxValue(state):
    if terminal(state):
        return utility(state)
    v = -math.inf
    for action in actions(state):
        v = max(v, minValue(result(state, action)))
    return v

def minValue(state):
    if terminal(state):
        return utility(state)
    v = math.inf
    for action in actions(state):
        v = min(v, maxValue(result(state, action)))
    return v

def minimax(board):
    current_player = player(board)
    if current_player == X:
        min = -math.inf
        for action in actions(board):
            check = minValue(result(board, action)) # FIXED
            if check > min:
                min = check
                move = action
    else:
        max = math.inf
        for action in actions(board):
            check = maxValue(result(board, action)) # FIXED
            if check < max:
                max = check
                move = action
    return move

if __name__ == "__main__":
    board = initial_state()
    ai_turn = False
    print("Choose a player")
    user = input()
    if user == "X":
        ai = "O"
    else:
        ai = "X" ;
    while True:
        game_over = terminal(board)
        playr = player(board)
        if game_over:
            winner = winner(board)
            if winner is None:
                print("Game Over: Tie.")
            else:
                print("Game Over: {winner} wins.")
            break;
        else:
            if user != playr and not game_over:
                if ai_turn:
                    move = minimax(board)
                    board = result(board, move)
                    ai_turn = False
                    print(numpy.array(board))
            elif user == playr and not game_over:
                ai_turn = True
                print("Enter the position to move (row,col)")
                i = int(input("Row:"))
                j = int(input("Col:"))
                if board[i][j] == EMPTY:
                    board = result(board, (i, j))
                    print(numpy.array(board))
