from collections import Counter
import numpy as np

NUM_COLUMNS = 7
COLUMN_HEIGHT = 6
FOUR = 4

# Board can be initiatilized with `board = np.zeros((NUM_COLUMNS, COLUMN_HEIGHT), dtype=np.byte)`
# Notez Bien: Connect 4 "columns" are actually NumPy "rows"
def valid_moves(board):
    """Returns columns where a disc may be played"""
    return [n for n in range(NUM_COLUMNS) if board[n, COLUMN_HEIGHT - 1] == 0]


def play(board, column, player):
    """Updates `board` as `player` drops a disc in `column`"""
    (index,) = next((i for i, v in np.ndenumerate(board[column]) if v == 0))
    board[column, index] = player

def take_back(board, column):
    """Updates `board` removing top disc from `column`"""
    (index,) = [i for i, v in np.ndenumerate(board[column]) if v != 0][-1]
    board[column, index] = 0


def four_in_a_row(board, player):
    """Checks if `player` has a 4-piece line"""
    return (
        any(
            all(board[c, r] == player)
            for c in range(NUM_COLUMNS)
            for r in (list(range(n, n + FOUR)) for n in range(COLUMN_HEIGHT - FOUR + 1))
        )
        or any(
            all(board[c, r] == player)
            for r in range(COLUMN_HEIGHT)
            for c in (list(range(n, n + FOUR)) for n in range(NUM_COLUMNS - FOUR + 1))
        )
        or any(
            np.all(board[diag] == player)
            for diag in (
                (range(ro, ro + FOUR), range(co, co + FOUR))
                for ro in range(0, NUM_COLUMNS - FOUR + 1)
                for co in range(0, COLUMN_HEIGHT - FOUR + 1)
            )
        )
        or any(
            np.all(board[diag] == player)
            for diag in (
                (range(ro, ro + FOUR), range(co + FOUR - 1, co - 1, -1))
                for ro in range(0, NUM_COLUMNS - FOUR + 1)
                for co in range(0, COLUMN_HEIGHT - FOUR + 1)
            )
        )
    )

def minmax(board, depth, player):
    print ("JUGA EL PLAYER", player)
    possible = list(valid_moves(board))
    print("movs possibles: ", possible)
    terminal = eval_terminal(board)
    print("es terminal?", terminal)

    if depth == 0 or terminal:
        if four_in_a_row(board, 1):
            print("N 1 wins")
            return (None, 1)
        elif four_in_a_row(board, -1):
            print("N -1 wins")
            return (None, -1)
        else: 
            print("N 0 wins")
            return (None, 0)

    value = -player

    for ply in possible:
        try:
            board_copy = np.copy(board)
            play(board_copy, ply, player)
            print("jugada feta: ")
            print (board_copy)
            
            _, score = minmax(board_copy, depth-1, -player)
            print ("la puntuacio es: ", score)
            
            if player == 1 and score > value:
                value = score
                column = ply
            elif player == -1 and score < value:
                value = score
                column = ply
            if eval_terminal(board_copy):
                break
        except: 
            print("Aixo es un no possible")
            print(board)                    
    return column, value

def eval_terminal(board):
    return four_in_a_row(board, 1) or four_in_a_row(board, -1) or len(valid_moves(board))==0

def _mc(board, player):
    p = -player
    while valid_moves(board):
        p = -p
        c = np.random.choice(valid_moves(board))
        play(board, c, p)
        if four_in_a_row(board, p):
            return p
    return 0


def montecarlo(board, player):
    montecarlo_samples = 100
    cnt = Counter(_mc(np.copy(board), player) for _ in range(montecarlo_samples))
    return (cnt[1] - cnt[-1]) / montecarlo_samples


def eval_board(board, player):
    if four_in_a_row(board, 1):
        # Alice won
        return 1
    elif four_in_a_row(board, -1):
        # Bob won
        return -1
    else:
        # Not terminal, let's simulate...
        return montecarlo(board, player)

board = board = np.zeros((NUM_COLUMNS, COLUMN_HEIGHT), dtype=np.byte)
play(board, 0,-1)
play(board, 3, 1)
play(board, 0,-1)

print(board)
evaluations, val=minmax(board, 5, 1)
monc = montecarlo(board, 1)
print ("evaluations: ", evaluations)
print ("val: ", val)
print ("montecarlo: ", monc)
