import chess
import random
import numpy as np

class Move(object):
    def __init__(self, p, move, board, score=None):
        self.move = move
        self.p = p

        if self.move:
            board.push(self.move)

        if score:
            self.score = score
        else:
            self.score = p.board_score(board)

        if self.move:
            board.pop()

        self.score += np.random.normal(0, 0.01)
        # Depth of subtree
        self.depth = 0
        self.subtree = []

    def __str__(self):
        ret = "{}: {}, score {}\n".format(self.depth, self.move, self.score)
        for move in self.subtree:
            ret += str(move)
    
        return ret
    
    def print_greedy_line(self, board, mnum=1):
        print "Move {}: {} ({})".format(mnum, self.move, self.score)
        if self.move:
            board.push(self.move)

        best_score = -10000000000000
        mult = board.turn * 2 - 1
        for move in self.subtree:
            if move.score * mult > best_score:
                best_score = move.score * mult
                best_move = move
    
        if best_score > -10000000000:
            best_move.print_greedy_line(board, mnum=mnum+1)
    
        if self.move:
            board.pop()
    
    def prop(self, player=True):
        if self.depth == 0:
            return (self.score, None)
    
        if len(self.subtree) == 0:
            return (self.score, None)
    
        mult = player * 2 - 1
        best_score = -1000000000
        best_move = None
        for move in self.subtree:
            score, _ = move.prop(player=(player==False))
            if score * mult > best_score:
                best_score = score * mult
                best_move = move.move
    
        # Normal score -10000 <-> 10000
        # High alpha => more agressive?
        alpha = self.p.aggro / self.depth
        if player == self.p.color:
            self.score = alpha * self.score + (1-alpha) * best_score * mult
        else:
            self.score = best_score * mult
        return (self.score, best_move)
        #return (best_score * mult, best_move)
    
    def prune(self, player=True, keep=3):
        if self.depth == 0:
            return
    
        l = len(self.subtree)
        mvs = sorted([(m.score, m) for m in self.subtree])
    
        if player:
            self.subtree = [m for _, m in mvs[-keep:]]
        else:
            self.subtree = [m for _, m in mvs[:keep]]
    
        for m in self.subtree:
            m.prune(player=(player==False), keep=max(2, keep/2))
    
    
    # We have to go deeper!
    def deeper(self, board):
        # If this is the first move it is None
    
        if self.move:
            board.push(self.move)
    
        # At the lowest depth
        if self.depth == 0:
    
            mult = board.turn * 2 - 1
            if board.is_checkmate():
                self.subtree.append(Move(self.p, None, board, score=-mult *
                    100000))
            elif board.is_game_over():
                self.subtree.append(Move(self.p, None, board, score=0))
            else:
                for move in board.legal_moves:
                    self.subtree.append(Move(self.p, move, board))
    
        else:
            for move in self.subtree:
                move.deeper(board)
    
        if self.move:
            board.pop()
    
        self.depth += 1
    

class Player(object):
    def __init__(self, beta=0.01, pin=0.01, attack=0.1, aggro=0.5):
        self.debug = False
        self.beta = beta
        self.attack_par = attack
        self.aggro = aggro
        self.piece_move_par = 0.005

        self.board_preference = np.array([
            [1,-1,-1, 1, 1,-1,-1, 1], #1
            [0, 0, 0, 1, 1, 0, 0, 0], #2
            [0, 1, 3, 2, 2, 3, 1, 0], #3
            [0, 1, 2, 3, 3, 2, 1, 0], #4
            [0, 1, 2, 3, 3, 2, 1, 0], #5
            [0, 1, 3, 2, 2, 3, 1, 0], #6
            [0, 0, 0, 1, 1, 0, 0, 0], #7
            [1,-1,-1, 1, 1,-1,-1, 1]  #8
            ]).flatten()
        #    A  B  C  D  E  F  G  H

        self.piece_types = [chess.PAWN, chess.KNIGHT, chess.BISHOP,
                chess.ROOK, chess.QUEEN, chess.KING]
    
        self.piece_score = { chess.PAWN: 1, chess.KNIGHT: 3,
                chess.BISHOP: 4, chess.ROOK: 5, chess.QUEEN: 12 }

        self.piece_move_score = { chess.PAWN: 1, chess.KNIGHT: 0.5,
                chess.BISHOP: 0.5, chess.ROOK: 0, chess.QUEEN: 0,
                chess.KING: 0 }
        
    def __str__(self):
        return "splort"
    
    def material_score(self, b, beta=0.01):
        score = 0
        for t, squares in [(t, b.pieces(t, True)) for t in self.piece_types]:
            if t == chess.KING:
                continue
            for sq in squares:
                score += self.piece_score[t]
                if b.fullmove_number < 30:
                    score += self.beta * self.board_preference[sq]
        for t, squares in [(t, b.pieces(t, False)) for t in self.piece_types]:
            if t == chess.KING:
                continue
            for sq in squares:
                score -= self.piece_score[t]
                if b.fullmove_number < 30:
                    score -= self.beta * self.board_preference[sq]
        return score
    
    def attack_score(self, b):
        att = 0
        for sq in xrange(64):
            if b.is_attacked_by(True, sq):
                att += self.board_preference[sq]
            if b.is_attacked_by(False, sq):
                att -= self.board_preference[sq]
        return att
    
    def board_score(self, b):
        mat = self.material_score(b, self.beta)
        attack = self.attack_score(b)
        if b.fullmove_number > 1:
            piece = b.piece_at(b.peek().to_square)
            if piece:
                pscore = self.piece_move_score[piece.piece_type]
            else:
                pscore = 0
        else:
            pscore = 0
    
        return mat \
                + self.attack_par * attack \
                + self.piece_move_par * pscore \
                * np.sqrt(b.fullmove_number) \
                + (b.turn * 2 - 1) * (len(b.legal_moves) < 3)

    
    def best_move(self, board):
        self.color = board.turn
    
        move = Move(self, None, board)
    
        move.deeper(board)
        move.deeper(board)
        move.prop(player=board.turn)
        move.prune(board.turn, keep=8)
    
        move.deeper(board)
        move.prop(player=board.turn)
        move.prune(board.turn, keep=2)
    
        if board.fullmove_number > 50:
            move.deeper(board)
            move.deeper(board)
            move.prop(player=board.turn)
            move.prune(board.turn, keep=2)
    
        move.deeper(board)
    
        bscore, bmove = move.prop(player=board.turn)
        #print "SPLORT BEST move {}, score {}".format(bmove, bscore)
        #move.print_greedy_line(board)
    
        return bscore, bmove
    
    def get_move(self, board):
    
        score, move = self.best_move(board)
    
        return move, score

def get_move(board):
    playa = Player(beta=0.00101, pin=0.001, attack=0.2, aggro=0.3)

    move, score = playa.get_move(board)
    return move
    
