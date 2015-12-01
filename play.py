import chess
import splort
import splold
import splold2
import random_player
import matplotlib.pyplot as plt
import numpy as np
import mr_final

def play(stats):

    board = chess.Board()

    #bparms = [np.random.normal(0.01, 0.01), np.random.normal(0.01,
    #    0.01), np.random.normal(0.3, 0.1), np.random.normal(0.8, 0.2)]
    wparms = [np.random.normal(0.001, 0.001), np.random.normal(0.001,
        0.001), np.random.normal(0.2, 0.01), np.random.normal(0.3, 0.1)]
    #black = splort.Player(beta=bparms[0], pin=bparms[1],
    #        attack=bparms[2], aggro=bparms[3])
    white = splort.Player(beta=wparms[0], pin=wparms[1],
            attack=wparms[2], aggro=wparms[3])
    black = mr_final
    #white = splold2

    black_score = []
    white_score = []

    num = 1
    while True:

        if num % 2 == 1:
            move, score = white.get_move(board)
            board.push(move)
            white_score.append(score)
        else:
            move = black.move(board)
            score = 1
            board.push(move)
            black_score.append(score)

        print "Move {}, halfmove: {}".format(num, board.halfmove_clock)
        print board
        text_file = open("fen", "w")
        text_file.write(board.fen())
        text_file.close()

        text_file = open("eval", "w")
        text_file.write(str(score))
        text_file.close()

        if board.is_stalemate():
            print "Stalemate!"
            break
        if board.is_insufficient_material():
            print "Insufficient material!"
            break
        if board.is_game_over():
            print "Game over!"
            break

        num += 1

    if board.is_checkmate():
        if board.turn:
            print "Black ({}) wins!".format(black)
            text_file = open("eval", "w")
            text_file.write("Black ({}) wins!".format(black))
            text_file.close()
            stats.write(", ".join(map(str,bparms)) + ", 1\n")
            stats.write(", ".join(map(str,wparms)) + ", 0\n")
        else:
            print "White ({}) wins!".format(white)
            text_file = open("eval", "w")
            text_file.write("White ({}) wins!".format(white))
            text_file.close()
            stats.write(", ".join(map(str,bparms)) + ", 0\n")
            stats.write(", ".join(map(str,wparms)) + ", 1\n")
    else:
        stats.write(", ".join(map(str,bparms)) + ", 0.5\n")
        stats.write(", ".join(map(str,wparms)) + ", 0.5\n")

    stats.flush()

    plt.figure(1)
    plt.plot(white_score)
    plt.plot(black_score)
    plt.ylim([-30, 30])
    plt.show()

    return board.turn

if __name__ == "__main__":
    stats = open("stats", "a+", 0)
    for i in xrange(20):
        play(stats)

