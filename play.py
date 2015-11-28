import chess
import splort

def play():

    board = chess.Board()

    num = 1
    while True:

        board.push(splort.get_move(board))

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

if __name__ == "__main__":
    play()

