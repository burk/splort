import chess
import splort
import splold
import splold2
import random_player
import matplotlib.pyplot as plt

def play():

    board = chess.Board()

    black = splort
    white = splold2

    black_score = []
    white_score = []

    num = 1
    while True:

        if num % 2 == 1:
            move, score = white.get_move(board)
            board.push(move)
            white_score.append(score)
        else:
            move, score = black.get_move(board)
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
            print "Black ({}) wins!".format(black._str())
            text_file = open("eval", "w")
            text_file.write("Black ({}) wins!".format(black._str()))
            text_file.close()
        else:
            print "White ({}) wins!".format(white._str())
            text_file = open("eval", "w")
            text_file.write("White ({}) wins!".format(black._str()))
            text_file.close()

    plt.figure(1)
    plt.plot(white_score)
    plt.plot(black_score)
    plt.ylim([-30, 30])
    plt.show()

    return board.turn

if __name__ == "__main__":
    play()

