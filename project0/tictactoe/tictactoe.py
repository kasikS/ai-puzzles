"""
Tic Tac Toe Player
"""

import math
import collections
import  copy
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
    flattened_board = [item for sublist in board for item in sublist]
    counter = collections.Counter(flattened_board)
    x_counts = counter[X]
    o_counts = counter[O]
    if x_counts == o_counts:
        return X
    else:
        return O


test_board = [[X,EMPTY, X], [X,O, X], [EMPTY,O,EMPTY]]

print(player([[X,O], [EMPTY,EMPTY], [EMPTY,EMPTY]]))


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions=set()
    for row in range(len(board)):
        for column in range(len(board[row])):
            if board[row][column] == EMPTY:
                possible_actions.add((row, column))
    return possible_actions

print(actions([[X,O], [X,X], [O,O]]))

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("action cell already taken!")
    copied_board = copy.deepcopy(board)
    copied_board[action[0]][action[1]] = player(copied_board)

    return copied_board


#print(result(test_board,(0,0) ))


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    assert(len(board) == len(board[0]))
    board_size = len(board)

    for row in range(board_size):
        if all([(cell == X) for cell in board[row]]):
            return board[row][0]

        if all([(cell == O) for cell in board[row]]):
            return board[row][0]

    # for column in range(len(board[0])):
    #     value = board[0][column]
    #     all_rows = True
    #     for row in range(len(board)):
    #         if value != board[row][column]:
    #             all_rows=False
    #     if all_rows:
    #         return board[0][column]

    for column in range(board_size):
        if board[0][column] != EMPTY:
            if all([board[row][column] == board[0][column] for row in range(board_size)]):
                return board[0][column]

    value = board[0][0]
    for index in range(board_size):
        if value != board[index][index]:
            value = EMPTY
            break
    if value != EMPTY:
        return value

    value = board[board_size-1][0]
    for index in range(board_size):
        if value != board[board_size - 1 - index][index]:
            value = EMPTY
            break
    if value != EMPTY:
        return value
    return None


winner_row_x = [[X,EMPTY, X], [X,X, X], [EMPTY,O,EMPTY]]
winner_col_o = [[X,EMPTY, O], [X,X, O], [EMPTY,O,O]]
no_winner = [[X,EMPTY, O], [X,X, O], [EMPTY,EMPTY,EMPTY]]
winner_diag_down = [[X,EMPTY, O], [X,X, O], [EMPTY,EMPTY,X]]
winner_diag_up = [[X,EMPTY, O], [X,O, O], [O,EMPTY,EMPTY]]
no_winner_term = [[X,O, X], [X,X, O], [O,X,O]]

assert(winner(winner_row_x) == X)
assert(winner(winner_col_o) == O)
assert(winner(no_winner) == None)
assert(winner(winner_diag_up) == O)
assert (winner(winner_diag_down) == X)

#print(winner(test_board))


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True

    for row in board:
        if any([(cell == EMPTY) for cell in row]):
            return False
    return True


assert(terminal(winner_col_o) == True)
assert(terminal(no_winner) == False)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    val = winner(board)
    if val == X:
        return 1
    if val == O:
        return -1

    return 0


assert(utility(winner_row_x) == 1)
assert(utility(winner_col_o) == -1)
assert(utility(no_winner_term) == 0)


def evaluate(board):
    current_player = player(board)


    for action in actions(board):
        modified_board = result(board, action)
        if terminal(modified_board):
            current_utility = utility(modified_board)
            if (current_player == X) and current_utility > 0:
                return current_utility

            if (current_player == O) and current_utility < 0:
                return current_utility
        else:
            return evaluate(modified_board)
    return 0



def min_value(board):
    if terminal(board):
        return utility(board)
    val = 1000
    for action in actions(board):
        modified_board = result(board, action)
        val = min(max_value(modified_board), val)
    return val


def max_value(board):
    if terminal(board):
        return utility(board)
    val = -1000
    for action in actions(board):
        modified_board = result(board, action)
        val = max(min_value(modified_board), val)
    return val


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    current_player = player(board)
    best_utility = 0
    best_action = None

    for action in actions(board):
        modified_board = result(board, action)
        if current_player == X:
            current_utility = max_value(modified_board)
            if current_utility >= best_utility:
                best_utility = current_utility
                best_action = action

        if current_player == O:
            current_utility = min_value(modified_board)
            if current_utility <= best_utility:
                best_utility = current_utility
                best_action = action

    return best_action
