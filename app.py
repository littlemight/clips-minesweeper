from flask import Flask, send_from_directory, request, jsonify
from solver import MinesweeperSolver
import random
import json

app = Flask(__name__)

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)

solver = None

import json

@app.route('/initSolver', methods = ['POST'])
def initSolver():
    # solver = MinesweeperSolver
    # nGrid, nBombs, bombPos = request.json
    json = request.json
    nGrid = json['nGrid']
    nBombs = json['nBombs']
    bombPos = [(v['x'], v['y']) for v in json['bombPos']]
    solver = MinesweeperSolver(nGrid, nBombs, bombPos)
    ret = solver.solve()
    # print(ret)
    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True)