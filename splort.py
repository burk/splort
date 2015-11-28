import chess
import random
import numpy as np

board_preference = np.array([
    [1, 1, 2, 2, 2, 2, 1, 1], #8
    [1, 2, 2, 2, 2, 2, 2, 1], #7
    [1, 2, 3, 3, 3, 3, 2, 1], #6
    [1, 2, 3, 4, 4, 3, 2, 1], #5
    [1, 2, 3, 4, 4, 3, 2, 1], #4
    [1, 2, 3, 3, 3, 3, 2, 1], #3
    [1, 2, 2, 2, 2, 2, 2, 1], #2
    [1, 1, 2, 2, 2, 2, 1, 1]  #1
    ])
#    A  B  C  D  E  F  G  H

class Move(object):
    def __init__(self, move, board):
        self.move = move
        self.score = move_score(move, board)
        # Depth of subtree
        self.depth = 0
        self.subtree = []

def move_to_index(move):
    f, s = str(move)[2:4]

    ret = (int(s) - 1, ord(f) - ord('a'))
    return ret
    
def move_score(move, board):
    return board_preference[move_to_index(move)]

def best_move(board, depth=1):

    if depth == 0:
        return 0

    move_scores = []
    for move in board.legal_moves:
        print "Evaluating move {}".format(move)
        score = move_score(move, board)
        score += np.random.normal(0, score/10.0)
        move_scores.append((score, move))

    move_scores.sort()
    print "Sorted."

    print "Best move {}".format(move_scores[-1][1])
    return move_scores[-1]

def get_move(board):

    score, move = best_move(board)

    return move

