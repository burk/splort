import chess
import splort
import splold
import random_player

def play():

    board = chess.Board()

    num = 1
    while True:

        if num % 2 == 0:
            board.push(splort.get_move(board))
        else:
            board.push(random_player.get_move(board))

        print "Move {}, halfmove: {}".format(num, board.halfmove_clock)
        print board

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

    print "BOARD.TURN {}, num {}".format(board.turn, num)

if __name__ == "__main__":
    play()

