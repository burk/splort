import chess
import random
import numpy as np

debug = False

board_preference = np.array([
    [1, 1, 2, 2, 2, 2, 1, 1], #1
    [1, 2, 2, 2, 2, 2, 2, 1], #2
    [1, 2, 3, 3, 3, 3, 2, 1], #3
    [1, 2, 3, 4, 4, 3, 2, 1], #4
    [1, 2, 3, 4, 4, 3, 2, 1], #5
    [1, 2, 3, 3, 3, 3, 2, 1], #6
    [1, 2, 2, 2, 2, 2, 2, 1], #7
    [1, 1, 2, 2, 2, 2, 1, 1]  #8
    ]).flatten()
#    A  B  C  D  E  F  G  H

class Move(object):
    def __init__(self, move, board, score=None):
        self.move = move

        if self.move:
            board.push(self.move)

        if score:
            self.score = score
        else:
            self.score = board_score(board)

        if self.move:
            board.pop()

        self.score += np.random.normal(0, max(self.score/10.0, 0.001))
        # Depth of subtree
        self.depth = 0
        self.subtree = []

    def __str__(self):
        ret = "{}: {}, score {}\n".format(self.depth, self.move, self.score)
        for move in self.subtree:
            ret += str(move)

        return ret

    def print_greedy_line(self, board, move=1):
        print "Move {}: {}".format(move, self.move)
        if self.move:
            board.push(self.move)
        print board
        best_score = None
        for move in self.subtree:
            if move.score > best_score:
                best_score = move.score
                best_move = move

        if best_score:
            best_move.print_greedy_line(board, move=2)

        if self.move:
            board.pop()

    def best(self, player=True):
        if self.depth == 0:
            return (self.score, None)

        mult = player * 2 - 1
        best_score = -100000
        best_move = None
        for move in self.subtree:
            score, _ = move.best(player=(player == False))
            if score * mult > best_score:
                best_score = score * mult
                best_move = move.move

        return (best_score * mult, best_move)


    # We have to go deeper!
    def deeper(self, board):
        # If this is the first move it is None

        if self.move:
            if debug:
                print "Pushing {}".format(self.move)
            board.push(self.move)

        if debug:
            print "deeper called at depth {}".format(self.depth)
            print "self.move is {}".format(self.move)
            print "subtree is {}".format(self.subtree)

        # At the lowest depth
        if self.depth == 0:

            if debug:
                print "OK, at lowest depth"
                print "Board is now:"
                print board

            mult = board.turn * 2 - 1
            if len(board.legal_moves) == 0:
                print "LELELLE"
                self.subtree.append(Move(None, board, score=-mult *
                    100000))
            for move in board.legal_moves:
                self.subtree.append(Move(move, board))

            if debug:
                print "Appended {} things".format(len(self.subtree))

            self.depth += 1

        else:
            for move in self.subtree:
                if debug:
                    print "We have to go deeper, board is"
                    print board
                move.deeper(board)
                if debug:
                    print "We came out of it"

        if debug:
            print "Getting out of deeper, board is:"
            print board
        if self.move:
            board.pop()
        if debug:
            print "POPPED"

        self.depth += 1

piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK,
        chess.QUEEN, chess.KING]

piece_score = { chess.PAWN: 1, chess.KNIGHT: 3, chess.BISHOP: 3,
        chess.ROOK: 5, chess.QUEEN: 9 }
    
def material_score(b):
    score = 0
    for t, squares in [(t, b.pieces(t, True)) for t in piece_types]:
        if t == chess.KING:
            continue
        for sq in squares:
            score += piece_score[t]
    for t, squares in [(t, b.pieces(t, False)) for t in piece_types]:
        if t == chess.KING:
            continue
        for sq in squares:
            score -= piece_score[t]
    return score

def position_score(b, other=False):
    score = 0
    if other:
        who = not b.turn
    else:
        who = b.turn
    for t, squares in [(t, b.pieces(t, who)) for t in piece_types]:
        if t == chess.KING:
            continue

        for sq in squares:
            score += board_preference[sq]
    return score

def board_score(board):
    mat_score = material_score(board)
    pos_score = position_score(board) - position_score(board,
            other=True)

    return mat_score #- 0.1 * pos_score

def best_move(board, depth=1):

    move = Move(None, board)
    move.deeper(board)
    move.deeper(board)

    bscore, bmove = move.best(player=board.turn)
    print "BEST move {}, score {}".format(bmove, bscore)

    #moves = sorted([(m.score, m.move) for m in move.subtree])

    #print moves
    #print "Best move {}".format(moves[-1][1])
    return bscore, bmove

def get_move(board):

    score, move = best_move(board)

    return move

