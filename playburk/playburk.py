from flask import Flask, request, send_from_directory, jsonify
import sys
sys.path.append("../")
import splort
import chess

app = Flask(__name__, static_url_path="/static")

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/img/<path:path>')
def send_img(path):
    return send_from_directory('img', path)

@app.route("/")
def index():
    return send_from_directory('', 'index.html')

def board_status(board):
    if board.turn:
        color = "black"
    else:
        color = "white"

    if board.is_checkmate():
        status = "Checkmate, {} wins!".format(color)
    elif board.is_stalemate():
        status = "Stalemate!"
    elif board.is_insufficient_material():
        status = "Insufficient material!"
    elif board.is_seventyfive_moves():
        status = "Draw! (75 move rule)"
    elif board.is_fivefold_repetition():
        status = "Draw! Fivefold repetition."
    else:
        status = "Your move."

    if board.is_game_over():
        over = True
    else:
        over = False

    return over, status


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = chess.Board(fen=data['fen'])

    over, status = board_status(board)

    if over:
        return jsonify(**{ "fen": board.fen(), "status": status })

    ai = splort.Player(beta=0.001, pin=0.001, attack=0.2, aggro=0.3)

    move, score = ai.get_move(board)
    board.push(move)

    over, status = board_status(board)
    return jsonify(**{ "fen": board.fen(), "status": status })

if __name__ == "__main__":
    app.run(debug=False)

