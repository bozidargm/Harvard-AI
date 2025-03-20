"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # At the start of game X plays first
    if board == initial_state():
        return X
    # If the game is over
    elif board == terminal(board):
        return "The game is already over"

    # Next turn is calculated by comparing total nuber of X and O moves
    str_board = str(board)                
    if str_board.count(X) == str_board.count(O):
        return X
    elif str_board.count(X) > str_board.count(O):
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """

    moves = set()

    for row in range(3):       
        for col in range(3):
            if board[row][col] == EMPTY:
                moves.add((row, col))
    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    if action not in actions(board):
        raise Exception("Not valid move")

    result_board = [board[i].copy() for i in range(len(board))]
    result_board[action[0]][action[1]] = player(board)
    return result_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Determining the winning combination
    a = [board[0][0], board[0][1], board[0][2]]
    b = [board[1][0], board[1][1], board[1][2]]
    c = [board[2][0], board[2][1], board[2][2]]
    d = [board[0][0], board[1][0], board[2][0]]
    e = [board[0][1], board[1][1], board[2][1]]
    f = [board[0][2], board[1][2], board[2][2]]
    g = [board[0][0], board[1][1], board[2][2]]
    h = [board[0][2], board[1][1], board[2][0]]
    me = [X, X, X]
    ai = [O, O, O]
    win_me = False
    win_ai = False

    # Checking if there is a winning combination
    if a == me or b == me or c == me or d == me or e == me or f == me or g == me or h == me:
        win_me = True
    if a == ai or b == ai or c == ai or d == ai or e == ai or f == ai or g == ai or h == ai:
        win_ai = True
    
    if win_me == True:
        return X
    elif win_ai == True:
        return O
    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) == X or winner(board) == O:
        return True
    
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    """
    Returns the maximum value possible for the given board.
    """

    if terminal(board):
        return utility(board)
    v = -math.inf
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
        # Stops searching if finds the absolute maximum for this game
        if v == 1:
            break
    return v


def min_value(board):
    """
    Returns the minimum value possible for the given board.
    """

    if terminal(board):
        return utility(board)
    v = math.inf
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
        # Stops searching if finds the absolute minimum for this game
        if v == -1:
            break
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None

    # Best move for X player
    elif player(board) == X:  
        moves = []
        for action in actions(board):
            moves.append([min_value(result(board, action)), action])
        return sorted(moves, key=lambda a: a[0])[-1][1]

    # Best move for O player
    elif player(board) == O:   
        moves = []
        for action in actions(board):
            moves.append([max_value(result(board, action)), action])
        return sorted(moves, key=lambda a: a[0])[0][1]

