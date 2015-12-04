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

@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    board = chess.Board(fen=data['fen'])

    ai = splort.Player(beta=0.001, pin=0.001, attack=0.2, aggro=0.3)

    move, score = ai.get_move(board)
    board.push(move)
    return jsonify(**{ "fen": board.fen() })

if __name__ == "__main__":
    app.run(debug=False)

